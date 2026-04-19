# Bi-Temporal Hurricane Street-View Dataset

[中文说明](./README_CN.md)

This directory is reserved for the final local bi-temporal hurricane street-view dataset included in this repository.

The local dataset is organized as paired pre- and post-disaster street-view samples, plus a location table and a city-boundary shapefile.

## Local structure

```text
Bi-temporal_hurricane/
|-- folder_0/
|-- folder_1/
|-- folder_2/
|-- Location.csv
|-- Horseshoe_Beach_City_Boundary.shp
|-- Horseshoe_Beach_City_Boundary.shx
|-- Horseshoe_Beach_City_Boundary.dbf
|-- Horseshoe_Beach_City_Boundary.prj
`-- ...
```

## Current local snapshot

The current local snapshot on disk contains:

- 2,556 paired sample folders in total
- 5,112 image files in total
- 657 sample folders under `folder_0`
- 1,196 sample folders under `folder_1`
- 703 sample folders under `folder_2`
- one `Location.csv` table with coordinates and labels
- one Horseshoe Beach city-boundary shapefile set

Each sample folder contains two images, for example:

- `*_2023.png`
- `*_2024.png`

This indicates a pre/post temporal pairing setup.

## Label distribution

Based on `Location.csv`, the local human damage perception counts are:

| Label | Count |
| --- | ---: |
| `mild` | 657 |
| `Moderate` | 1,196 |
| `Severe` | 703 |
| Total | 2,556 |

## `Location.csv` schema

The local table includes:

- `degree`
- `score`
- `trees`
- `trash`
- `building`
- `water`
- `image_path`
- `year`
- `root`
- `summary`
- `contrast`
- `lon`
- `lat`
- `human_damage_perception`

Important notes:

- unlike `IAN_hurricane/`, this dataset does include `lon` and `lat`
- the local path fields should be interpreted as machine-specific provenance references
- the folder names and labels indicate a pair-based disaster-perception workflow rather than a standard train/test CSV workflow

## Source and attribution

This dataset should be attributed to:

Yang, Y., Zou, L., Zhou, B., Li, D., Lin, B., Abedin, J., and Yang, M. (2025). *Hyperlocal disaster damage assessment using bi-temporal street-view imagery and pre-trained vision models*. *Computers, Environment and Urban Systems*, 116, 102335. [https://doi.org/10.1016/j.compenvurbsys.2025.102335](https://doi.org/10.1016/j.compenvurbsys.2025.102335)

The article describes a bi-temporal street-view dataset collected before and after 2024 Hurricane Milton in Horseshoe Beach, Florida.

## Repository note

This repository tracks the documentation and folder skeleton for `Bi-temporal_hurricane/`, while the actual image files, CSV tables, and shapefile components remain ignored by Git.
