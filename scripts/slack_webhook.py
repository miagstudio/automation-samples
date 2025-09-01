
#!/usr/bin/env python3
"""
Post a message to a Slack/Discord webhook.
Only standard library (urllib).
"""
import argparse, json, os, sys, urllib.request

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--text", required=True, help="Message text")
    p.add_argument("--webhook", default=os.getenv("SLACK_WEBHOOK_URL"), help="Webhook URL (or set SLACK_WEBHOOK_URL in env)")
    args = p.parse_args()

    if not args.webhook:
        print("Webhook URL missing. Provide --webhook or set SLACK_WEBHOOK_URL.", file=sys.stderr)
        sys.exit(2)

    payload = {"text": args.text}
    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(args.webhook, data=data, headers={"Content-Type":"application/json"})
    with urllib.request.urlopen(req) as r:
        print("Posted:", r.status)

if __name__ == "__main__":
    main()
