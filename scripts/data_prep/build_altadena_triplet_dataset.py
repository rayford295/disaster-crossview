"""
Build Altadena triplets with pre-disaster remote sensing, post-disaster remote
sensing, and post-disaster street-view images.

The source post-disaster dataset already contains per-sample folders with:

    remote_sensing.jpg
    street_view.jpg

This script crops matching 512 x 512 pre-disaster remote-sensing chips from a
large GeoTIFF using the latitude/longitude stored in dataset_index.csv, then
creates a new sample-organized triplet dataset.
"""

from __future__ import annotations

import argparse
import csv
import json
import os
import shutil
from pathlib import Path
from typing import Any

import numpy as np
import rasterio
from PIL import Image
from rasterio.enums import Resampling
from rasterio.windows import Window


TRIPLET_FILENAMES = {
    "pre": "pre_disaster_remote_sensing.jpg",
    "post": "post_disaster_remote_sensing.jpg",
    "street": "street_view.jpg",
}


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp_path = path.with_suffix(path.suffix + ".tmp")
    tmp_path.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    tmp_path.replace(path)


def link_or_copy(src: Path, dst: Path, mode: str, overwrite: bool) -> str:
    if dst.exists():
        if not overwrite:
            return "exists"
        dst.unlink()

    dst.parent.mkdir(parents=True, exist_ok=True)

    if mode == "copy":
        shutil.copy2(src, dst)
        return "copied"

    try:
        os.link(src, dst)
        return "hardlinked"
    except OSError:
        shutil.copy2(src, dst)
        return "copied_fallback"


def read_rows(index_csv: Path) -> list[dict[str, str]]:
    with index_csv.open(newline="", encoding="utf-8-sig") as f:
        return list(csv.DictReader(f))


def image_from_array(data: np.ndarray) -> Image.Image:
    if data.shape[0] == 1:
        data = np.repeat(data, 3, axis=0)
    elif data.shape[0] > 3:
        data = data[:3]

    arr = np.moveaxis(data, 0, -1)
    if arr.dtype != np.uint8:
        arr = np.clip(arr, 0, 255).astype(np.uint8)
    return Image.fromarray(arr, "RGB")


def lonlat_to_utm_zone_11n(longitude: float, latitude: float) -> tuple[float, float]:
    """Project WGS84 lon/lat into UTM zone 11N without requiring a PROJ database."""
    lat = np.deg2rad(latitude)
    lon = np.deg2rad(longitude)
    lon0 = np.deg2rad(-117.0)

    a = 6378137.0
    f = 1 / 298.257223563
    k0 = 0.9996
    e2 = f * (2 - f)
    e4 = e2 * e2
    e6 = e4 * e2
    ep2 = e2 / (1 - e2)

    sin_lat = np.sin(lat)
    cos_lat = np.cos(lat)
    tan_lat = np.tan(lat)

    n = a / np.sqrt(1 - e2 * sin_lat * sin_lat)
    t = tan_lat * tan_lat
    c = ep2 * cos_lat * cos_lat
    a_term = cos_lat * (lon - lon0)

    m = a * (
        (1 - e2 / 4 - 3 * e4 / 64 - 5 * e6 / 256) * lat
        - (3 * e2 / 8 + 3 * e4 / 32 + 45 * e6 / 1024) * np.sin(2 * lat)
        + (15 * e4 / 256 + 45 * e6 / 1024) * np.sin(4 * lat)
        - (35 * e6 / 3072) * np.sin(6 * lat)
    )

    easting = 500000 + k0 * n * (
        a_term
        + (1 - t + c) * a_term**3 / 6
        + (5 - 18 * t + t**2 + 72 * c - 58 * ep2) * a_term**5 / 120
    )
    northing = k0 * (
        m
        + n
        * tan_lat
        * (
            a_term**2 / 2
            + (5 - t + 9 * c + 4 * c**2) * a_term**4 / 24
            + (61 - 58 * t + t**2 + 600 * c - 330 * ep2) * a_term**6 / 720
        )
    )
    return float(easting), float(northing)


def project_lonlat(src: rasterio.io.DatasetReader, longitude: float, latitude: float) -> tuple[float, float]:
    crs_text = str(src.crs or "")
    if "UTM zone 11N" in crs_text or "UTM_Zone_11N" in crs_text:
        return lonlat_to_utm_zone_11n(longitude, latitude)
    return longitude, latitude


