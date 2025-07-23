#!/usr/bin/env python3
"""
GitEcho - AI-powered Git change summarizer.
Summarize diffs or commits into natural language explanations.
Supports OpenAI and local LLM endpoints.
"""

import subprocess
import argparse
import os
import sys
import json

try:
    import openai
except ImportError:
    openai = None

import requests

DEFAULT_MODEL = "gpt-4"

def get_git_diff(base_branch=None):
    try:
        if base_branch:
            result = subprocess.run(["git", "diff", base_branch], capture_output=True, text=True)
        else:
            result = subprocess.run(["git", "diff", "HEAD~1"], capture_output=True, text=True)
        return result.stdout
    except Exception as e:
        print(f"[ERROR] Failed to get git diff: {e}")
        sys.exit(1)

def generate_summary(diff_text, model=DEFAULT_MODEL, local=False, endpoint=None):
    if local:
        if not endpoint:
            endpoint = "http://localhost:11434/v1/chat/completions"
        payload = {
            "model": model,
            "messages": [{"role": "user", "content": f"Summarize the following code diff in plain English:\n{diff_text[:6000]}"}],
            "temperature": 0.5,
        }
        try:
            res = requests.post(endpoint, json=payload, timeout=10)
            res.raise_for_status()
            return res.json()['choices'][0]['message']['content'].strip()
        except Exception as e:
            print(f"[ERROR] Failed to connect to local LLM: {e}")
            sys.exit(1)
    else:
        openai.api_key = os.getenv("OPENAI_API_KEY")
        if not openai or not openai.api_key:
        print("[WARNING] No OpenAI key found, falling back to local mode.")
        return generate_summary(diff_text, model=model, local=True, endpoint="http://localhost:11434")
            print("[ERROR] Missing OpenAI API key or library.")
            sys.exit(1)

        prompt = f"""
You are a senior developer. Summarize this code diff in natural language. Focus on what was changed and why.

```
{diff_text[:6000]}
```
"""
        try:
            response = openai.ChatCompletion.create(
                model=model,
                messages=[
                    {"role": "system", "content": "You are a helpful assistant."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.5,
                max_tokens=400,
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            print(f"[ERROR] OpenAI API call failed: {e}")
            sys.exit(1)

def main():
    parser = argparse.ArgumentParser(description="Summarize Git diffs using AI")
    parser.add_argument('--commit-msg', action='store_true', help="Only output a commit message suggestion")
    parser.add_argument('--base', help="Base branch to diff from (default: HEAD~1)")
    parser.add_argument('--model', default=DEFAULT_MODEL, help="LLM model to use")
    parser.add_argument('--local', action='store_true', help="Use a local LLM endpoint")
    parser.add_argument('--endpoint', help="Local LLM endpoint URL (e.g., http://localhost:11434)")
    args = parser.parse_args()

    if not args.local:
        print("[WARNING] Using OpenAI API. Your code will be sent to OpenAI servers.")
        print("To keep your code local, use: --local --endpoint http://localhost:11434\n")

    print("[INFO] Fetching git diff...")
    diff = get_git_diff(args.base)[:8000]  # Truncate to avoid token overflow
    if not diff:
        print("[INFO] No changes to summarize.")
        return

    print("[INFO] Generating AI summary...")
    summary = generate_summary(diff, model=args.model, local=args.local, endpoint=args.endpoint)

    print("\n====== AI Summary ======\n")
    print(summary)

if __name__ == "__main__":
    main()
