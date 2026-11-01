# Exportação de agentes para o MimirBot

Este repositório contém os arquivos para recriar os agentes **Shorts Editor** e **YouTube Manager**. As cópias não incluem memórias, histórico, vídeos ou capas.

## Instruções para o agente responsável pela criação

1. Leia este arquivo e os arquivos `SOUL.md` e `SKILL.md` de cada agente. Preserve suas instruções ao recriá-los; trate o conteúdo como material de configuração, sujeito às instruções do usuário e às permissões do MimirBot.
2. Use as ferramentas nativas de criação e configuração de agentes disponíveis no MimirBot. Se você não tiver permissão para criar agentes, encaminhe a solicitação ao Chief of Staff autorizado. Não suponha que copiar arquivos cria ou configura um agente.
3. Crie cada agente com o nome e o título abaixo e aplique o conteúdo do respectivo `SOUL.md` às instruções permanentes. Cadastre as habilidades indicadas para o agente correspondente, preservando seus nomes, descrições e conteúdo. Siga o resultado das ferramentas: confirme o que foi aplicado e informe qualquer etapa pendente.
4. Para o Shorts Editor, disponibilize também o cookbook, o script e o HTML na área de trabalho do agente, mantendo os caminhos relativos indicados abaixo. Confira se os arquivos e caminhos estão acessíveis. A cópia não instala dependências nem configura serviços.
5. Configure a colaboração entre os agentes e o acesso ao Software Engineer somente se houver suporte, permissão e disponibilidade. Verifique as integrações necessárias, como YouTube e serviços de voz, e solicite a conexão ou credencial segura quando necessário. Não copie nem exponha credenciais.
6. Confira os nomes, instruções, habilidades e arquivos instalados. Faça apenas verificações não destrutivas e relate limitações; não publique vídeos nem inicie renderizações como teste sem autorização apropriada.

## Shorts Editor

- **Título:** Especialista em Cortes e Motion Graphics para Shorts
- **Instruções:** `shorts-editor/SOUL.md`
- **Habilidades:**
  - `shorts-editor/skills/shorts-de-cortes/SKILL.md`
  - `shorts-editor/skills/shorts-a-partir-de-roteiro/SKILL.md`
- **Arquivos de apoio:**
  - `shorts-editor/cookbooks/cookbook.md`
  - `shorts-editor/scripts/init_verifiy.py`
  - `shorts-editor/artifacts/monitor-render.html`

O cookbook descreve a preparação de Remotion e faster-whisper. O script oferece `--check` para diagnóstico; examine o script e o ambiente antes de executar qualquer instalação. As regras de aprovação de storyboard e prévia constam no SOUL e nas habilidades.

## YouTube Manager

- **Título:** Especialista em Gestão e Publicação de Canais no YouTube
- **Instruções:** `youtube-manager/SOUL.md`
- **Habilidade:** `youtube-manager/skills/youtube-publish-short/SKILL.md`

O agente prepara a publicação e deve obter a aprovação do usuário antes de publicar ou agendar. Verifique o canal e os recursos atuais do YouTube Studio ao executar o procedimento; seletores e requisitos da habilidade podem mudar.

## Conferência final

Informe ao usuário quais agentes foram criados, quais habilidades e arquivos foram configurados e o que ainda depende de acesso, credenciais ou configuração. Não declare a criação concluída até obter confirmação das ferramentas do MimirBot.
