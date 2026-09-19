# Processo seguro de publicação de carrosséis EB

## Regra permanente

Um carrossel só pode ser publicado depois de aprovado no HTML e conferido na prancha de validação. As imagens finais devem estar em 1080 × 1350 e hospedadas publicamente no GitHub Pages.

## Processo

1. Revisar e aprovar o carrossel HTML.
2. Exportar as imagens finais.
3. Conferir a prancha de validação e as dimensões de todos os slides.
4. Atualizar `automation/posts.json` com as URLs finais e a copy aprovada.
5. Conferir que todas as URLs respondem com HTTP 200.
6. Agendar pelo painel privado ou registrar a data na agenda oficial.
7. Confirmar o status `publicado` e o ID de mídia antes de considerar o post concluído.

## Nunca fazer

- Publicar arquivos antigos, quadrados ou sem revisão visual.
- Usar links que não respondam publicamente.
- Duplicar uma publicação já marcada como `publicado`.
- Alterar `automation/agenda.json` em paralelo a uma publicação em andamento.
