# Cookbook — ambiente de produção de Shorts

O script [`init_verifiy.py`](../scripts/init_verifiy.py) detecta automaticamente Windows, macOS e Linux. Execute-o na raiz do projeto antes de iniciar um fluxo de Shorts:

```bash
python scripts/init_verifiy.py
```

Ele instala apenas o que estiver faltando: Remotion local no projeto e `faster-whisper` dentro de `.venv`. Para uma auditoria sem instalar nada:

```bash
python scripts/init_verifiy.py --check
```

## 1. Pré-requisitos

### Node.js (necessário para o Remotion)

Baixe a versão **LTS** no site oficial: [nodejs.org/download](https://nodejs.org/en/download).

Depois de instalar, feche e reabra o terminal e confirme:

```bash
node --version
npm --version
```

### Python 3.10 ou superior (necessário para faster-whisper)

Baixe no site oficial: [python.org/downloads](https://www.python.org/downloads/).

No Windows, marque **Add Python to PATH** no instalador. Confirme depois:

```bash
python --version
```

Se `python` não for reconhecido no macOS/Linux, tente `python3`.

## 2. Instalação automática recomendada

Na raiz do projeto, rode:

```bash
python scripts/init_verifiy.py
```

O script usa os instaladores oficiais `npm` e `pip`, cria `.venv` local para o Python e confirma as versões ao final.

## 3. Instalação manual

### Remotion

Documentação e instalação oficial: [remotion.dev/docs/installation](https://www.remotion.dev/docs/installation).

Dentro da pasta do projeto:

```bash
npm install remotion @remotion/cli
npx remotion --version
```

### faster-whisper

Projeto oficial: [SYSTRAN/faster-whisper](https://github.com/SYSTRAN/faster-whisper).

**macOS / Linux**

```bash
python3 -m venv .venv
.venv/bin/python -m pip install --upgrade pip faster-whisper
.venv/bin/python -c "import faster_whisper; print('faster-whisper OK')"
```

**Windows (PowerShell)**

```powershell
py -m venv .venv
.\.venv\Scripts\python.exe -m pip install --upgrade pip faster-whisper
.\.venv\Scripts\python.exe -c "import faster_whisper; print('faster-whisper OK')"
```

`faster-whisper` já traz o PyAV necessário para leitura de áudio. Para aceleração por GPU, siga a seção de requisitos CUDA do repositório oficial, pois a combinação correta depende da placa e da versão do CUDA.

## 4. Diagnóstico rápido

| Problema | Ação |
| --- | --- |
| `npm` não encontrado | Instale/reinstale o Node.js LTS pelo link oficial e abra outro terminal. |
| `python` não encontrado | Instale o Python pelo link oficial; no Windows, habilite o PATH. |
| `pip` falha no Linux gerenciado | Use a `.venv` criada pelos comandos acima; não use `sudo pip`. |
| Remotion não executa | Rode `npm install` na raiz do projeto e depois `npx remotion --version`. |
