
#!/usr/bin/env python3
"""
Check a list of URLs and write a CSV report.
Uses only the Python standard library.
"""
import argparse, csv, time, urllib.request, urllib.error, ssl, os, sys
from datetime import datetime

def fetch(url: str, timeout: int):
    ctx = ssl.create_default_context()
    req = urllib.request.Request(url, headers={"User-Agent":"automation-samples/1.0"})
    start = time.time()
    code = None
    ok = False
    err = ""
    try:
        with urllib.request.urlopen(req, timeout=timeout, context=ctx) as r:
            code = r.getcode()
            ok = 200 <= code < 400
    except urllib.error.HTTPError as e:
        code = e.code
        err = f"HTTPError: {e.reason}"
    except urllib.error.URLError as e:
        err = f"URLError: {e.reason}"
    except Exception as e:
        err = f"Error: {e}"
    elapsed_ms = int((time.time()-start)*1000)
    return ok, code, elapsed_ms, err

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--input", default="urls.txt", help="File with one URL per line")
    p.add_argument("--out", default="reports/uptime.csv", help="CSV report path")
    p.add_argument("--timeout", type=int, default=10, help="Per-request timeout (s)")
    p.add_argument("--retries", type=int, default=0, help="Retries per URL")
    args = p.parse_args()

    if not os.path.exists(args.input):
        print(f"Input not found: {args.input}", file=sys.stderr)
        sys.exit(2)

    os.makedirs(os.path.dirname(args.out), exist_ok=True)

    rows = []
    with open(args.input, "r", encoding="utf-8") as f:
        urls = [line.strip() for line in f if line.strip() and not line.strip().startswith("#")]

    ts = datetime.utcnow().isoformat(timespec="seconds") + "Z"

    for url in urls:
        attempts = args.retries + 1
        ok = False
        code = None
        elapsed = None
        err = ""
        for i in range(attempts):
            ok, code, elapsed, err = fetch(url, args.timeout)
            if ok: break
            time.sleep(0.5)
        rows.append({
            "timestamp": ts,
            "url": url,
            "ok": ok,
            "status_code": code if code is not None else "",
            "latency_ms": elapsed if elapsed is not None else "",
            "error": err
        })
        print(f"[{ts}] {url} -> ok={ok} code={code} {elapsed}ms {err}")

    write_header = not os.path.exists(args.out)
    with open(args.out, "a", newline="", encoding="utf-8") as f:
        fieldnames = ["timestamp","url","ok","status_code","latency_ms","error"]
        w = csv.DictWriter(f, fieldnames=fieldnames)
        if write_header:
            w.writeheader()
        w.writerows(rows)

if __name__ == "__main__":
    main()
