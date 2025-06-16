#!/usr/bin/env python3
"""
Fix mixes of objects / JSON-stringified objects in the INCAR dataset.
There are some dialogues that are stored as JSON strings instead of
Python dicts, which causes issues when loading the dataset.
This script will read the original INCAR .json file, remove the stringified
dialogues, and write a new file with all dialogues as proper dicts.
This script is intended to be run from the command line.
It takes two arguments:
    --infile: Path to the original INCAR .json file
    --outfile: Path to the cleaned output file
It will read the input file, convert any stringified dialogues to dicts,
and write the cleaned data to the output file.
# -*- coding: utf-8 -*-

Usage:
    python fix_incar_json.py  \
        --infile  data/train.json \
        --outfile data/train_fixed.json
"""
import json
import argparse
from pathlib import Path

def load_json(path: Path):
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)

def dump_json(obj, path: Path):
    with path.open("w", encoding="utf-8") as f:
        json.dump(obj, f, ensure_ascii=False, indent=2)

def normalise_dialogues(raw_data: dict) -> dict:
    """
    Convert any value that is a JSON string into a real dict.
    Leaves already-correct entries untouched.
    """
    fixed = {}
    for dial_id, dlg in raw_data.items():
        # If the dialogue is already a dict we’re good.
        if isinstance(dlg, dict):
            fixed[dial_id] = dlg
            continue

        # If it’s a string, try to decode it.
        if isinstance(dlg, str):
            try:
                fixed[dial_id] = json.loads(dlg)
            except json.JSONDecodeError as err:
                # Log and skip completely broken lines
                print(f"[WARN] Dialogue {dial_id} could not be parsed: {err}")
            continue

        # Anything else (rare) – log and drop.
        print(f"[WARN] Dialogue {dial_id} has unexpected type {type(dlg)}")

    return fixed


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--infile", required=True, help="Original INCAR .json file")
    parser.add_argument("--outfile", required=True, help="Destination for cleaned file")
    args = parser.parse_args()

    src = Path(args.infile)
    dst = Path(args.outfile)
    data = load_json(src)
    cleaned = normalise_dialogues(data)
    dump_json(cleaned, dst)
    print(f"✔  Cleaned file written to {dst} (total dialogues: {len(cleaned)})")


if __name__ == "__main__":
    main()
