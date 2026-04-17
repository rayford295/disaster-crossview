"""
Create stratified train / val / test splits for the labeled Eaton Fire dataset.

Handles class imbalance: the Affected class (n=27) is very small, so we
use stratified sampling and report per-class counts in each split.

Usage:
    python scripts/data_prep/train_val_test_split.py --root .
    python scripts/data_prep/train_val_test_split.py --root . --val 0.15 --test 0.15

Outputs:
    data/splits/train.csv
    data/splits/val.csv
    data/splits/test.csv
"""

import argparse
import pandas as pd
from pathlib import Path
from sklearn.model_selection import train_test_split


def make_splits(
    df: pd.DataFrame,
    val_ratio: float = 0.15,
    test_ratio: float = 0.15,
    seed: int = 42,
) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    train_val, test = train_test_split(
        df,
        test_size=test_ratio,
        stratify=df["label"],
        random_state=seed,
    )
    adjusted_val = val_ratio / (1 - test_ratio)
    train, val = train_test_split(
        train_val,
        test_size=adjusted_val,
        stratify=train_val["label"],
        random_state=seed,
    )
    return train, val, test


def report(name: str, df: pd.DataFrame):
    print(f"\n  {name} ({len(df)} images)")
    for cls, cnt in df["damage_class"].value_counts().items():
        pct = cnt / len(df) * 100
        print(f"    {cls:20s}: {cnt:4d}  ({pct:.1f}%)")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", default=".")
    parser.add_argument("--val", type=float, default=0.15)
    parser.add_argument("--test", type=float, default=0.15)
    parser.add_argument("--seed", type=int, default=42)
    args = parser.parse_args()

    root = Path(args.root)
    metadata_path = root / "data" / "eaton_fire_metadata.csv"
    if not metadata_path.exists():
        raise FileNotFoundError(
            f"{metadata_path} not found. Run parse_metadata.py first."
        )

    df = pd.read_csv(metadata_path)
    train, val, test = make_splits(df, args.val, args.test, args.seed)

    out_dir = root / "data" / "splits"
    out_dir.mkdir(parents=True, exist_ok=True)

    for name, split in [("train", train), ("val", val), ("test", test)]:
        path = out_dir / f"{name}.csv"
        split.to_csv(path, index=False)
        print(f"  Saved {path}")

    print("\nSplit summary:")
    for name, split in [("train", train), ("val", val), ("test", test)]:
        report(name, split)

    print(
        f"\n  Note: Affected class has only {(df['label'] == 1).sum()} samples total. "
        "Consider oversampling or class-weighted loss."
    )


if __name__ == "__main__":
    main()
