"""
Sample remote sensing raster values at labeled street view point locations.

Given a GeoTIFF (e.g., dNBR, RdNBR, NDVI difference), this script
samples pixel values at each GPS coordinate from the labeled dataset
and appends them as new columns to the metadata CSV.

Typical remote sensing layers for wildfire research:
    - dNBR  : differenced Normalized Burn Ratio (burn severity proxy)
    - RdNBR : relativized dNBR (accounts for pre-fire vegetation)
    - post_NDVI / pre_NDVI : vegetation index before/after fire
    - post_NBR  / pre_NBR  : NBR bands for dNBR computation

Usage:
    python scripts/features/sample_raster_values.py \\
        --root . \\
        --raster /path/to/dNBR.tif \\
        --band_name dNBR

    # Multiple rasters at once
    python scripts/features/sample_raster_values.py \\
        --root . \\
        --raster /path/to/dNBR.tif /path/to/RdNBR.tif \\
        --band_name dNBR RdNBR

Output:
    data/eaton_fire_with_rs_features.csv  (metadata + sampled raster values)
"""

import argparse
import numpy as np
import pandas as pd
import rasterio
from rasterio.transform import rowcol
from pathlib import Path
from tqdm import tqdm


def sample_raster_at_points(
    raster_path: str,
    lats: np.ndarray,
    lons: np.ndarray,
    band: int = 1,
    nodata_fill: float = np.nan,
) -> np.ndarray:
    """
    Sample a single-band GeoTIFF at (lat, lon) coordinates.

    Returns an array of sampled values, with nodata pixels filled
    by nodata_fill (default NaN).
    """
    values = np.full(len(lats), np.nan, dtype=np.float64)

    with rasterio.open(raster_path) as src:
        # Reproject coordinates to the raster CRS if needed
        from pyproj import Transformer

        if src.crs.to_epsg() != 4326:
            transformer = Transformer.from_crs("EPSG:4326", src.crs, always_xy=True)
            xs, ys = transformer.transform(lons, lats)
        else:
            xs, ys = lons, lats

        nodata = src.nodata
        data = src.read(band)

        for i, (x, y) in enumerate(tqdm(zip(xs, ys), total=len(xs), desc=f"  sampling {Path(raster_path).name}", leave=False)):
            try:
                row, col = rowcol(src.transform, x, y)
                if 0 <= row < data.shape[0] and 0 <= col < data.shape[1]:
                    v = data[row, col]
                    values[i] = nodata_fill if (nodata is not None and v == nodata) else float(v)
            except Exception:
                pass  # out-of-bounds → stays NaN

    return values


def main():
    parser = argparse.ArgumentParser(description="Sample raster values at street view point locations")
    parser.add_argument("--root", default=".", help="Dataset root directory")
    parser.add_argument(
        "--raster",
        nargs="+",
        required=True,
        help="Path(s) to GeoTIFF raster file(s)",
    )
    parser.add_argument(
        "--band_name",
        nargs="+",
        required=True,
        help="Column name(s) for the sampled values (must match --raster count)",
    )
    parser.add_argument(
        "--band",
        type=int,
        default=1,
        help="Band index to read (default: 1)",
    )
    args = parser.parse_args()

    root = Path(args.root)
    metadata_path = root / "data" / "eaton_fire_metadata.csv"
    if not metadata_path.exists():
        raise FileNotFoundError(f"{metadata_path} not found. Run parse_metadata.py first.")

    if len(args.raster) != len(args.band_name):
        raise ValueError("--raster and --band_name must have the same number of entries.")

    df = pd.read_csv(metadata_path)
    lats = df["latitude"].values
    lons = df["longitude"].values

    for raster_path, band_name in zip(args.raster, args.band_name):
        print(f"Sampling {band_name} from {raster_path} ...")
        df[band_name] = sample_raster_at_points(raster_path, lats, lons, band=args.band)
        n_valid = df[band_name].notna().sum()
        print(f"  Valid samples: {n_valid}/{len(df)}")
        print(f"  Range: [{df[band_name].min():.4f}, {df[band_name].max():.4f}]")

    out_path = root / "data" / "eaton_fire_with_rs_features.csv"
    df.to_csv(out_path, index=False)
    print(f"\nSaved → {out_path}")
    print(f"Columns: {list(df.columns)}")


if __name__ == "__main__":
    main()