def crop_pre_disaster(
    src: rasterio.io.DatasetReader,
    longitude: float,
    latitude: float,
    crop_size: int,
) -> tuple[Image.Image, dict[str, Any]]:
    x, y = project_lonlat(src, longitude, latitude)

    row, col = src.index(x, y)
    half = crop_size / 2
    window = Window(round(col - half), round(row - half), crop_size, crop_size)
    boundless = (
        window.col_off < 0
        or window.row_off < 0
        or window.col_off + window.width > src.width
        or window.row_off + window.height > src.height
    )

    data = src.read(
        list(range(1, min(src.count, 3) + 1)),
        window=window,
        out_shape=(min(src.count, 3), crop_size, crop_size),
        boundless=True,
        fill_value=0,
        resampling=Resampling.bilinear,
    )
    valid_mask = np.any(data > 0, axis=0)
    nonzero_fraction = float(np.count_nonzero(valid_mask) / valid_mask.size)
    return image_from_array(data), {
        "pre_pixel_x": col,
        "pre_pixel_y": row,
        "pre_crop_box": f"{int(window.col_off)},{int(window.row_off)},{int(window.col_off + window.width)},{int(window.row_off + window.height)}",
        "pre_crop_boundless": str(bool(boundless)).lower(),
        "pre_nonzero_fraction": f"{nonzero_fraction:.6f}",
    }


