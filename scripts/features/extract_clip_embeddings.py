"""
Extract CLIP visual embeddings for street view images.

Uses openai/clip-vit-base-patch32 via HuggingFace Transformers.
Embeddings (512-d) are saved as a numpy array alongside an index CSV
for downstream fusion with remote sensing features.

Usage:
    # Labeled split
    python scripts/features/extract_clip_embeddings.py --root . --split labeled

    # Unlabeled Altadena split
    python scripts/features/extract_clip_embeddings.py --root . --split unlabeled

    # Custom batch size (default 32)
    python scripts/features/extract_clip_embeddings.py --root . --batch_size 64

Outputs:
    data/features/clip_embeddings_labeled.npy         shape: (N, 512)
    data/features/clip_embeddings_labeled_index.csv   rows match embedding rows
"""

import argparse
import numpy as np
import pandas as pd
import torch
from pathlib import Path
from PIL import Image
from tqdm import tqdm
from transformers import CLIPProcessor, CLIPModel

MODEL_NAME = "openai/clip-vit-base-patch32"


def load_model(device: str):
    print(f"Loading {MODEL_NAME} on {device} ...")
    model = CLIPModel.from_pretrained(MODEL_NAME).to(device)
    processor = CLIPProcessor.from_pretrained(MODEL_NAME)
    model.eval()
    return model, processor


def embed_batch(
    image_paths: list,
    model,
    processor,
    device: str,
):
    images, good_paths = [], []
    for p in image_paths:
        try:
            img = Image.open(p).convert("RGB")
            images.append(img)
            good_paths.append(p)
        except Exception as e:
            print(f"  [warn] skipping {p}: {e}")

    if not images:
        return np.zeros((0, 512), dtype=np.float32), []

    inputs = processor(images=images, return_tensors="pt", padding=True).to(device)
    with torch.no_grad():
        feats = model.get_image_features(**inputs)
        feats = feats / feats.norm(dim=-1, keepdim=True)   # L2-normalize

    return feats.cpu().numpy().astype(np.float32), good_paths


def extract_all(
    df: pd.DataFrame,
    filepath_col: str,
    model,
    processor,
    device: str,
    batch_size: int,
):
    paths = df[filepath_col].tolist()
    all_embeddings, kept_indices = [], []

    for start in tqdm(range(0, len(paths), batch_size), desc="Extracting CLIP"):
        batch_paths = paths[start : start + batch_size]
        batch_emb, good_paths = embed_batch(batch_paths, model, processor, device)
        if batch_emb.shape[0] > 0:
            all_embeddings.append(batch_emb)
            path_set = set(good_paths)
            kept_indices.extend(
                [start + i for i, p in enumerate(batch_paths) if p in path_set]
            )

    return np.vstack(all_embeddings), kept_indices


def main():
    parser = argparse.ArgumentParser(description="Extract CLIP embeddings from street view images")
    parser.add_argument("--root", default=".", help="Dataset root directory")
    parser.add_argument(
        "--split",
        choices=["labeled", "unlabeled"],
        default="labeled",
        help="Which dataset split to process",
    )
    parser.add_argument("--batch_size", type=int, default=32)
    args = parser.parse_args()

    root = Path(args.root)

    if torch.cuda.is_available():
        device = "cuda"
    elif torch.backends.mps.is_available():
        device = "mps"
    else:
        device = "cpu"
    print(f"Device: {device}")

    if args.split == "labeled":
        csv_path = root / "data" / "eaton_fire_metadata.csv"
        tag = "labeled"
    else:
        csv_path = root / "data" / "altadena_unlabeled_index.csv"
        tag = "unlabeled"

    if not csv_path.exists():
        raise FileNotFoundError(f"{csv_path} not found. Run parse_metadata.py first.")

    df = pd.read_csv(csv_path)
    print(f"Processing {len(df)} images ...")

    model, processor = load_model(device)
    embeddings, kept_indices = extract_all(df, "filepath", model, processor, device, args.batch_size)

    out_dir = root / "data" / "features"
    out_dir.mkdir(parents=True, exist_ok=True)

    emb_path = out_dir / f"clip_embeddings_{tag}.npy"
    idx_path = out_dir / f"clip_embeddings_{tag}_index.csv"

    np.save(emb_path, embeddings)
    df.iloc[kept_indices].reset_index(drop=True).to_csv(idx_path, index=False)

    print(f"\nEmbeddings shape : {embeddings.shape}  →  {emb_path}")
    print(f"Index CSV        : {len(kept_indices)} rows  →  {idx_path}")


if __name__ == "__main__":
    main()
