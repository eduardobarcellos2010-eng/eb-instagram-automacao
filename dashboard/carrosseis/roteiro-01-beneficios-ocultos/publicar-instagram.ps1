$ErrorActionPreference='Stop'
$base='C:\Users\eduar\OneDrive\Documents\Edição de video\carrosseis\roteiro-01-beneficios-ocultos'
$log=Join-Path $base 'publicacao-2026-09-16.log'
function Log($text){ Add-Content -LiteralPath $log -Value (('['+(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')+'] '+$text)) }
try {
  $token=(Get-Content -LiteralPath 'C:\Users\eduar\Downloads\ig_token.txt' -Raw).Trim()
  $urls=Get-Content -LiteralPath (Join-Path $base 'image-urls.txt') | Where-Object { $_.Trim() }
  if($urls.Count -ne 7){ throw 'Quantidade de imagens inválida' }
  $headers=@{ Authorization=('Bearer '+$token) }
  $igUser='17841400026100550'
  $version='v23.0'
  $children=@()
  foreach($url in $urls){
    $r=Invoke-RestMethod -Method Post -Uri ('https://graph.instagram.com/'+$version+'/'+$igUser+'/media') -Headers $headers -Body @{ image_url=$url; is_carousel_item='true' }
    if(-not $r.id){ throw 'Falha ao criar item do carrossel' }
    $children += $r.id
  }
  Log 'Itens do carrossel enviados ao Instagram.'
  $nl=[Environment]::NewLine
  $caption='Seu banco pode ter benefícios que já são seus e você pode nem saber.'+$nl+$nl+'Em uma consultoria, um cliente encontrou R$200 por mês disponíveis no próprio aplicativo do banco. O valor sempre esteve lá. Faltava estratégia para enxergar e usar.'+$nl+$nl+'Gastar muito no cartão não significa aproveitar tudo o que ele pode oferecer. Benefícios, pontos e emissões precisam trabalhar juntos.'+$nl+$nl+'Envie DIAGNÓSTICO no direct e eu analiso o potencial da sua estratégia.'+$nl+$nl+'#milhas #pontosemilhas #cartãodecrédito #gestãodemilhas #viagensdeluxo'
  $carousel=Invoke-RestMethod -Method Post -Uri ('https://graph.instagram.com/'+$version+'/'+$igUser+'/media') -Headers $headers -Body @{ media_type='CAROUSEL'; children=($children -join ','); caption=$caption }
  if(-not $carousel.id){ throw 'Falha ao criar o carrossel' }
  $status=$null
  for($i=0;$i -lt 36;$i++){
    Start-Sleep -Seconds 10
    $status=Invoke-RestMethod -Method Get -Uri ('https://graph.instagram.com/'+$version+'/'+$carousel.id+'?fields=status_code,status') -Headers $headers
    if($status.status_code -eq 'FINISHED'){ break }
    if($status.status_code -eq 'ERROR'){ throw ('Instagram retornou erro: '+$status.status) }
  }
  if($status.status_code -ne 'FINISHED'){ throw 'O Instagram não finalizou o processamento a tempo' }
  $published=Invoke-RestMethod -Method Post -Uri ('https://graph.instagram.com/'+$version+'/'+$igUser+'/media_publish') -Headers $headers -Body @{ creation_id=$carousel.id }
  Log ('PUBLICADO: '+$published.id)
} catch { Log ('ERRO: '+$_.Exception.Message); exit 1 }
