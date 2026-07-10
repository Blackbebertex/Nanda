"""One-off Gemini API diagnostic — does not print API key."""
import os
import httpx
from pathlib import Path
from dotenv import load_dotenv

load_dotenv(Path(__file__).resolve().parent.parent.parent / ".env")
load_dotenv(Path(__file__).resolve().parent.parent / ".env")
key = os.environ.get("GEMINI_API_KEY", "")
if not key:
    print("NO_KEY")
    raise SystemExit(1)

base = "https://generativelanguage.googleapis.com/v1beta"
headers = {"Content-Type": "application/json"}

r = httpx.get(f"{base}/models", params={"key": key}, timeout=30)
print("list_models:", r.status_code)
if r.status_code == 200:
    names = [m.get("name", "") for m in r.json().get("models", []) if "generateContent" in (m.get("supportedGenerationMethods") or [])]
    for n in names[:15]:
        print(" ", n)
    if names:
        model = names[0].replace("models/", "")
        r2 = httpx.post(
            f"{base}/models/{model}:generateContent",
            params={"key": key},
            json={"contents": [{"role": "user", "parts": [{"text": "hi"}]}]},
            timeout=30,
        )
        print("generate:", r2.status_code, r2.text[:200])
else:
    print(r.text[:300])
