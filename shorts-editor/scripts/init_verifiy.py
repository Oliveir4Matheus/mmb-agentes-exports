#!/usr/bin/env python3
"""Inicializa o ambiente de produção de Shorts.

Verifica o Remotion local do projeto e o faster-whisper. Por padrão instala
somente as dependências que estiverem ausentes. Use --check para apenas auditar.
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


def package_declares_remotion() -> bool:
    package_file = ROOT / "package.json"
    if not package_file.exists():
        return False
    try:
        package = json.loads(package_file.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return False
    dependencies = {**package.get("dependencies", {}), **package.get("devDependencies", {})}
    return "remotion" in dependencies or "@remotion/cli" in dependencies


def check_remotion() -> Check:
    node = executable("node")
    npm = executable("npm")
    if not node or not npm:
        return Check("Remotion", False, "Node.js e/ou npm não encontrados no PATH")

    local_cli = ROOT / "node_modules" / ".bin" / ("remotion.cmd" if IS_WINDOWS else "remotion")
    if not local_cli.exists():
        declared = "declarado no package.json, mas node_modules ainda não foi instalado" if package_declares_remotion() else "não declarado no package.json"
        return Check("Remotion", False, declared)

    result = run([str(local_cli), "--version"])
    version = (result.stdout or result.stderr).strip().splitlines()
    if result.returncode == 0:
        return Check("Remotion", True, version[-1] if version else "CLI local disponível")
    return Check("Remotion", False, "CLI local encontrado, mas não executou corretamente")


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


def install_remotion() -> bool:
    npm = executable("npm")
    if not npm:
        print("  Não foi possível instalar o Remotion: npm não está disponível.")
        return False
    command = [npm, "install"] if package_declares_remotion() else [npm, "install", "remotion", "@remotion/cli"]
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


def print_check(check: Check) -> None:
    label = "OK" if check.installed else "FALTANDO"
    print(f"[{label}] {check.name}: {check.detail}")


def main() -> int:
    parser = argparse.ArgumentParser(description="Verifica e prepara Remotion e faster-whisper.")
    parser.add_argument("--check", action="store_true", help="Somente verifica; não instala dependências ausentes.")
    args = parser.parse_args()

    print(f"Sistema: {platform.system()} {platform.release()}")
    print(f"Projeto: {ROOT}")
    print("\nVerificação inicial")
    remotion = check_remotion()
    whisper = check_faster_whisper()
    print_check(remotion)
    print_check(whisper)

    missing = [check for check in (remotion, whisper) if not check.installed]
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

    print("\nVerificação final")
    remotion = check_remotion()
    whisper = check_faster_whisper()
    print_check(remotion)
    print_check(whisper)
    if remotion.installed and whisper.installed:
        print("\nAmbiente pronto para iniciar a produção.")
        return 0
    print("\nNão foi possível concluir a preparação. Siga cookbooks/cookbook.md.")
    return 1 if not success else 2


if __name__ == "__main__":
    raise SystemExit(main())