def build_triplets(args: argparse.Namespace) -> dict[str, Any]:
    source_dataset = args.source_dataset.resolve()
    index_csv = args.index_csv.resolve()
    pre_disaster_tif = args.pre_disaster_tif.resolve()
    output_root = args.output_root.resolve()
    output_index = output_root / "_triplet_dataset_index.csv"
    progress_json = args.progress_json.resolve() if args.progress_json else output_root / "_build_progress.json"
    summary_json = output_root / "_build_summary.json"

    all_rows = read_rows(index_csv)
    rows = all_rows[args.start_row - 1 :]
    if args.limit:
        rows = rows[: args.limit]

    output_root.mkdir(parents=True, exist_ok=True)
    fieldnames = [
        "pair_id",
        "sample_folder",
        "triplet_sample_folder",
        "pre_disaster_remote_sensing_relative_path",
        "post_disaster_remote_sensing_relative_path",
        "street_view_relative_path",
        "latitude",
        "longitude",
        "category",
        "objectid",
        "attachment_id",
        "pre_crop_status",
        "pre_pixel_x",
        "pre_pixel_y",
        "pre_crop_box",
        "pre_crop_boundless",
        "pre_nonzero_fraction",
        "post_link_status",
        "street_link_status",
    ]

    summary = {
        "source_dataset": str(source_dataset),
        "index_csv": str(index_csv),
        "pre_disaster_tif": str(pre_disaster_tif),
        "output_root": str(output_root),
        "crop_size": args.crop_size,
        "link_mode": args.link_mode,
        "source_total_rows": len(all_rows),
        "start_row": args.start_row,
        "total_rows_seen": len(rows),
        "triplets_written": 0,
        "skipped_missing_source": 0,
        "skipped_bad_coordinate": 0,
        "failed_pre_crop": 0,
        "skipped_empty_pre": 0,
    }

    write_mode = "a" if args.append_index else "w"
    write_header = not args.append_index or not output_index.exists() or output_index.stat().st_size == 0

    with rasterio.open(pre_disaster_tif) as pre_src, output_index.open(
        write_mode, newline="", encoding="utf-8"
    ) as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        if write_header:
            writer.writeheader()

        for i, row in enumerate(rows, start=1):
            pair_id = row.get("pair_id") or Path(row.get("sample_folder", "")).name
            if not pair_id:
                summary["skipped_missing_source"] += 1
                continue

            source_sample = source_dataset / pair_id
            post_src = source_sample / "remote_sensing.jpg"
            street_src = source_sample / "street_view.jpg"
            if not post_src.exists() or not street_src.exists():
                summary["skipped_missing_source"] += 1
                continue

            try:
                latitude = float(row["latitude"])
                longitude = float(row["longitude"])
            except (KeyError, TypeError, ValueError):
                summary["skipped_bad_coordinate"] += 1
                continue

            triplet_sample = output_root / pair_id
            pre_dst = triplet_sample / TRIPLET_FILENAMES["pre"]
            post_dst = triplet_sample / TRIPLET_FILENAMES["post"]
            street_dst = triplet_sample / TRIPLET_FILENAMES["street"]

            try:
                if args.overwrite or not pre_dst.exists():
                    pre_img, pre_meta = crop_pre_disaster(
                        pre_src,
                        longitude=longitude,
                        latitude=latitude,
                        crop_size=args.crop_size,
                    )
                    if (
                        args.skip_empty_pre
                        and float(pre_meta["pre_nonzero_fraction"]) < args.min_nonzero_fraction
                    ):
                        summary["skipped_empty_pre"] += 1
                        continue
                    triplet_sample.mkdir(parents=True, exist_ok=True)
                    pre_img.save(pre_dst, quality=args.jpeg_quality, optimize=True)
                    pre_status = "cropped"
                else:
                    pre_meta = {
                        "pre_pixel_x": "",
                        "pre_pixel_y": "",
                        "pre_crop_box": "",
                        "pre_crop_boundless": "",
                        "pre_nonzero_fraction": "",
                    }
                    pre_status = "exists"
            except Exception as exc:
                summary["failed_pre_crop"] += 1
                summary["last_pre_crop_error"] = f"{pair_id}: {type(exc).__name__}: {exc}"
                continue

            post_status = link_or_copy(post_src, post_dst, args.link_mode, args.overwrite)
            street_status = link_or_copy(street_src, street_dst, args.link_mode, args.overwrite)

            rel_sample = pair_id
            out_row = {
                "pair_id": pair_id,
                "sample_folder": row.get("sample_folder", ""),
                "triplet_sample_folder": rel_sample,
                "pre_disaster_remote_sensing_relative_path": f"{rel_sample}/{TRIPLET_FILENAMES['pre']}",
                "post_disaster_remote_sensing_relative_path": f"{rel_sample}/{TRIPLET_FILENAMES['post']}",
                "street_view_relative_path": f"{rel_sample}/{TRIPLET_FILENAMES['street']}",
                "latitude": row.get("latitude", ""),
                "longitude": row.get("longitude", ""),
                "category": row.get("category", ""),
                "objectid": row.get("objectid", ""),
                "attachment_id": row.get("attachment_id", ""),
                "pre_crop_status": pre_status,
                "pre_pixel_x": pre_meta["pre_pixel_x"],
                "pre_pixel_y": pre_meta["pre_pixel_y"],
                "pre_crop_box": pre_meta["pre_crop_box"],
                "pre_crop_boundless": pre_meta["pre_crop_boundless"],
                "pre_nonzero_fraction": pre_meta["pre_nonzero_fraction"],
                "post_link_status": post_status,
                "street_link_status": street_status,
            }
            writer.writerow(out_row)
            summary["triplets_written"] += 1

            if i == 1 or i % args.progress_every == 0:
                summary["last_pair_id"] = pair_id
                summary["rows_processed"] = i
                write_json(progress_json, summary)
                print(
                    f"[{i}/{len(rows)}] wrote {summary['triplets_written']} triplets; last={pair_id}",
                    flush=True,
                )

    summary["rows_processed"] = len(rows)
    write_json(progress_json, summary)
    write_json(summary_json, summary)
    print(json.dumps(summary, indent=2), flush=True)
    return summary


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Build pre/post/street-view Altadena triplets."
    )
    parser.add_argument("--source-dataset", required=True, type=Path)
    parser.add_argument("--index-csv", required=True, type=Path)
    parser.add_argument("--pre-disaster-tif", required=True, type=Path)
    parser.add_argument("--output-root", required=True, type=Path)
    parser.add_argument("--crop-size", default=512, type=int)
    parser.add_argument("--jpeg-quality", default=90, type=int)
    parser.add_argument(
        "--link-mode",
        default="hardlink",
        choices=["hardlink", "copy"],
        help="Use hardlinks for existing post/street images when possible.",
    )
    parser.add_argument("--overwrite", action="store_true")
    parser.add_argument(
        "--skip-empty-pre",
        action="store_true",
        help="Skip samples whose pre-disaster crop is mostly empty/nodata.",
    )
    parser.add_argument(
        "--min-nonzero-fraction",
        default=0.01,
        type=float,
        help="Minimum nonzero pixel fraction required when --skip-empty-pre is set.",
    )
    parser.add_argument("--start-row", default=1, type=int)
    parser.add_argument("--limit", type=int)
    parser.add_argument("--append-index", action="store_true")
    parser.add_argument("--progress-every", default=250, type=int)
    parser.add_argument("--progress-json", type=Path)
    return parser.parse_args()


def main() -> None:
    build_triplets(parse_args())


if __name__ == "__main__":
    main()
