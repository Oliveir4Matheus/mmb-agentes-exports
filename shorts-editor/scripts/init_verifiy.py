#!/usr/bin/env python3
"""Inicializa o ambiente de produção de Shorts e Motion Graphics.

Verifica o Remotion, faster-whisper e HyperFrames.
Por padrão instala somente as dependências que estiverem ausentes.
Use --check para apenas auditar.
"""

from __future__ import annotations

import argparse
import json
import os
import platform
import shutil
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Sequence


ROOT = Path(__file__).resolve().parents[1]
VENV = ROOT / ".venv"
IS_WINDOWS = platform.system() == "Windows"


@dataclass
class Check:
    name: str
    installed: bool
    detail: str


def run(command: Sequence[str], *, cwd: Path | None = None) -> subprocess.CompletedProcess[str]:
    """Execute a command without raising and retaining enough output for diagnosis."""
    return subprocess.run(
        list(command),
        cwd=cwd or ROOT,
        capture_output=True,
        text=True,
        check=False,
    )


def executable(name: str) -> str | None:
    """Resolve .cmd executables too, which is required on Windows."""
    return shutil.which(name) or (shutil.which(f"{name}.cmd") if IS_WINDOWS else None)


def venv_python() -> Path:
    return VENV / ("Scripts/python.exe" if IS_WINDOWS else "bin/python")


def project_python() -> str:
    return str(venv_python()) if venv_python().exists() else sys.executable


