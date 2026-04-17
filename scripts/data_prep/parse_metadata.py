"""
Parse Eaton Fire street view image filenames into a structured metadata CSV.

Filename format: {latitude}_{longitude}_OID{objectID}_A{attachmentID}.jpg
Example:         34.165766_-118.094590_OID7760_A20211.jpg

Outputs:
    data/eaton_fire_metadata.csv  — one row per image with coords + label
    data/eaton_fire_points.geojson — GeoJSON for GIS use
"""

import os
import re
import json
import argparse
import pandas as pd
from pathlib import Path

DAMAGE_CLASSES = {
    "No_Damage":    0,
    "Affected_1-9_": 1,
    "Destroyed_50_": 2,
}

LABEL_NAMES = {0: "no_damage", 1: "affected", 2: "destroyed"}

FILENAME_RE = re.compile(
    r"(?P<lat>-?[\d.]+)_(?P<lon>-?[\d.]+)_OID(?P<oid>\d+)_A(?P<aid>\d+)\.jpg",
    re.IGNORECASE,
)


def parse_labeled_split(eaton_fire_root: Path) -> pd.DataFrame:
    records = []
    for class_name, label in DAMAGE_CLASSES.items():
        folder = eaton_fire_root / class_name / "attachments"
        if not folder.exists():
            print(f"  [warn] not found: {folder}")
            continue
        for fname in sorted(os.listdir(folder)):
            m = FILENAME_RE.match(fname)
            if not m:
                continue
            records.append(
                {
                    "filename": fname,
                    "filepath": str(folder / fname),
                    "latitude": float(m.group("lat")),
                    "longitude": float(m.group("lon")),
                    "object_id": int(m.group("oid")),
                    "attachment_id": int(m.group("aid")),
                    "damage_class": class_name,
                    "label": label,
                    "label_name": LABEL_NAMES[label],
                }
            )
    return pd.DataFrame(records)


def parse_altadena_unlabeled(altadena_root: Path) -> pd.DataFrame:
    """Parse sample_XXXXX directories from the unlabeled Altadena dataset."""
    dataset_dir = altadena_root / "Eaton_Fire_attachments_index_output" / "dataset"
    if not dataset_dir.exists():
        print(f"  [warn] not found: {dataset_dir}")
        return pd.DataFrame()

    records = []
    for sample_dir in sorted(dataset_dir.iterdir()):
        img_path = sample_dir / "street_view.jpg"
        if img_path.exists():
            records.append(
                {
                    "sample_id": sample_dir.name,
                    "filepath": str(img_path),
                    "split": "unlabeled",
                }
            )
    return pd.DataFrame(records)


def to_geojson(df: pd.DataFrame, out_path: Path):
    """Convert labeled metadata DataFrame to GeoJSON FeatureCollection."""
    features = []
    for _, row in df.iterrows():
        features.append(
            {
                "type": "Feature",
                "geometry": {
                    "type": "Point",
                    "coordinates": [row["longitude"], row["latitude"]],
                },
                "properties": {
                    "filename": row["filename"],
                    "object_id": row["object_id"],
                    "damage_class": row["damage_class"],
                    "label": row["label"],
                    "label_name": row["label_name"],
                },
            }
        )
    geojson = {"type": "FeatureCollection", "features": features}
    with open(out_path, "w") as f:
        json.dump(geojson, f, indent=2)
    print(f"  GeoJSON saved → {out_path}  ({len(features)} features)")


def main():
    parser = argparse.ArgumentParser(description="Parse Eaton Fire metadata")
    parser.add_argument(
        "--root",
        default=".",
        help="Path to the dataset root directory (default: current dir)",
    )
    args = parser.parse_args()

    root = Path(args.root)
    out_dir = root / "data"
    out_dir.mkdir(exist_ok=True)

    print("Parsing labeled split (Eaton_Fire/) ...")
    df_labeled = parse_labeled_split(root / "Eaton_Fire")
    print(f"  Total images: {len(df_labeled)}")
    print(df_labeled["damage_class"].value_counts().to_string())

    csv_path = out_dir / "eaton_fire_metadata.csv"
    df_labeled.to_csv(csv_path, index=False)
    print(f"  CSV saved → {csv_path}")

    geojson_path = out_dir / "eaton_fire_points.geojson"
    to_geojson(df_labeled, geojson_path)

    print("\nParsing unlabeled split (Altadena_Images/) ...")
    df_unlabeled = parse_altadena_unlabeled(root / "Altadena_Images")
    if not df_unlabeled.empty:
        print(f"  Total samples: {len(df_unlabeled)}")
        unlabeled_csv = out_dir / "altadena_unlabeled_index.csv"
        df_unlabeled.to_csv(unlabeled_csv, index=False)
        print(f"  CSV saved → {unlabeled_csv}")


if __name__ == "__main__":
    main()
