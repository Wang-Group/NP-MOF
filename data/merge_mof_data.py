#!/usr/bin/env python3
"""
merge_mof_data_v2.py

Scans a base folder (default: ./data) that contains many MOF subfolders like:
  ./data/MOF-808/
    ├─ MOF-808.csv        (preferred if present; otherwise any single CSV in the folder)
    └─ geo_pro/
         └─ data.csv

For each MOF folder, merges the first row of the main CSV with the first row of geo_pro/data.csv,
keeping the ORIGINAL column names (no prefixes). The folder name is stored in 'mof_name'.
All MOFs are stacked into a single CSV (MOF_data.csv by default).

Usage:
  python merge_mof_data_v2.py --base ./data --output MOF_data.csv

Notes & assumptions:
- If a CSV has multiple rows, only the first row is used.
- If both CSVs have identical column names, duplicates will appear in the final table (pandas allows this for concat).
- If there's ambiguity about the main CSV (multiple CSVs), the folder is skipped with a reason flagged.

"""
from __future__ import annotations

import argparse
from pathlib import Path
import sys
import pandas as pd


def find_main_csv(folder: Path) -> Path | None:
    """Prefer <foldername>.csv. If not present, use the only CSV in the folder.
    If multiple CSVs exist, return None to signal ambiguity.
    """
    preferred = folder / f"{folder.name}.csv"
    if preferred.exists():
        return preferred

    csvs = sorted(folder.glob("*.csv"))
    if len(csvs) == 1:
        return csvs[0]
    # None if 0 or many
    return None


def read_first_row(csv_path: Path) -> pd.DataFrame:
    """Read the CSV and return the first row as a single-row DataFrame with original column names.
    If missing/empty, return a 1-row empty DataFrame.
    """
    try:
        df = pd.read_csv(csv_path)
    except FileNotFoundError:
        return pd.DataFrame([{}])
    except pd.errors.EmptyDataError:
        return pd.DataFrame([{}])

    if df.shape[0] == 0:
        return pd.DataFrame([{}])

    return df.iloc[[0]].copy().reset_index(drop=True)


def process_base_folder(base: Path) -> pd.DataFrame:
    """Process the base folder and return a DataFrame with one row per MOF subfolder."""
    if not base.exists() or not base.is_dir():
        raise FileNotFoundError(f"Base folder not found or not a directory: {base}")

    all_rows = []
    for mof_dir in sorted([p for p in base.iterdir() if p.is_dir()]):
        mof_name = mof_dir.name

        main_csv = find_main_csv(mof_dir)
        geo_csv = mof_dir / "geo_pro" / "data.csv"

        status = {
            "filename": mof_name,
        }


        # Build the combined single row
        main_row = read_first_row(main_csv)
        geo_row = read_first_row(geo_csv)

        combined = pd.concat([main_row.reset_index(drop=True),
                              geo_row.reset_index(drop=True)], axis=1)
        combined["MOF_index"] = len(all_rows)
        combined["MOF"] = mof_name
        # Insert identifier and status columns
        all_rows.append(combined)

    if not all_rows:
        return pd.DataFrame(columns=["filename"])

    return pd.concat(all_rows, ignore_index=True)


def main():
    parser = argparse.ArgumentParser(description="Merge MOF CSVs with geo_pro/data.csv into one MOF_data.csv")
    parser.add_argument("--base", type=str, default="./data",
                        help="Base directory containing MOF subfolders (default: ./data)")
    parser.add_argument("--output", type=str, default="MOF_data.csv",
                        help="Output CSV filename (default: MOF_data.csv). If a relative path, it's placed inside --base.")
    args = parser.parse_args()

    base = Path(args.base).resolve()
    try:
        df = process_base_folder(base)
    except Exception as e:
        print(f"ERROR: {e}", file=sys.stderr)
        sys.exit(1)

    out_path = Path(args.output)
    if not out_path.is_absolute():
        out_path = base / out_path

    out_path.parent.mkdir(parents=True, exist_ok=True)
    df = df.drop(columns=["Unnamed: 0"])

    col = "MOF"
    df = df[[col] + [c for c in df.columns if c != col]]
    df.to_csv(out_path, index=False)

    print(f"Wrote {out_path} with {len(df)} row(s) and {len(df.columns)} column(s).")

if __name__ == "__main__":
    main()
