# California Wildfire — Eaton Fire Street View & Remote Sensing Dataset

A research dataset combining **Google Street View imagery** with **damage assessment labels** for the 2025 Eaton Fire in Altadena, Los Angeles County, California. Designed to support multi-modal wildfire damage assessment research integrating street-level imagery and remote sensing data.

---

## Background

The **Eaton Fire** ignited on January 7, 2025, in the Altadena–Pasadena area of Los Angeles County. It became one of the most destructive wildfires in California history, burning over 14,000 acres and destroying approximately 9,400 structures. The fire occurred in a densely populated wildland-urban interface (WUI), making it a critical case study for disaster damage assessment research.

This dataset was compiled to support research that integrates:
- **Street-level visual evidence** (Google Street View) of structural damage
- **Satellite remote sensing** data (burn severity, spectral indices) for spatial analysis
- **Geospatially referenced** images enabling fusion with raster and vector GIS layers

---

## Dataset Structure

```
california wildfire/
├── Eaton_Fire/                          # Labeled street view dataset (819 images)
│   ├── Affected_1-9_/
│   │   └── attachments/                 #  27 images — 1–9% damage (minor/partial)
│   ├── Destroyed_50_/
│   │   └── attachments/                 # 638 images — ≥50% damage (destroyed)
│   └── No_Damage/
│       └── attachments/                 # 154 images — no visible damage
│
└── Altadena_Images/                     # Unlabeled street view dataset (~2 GB)
    └── Eaton_Fire_attachments_index_output/
        └── dataset/
            ├── sample_00468/
            │   └── street_view.jpg      # One street view image per location
            ├── sample_00472/
            │   └── street_view.jpg
            └── ...                      # 6,333 sample locations total
```

---

## Data Description

### 1. Eaton_Fire — Labeled Damage Dataset

| Label | Folder | Image Count | Damage Threshold |
|---|---|---|---|
| 0 — No Damage    | `No_Damage/attachments/`      | 4,336 | 0% structural loss |
| 1 — Affected     | `Affected_1-9_/attachments/`  | 1,759 | 1–9% structural loss |
| 2 — Minor        | `Minor_10-25_/attachments/`   |   312 | 10–25% structural loss |
| 3 — Major        | `Major_26-50_/attachments/`   |   155 | 26–50% structural loss |
| 4 — Destroyed    | `Destroyed_50_/attachments/`  | 4,413 | >50% structural loss |
| 5 — Inaccessible | `Inaccessible/attachments/`   |    33 | Site could not be assessed |
| **Total** | | **11,008** | |

The 6-class schema follows the standard FEMA/California damage assessment grading used in official post-disaster inspections.

**Image Naming Convention:**

```
{latitude}_{longitude}_OID{objectID}_A{attachmentID}.jpg
```

Example: `34.165766_-118.094590_OID7760_A20211.jpg`

| Field | Description |
|---|---|
| `latitude` | WGS84 decimal degrees (approx. 34.16–34.20°N) |
| `longitude` | WGS84 decimal degrees (approx. -118.05 to -118.16°W) |
| `OID` | Object ID from the damage assessment database |
| `A` | Attachment ID (multiple views per location possible) |

The embedded coordinates allow **direct spatial join** with any GIS layer or raster dataset (burn severity maps, NDVI, dNBR, LiDAR, etc.) without a separate metadata file.

**Geographic Coverage:** Altadena community, unincorporated Los Angeles County, CA  
**Approximate Bounding Box:** 34.16–34.20°N, 118.05–118.16°W

### 2. Altadena_Images — Unlabeled Street View Dataset

- **6,333 sample locations**, each in its own directory (`sample_XXXXX/`)
- Each directory contains a single `street_view.jpg`
- Total dataset size: ~2.0 GB
- Broader spatial coverage of the Altadena area, suitable for:
  - Pre/post-fire comparison
  - Semi-supervised or self-supervised learning
  - Pseudo-labeling using remote sensing burn extents

---

## Research Applications

This dataset is designed to support the following research directions:

