
#!/usr/bin/env python3
"""
Deduplicate a CSV by one or more key columns.
"""
import argparse, csv, sys

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--in", dest="inp", required=True, help="Input CSV path")
    p.add_argument("--out", dest="out", required=True, help="Output CSV path")
    p.add_argument("--keys", required=True, help="Comma-separated column names to dedupe by")
    args = p.parse_args()

    keys = [k.strip() for k in args.keys.split(",") if k.strip()]
    seen = set()
    wrote = 0

    with open(args.inp, newline="", encoding="utf-8") as f_in, \
         open(args.out, "w", newline="", encoding="utf-8") as f_out:
        r = csv.DictReader(f_in)
        w = csv.DictWriter(f_out, fieldnames=r.fieldnames)
        w.writeheader()
        for row in r:
            key = tuple(row[k] for k in keys)
            if key in seen:
                continue
            seen.add(key)
            w.writerow(row); wrote += 1
    print(f"Wrote {wrote} rows.")

if __name__ == "__main__":
    main()
