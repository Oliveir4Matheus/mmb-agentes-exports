---
name: youtube-publish-short
description: Procedimento rápido e otimizado para upload e publicação de vídeos Shorts no YouTube Studio com vídeo Full HD, capa 9:16 e metadados, minimizando o consumo de tokens.
---

# Publicação Rápida de Shorts no YouTube Studio

Este procedimento documenta o fluxo enxuto para upload e publicação de Shorts no YouTube Studio, evitando re-snapshots desnecessários e reduzindo o consumo de tokens.

## 1. Pré-requisitos e Validação dos Arquivos
- **Vídeo**: Deve ser vertical (proporção 9:16, ex: 1080x1920), até 60 segundos de duração.
- **Capa (Thumbnail)**: Arquivo JPG ou PNG, proporção 9:16 (até 2160x3840, <50MB).
- Se os arquivos estiverem em diretórios externos, copie-os previamente para o workspace local para permitir o uso em `agent_browser_upload`.

## 2. Abertura do YouTube Studio
- Navegue para `https://studio.youtube.com`.
- Confirme se o canal logado é o correto (ex: `@dnextlevelAi`).

## 3. Upload do Vídeo
1. Clique no botão de criação ou no menu de upload:
   - Seletor: `button:has-text("Criar")` ou `@ref` de "Criar".
   - Clique no menuitem `Enviar vídeos`.
2. O diálogo de upload (`ytcp-uploads-dialog`) conterá o input de arquivo:
   - Seletor do input: `input[type="file"][name="Filedata"]` (ou simplesmente `input[type="file"]`).
3. Execute `agent_browser_upload` informando o caminho do vídeo no workspace.
4. Aguarde 3 a 5 segundos para que o formulário de metadados renderize.

## 4. Preenchimento de Metadados (Execução Rápida)
Para economizar tokens, prefira injeção direta de eventos ou seletores exatos em vez de múltiplos snapshots sucessivos:
- **Título**:
  - Elemento: `#title-textarea #textbox`
  - Inclua hashtag `#Shorts` e mantenha até 100 caracteres.
- **Descrição**:
  - Elemento: `#description-textarea #textbox`
  - Texto chamativo com tags relevantes.
- **Capa / Thumbnail**:
  - No YouTube Studio para Shorts, o seletor do arquivo de capa é `input#file-loader` (dentro de `ytcp-thumbnail-uploader`).
  - Chame `agent_browser_upload` apontando para a imagem da capa e o seletor `input#file-loader`.
- **Público (COPPA)**:
  - Selecione a opção "Não é conteúdo para crianças":
    `tp-yt-paper-radio-button[name="VIDEO_MADE_FOR_KIDS_NOT_MFK"]`

## 5. Navegação pelas Abas até Visibilidade
- Clique no botão avançar (`#next-button`) para avançar:
  - Da aba **Detalhes** -> **Elementos do vídeo** -> **Verificações** -> **Visibilidade**.
- Na aba **Visibilidade**, selecione a visibilidade desejada:
  - Público: `tp-yt-paper-radio-button[name="PUBLIC"]`

## 6. Publicação e Extração do Link
- O botão final `#done-button` (rotulado como "Publicar") fica desabilitado temporariamente enquanto o YouTube processa os primeiros chunks do arquivo e cria o link ("Criando o link...").
- Para poupar tokens, evite tirar snapshots inteiros durante a espera; use checagens pontuais de texto ou aguarde com `agent_browser_wait_ms`.
- Quando `#done-button` estiver habilitado (`aria-disabled="false"`), clique nele.
- Obtenha a URL do vídeo gerada (`https://youtu.be/...` ou `https://www.youtube.com/shorts/...`).
