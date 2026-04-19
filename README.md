# Multimodal Disaster Datasets

[中文说明](./README_CN.md)

This repository contains the code, documentation, and folder skeletons for multiple local disaster-image datasets used in cross-view and post-disaster analysis.

The repository is intentionally lightweight:

- code and documentation are versioned in GitHub
- raw images, raster tiles, and large derived tables stay local
- folder skeletons are preserved so the workflows can be recreated on another machine

## Included datasets

### `Eaton_Fire/`

The canonical labeled street-view dataset for the 2025 Eaton Fire.

- 18,428 inspection points
- 19,780 image attachments
- six damage classes
- coordinates available through the exported point and attachment tables

Detailed notes: [`Eaton_Fire/README.md`](./Eaton_Fire/README.md)

### `Altadena_Images/`

The sample-organized paired dataset derived from the Eaton Fire attachment index.

- 19,780 sample folders
- 19,746 complete `street_view.jpg` plus `remote_sensing.jpg` pairs
- 91 GeoTIFF tiles and 91 `.aux.xml` sidecars in the local raster source folder
- coordinates retained in the generated paired index files

Detailed notes: [`Altadena_Images/README.md`](./Altadena_Images/README.md)

### `IAN_hurricane/`

A Hurricane Ian cross-view dataset of paired satellite and street-view imagery.

- 4,121 satellite/street-view pairs
- 8,242 image files total
- `train_split.csv` with 3,821 rows
- `test_split.csv` with 300 rows
- three damage severities: minor, moderate, and severe
- no latitude/longitude columns in the provided local CSV files

Detailed notes: [`IAN_hurricane/README.md`](./IAN_hurricane/README.md)

### `Bi-temporal_hurricane/`

A bi-temporal street-view disaster dataset built from pre- and post-hurricane image pairs.

- current local snapshot: 2,556 paired sample folders and 5,112 image files
- three local class folders: mild, moderate, and severe
- `Location.csv` includes coordinates and human damage perception labels
- local files also include a Horseshoe Beach city boundary shapefile

Detailed notes: [`Bi-temporal_hurricane/README.md`](./Bi-temporal_hurricane/README.md)

## Quick summary

| Dataset | Structure | Scale | Coordinates |
| --- | --- | --- | --- |
| `Eaton_Fire/` | class-organized street-view attachments | 18,428 points / 19,780 images | yes |
| `Altadena_Images/` | sample-organized street-view plus remote-sensing pairs | 19,780 samples / 19,746 complete pairs | yes |
| `IAN_hurricane/` | paired satellite plus street-view images | 4,121 pairs / 8,242 images | no |
| `Bi-temporal_hurricane/` | paired pre/post street-view samples | 2,556 pairs / 5,112 images | yes |

## Current code status

The scripts in `scripts/` are still primarily written for the Eaton Fire and Altadena workflows.

- `scripts/data_prep/parse_metadata.py` parses the labeled Eaton Fire dataset and indexes the paired Altadena sample folders
- `scripts/data_prep/train_val_test_split.py` creates supervised splits for the Eaton Fire metadata
- `scripts/features/extract_clip_embeddings.py` extracts CLIP embeddings for the Eaton Fire and Altadena workflows
- `scripts/features/sample_raster_values.py` samples raster values at labeled Eaton Fire point locations
- `scripts/visualization/` generates Eaton Fire quality-assurance outputs

The Hurricane Ian dataset is now documented and reserved in the repository structure, but it is not yet wired into the current Eaton-specific preprocessing scripts because its schema is pair-based and the provided CSV files do not include coordinates.

The bi-temporal hurricane dataset is also documented in the repository structure, but it is not yet integrated into the current scripts because its organization is pair-folder based and differs from the Eaton Fire and Altadena formats.

## Hurricane Ian source and attribution

The `IAN_hurricane/` dataset should be attributed to the Hurricane Ian cross-view dataset described in:

Li, H., Deuser, F., Yin, W., Luo, X., Walther, P., Mai, G., Huang, W., and Werner, M. (2025). *Cross-view geolocalization and disaster mapping with street-view and VHR satellite imagery: A case study of Hurricane IAN*. *ISPRS Journal of Photogrammetry and Remote Sensing*, 220, 841-854. [https://doi.org/10.1016/j.isprsjprs.2025.01.003](https://doi.org/10.1016/j.isprsjprs.2025.01.003)

Based on the publication metadata, the paper introduces a novel Hurricane Ian cross-view dataset named `CVIAN` and reports that its data and code are publicly available through the related CVDisaster project.

## Bi-temporal hurricane source and attribution

The `Bi-temporal_hurricane/` dataset should be attributed to:

Yang, Y., Zou, L., Zhou, B., Li, D., Lin, B., Abedin, J., and Yang, M. (2025). *Hyperlocal disaster damage assessment using bi-temporal street-view imagery and pre-trained vision models*. *Computers, Environment and Urban Systems*, 116, 102335. [https://doi.org/10.1016/j.compenvurbsys.2025.102335](https://doi.org/10.1016/j.compenvurbsys.2025.102335)

## Repository layout

```text
.
|-- README.md
|-- README_CN.md
|-- requirements.txt
|-- Eaton_Fire/
|-- Altadena_Images/
|-- IAN_hurricane/
|-- Bi-temporal_hurricane/
|-- scripts/
|   |-- data_prep/
|   |-- features/
|   `-- visualization/
|-- notebooks/
|-- data/
`-- outputs/
```

## Versioning policy

Versioned in GitHub:

- source code
- notebooks
- documentation
- folder skeletons and `.gitkeep` placeholders

Kept local and ignored by Git:

- raw street-view, satellite, and remote-sensing images
- local CSV exports and split files
- generated feature arrays and metadata tables
- generated maps, figures, and reports
- virtual environments and archive files

## Suggested future repo name

Because the repository now spans both wildfire and hurricane datasets, a clearer future GitHub name would be something like:

- `multimodal-disaster-datasets`
- `disaster-crossview-datasets`
- `disaster-vision-datasets`
