from __future__ import annotations
import argparse,json,os,time
from datetime import datetime,timezone
from pathlib import Path
from urllib.parse import urlencode
from urllib.request import Request,urlopen
ROOT=Path(__file__).resolve().parents[1]; AGENDA=ROOT/"automation"/"agenda.json"; POSTS=ROOT/"automation"/"posts.json"; API="https://graph.instagram.com/v23.0"
def load(p,f): return json.loads(p.read_text(encoding="utf-8")) if p.exists() else f
def save(p,x): p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
def request(method,path,token,data=None):
 u=f"{API}/{path.lstrip('/')}"; h={"Authorization":f"Bearer {token}"}; b=None
 if method=="GET":
  if data:u+="?"+urlencode(data)
 else:h["Content-Type"]="application/x-www-form-urlencoded";b=urlencode(data or {}).encode()
 with urlopen(Request(u,data=b,headers=h,method=method),timeout=60) as r:return json.loads(r.read().decode())
def find(pid):
 for p in load(POSTS,[]):
  if str(p["id"])==str(pid):return p
 raise RuntimeError("Post not found")
def publish(pid):
 token=os.getenv("IG_TOKEN");user=os.getenv("IG_USER_ID")
 if not token or not user:raise RuntimeError("IG secrets not configured")
 p=find(pid);kids=[]
 for image in p["images"]:kids.append(request("POST",f"{user}/media",token,{"image_url":image,"is_carousel_item":"true"})["id"])
 c=request("POST",f"{user}/media",token,{"media_type":"CAROUSEL","children":",".join(kids),"caption":p["caption"]})["id"]
 for _ in range(24):
  s=request("GET",c,token,{"fields":"status_code,status"})
  if s.get("status_code")=="FINISHED":return request("POST",f"{user}/media_publish",token,{"creation_id":c})["id"]
  if s.get("status_code")=="ERROR":raise RuntimeError(str(s))
  time.sleep(5)
 raise RuntimeError("Instagram processing timeout")
def asutc(v):
 d=datetime.fromisoformat(v);return (d if d.tzinfo else d.replace(tzinfo=timezone.utc)).astimezone(timezone.utc)
def main():
 a=argparse.ArgumentParser();a.add_argument("--operation",required=True);a.add_argument("--post-id",default="");a.add_argument("--scheduled-at",default="");x=a.parse_args();agenda=load(AGENDA,[])
 if x.operation=="agendar":
  if not x.post_id or not x.scheduled_at:raise RuntimeError("post_id and scheduled_at required")
  find(x.post_id);t=asutc(x.scheduled_at);agenda=[i for i in agenda if str(i["post_id"])!=x.post_id];agenda.append({"post_id":int(x.post_id),"scheduled_at":t.isoformat(),"status":"agendado"});save(AGENDA,agenda);print("AGENDADO",x.post_id);return
 if x.operation=="publicar":print("PUBLICADO",x.post_id,publish(x.post_id));return
 now=datetime.now(timezone.utc);changed=False
 for i in agenda:
  if i.get("status")=="agendado" and asutc(i["scheduled_at"])<=now:
   try:i.update({"status":"publicado","published_at":now.isoformat(),"media_id":publish(i["post_id"])})
   except Exception as e:i.update({"status":"erro","failed_at":now.isoformat(),"last_error":str(e)})
   changed=True
 if changed:save(AGENDA,agenda)
 print("PROCESSADO" if changed else "SEM_PUBLICACOES_PENDENTES")
if __name__=="__main__":main()
