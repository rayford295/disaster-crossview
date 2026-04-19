# 多灾种灾害影像数据集

[English README](./README.md)

这个仓库保存的是多个本地灾害影像数据集对应的代码、文档和目录骨架，主要用于 cross-view 和灾后分析相关研究。

仓库目前遵循轻量化原则：

- GitHub 里保留代码和文档
- 原始图片、遥感瓦片和大体量派生结果保留在本地
- 通过保留目录骨架，方便在别的机器上复现同样的流程

## 当前纳入仓库的数据集

### `Eaton_Fire/`

这是 2025 年 Eaton Fire 的权威标注街景数据集。

- 18,428 个 inspection points
- 19,780 张 image attachments
- 6 个损毁等级
- 点位表和附件表中都保留了坐标信息

详细说明见：[`Eaton_Fire/README.md`](./Eaton_Fire/README.md)

### `Altadena_Images/`

这是基于 Eaton Fire 附件索引生成的 sample 级配对数据集。

- 19,780 个 sample 文件夹
- 其中 19,746 个是完整的 `street_view.jpg` 和 `remote_sensing.jpg` 配对
- 本地遥感源目录中有 91 个 GeoTIFF 和 91 个 `.aux.xml`
- 生成的配对索引表中保留了坐标信息

详细说明见：[`Altadena_Images/README.md`](./Altadena_Images/README.md)

### `IAN_hurricane/`

这是 Hurricane Ian 的 cross-view 配对数据集，包含卫星图和街景图。

- 4,121 对 satellite/street-view pairs
- 共 8,242 张图片
- `train_split.csv` 有 3,821 行
- `test_split.csv` 有 300 行
- 3 个损毁等级：minor、moderate、severe
- 你现在这份本地 CSV 里没有纬度和经度字段

详细说明见：[`IAN_hurricane/README_CN.md`](./IAN_hurricane/README_CN.md)

### `Bi-temporal_hurricane/`

这是一个基于灾前和灾后街景图像对构建的 bi-temporal 飓风灾害数据集。

- 你当前本地快照中有 2,556 个样本文件夹、5,112 张图片
- 本地分成 3 个类别目录：mild、moderate、severe
- `Location.csv` 中包含坐标和人工损毁感知标签
- 本地还包含 Horseshoe Beach 的城市边界 shapefile
- 对应论文中报告的 benchmark 规模是 2,249 对 Hurricane Milton 灾前/灾后街景图像

详细说明见：[`Bi-temporal_hurricane/README_CN.md`](./Bi-temporal_hurricane/README_CN.md)

## 快速对比

| 数据集 | 组织方式 | 规模 | 是否有坐标 |
| --- | --- | --- | --- |
| `Eaton_Fire/` | 按类别组织的街景附件 | 18,428 points / 19,780 images | 有 |
| `Altadena_Images/` | 按 sample 组织的街景 + 遥感配对 | 19,780 samples / 19,746 完整配对 | 有 |
| `IAN_hurricane/` | 卫星图 + 街景图配对 | 4,121 pairs / 8,242 images | 没有 |
| `Bi-temporal_hurricane/` | 灾前/灾后街景配对样本 | 2,556 pairs / 5,112 images | 有 |

## 当前代码状态

目前 `scripts/` 里的代码仍然主要服务于 Eaton Fire 和 Altadena 工作流：

- `scripts/data_prep/parse_metadata.py` 解析 Eaton Fire 标注数据，并索引 Altadena 的 sample 文件夹
- `scripts/data_prep/train_val_test_split.py` 为 Eaton Fire 元数据生成训练/验证/测试划分
- `scripts/features/extract_clip_embeddings.py` 为 Eaton Fire 和 Altadena 工作流提取 CLIP 特征
- `scripts/features/sample_raster_values.py` 在 Eaton Fire 标注点位上采样遥感栅格值
- `scripts/visualization/` 生成 Eaton Fire 的质检可视化结果

Ian 数据集现在已经被纳入仓库文档和目录结构，但还没有接进现有的 Eaton 专用脚本流程。原因是它的表结构是 pair-based，而且你给的本地 CSV 不包含坐标字段。

Bi-temporal 飓风数据集现在也已经纳入仓库文档和目录结构，但同样还没有接进现有脚本流程，因为它采用的是 pair-folder 组织方式，和 Eaton Fire / Altadena 的结构不同。

## Hurricane Ian 数据来源与引用

`IAN_hurricane/` 这个数据集建议标注为以下论文来源：

Li, H., Deuser, F., Yin, W., Luo, X., Walther, P., Mai, G., Huang, W., and Werner, M. (2025). *Cross-view geolocalization and disaster mapping with street-view and VHR satellite imagery: A case study of Hurricane IAN*. *ISPRS Journal of Photogrammetry and Remote Sensing*, 220, 841-854. [https://doi.org/10.1016/j.isprsjprs.2025.01.003](https://doi.org/10.1016/j.isprsjprs.2025.01.003)

根据该论文公开的元数据说明，作者在论文中构建了一个新的 Hurricane Ian cross-view 数据集 `CVIAN`，并说明相关数据与代码与 CVDisaster 项目关联公开。

## Bi-temporal 飓风数据来源与引用

`Bi-temporal_hurricane/` 这个数据集建议引用为：

Yang, Y., Zou, L., Zhou, B., Li, D., Lin, B., Abedin, J., and Yang, M. (2025). *Hyperlocal disaster damage assessment using bi-temporal street-view imagery and pre-trained vision models*. *Computers, Environment and Urban Systems*, 116, 102335. [https://doi.org/10.1016/j.compenvurbsys.2025.102335](https://doi.org/10.1016/j.compenvurbsys.2025.102335)

根据论文内容，文中 benchmark 数据集是 2024 Hurricane Milton 在 Florida 州 Horseshoe Beach 的 2,249 对灾前/灾后街景图像。你当前机器上的本地快照共有 2,556 个样本文件夹，所以这份本地数据看起来是论文公开基准数据的扩展版或后续版本。

## 仓库结构

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

## 版本管理策略

提交到 GitHub 的内容：

- 源代码
- notebooks
- 文档
- 目录骨架和 `.gitkeep`

只保留在本地、不提交的内容：

- 原始街景图、卫星图和遥感图
- 本地 CSV 导出和 split 文件
- 生成的特征数组和元数据表
- 生成的地图、图片和报告
- 虚拟环境和压缩包

## 推荐的新仓库名

因为这个仓库现在已经不只是 Eaton Fire，而是同时包含 wildfire 和 hurricane 数据，更合适的新名字可以考虑：

- `multimodal-disaster-datasets`
- `disaster-crossview-datasets`
- `disaster-vision-datasets`
