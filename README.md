# EB Instagram Automação

Este repositório reúne os carrosséis aprovados, as imagens de publicação, as copies e a agenda do Instagram **@eduardobarcellos**.

## Como a publicação funciona

- O painel privado é usado para revisar, agendar ou publicar um carrossel.
- A agenda oficial fica em `automation/agenda.json`.
- A automação na Cloudflare verifica a agenda a cada minuto, sem depender do computador ligado.
- Para cada post pendente, ela dispara o workflow do GitHub uma única vez por ciclo de cinco minutos.
- Se a Meta devolver um erro temporário, a tentativa fica registrada na agenda e o sistema tenta novamente automaticamente.
- O workflow registra o ID da publicação ao concluir.

## Fonte de verdade

- Conteúdo e copy: `automation/posts.json`
- Agenda e histórico: `automation/agenda.json`
- Imagens publicáveis: `dashboard/instagram-assets/`
- Pré-visualizações: `dashboard/carrosseis/`

## Regra de publicação

Publique apenas imagens finais, em 1080 × 1350, que tenham sido revisadas na prancha de validação. Cada URL de imagem precisa responder publicamente antes do agendamento.