def package_declares(pkg_names: Sequence[str]) -> bool:
    package_file = ROOT / "package.json"
    if not package_file.exists():
        return False
    try:
        package = json.loads(package_file.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return False
    dependencies = {**package.get("dependencies", {}), **package.get("devDependencies", {})}
    return any(pkg in dependencies for pkg in pkg_names)


def check_remotion() -> Check:
    node = executable("node")
    npm = executable("npm")
    if not node or not npm:
        return Check("Remotion", False, "Node.js e/ou npm não encontrados no PATH")

    cli_candidates = []
    global_cli = executable("remotion")
    if global_cli:
        cli_candidates.append((global_cli, "global"))

    local_cli = ROOT / "node_modules" / ".bin" / ("remotion.cmd" if IS_WINDOWS else "remotion")
    if local_cli.exists():
        cli_candidates.append((str(local_cli), "local"))

    for cli, scope in cli_candidates:
        result = run([cli, "--version"])
        output = (result.stdout or result.stderr).strip()
        lines = output.splitlines()
        if lines and ("@remotion" in lines[0] or "remotion" in lines[0].lower()):
            return Check("Remotion", True, f"{lines[0].strip()} ({scope})")
        if result.returncode == 0 and lines:
            return Check("Remotion", True, f"{lines[-1].strip()} ({scope})")

    if not cli_candidates:
        declared = (
            "declarado no package.json, mas node_modules ainda não foi instalado"
            if package_declares(["remotion", "@remotion/cli"])
            else "não declarado no package.json nem instalado globalmente"
        )
        return Check("Remotion", False, declared)

    return Check("Remotion", False, "CLI encontrado, mas não executou corretamente")


def check_faster_whisper() -> Check:
    python = project_python()
    result = run(
        [python, "-c", "import faster_whisper; print(getattr(faster_whisper, '__version__', 'instalado'))"]
    )
    if result.returncode == 0:
        version = result.stdout.strip() or "instalado"
        scope = ".venv do projeto" if Path(python) == venv_python() else "Python atual"
        return Check("faster-whisper", True, f"{version} ({scope})")
    return Check("faster-whisper", False, "módulo Python não encontrado")


def check_hyperframes() -> Check:
    node = executable("node")
    npm = executable("npm")
    if not node or not npm:
        return Check("HyperFrames", False, "Node.js e/ou npm não encontrados no PATH")

    # 1. Executável no PATH (global ou ~/.local/bin)
    for name in ("hyperframes", "hyperframe"):
        global_cli = executable(name)
        if global_cli:
            result = run([global_cli, "--version"])
            output = (result.stdout or result.stderr).strip()
            lines = output.splitlines()
            if result.returncode == 0 and lines:
                return Check("HyperFrames", True, f"{lines[-1].strip()} (global)")

    # 2. Executável local no projeto (node_modules/.bin)
    for name in ("hyperframes", "hyperframe"):
        local_cli = ROOT / "node_modules" / ".bin" / (f"{name}.cmd" if IS_WINDOWS else name)
        if local_cli.exists():
            result = run([str(local_cli), "--version"])
            output = (result.stdout or result.stderr).strip()
            lines = output.splitlines()
            if result.returncode == 0 and lines:
                return Check("HyperFrames", True, f"{lines[-1].strip()} (local)")
            return Check("HyperFrames", False, "CLI local encontrado, mas não executou corretamente")

    declared = (
        "declarado no package.json, mas node_modules ainda não foi instalado"
        if package_declares(["hyperframes", "hyperframe"])
        else "não instalado no sistema nem no projeto"
    )
    return Check("HyperFrames", False, declared)


def install_remotion() -> bool:
    npm = executable("npm")
    if not npm:
        print("  Não foi possível instalar o Remotion: npm não está disponível.")
        return False
    command = [npm, "install"] if package_declares(["remotion", "@remotion/cli"]) else [npm, "install", "remotion", "@remotion/cli"]
    print(f"  Executando: {' '.join(command)}")
    result = run(command)
    if result.returncode:
        print((result.stderr or result.stdout).strip()[-1200:])
        return False
    return True


def install_faster_whisper() -> bool:
    python = venv_python()
    if not python.exists():
        print(f"  Criando ambiente virtual em {VENV.relative_to(ROOT)}")
        created = run([sys.executable, "-m", "venv", str(VENV)])
        if created.returncode:
            print((created.stderr or created.stdout).strip()[-1200:])
            return False
    command = [str(python), "-m", "pip", "install", "--upgrade", "faster-whisper"]
    print(f"  Executando: {' '.join(command)}")
    result = run(command)
    if result.returncode:
        print((result.stderr or result.stdout).strip()[-1200:])
        return False
    return True


def install_hyperframes() -> bool:
    npm = executable("npm")
    if not npm:
        print("  Não foi possível instalar o HyperFrames: npm não está disponível.")
        return False

    print("  Instalando HyperFrames pelos meios oficiais (npm)...")

    # 1. Tenta instalação oficial global via npm com prefixo ~/.local (se não-root) ou padrão
    user_local = Path.home() / ".local"
    prefix_args = ["--prefix", str(user_local)] if not IS_WINDOWS and (user_local / "bin").exists() else []

    command_global = [npm, "install", "-g", *prefix_args, "hyperframes"]
    print(f"  Executando: {' '.join(command_global)}")
    result_global = run(command_global)
    if result_global.returncode == 0:
        print("  HyperFrames instalado com sucesso via npm.")
        return True

    # 2. Se falhar por permissão, tenta no escopo local do projeto
    command_local = [npm, "install"] if package_declares(["hyperframes", "hyperframe"]) else [npm, "install", "hyperframes"]
    print(f"  Tentando instalação local no projeto: {' '.join(command_local)}")
    result_local = run(command_local)
    if result_local.returncode == 0:
        print("  HyperFrames instalado localmente via npm com sucesso.")
        return True

    error_msg = (result_local.stderr or result_local.stdout or result_global.stderr or result_global.stdout).strip()
    print(error_msg[-1200:])
    return False


def print_check(check: Check) -> None:
    label = "OK" if check.installed else "FALTANDO"
    print(f"[{label}] {check.name}: {check.detail}")


def main() -> int:
    parser = argparse.ArgumentParser(description="Verifica e prepara Remotion, faster-whisper e HyperFrames.")
    parser.add_argument("--check", action="store_true", help="Somente verifica; não instala dependências ausentes.")
    args = parser.parse_args()

    print(f"Sistema: {platform.system()} {platform.release()}")
    print(f"Projeto: {ROOT}")
    print("\nVerificação inicial")
    remotion = check_remotion()
    whisper = check_faster_whisper()
    hyperframes = check_hyperframes()
    print_check(remotion)
    print_check(whisper)
    print_check(hyperframes)

    missing = [check for check in (remotion, whisper, hyperframes) if not check.installed]
    if not missing:
        print("\nAmbiente pronto para iniciar a produção.")
        return 0
    if args.check:
        print("\nDependências ausentes. Consulte cookbooks/cookbook.md ou execute sem --check para instalar.")
        return 1

    print("\nInstalando somente o que está ausente")
    success = True
    if not remotion.installed:
        success = install_remotion() and success
    if not whisper.installed:
        success = install_faster_whisper() and success
    if not hyperframes.installed:
        success = install_hyperframes() and success

    print("\nVerificação final")
    remotion = check_remotion()
    whisper = check_faster_whisper()
    hyperframes = check_hyperframes()
    print_check(remotion)
    print_check(whisper)
    print_check(hyperframes)
    if remotion.installed and whisper.installed and hyperframes.installed:
        print("\nAmbiente pronto para iniciar a produção.")
        return 0
    print("\nNão foi possível concluir a preparação. Siga cookbooks/cookbook.md.")
    return 1 if not success else 2


if __name__ == "__main__":
    raise SystemExit(main())
