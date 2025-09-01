
#!/usr/bin/env python3
"""
Bulk rename files by adding a prefix/suffix or replacing text.
"""
import argparse, os, sys

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--dir", default=".", help="Target directory")
    p.add_argument("--prefix", default="", help="Add this prefix")
    p.add_argument("--suffix", default="", help="Add this suffix before extension")
    p.add_argument("--replace", nargs=2, metavar=("OLD","NEW"), help="Replace substring OLD with NEW")
    args = p.parse_args()

    count = 0
    for name in os.listdir(args.dir):
        old = os.path.join(args.dir, name)
        if not os.path.isfile(old): 
            continue
        base, ext = os.path.splitext(name)
        new_base = base
        if args.replace:
            new_base = new_base.replace(args.replace[0], args.replace[1])
        new_name = f"{args.prefix}{new_base}{args.suffix}{ext}"
        new = os.path.join(args.dir, new_name)
        if old != new:
            os.rename(old, new)
            count += 1
    print(f"Renamed {count} files.")

if __name__ == "__main__":
    main()
