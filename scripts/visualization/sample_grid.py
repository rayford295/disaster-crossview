"""
Visualize a grid of sample street view images for each damage class.

Usage:
    python scripts/visualization/sample_grid.py --root . --n 6
    python scripts/visualization/sample_grid.py --root . --n 4 --seed 99
"""

import argparse
import random
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from pathlib import Path
from PIL import Image

CLASS_COLORS = {
    "No_Damage":     "#2ecc71",
    "Affected_1-9_": "#f39c12",
    "Destroyed_50_": "#e74c3c",
}
CLASS_LABELS = {
    "No_Damage":     "No Damage",
    "Affected_1-9_": "Affected (1–9%)",
    "Destroyed_50_": "Destroyed (≥50%)",
}


def load_images(df: pd.DataFrame, damage_class: str, n: int, seed: int):
    subset = df[df["damage_class"] == damage_class].sample(
        min(n, len(df[df["damage_class"] == damage_class])),
        random_state=seed,
    )
    images, titles = [], []
    for _, row in subset.iterrows():
        try:
            img = Image.open(row["filepath"]).convert("RGB")
            images.append(img)
            titles.append(f"({row['latitude']:.4f}, {row['longitude']:.4f})")
        except Exception as e:
            print(f"  [warn] could not load {row['filepath']}: {e}")
    return images, titles


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", default=".")
    parser.add_argument("--n", type=int, default=6, help="Samples per class")
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--out", default=None, help="Output PNG path")
    args = parser.parse_args()

    root = Path(args.root)
    metadata_path = root / "data" / "eaton_fire_metadata.csv"
    if not metadata_path.exists():
        raise FileNotFoundError(
            f"{metadata_path} not found. Run scripts/data_prep/parse_metadata.py first."
        )

    df = pd.read_csv(metadata_path)
    classes = list(CLASS_LABELS.keys())
    n = args.n

    fig, axes = plt.subplots(len(classes), n, figsize=(n * 3, len(classes) * 3))
    fig.suptitle("Eaton Fire — Street View Samples by Damage Class", fontsize=14, y=1.01)

    for row_idx, cls in enumerate(classes):
        images, titles = load_images(df, cls, n, args.seed)
        color = CLASS_COLORS[cls]

        for col_idx in range(n):
            ax = axes[row_idx, col_idx]
            if col_idx < len(images):
                ax.imshow(images[col_idx])
                ax.set_title(titles[col_idx], fontsize=6, pad=2)
            else:
                ax.set_facecolor("#f0f0f0")
                ax.text(0.5, 0.5, "N/A", ha="center", va="center", transform=ax.transAxes)
            ax.axis("off")
            for spine in ax.spines.values():
                spine.set_visible(True)
                spine.set_edgecolor(color)
                spine.set_linewidth(2.5)

        axes[row_idx, 0].set_ylabel(
            CLASS_LABELS[cls], rotation=90, labelpad=8, fontsize=10, color=color
        )

    plt.tight_layout()

    out_path = args.out or str(root / "outputs" / "sample_grid.png")
    Path(out_path).parent.mkdir(parents=True, exist_ok=True)
    plt.savefig(out_path, dpi=150, bbox_inches="tight")
    print(f"Saved → {out_path}")
    plt.show()


if __name__ == "__main__":
    main()
