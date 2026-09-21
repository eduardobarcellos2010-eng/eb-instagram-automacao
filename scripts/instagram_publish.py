from __future__ import annotations

import argparse
import json
import os
import time
from datetime import datetime, timedelta, timezone
from pathlib import Path
from urllib.parse import urlencode
from urllib.request import Request, urlopen

ROOT = Path(__file__).resolve().parents[1]
AGENDA = ROOT / "automation" / "agenda.json"
POSTS = ROOT / "automation" / "posts.json"
API = "https://graph.instagram.com/v23.0"


def load(path, fallback):
    return json.loads(path.read_text(encoding="utf-8-sig")) if path.exists() else fallback


def save(path, value):
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def request(method, path, token, data=None):
    url = f"{API}/{path.lstrip('/')}"
    headers = {"Authorization": f"Bearer {token}"}
    body = None
    if method == "GET":
        if data:
            url += "?" + urlencode(data)
    else:
        headers["Content-Type"] = "application/x-www-form-urlencoded"
        body = urlencode(data or {}).encode()
    with urlopen(Request(url, data=body, headers=headers, method=method), timeout=60) as response:
        return json.loads(response.read().decode())


def post_type(post):
    if post.get("media_type") == "reel" or post.get("video_url"):
        return "reel"
    return "carousel"


def validate_post(post):
    if not isinstance(post.get("caption"), str) or not post["caption"].strip():
        raise RuntimeError("Post caption is missing")

    if post_type(post) == "reel":
        video_url = post.get("video_url")
        if not isinstance(video_url, str) or not video_url.startswith("https://"):
            raise RuntimeError("Reel video_url must use a public HTTPS URL")
        return

    images = post.get("images", [])
    if not 2 <= len(images) <= 10:
        raise RuntimeError("Carousel must contain between 2 and 10 images")
    if not all(isinstance(image, str) and image.startswith("https://") for image in images):
        raise RuntimeError("Every carousel image must use a public HTTPS URL")


def find(post_id):
    for post in load(POSTS, []):
        if str(post["id"]) == str(post_id):
            validate_post(post)
            return post
    raise RuntimeError("Post not found")


def wait_for_container(container_id, token):
    for _ in range(36):
        status = request("GET", container_id, token, {"fields": "status_code,status"})
        if status.get("status_code") == "FINISHED":
            return
        if status.get("status_code") == "ERROR":
            raise RuntimeError(str(status))
        time.sleep(5)
    raise RuntimeError("Instagram processing timeout")


def publish_carousel(post, token, user):
    children = []
    for image in post["images"]:
        child = request("POST", f"{user}/media", token, {"image_url": image, "is_carousel_item": "true"})
        children.append(child["id"])
    container = request(
        "POST",
        f"{user}/media",
        token,
        {"media_type": "CAROUSEL", "children": ",".join(children), "caption": post["caption"]},
    )["id"]
    wait_for_container(container, token)
    return request("POST", f"{user}/media_publish", token, {"creation_id": container})["id"]


def publish_reel(post, token, user):
    container = request(
        "POST",
        f"{user}/media",
        token,
        {
            "media_type": "REELS",
            "video_url": post["video_url"],
            "caption": post["caption"],
            "share_to_feed": "true",
        },
    )["id"]
    wait_for_container(container, token)
    return request("POST", f"{user}/media_publish", token, {"creation_id": container})["id"]


def publish(post_id):
    token = os.getenv("IG_TOKEN")
    user = os.getenv("IG_USER_ID")
    if not token or not user:
        raise RuntimeError("IG secrets not configured")
    post = find(post_id)
    if post_type(post) == "reel":
        return publish_reel(post, token, user)
    return publish_carousel(post, token, user)


def asutc(value):
    date = datetime.fromisoformat(value)
    if date.tzinfo is None:
        date = date.replace(tzinfo=timezone(timedelta(hours=-3)))
    return date.astimezone(timezone.utc)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--operation", required=True)
    parser.add_argument("--post-id", default="")
    parser.add_argument("--scheduled-at", default="")
    args = parser.parse_args()
    agenda = load(AGENDA, [])

    if args.operation == "agendar":
        if not args.post_id or not args.scheduled_at:
            raise RuntimeError("post_id and scheduled_at required")
        find(args.post_id)
        scheduled_at = asutc(args.scheduled_at)
        if scheduled_at <= datetime.now(timezone.utc):
            raise RuntimeError("Scheduled time must be in the future")
        agenda = [item for item in agenda if str(item["post_id"]) != args.post_id]
        agenda.append({"post_id": int(args.post_id), "scheduled_at": scheduled_at.isoformat(), "status": "agendado"})
        save(AGENDA, agenda)
        print("AGENDADO", args.post_id)
        return

    if args.operation == "aguardar":
        print("AGUARDANDO", args.post_id)
        return

    if args.operation == "diagnosticar":
        token = os.getenv("IG_TOKEN")
        user = os.getenv("IG_USER_ID")
        if not token or not user:
            raise RuntimeError("IG secrets not configured")
        profile = request("GET", user, token, {"fields": "id,username"})
        print("INSTAGRAM_PROFILE", profile.get("id", ""), profile.get("username", ""))
        return

    if args.operation == "verificar":
        token = os.getenv("IG_TOKEN")
        user = os.getenv("IG_USER_ID")
        if not token or not user:
            raise RuntimeError("IG secrets not configured")
        profile = request("GET", user, token, {"fields": "id,username"})
        if str(profile.get("id")) != str(user):
            raise RuntimeError("Instagram user mismatch")
        print("INSTAGRAM_OK", profile.get("username", ""))
        return

    if args.operation == "publicar":
        if not args.post_id:
            raise RuntimeError("post_id required")
        existing = next((item for item in agenda if str(item["post_id"]) == str(args.post_id)), None)
        if existing and existing.get("status") == "publicado":
            print("JA_PUBLICADO", args.post_id, existing.get("media_id", ""))
            return
        media_id = publish(args.post_id)
        if existing is None:
            existing = {"post_id": int(args.post_id)}
            agenda.append(existing)
        existing.update({"status": "publicado", "published_at": datetime.now(timezone.utc).isoformat(), "media_id": media_id})
        for key in ("attempts", "last_error", "last_attempt_at"):
            existing.pop(key, None)
        save(AGENDA, agenda)
        print("PUBLICADO", args.post_id, media_id)
        return

    now = datetime.now(timezone.utc)
    changed = False
    for item in agenda:
        if item.get("status") == "agendado" and asutc(item["scheduled_at"]) <= now:
            try:
                item.update({"status": "publicado", "published_at": now.isoformat(), "media_id": publish(item["post_id"])})
                for key in ("attempts", "last_error", "last_attempt_at"):
                    item.pop(key, None)
            except Exception as exc:
                item.update(
                    {
                        "status": "agendado",
                        "attempts": int(item.get("attempts", 0)) + 1,
                        "last_attempt_at": now.isoformat(),
                        "last_error": str(exc),
                    }
                )
                print("TENTATIVA_FALHOU", item["post_id"], str(exc))
            changed = True
    if changed:
        save(AGENDA, agenda)
    print("PROCESSADO" if changed else "SEM_PUBLICACOES_PENDENTES")


if __name__ == "__main__":
    main()