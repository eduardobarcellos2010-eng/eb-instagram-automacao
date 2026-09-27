# Padrão de carrosséis EB

Este repositório usa o padrão visual aprovado do perfil **@eduardobarcellos** para todos os carrosséis futuros.

- Exportação: **1080 × 1350 px** (Instagram 4:5)
- Cores: azul-marinho `#07152E` e `#102A4C`, dourado `#C0A062` e `#E5D0A2`, creme `#F3EFE4`
- Fontes: **Playfair Display** para títulos e **DM Sans** para apoio
- Assinatura em cada slide: foto circular do Eduardo + `@eduardobarcellos`
- Composição: visual editorial premium, barra de progresso e slides alternando azul/creme
- CTA final: **Envie DIAGNÓSTICO no direct**

A referência técnica é [`dashboard/carrosseis/eb-carousel.css`](../dashboard/carrosseis/eb-carousel.css). Não alterar esse padrão sem pedido explícito.

## Modelo de teste: editorial escuro com assinatura fixa

Referência visual: https://www.instagram.com/p/DdZEj_6F4hl/?img_index=1

Usar como inspiração estrutural, sem copiar o design literal:
- Formato editorial de artigo/coluna, com sensação premium e intelectual.
- Fundo azul-marinho muito escuro ou preto azulado.
- Slides internos com texto em blocos, alinhado à esquerda, margens amplas e respiro.
- Headline grande no topo ou centro, com uma frase principal por slide.
- Destaques em azul/ciano ou dourado EB apenas em palavras-chave, sem poluir.
- Usar negrito para criar ritmo de leitura, não para destacar tudo.
- Rodapé fixo com foto de Eduardo, nome/arroba `@eduardobarcellos` e indicadores de páginas discretos.
- Capa pode ter imagem/ilustração/foto com degradê escuro na base, headline forte e subtítulo curto.
- Adaptar para paleta EB: azul-marinho, dourado e off-white; se usar azul vivo, usar com moderação como cor de destaque.
- CTA final: `Envie DIAGNÓSTICO no direct.`

Aplicação indicada:
- Temas mais densos, opinião forte, quebra de crença e explicações consultivas.
- Transformar os conteúdos cancelados 111 a 115 em carrosséis mais editoriais, com menos cara de anúncio e mais cara de insight estratégico.

## Modelo aprovado — Reel 11 editorial escuro

Aprovado pelo Eduardo em 2026-09-27 12:14:45.

Usar como base para os próximos testes de carrossel quando ele pedir transformar reels/posts pendentes em carrosséis com novo visual.

Arquivo aprovado:
dashboard/carrosseis/roteiro-11-porta-de-entrada-editorial/index.html

Características aprovadas:
- Fundo editorial escuro com azul-marinho profundo.
- Destaques em dourado/off-white e acento azul discreto.
- Assinatura fixa com foto do Eduardo e @eduardobarcellos.
- Texto grande, direto, com hierarquia forte.
- CTA final: Envie DIAGNÓSTICO no direct.
- Não copiar literalmente o modelo externo do Instagram; usar apenas como referência de composição editorial.

## Regra operacional permanente — carrosséis EB

Fluxo mais eficiente para novos carrosséis:
1. Usar como base o modelo aprovado do Reel 11 editorial escuro quando o pedido for transformar reels/posts pendentes em carrossel.
2. Escrever primeiro a copy dos slides em texto limpo, com acentos corretos, antes de montar o HTML.
3. Gravar sempre em UTF-8 e validar encoding antes de mostrar ao Eduardo.
4. Rodar uma varredura automática procurando `?`, `Ã`, `Â`, `�`, palavras sem acento e mojibake antes de entregar.
5. Conferir se cada slide tem área segura no rodapé para foto, @eduardobarcellos, logo/assinatura e contador.
6. Nunca deixar logo, assinatura, foto, @ ou contador por cima de dados, números, bullets ou CTA.
7. Se o conteúdo for grande demais para caber com a assinatura, reduzir texto, quebrar em mais slides ou sugerir remover/mover a assinatura daquele slide.
8. Antes de mandar para aprovação, revisar visualmente pelo menos capa, slide com dados/números, slide de bullets e CTA final.
9. Se a checagem visual não puder ser feita por limitação técnica, informar isso claramente e não dizer que está 100% revisado visualmente.

Área segura padrão:
- Conteúdo principal deve terminar acima da assinatura fixa.
- Para slides 1080x1350, reservar no mínimo 170px inferiores para assinatura, contador/progresso e margem.
- Para o protótipo HTML em escala 360x450, reservar no mínimo 58px inferiores livres.
