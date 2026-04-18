# California Wildfire Eaton Fire

Codebase for building a reproducible wildfire damage assessment workflow around the 2025 Eaton Fire in Altadena, California.

This repository is now configured to keep the full project structure on GitHub while **excluding raw imagery, downloaded indexes, derived tables, and other bulky local artifacts**. That makes it safer for long-term development, collaboration, and future pushes.

## Current Data Snapshot

The counts below reflect the local dataset snapshot currently present in this project on April 17, 2026.

### Labeled Eaton Fire Street-View Dataset

| Class | Count | Share |
|---|---:|---:|
| No_Damage | 4,336 | 39.4% |
| Affected_1-9_ | 1,759 | 16.0% |
| Minor_10-25_ | 312 | 2.8% |
| Major_26-50_ | 155 | 1.4% |
| Destroyed_50_ | 4,413 | 40.1% |
| Inaccessible | 33 | 0.3% |
| **Total** | **11,008** | **100.0%** |

### Unlabeled Altadena and Matching Status

- Raw unlabeled Altadena street-view images: `6,333`
- Rows in `Altadena_Images/Eaton_Fire_attachments_index.csv`: `19,780`
- Sample folders under `Altadena_Images/Eaton_Fire_attachments_index_output/dataset/`: `6,333`
- Samples with both `street_view.jpg` and `remote_sensing.jpg`: `6,148`
- Incomplete sample folders still missing one modality: `185`

At the moment, the local matching coverage is about **97.1%** (`6,148 / 6,333`) for the generated sample folders.

## What Is Versioned

The repository is intended to track:

- preprocessing, feature extraction, and visualization scripts
- notebooks and project documentation
- dependency files
- empty folder skeletons for raw data, generated data, and outputs

The repository is intended to ignore:

- labeled and unlabeled street-view image files
- raw CSV exports and local attachment indexes
- generated feature tables, split files, maps, and reports
- virtual environments, zip backups, and OS/editor noise

## Repository Layout

```text
california wildfire/
├── README.md
├── .gitignore
├── requirements.txt
├── notebooks/
│   └── 01_dataset_exploration.ipynb
├── scripts/
│   ├── data_prep/
│   │   ├── parse_metadata.py
│   │   └── train_val_test_split.py
│   ├── features/
│   │   ├── extract_clip_embeddings.py
│   │   └── sample_raster_values.py
│   └── visualization/
│       ├── map_damage_points.py
│       └── sample_grid.py
├── Eaton_Fire/                        # local raw labeled imagery lives here
├── Altadena_Images/                   # local raw unlabeled imagery + helper scripts
├── data/                              # generated metadata / features / splits
└── outputs/                           # generated maps / figures / reports
```

## Local Data Layout

Keep the raw project data on your machine in the same folder structure shown below. Git will preserve the folder skeleton, but it will not upload the actual data files.

```text
Eaton_Fire/
├── Affected_1-9_/attachments/
├── Minor_10-25_/attachments/
├── Major_26-50_/attachments/
├── Destroyed_50_/attachments/
├── No_Damage/attachments/
└── Inaccessible/attachments/

Altadena_Images/
├── Altadena_Images/                   # raw unlabeled imagery
├── Eaton_Fire_attachments_index_output/
│   └── dataset/
├── download_attachment_index.py
├── match_remote_sensing.py
└── requirements.txt
```

## Setup

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

If you want to use the helper scripts under `Altadena_Images/`, install those dependencies as needed:

```bash
pip install -r Altadena_Images/requirements.txt
```

## Typical Workflow

1. Put local raw imagery and source indexes into `Eaton_Fire/` and `Altadena_Images/`.
2. Parse image metadata into generated files under `data/`.
3. Build train/validation/test splits.
4. Extract features and create visualizations.
5. Commit only code, notebooks, docs, and folder placeholders.

### Parse Metadata

```bash
python scripts/data_prep/parse_metadata.py --root .
```

### Build Splits

```bash
python scripts/data_prep/train_val_test_split.py --root .
```

### Extract CLIP Features

```bash
python scripts/features/extract_clip_embeddings.py --root . --split labeled
python scripts/features/extract_clip_embeddings.py --root . --split unlabeled
```

### Create Visualization Outputs

```bash
python scripts/visualization/map_damage_points.py --root .
python scripts/visualization/sample_grid.py --root .
```

## GitHub Hygiene

Before pushing, this repository should usually show code and documentation changes only. The following command is useful for a quick sanity check:

```bash
git status --short
```

If you see raw images, generated CSVs, or output HTML files listed there, update `.gitignore` before pushing.

## Notes

- The helper scripts inside `Altadena_Images/` are kept in Git because they are part of the reproducible workflow.
- Generated files under `data/` and `outputs/` are intentionally local by default.
- If you later want to share small metadata samples, add them to a dedicated `examples/` or `sample_data/` folder instead of mixing them with raw data.
