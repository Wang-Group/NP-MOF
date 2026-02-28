# NP-MOF

## Overview

This repository contains the data, visualizations, and machine-learning analyses used in the study **Predicting Internal versus External Nanoparticle Formation in Zr-Based Metal–Organic Frameworks**.

It includes curated experimental data, MOF structures and descriptors, literature-analysis outputs, and Jupyter notebooks for feature selection and classification modeling.

## Repository Layout

- `data/`
  Core data directory containing experimental labels, MOF descriptors, low-dimensional factors, literature data, factor-contribution analyses, and per-MOF raw subfolders.

- `cifs/`
  Curated CIF structure files.

- `1-over_fitting_with_linear_model/`
  Main modeling notebooks and figure outputs, including feature selection, linear separability checks, descriptor-combination comparisons, and extra visualizations.

- `0-complete_literature_data/`
  Literature-data curation and statistical-visualization notebooks, together with exported figures, HTML, and Excel outputs.

## Key Files

- `data/all_NPs.xlsx`
  Experimental label table describing whether nanoparticles are located inside MOF pores or on the external surface for each metal-MOF pair.

- `data/MOF_data.csv`
  Merged MOF descriptor table generated from per-MOF CSV files and `geo_pro/data.csv`.

- `data/MOF_factor.csv`
  The main 45-dimensional MOF factor table used as MOF-side model input.

- `data/MOF_factors.csv`
  A backup copy with the same content as `MOF_factor.csv`.

- `data/literature_data.xlsx`
  Curated literature dataset used for summary statistics and Sankey-style analyses.

- `data/single_metal_atoms_on_graphene_binding_energy_and_diffusion_barrier.xlsx`
  Binding-energy and diffusion-barrier table for metals on graphene.

- `data/supported_metal_M_oxygen_affinity_QMO_and_support_metal_affinity_QMM_prime.xlsx`
  Table containing metal-oxygen affinity `QMO` and metal-support affinity `QMM'`.

- `data/supported_metal_M_support_metal_affinity_QMM_prime.xlsx`
  Table containing metal-support affinity `QMM'`.

- `data/merge_mof_data.py`
  Script for traversing MOF subfolders under `data/` and merging descriptor tables.

- `1-over_fitting_with_linear_model/NPs.xlsx`
  Curated experimental sheet used by the modeling notebooks.

## Main Notebooks

- `1-over_fitting_with_linear_model/0-feature_selection.ipynb`
  Baseline feature selection, model comparison, and performance evaluation.

- `1-over_fitting_with_linear_model/0-if_linear_separatable.ipynb`
  Checks whether the task is approximately linearly separable and compares against more flexible models.

- `1-over_fitting_with_linear_model/1-feature_selection.ipynb`
  Systematically enumerates metal + MOF feature combinations and generates result tables and figures.

- `1-over_fitting_with_linear_model/additional_visualization/1-visualize_selected_features.ipynb`
  Provides additional visualization for selected key features.

- `0-complete_literature_data/visualize.ipynb`
  Performs grouped literature statistics, summary-table export, and Sankey visualization.

## Environment

Python 3.10+ is recommended.

Common dependencies:

```bash
pip install pandas numpy scikit-learn matplotlib jupyter openpyxl
```

Optional packages for richer visualization:

```bash
pip install seaborn plotly
```

## Large Files

Large and binary-like artifacts under `data/`, including CSV tables, notebooks, Excel workbooks, and generated figures, are stored with Git LFS. Text helper files such as `data/merge_mof_data.py` remain in normal Git.

Before cloning, pulling, or checking out branches, make sure Git LFS is enabled locally:

```bash
git lfs install
git lfs pull
```

## Usage

1. Launch Jupyter from the repository root.

```bash
jupyter notebook
```

2. Recommended order for browsing and reproducing the analyses.

```text
1-over_fitting_with_linear_model/0-feature_selection.ipynb
1-over_fitting_with_linear_model/0-if_linear_separatable.ipynb
1-over_fitting_with_linear_model/1-feature_selection.ipynb
1-over_fitting_with_linear_model/additional_visualization/1-visualize_selected_features.ipynb
0-complete_literature_data/visualize.ipynb
```

3. To rebuild the merged MOF descriptor table, run:

```bash
python data/merge_mof_data.py --base ./data --output MOF_data.csv
```

## Notes

- The three Excel files in `data/` that previously used Chinese filenames have been renamed to English, and notebook references have been updated accordingly.
- `data/` contains Git LFS-managed artifacts; cloning or pulling without Git LFS will leave pointer files instead of the full datasets, notebooks, and figures.
- Some notebook outputs are large, and rerunning notebooks may overwrite existing figures or result tables.

## Contact

For citation or research communication, please refer to the paper authors or contact:

- `yibin_jiang@outlook.com`
- `wangchengxmu@xmu.edu.cn`
