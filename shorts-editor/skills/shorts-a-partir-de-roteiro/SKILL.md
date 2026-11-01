---
name: shorts-a-partir-de-roteiro
description: Cria Shorts verticais a partir de um roteiro, com storyboard de 10 cenas, capa, prévia de voz e versão final com Gemini TTS. Use quando o usuário trouxer um roteiro e quiser transformar em vídeo.
---

# Shorts a partir de roteiro

Use este fluxo para transformar um roteiro em um Short educativo/explicativo. Não use para editar um vídeo já cortado quando o usuário não forneceu roteiro.

## Fluxo

1. Receba e analise o roteiro: tema, gancho, promessa, ritmo e trechos que pedem reforço visual. Preserve o sentido das falas.
2. Pergunte o formato desejado antes de criar os assets: duração, proporção, referência/estilo visual, tom da locução e se haverá rosto ou vídeo de apoio.
3. Gere o pacote visual para aprovação:
   - uma única contact sheet com **10 imagens** de storyboard;
   - proposta de estilo de legenda;
   - capa do vídeo.
4. Aguarde a aprovação explícita do storyboard, legenda e capa. Não renderize vídeo antes disso.
5. Gere uma prévia com voz sintetizada, legendas e motion graphics aprovados.
6. Aguarde a aprovação explícita da prévia.
7. Gere a versão final com voz Gemini TTS. Se a chave necessária não estiver configurada, solicite-a de forma segura antes de iniciar.
8. Renderize o master em 1080p, 60 fps e 9:16. Inicie junto um HTML de acompanhamento em tempo real.
9. Valide o arquivo final antes de encaminhar para publicação. Se houver publicação autorizada, use exatamente a capa aprovada e confirme que ela foi aplicada no YouTube antes de informar conclusão.

## Edição e acompanhamento

- Mantenha rosto e elementos importantes legíveis no celular.
- Use legenda karaokê sincronizada, destacando a palavra falada.
- Insira motion graphics para reforçar a fala, sem mudar seu conteúdo.
- O painel HTML deve mostrar porcentagem, frames concluídos/total, estimativa restante, velocidade e log recente.
- Diferencie sempre “encaminhado para publicação” de “publicado e conferido”.
