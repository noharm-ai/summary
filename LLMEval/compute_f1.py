#!/usr/bin/env python3
import csv
import re
import argparse

def compute_f1(p: float, r: float) -> float:
    """
    Compute the F1 score given precision (p) and recall (r).
    """
    if p + r == 0:
        return 0.0
    return 2 * p * r / (p + r)

def parse_precision_recall(text: str) -> tuple[float, float] | None:
    """
    Given a string like '[[0.7333, 0.2708]]',
    return (precision, recall) as floats.
    Returns None if the pattern isn't found.
    """
    # Regex to capture two floats inside double brackets
    m = re.search(r"\[\[\s*([0-9]*\.?[0-9]+)\s*,\s*([0-9]*\.?[0-9]+)\s*\]\]", text)
    if not m:
        return None
    p, r = float(m.group(1)), float(m.group(2))
    return p, r

def main(filename: str, column: str = "RESPONSES"):
    f1_list = []
    with open(filename, encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f, delimiter="\t")
        for idx, row in enumerate(reader, start=1):
            cell = row.get(column, "")
            pr = parse_precision_recall(cell)
            if pr is None:
                print(f"Row {idx}: could not parse [[p, r]] from '{cell}'")
                continue
            p, r = pr
            f1 = compute_f1(p, r)
            f1_list.append(f1)
            print(f"Row {idx}: Precision={p:.4f}, Recall={r:.4f}, F1={f1:.4f}")

    if f1_list:
        mean_f1 = sum(f1_list) / len(f1_list)
        print(f"\nMean F1 over {len(f1_list)} rows: {mean_f1:.4f}")
    else:
        print("\nNo valid F1 scores computed.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Compute F1 from a TSV whose 'RESPONSES' column has [[p, r]] values.")
    parser.add_argument("file", help="Path to the TSV file")
    parser.add_argument(
        "--column", "-c", default="RESPONSES",
        help="Name of the column containing the [[p, r]] text")
    args = parser.parse_args()
    main(args.file, args.column)
