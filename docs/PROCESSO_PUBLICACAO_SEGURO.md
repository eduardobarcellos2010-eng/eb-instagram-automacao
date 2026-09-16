# Publica??o segura de carross?is EB

## Regra permanente

Nenhum carrossel pode ser publicado a partir de PNGs antigos ou sem uma prancha de valida??o revisada. A exporta??o aprovada usa cards HTML de 360?450 renderizados em uma sess?o isolada do Chrome e ampliados para 1080?1350.

## Processo obrigat?rio

1. Abra e aprove o carrossel HTML.
2. Exporte com `ferramentas/exportar_carrossel.py`.
3. Confirme que todos os PNGs t?m 1080?1350 e revise `prancha-validacao.jpg`.
4. Copie somente os PNGs validados para `dashboard/instagram-assets/<slug>/` neste reposit?rio.
5. Fa?a commit e push. Espere cada URL do GitHub Pages responder HTTP 200.
6. Use apenas as URLs do GitHub Pages na API do Instagram.
7. Confirme o ID de publica??o no log antes de informar que o post foi publicado.

## Proibido

- N?o usar `png/`, `png-seguro/` ou `png-quadrado/` antigos.
- N?o enviar sem revisar a prancha.
- N?o usar links que n?o respondam HTTP 200.
- N?o republicar vers?es de teste sem validar o arquivo final.

## Comando

```powershell
python ferramentas\exportar_carrossel.py carrosseisoteiro-01-beneficios-ocultos\index.html carrosseisoteiro-01-beneficios-ocultos\png-final --slides 7
```
