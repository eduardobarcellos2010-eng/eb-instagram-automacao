from __future__ import annotations
import argparse, json, os, subprocess, sys, time
from datetime import datetime, timezone
from urllib.request import Request, urlopen
from urllib.error import HTTPError

MAX_WAIT_SECONDS = 5 * 60 * 60 + 45 * 60
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def dispatch_next(post_id, scheduled_at, operation="aguardar"):
    token = os.getenv("GH_TOKEN")
    repo = os.getenv("GITHUB_REPOSITORY")
    if not token or not repo:
        raise RuntimeError("GitHub workflow token unavailable")
    body = json.dumps({"ref": "main", "inputs": {"operation": operation, "post_id": str(post_id), "scheduled_at": scheduled_at}}).encode()
    request = Request(
        f"https://api.github.com/repos/{repo}/actions/workflows/instagram.yml/dispatches",
        data=body,
        method="POST",
        headers={
            "Authorization": f"Bearer {token}",
            "Accept": "application/vnd.github+json",
            "Content-Type": "application/json",
            "User-Agent": "EB-Instagram-Automacao",
            "X-GitHub-Api-Version": "2022-11-28",
        },
    )
    try:
        with urlopen(request, timeout=30) as response:
            if response.status != 204:
                raise RuntimeError(f"GitHub rejected continuation: {response.status}")
    except HTTPError as error:
        raise RuntimeError(f"GitHub rejected continuation: {error.code}") from error

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--post-id", required=True)
    parser.add_argument("--scheduled-at", required=True)
    args = parser.parse_args()
    due = datetime.fromisoformat(args.scheduled_at).astimezone(timezone.utc)
    remaining = (due - datetime.now(timezone.utc)).total_seconds()
    if remaining > MAX_WAIT_SECONDS:
        time.sleep(MAX_WAIT_SECONDS)
        dispatch_next(args.post_id, args.scheduled_at)
        print("CONTINUACAO_AGENDADA", args.post_id)
        return
    if remaining > 0:
        time.sleep(remaining)
    result = subprocess.run([sys.executable, os.path.join(ROOT, "scripts", "instagram_publish.py"), "--operation", "processar"], cwd=ROOT)
    raise SystemExit(result.returncode)

if __name__ == "__main__":
    main()
