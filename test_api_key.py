#!/usr/bin/env python3
import os
import json
import urllib.request
import urllib.error
from dotenv import load_dotenv

load_dotenv()

def test_api_key():
    api_key = os.environ.get("LLM_API_KEY")
    api_base = os.environ.get("LLM_API_BASE", "https://api.deepseek.com/v1")
    api_model = os.environ.get("LLM_MODEL", "deepseek-chat")

    print(f"Testing LLM API key...")
    print(f"API Base: {api_base}")
    print(f"API Model: {api_model}")
    print(f"API Key: {api_key[:8]}...{api_key[-8:]}")
    print()

    endpoint = f"{api_base.rstrip('/')}/chat/completions"
    prompt = "Hello! Please respond with just 'OK' if you can read this."

    body = json.dumps({
        "model": api_model,
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.1,
        "max_tokens": 10,
    }).encode("utf-8")

    req = urllib.request.Request(
        endpoint,
        data=body,
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_key}",
        },
    )

    try:
        print("Sending request...")
        with urllib.request.urlopen(req, timeout=30) as resp:
            result = json.loads(resp.read())
        content = result["choices"][0]["message"]["content"]
        print(f"\n✅ SUCCESS! API key is valid.")
        print(f"Response: {content}")
        return True
    except urllib.error.HTTPError as e:
        print(f"\n❌ API HTTP error: {e.code} {e.reason}")
        try:
            detail = e.read().decode("utf-8")
            print(f"  Response: {detail[:500]}")
        except Exception:
            pass
        return False
    except urllib.error.URLError as e:
        print(f"\n❌ API connection error: {e.reason}")
        return False
    except json.JSONDecodeError as e:
        print(f"\n❌ API returned invalid JSON: {e}")
        return False
    except KeyError as e:
        print(f"\n❌ Unexpected API response format (missing {e})")
        return False
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        return False

if __name__ == "__main__":
    success = test_api_key()
    exit(0 if success else 1)
