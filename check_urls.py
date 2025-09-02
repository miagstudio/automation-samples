import sys, time, pathlib, requests

URLS_FILE = pathlib.Path("urls.txt")
REPORT = pathlib.Path("report.md")

def main():
    if not URLS_FILE.exists():
        print("urls.txt not found", file=sys.stderr)
        sys.exit(2)

    urls = [l.strip() for l in URLS_FILE.read_text().splitlines() if l.strip() and not l.startswith("#")]
    failures = []
    lines = [f"# URL Uptime Report\n\nGenerated: {time.strftime('%Y-%m-%d %H:%M:%S')}\n\n", "| URL | Status |\n|---|---|\n"]

    for u in urls:
        try:
            r = requests.get(u, timeout=15)
            ok = 200 <= r.status_code < 400
            lines.append(f"| {u} | {r.status_code} {'✅' if ok else '❌'} |\n")
            if not ok:
                failures.append((u, r.status_code))
        except Exception as e:
            lines.append(f"| {u} | ERROR ❌ ({e.__class__.__name__}) |\n")
            failures.append((u, "ERROR"))

    REPORT.write_text("".join(lines), encoding="utf-8")
    print(f"Wrote {REPORT.resolve()}")
    sys.exit(1 if failures else 0)

if __name__ == "__main__":
    main()
