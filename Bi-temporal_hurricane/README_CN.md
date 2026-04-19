# Bi-temporal 飓风街景数据集

[English README](./README.md)

这个目录用于保留仓库中的 bi-temporal 飓风街景数据集结构。

这份本地数据集由灾前和灾后的街景图像对组成，同时附带一个位置表和 Horseshoe Beach 城市边界 shapefile。

## 本地结构

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

## 当前本地快照

你当前机器上的本地快照包含：

- 总计 2,556 个样本文件夹
- 总计 5,112 张图片
- `folder_0` 下有 657 个样本文件夹
- `folder_1` 下有 1,196 个样本文件夹
- `folder_2` 下有 703 个样本文件夹
- 1 个包含坐标和标签的 `Location.csv`
- 1 套 Horseshoe Beach 城市边界 shapefile

每个样本文件夹里通常有两张图片，例如：

- `*_2023.png`
- `*_2024.png`

这说明它是典型的灾前/灾后时间配对结构。

## 标签分布

根据 `Location.csv`，当前本地数据中的人工损毁感知标签分布为：

| Label | Count |
| --- | ---: |
| `mild` | 657 |
| `Moderate` | 1,196 |
| `Severe` | 703 |
| Total | 2,556 |

## `Location.csv` 字段

本地表包含以下字段：

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

重要说明：

- 和 `IAN_hurricane/` 不同，这份数据是包含 `lon` 和 `lat` 的
- 本地路径字段应当理解为当前机器上的来源路径，而不是通用可移植路径
- 目录命名和标签结构说明它更适合被看作 pair-based 的灾害感知数据，而不是标准的 train/test CSV 数据集

## 来源与引用

这份数据建议引用以下论文：

Yang, Y., Zou, L., Zhou, B., Li, D., Lin, B., Abedin, J., and Yang, M. (2025). *Hyperlocal disaster damage assessment using bi-temporal street-view imagery and pre-trained vision models*. *Computers, Environment and Urban Systems*, 116, 102335. [https://doi.org/10.1016/j.compenvurbsys.2025.102335](https://doi.org/10.1016/j.compenvurbsys.2025.102335)

论文说明，这份数据基于 2024 Hurricane Milton 在 Florida 州 Horseshoe Beach 的灾前/灾后街景图像对。

## 仓库说明

这个仓库只跟踪 `Bi-temporal_hurricane/` 的文档和目录骨架，真正的图片、CSV 和 shapefile 文件默认仍然被 Git 忽略，不直接提交。
