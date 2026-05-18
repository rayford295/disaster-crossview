# disaster-crossview

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
- new pre-disaster wildfire remote-sensing mosaic: `pre_disaster_svi.tif` kept locally
- 13,397 valid local triplets combining pre-disaster remote sensing, post-disaster remote sensing, and street view
- coordinates retained in the generated paired index files

Detailed notes: [`Altadena_Images/README.md`](./Altadena_Images/README.md)

Pre-disaster remote-sensing preview:

![Altadena pre-disaster remote-sensing preview](./docs/assets/altadena_pre_disaster_svi_preview.jpg)

The full source GeoTIFF is a local, unversioned RGB mosaic for the Altadena wildfire
study area. It is `50,176 x 50,176` pixels at approximately `0.305 m` resolution
in WGS 84 / UTM zone 11N. The image above is a lightweight center-crop preview
created for GitHub documentation.

The local triplet folder is generated under
`Eaton_Fire_attachments_index_output/triplet_dataset/` by
`scripts/data_prep/build_altadena_triplet_dataset.py`. Each retained sample has:
`pre_disaster_remote_sensing.jpg`, `post_disaster_remote_sensing.jpg`, and
`street_view.jpg`.

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
- based on the Hurricane Milton bi-temporal street-view paper

Detailed notes: [`Bi-temporal_hurricane/README.md`](./Bi-temporal_hurricane/README.md)

### `SAGINDisaster/`

A paired remote-sensing / volunteered-ground-image disaster dataset currently
available in the local workspace.

- `2,080` remote-sensing images in `RSI/`
- `2,080` ground-view images in `VGI/`
- companion spreadsheet `SAGINDisaster_latlon.xlsx`
- observed metadata fields:
  - `ID`
  - `Type`
  - `Latitude`
  - `Longitude`
  - `Possible text description`

Current local path example:

- `C:/Users/yyang295/Desktop/SAGINDisaster/SAGINDisaster`
- `C:/Users/yyang295/Desktop/SAGINDisaster/SAGINDisaster_latlon.xlsx`

## Quick summary

| Dataset | Structure | Scale | Coordinates |
| --- | --- | --- | --- |
| `Eaton_Fire/` | class-organized street-view attachments | 18,428 points / 19,780 images | yes |
| `Altadena_Images/` | sample-organized street-view plus remote-sensing pairs, with local pre-disaster wildfire mosaic and valid triplets | 19,780 samples / 19,746 complete post-disaster pairs / 13,397 valid triplets | yes |
| `IAN_hurricane/` | paired satellite plus street-view images | 4,121 pairs / 8,242 images | no |
| `Bi-temporal_hurricane/` | paired pre/post street-view samples | 2,556 pairs / 5,112 images | yes |
| `SAGINDisaster/` | paired remote-sensing plus volunteered ground images | 2,080 pairs / 4,160 images | yes |

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

According to the article, the dataset is based on pre- and post-disaster street-view image pairs collected before and after 2024 Hurricane Milton in Horseshoe Beach, Florida.

## SAGINDisaster note

`SAGINDisaster/` is currently documented as a local external benchmark candidate.
Unlike the Eaton / Altadena workflow, it already exposes paired remote-sensing
and ground-view image folders together with a spreadsheet containing explicit
latitude / longitude coordinates and disaster-type metadata. That makes it a
useful future benchmark for cross-dataset retrieval, transfer, or
generalization experiments.
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

### 8. Evaluate whether generation helps

```bash
python scripts/firebridge_eval_generator.py \
  --generator-checkpoint "outputs/generator_controlnet/generator_best.pt" \
  --split-csv "data/splits/altadena_objectid/test.csv" \
  --localizer-checkpoint "outputs/localizer_baseline/localizer_best.pt" \
  --triage-checkpoint "outputs/triage_crossview/triage_best.pt" \
  --output-json "outputs/generator_eval.json"
```

### 9. Run the agentic pipeline

```bash
python scripts/firebridge_run_agentic.py \
  --localizer-checkpoint "outputs/localizer_baseline/localizer_best.pt" \
  --generator-checkpoint "outputs/generator_controlnet/generator_best.pt" \
  --triage-checkpoint "outputs/triage_crossview/triage_best.pt" \
  --split-csv "data/splits/altadena_objectid/test.csv" \
  --query-index 0 \
  --output-json "outputs/agentic_example.json"
```

### 10. Run a local smoke test

```bash
python scripts/firebridge_smoke_test.py \
  --train-csv "data/splits/altadena_objectid/train.csv" \
  --val-csv "data/splits/altadena_objectid/val.csv" \
  --test-csv "data/splits/altadena_objectid/test.csv"
```

## Binary Triage Mapping

The default operational binary mapping in this repo is:

- `0`: `No Damage` + `Affected (1-9%)`
- `1`: `Minor (10-25%)` + `Major (26-50%)` + `Destroyed (>50%)`
- ignored by default: `Inaccessible`

This mapping keeps the task close to a real response question: **does this property show actionable fire damage or not?**

## Paper Planning Docs

- [Current Status](./docs/current_status.md)
- [Task Definitions](./docs/tasks.md)
- [Experiment Plan](./docs/experiments.md)
- [Immediate Next Experiments](./docs/next_experiments.md)
- [Localizer Runbook](./docs/localizer_runbook.md)
- [Experiment Tracker Template](./docs/experiment_tracker_template.csv)
- [Agentic Pipeline](./docs/agentic_pipeline.md)
- [Paper Blueprint](./docs/paper_blueprint.md)
- [Progress Log](./docs/progress_log.md)
- [Triage Conflict Workflow](./docs/triage_conflict_workflow.md)
- [Improvement Roadmap](./docs/improvement_roadmap.md)

## Notes

- This repository's code and repository-authored documentation are licensed under Apache-2.0. The underlying datasets, imagery, and third-party source materials are not relicensed by this repository and remain subject to their own terms.
- Raw imagery and large generated artifacts remain local and are ignored by Git.
- The current models are meant to be solid baselines and scaffolding for a paper, not the final research claim.
