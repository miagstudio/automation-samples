
#!/usr/bin/env python3
"""
Convert JSONL (one JSON per line) or JSON array to CSV.
"""
import argparse, json, csv, sys

def iter_records(path):
    with open(path, "r", encoding="utf-8") as f:
        first = f.read(1)
        f.seek(0)
        if first == "[":
            data = json.load(f)
            for obj in data:
                yield obj
        else:
            for line in f:
                line = line.strip()
                if not line: 
                    continue
                yield json.loads(line)

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--in", dest="inp", required=True, help="Input JSON/JSONL")
    p.add_argument("--out", dest="out", required=True, help="Output CSV path")
    args = p.parse_args()

    recs = list(iter_records(args.inp))
    if not recs:
        print("No records.", file=sys.stderr); sys.exit(1)
    # union of keys
    keys = []
    seen = set()
    for r in recs:
        for k in r.keys():
            if k not in seen:
                keys.append(k); seen.add(k)

    with open(args.out, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=keys)
        w.writeheader()
        for r in recs:
            w.writerow({k: r.get(k, "") for k in keys})
    print(f"Wrote {len(recs)} records to {args.out}.")

if __name__ == "__main__":
    main()