### Multi-Modal Damage Assessment
Fuse street view imagery with satellite-derived indicators:
- **dNBR** (differenced Normalized Burn Ratio) from Landsat-8/9 or Sentinel-2
- **RdNBR** (relativized dNBR) for vegetation burn severity
- **NDVI change** (pre- vs. post-fire vegetation loss)
- **Post-fire LiDAR** for structural height loss detection

### Vision-Based Damage Classification
Train or fine-tune computer vision models (CNN, ViT, CLIP) on the labeled `Eaton_Fire/` split to classify:
- Binary: Damaged vs. Undamaged
- Multi-class: No Damage / Affected / Destroyed

### Spatial Fusion Pipeline
Use embedded GPS coordinates to:
1. Extract pixel values from remote sensing rasters at each image location
2. Build a tabular feature matrix combining visual embeddings + spectral indices
3. Train multi-modal classifiers or cross-modal retrieval models

### Spatial Generalization
Evaluate whether models trained on labeled data (`Eaton_Fire/`) generalize spatially across the broader `Altadena_Images/` unlabeled set.

---

## Data Sources & Attribution

| Dataset | Source |
|---|---|
| Street View Images | Google Street View (via ArcGIS / damage assessment workflow) |
| Damage Labels | Los Angeles County damage assessment records (Eaton Fire, Jan 2025) |
| Geographic Reference | WGS84 coordinate system |

> **Note:** Street view images are subject to Google's terms of service. Use for academic research only.

---

## Related Remote Sensing Resources

The following public datasets complement this street view corpus:

| Dataset | Description | Source |
|---|---|---|
| MTBS (Monitoring Trends in Burn Severity) | Pre/post-fire dNBR, burn perimeters | [mtbs.gov](https://www.mtbs.gov/) |
| USGS Landsat Collection 2 | Multispectral imagery for spectral index computation | [USGS EarthExplorer](https://earthexplorer.usgs.gov/) |
| Copernicus Sentinel-2 | 10m resolution MSI imagery | [Copernicus Hub](https://scihub.copernicus.eu/) |
| CALFIRE Fire Perimeters | Official California fire perimeter polygons | [CALFIRE FRAP](https://www.fire.ca.gov/incidents/2025/1/7/eaton-fire/) |
| Microsoft Buildings Footprints | Building polygons for WUI damage analysis | [GitHub](https://github.com/microsoft/USBuildingFootprints) |
| 3DEP LiDAR | 1m post-fire LiDAR point clouds | [USGS National Map](https://www.usgs.gov/3d-elevation-program) |

---

## Getting Started

### Prerequisites

```bash
pip install pillow numpy pandas geopandas rasterio matplotlib
```

### Parse Geolocation from Filenames

```python
import os
import re
import pandas as pd

def parse_filename(fname):
    match = re.match(r"([\d.]+)_([-\d.]+)_OID(\d+)_A(\d+)\.jpg", fname)
    if match:
        lat, lon, oid, aid = match.groups()
        return float(lat), float(lon), int(oid), int(aid)
    return None

records = []
for damage_class in ["No_Damage", "Affected_1-9_", "Destroyed_50_"]:
    folder = f"Eaton_Fire/{damage_class}/attachments"
    for fname in os.listdir(folder):
        parsed = parse_filename(fname)
        if parsed:
            lat, lon, oid, aid = parsed
            records.append({
                "filename": fname,
                "latitude": lat,
                "longitude": lon,
                "object_id": oid,
                "attachment_id": aid,
                "damage_class": damage_class,
                "filepath": os.path.join(folder, fname)
            })

df = pd.DataFrame(records)
print(df.shape)       # (819, 7)
print(df["damage_class"].value_counts())
```

### Convert to GeoDataFrame for Spatial Analysis

```python
import geopandas as gpd
from shapely.geometry import Point

gdf = gpd.GeoDataFrame(
    df,
    geometry=[Point(row.longitude, row.latitude) for _, row in df.iterrows()],
    crs="EPSG:4326"
)

# Reproject to California Albers for meter-based spatial operations
gdf_ca = gdf.to_crs("EPSG:3310")

# Export for use in QGIS or ArcGIS
gdf.to_file("eaton_fire_streetview_points.geojson", driver="GeoJSON")
```

### Sample Images by Class

```python
import random
from PIL import Image
import matplotlib.pyplot as plt

samples = df.groupby("damage_class").apply(lambda x: x.sample(3)).reset_index(drop=True)

fig, axes = plt.subplots(3, 3, figsize=(12, 10))
for i, row in samples.iterrows():
    ax = axes[i // 3, i % 3]
    img = Image.open(row["filepath"])
    ax.imshow(img)
    ax.set_title(f"{row['damage_class']}\n({row['latitude']:.4f}, {row['longitude']:.4f})")
    ax.axis("off")
plt.tight_layout()
plt.savefig("sample_grid.png", dpi=150)
plt.show()
```

---

## Dataset Statistics

| Class | Label | Count | % of Total |
|---|---|---|---|
| No Damage    | 0 | 4,336 | 39.4% |
| Affected     | 1 | 1,759 | 16.0% |
| Minor        | 2 |   312 |  2.8% |
| Major        | 3 |   155 |  1.4% |
| Destroyed    | 4 | 4,413 | 40.1% |
| Inaccessible | 5 |    33 |  0.3% |
| **Total (labeled)** | | **11,008** | **100%** |
| Unlabeled (Altadena) | — | 6,333 | — |

> The distribution is bimodal: No Damage and Destroyed together account for ~79% of the labeled set, reflecting the Eaton Fire's spatial pattern — neighborhoods were either mostly intact or completely devastated. The transitional classes (Minor, Major) are rare and may benefit from oversampling or class-weighted loss.

---

## Repository Contents

```
.
├── README.md
├── requirements.txt
├── .gitignore
│
├── scripts/
│   ├── data_prep/
│   │   ├── parse_metadata.py          # Parse filenames → CSV + GeoJSON
│   │   └── train_val_test_split.py    # Stratified train/val/test split
│   ├── visualization/
│   │   ├── sample_grid.py             # Grid of sample images by damage class
│   │   └── map_damage_points.py       # Interactive Folium map of locations
│   └── features/
│       ├── extract_clip_embeddings.py # CLIP visual embeddings (512-d)
│       └── sample_raster_values.py    # Sample RS raster values at GPS points
│
├── notebooks/
│   └── 01_dataset_exploration.ipynb  # End-to-end dataset exploration
│
├── data/                              # Generated by scripts (gitignored)
└── outputs/                           # Generated figures/maps (gitignored)
```

### Recommended Workflow

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Parse filenames → metadata CSV + GeoJSON
python scripts/data_prep/parse_metadata.py --root .

# 3. Create train/val/test splits
python scripts/data_prep/train_val_test_split.py --root .

# 4. Visualize samples and spatial distribution
python scripts/visualization/sample_grid.py --root .
python scripts/visualization/map_damage_points.py --root .

# 5. Extract CLIP embeddings
python scripts/features/extract_clip_embeddings.py --root . --split labeled

# 6. Sample burn severity (dNBR) raster values
python scripts/features/sample_raster_values.py \
    --root . \
    --raster /path/to/dNBR.tif \
    --band_name dNBR
```

> Raw image data is excluded from version control due to file size (~2.3 GB). Store locally or on a shared HPC/cloud storage system.

---

## Citation

If you use this dataset in your research, please cite the relevant sources (LA County damage assessment, CALFIRE Eaton Fire incident report) and note the data collection date (January–April 2025).

---

## License

Dataset usage is subject to:
- Google Street View Terms of Service (street view imagery)
- LA County open data terms (damage assessment records)

Code and documentation in this repository are released under the **MIT License**.

---

## Contact

Research project by [Yifan (Ray) Yang](https://github.com/rayford295) — Department of Geography & GIS  
Focus: Wildfire damage assessment, street-level imagery, remote sensing fusion, WUI resilience
