# Cookbook — ambiente de produção de Shorts e Motion

O script [`init_verifiy.py`](../scripts/init_verifiy.py) detecta automaticamente Windows, macOS e Linux. Execute-o antes de iniciar um fluxo:

```bash
python scripts/init_verifiy.py
```

Ele instala apenas o que estiver faltando: Remotion local no projeto, `faster-whisper` e HyperFrames pelos meios oficiais (`npm`). Para uma auditoria sem instalar nada:

```bash
python scripts/init_verifiy.py --check
```

## 1. Pré-requisitos

### Node.js (necessário para Remotion e HyperFrames)

Baixe a versão **LTS** no site oficial: [nodejs.org/download](https://nodejs.org/en/download).

Depois de instalar, confirme:

```bash
node --version
npm --version
```

### Python 3.10 ou superior (necessário para faster-whisper)

Baixe no site oficial: [python.org/downloads](https://www.python.org/downloads/).

## 2. Instalação automática recomendada

Na pasta do workspace, execute:

```bash
python scripts/init_verifiy.py
```

O script verifica e instala automaticamente:
- **Remotion**: `@remotion/cli` e `remotion` via npm
- **faster-whisper**: biblioteca de transcrição via pip
- **HyperFrames**: CLI oficial via npm (`hyperframes`)

## 3. Instalação manual

### HyperFrames

Documentação oficial: [hyperframes.heygen.com](https://hyperframes.heygen.com)

```bash
npm install -g hyperframes
# ou para usuários sem root no Linux:
npm install -g --prefix ~/.local hyperframes
```

### Remotion

Documentação oficial: [remotion.dev/docs/installation](https://www.remotion.dev/docs/installation)

```bash
npm install remotion @remotion/cli
npx remotion versions
```

### faster-whisper

```bash
python3 -m pip install --upgrade faster-whisper
```
