from __future__ import annotations
import argparse, json, os
from datetime import datetime
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
AGENDA=ROOT/'automation'/'agenda.json'

def load(): return json.loads(AGENDA.read_text(encoding='utf-8'))
def save(data): AGENDA.write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')

def main():
  p=argparse.ArgumentParser(); p.add_argument('--operation',required=True); p.add_argument('--post-id',default=''); p.add_argument('--scheduled-at',default=''); a=p.parse_args()
  agenda=load()
  if a.operation=='agendar':
    if not a.post_id or not a.scheduled_at: raise SystemExit('post_id e scheduled_at s?o obrigat?rios')
    datetime.fromisoformat(a.scheduled_at)
    agenda=[x for x in agenda if str(x['post_id'])!=a.post_id]
    agenda.append({'post_id':int(a.post_id),'scheduled_at':a.scheduled_at,'status':'agendado'})
    save(agenda); print('AGENDADO',a.post_id,a.scheduled_at); return
  if a.operation=='processar':
    now=datetime.now().strftime('%Y-%m-%dT%H:%M')
    due=[x for x in agenda if x['status']=='agendado' and x['scheduled_at']<=now]
    if not due: print('SEM_PUBLICACOES_PENDENTES'); return
    # A publica??o real ser? adicionada ap?s o primeiro teste de agenda confirmado.
    for item in due: item['status']='pronto_para_publicar'
    save(agenda); print('PENDENTES_MARCADOS',len(due)); return
  if a.operation=='publicar':
    if not os.getenv('IG_TOKEN') or not os.getenv('IG_USER_ID'): raise SystemExit('Segredos IG_TOKEN e IG_USER_ID n?o configurados')
    raise SystemExit('Publica??o direta ser? habilitada ap?s a valida??o do teste de agenda')
  raise SystemExit('Opera??o inv?lida')
if __name__=='__main__': main()
