# Predicting Internal versus External Nanoparticle Formation in Zr-Based Metal–Organic Frameworks

This repository contains the data, executed notebooks, and exported figures used to study nanoparticle formation in Zr-based MOFs. The workflow is notebook-driven and combines:

- curated experimental labels for metal-MOF pairs,
- structure-derived MOF descriptor tables,
- factor-analysis notebooks that compress MOF descriptors into low-dimensional factors,
- literature-survey visualizations, and
- classification experiments that predict whether nanoparticles are observed on the external MOF surface after reaction.

## At a glance

| Item | Summary |
| --- | --- |
| `1-over_fitting_with_linear_model/NPs.xlsx` | Internal modeling set with 110 metal-MOF entries across 11 MOFs |
| `data/all_NPs.xlsx` | Full labeled set with 130 entries across 13 MOFs; includes `UiO-66-F` and `UiO-66-I` used as an external-family hold-out in some notebooks |
| `data/MOF_data.csv` | Merged MOF descriptor table with 13 MOFs and 202 columns |
| `data/MOF_factor.csv` | Main MOF factor table with 13 MOFs and 45 factors |
| `data/RACs.csv` | Large reference descriptor matrix used for factor analysis (`472571 x 188`) |
| `1-over_fitting_with_linear_model/results_core_combos/results_all_core_sizes_2to4_k=1.csv` | Exported benchmark table with 990 feature-combination/model runs |

## Repository layout

- `data/`
  Main data directory. Includes MOF descriptor tables, factor-analysis notebooks, literature spreadsheets, factor-contribution exports, and per-MOF folders.
- `data/<MOF-name>/`
  Per-structure data bundles containing the main MOF CSV, `geo_pro/data.csv`, linker/SBU descriptor CSVs, CIF files, decomposed linker/SBU files, and geometry/log outputs.
- `cifs/`
  Curated CIF structure files for the Zr-MOF set.
- `1-over_fitting_with_linear_model/`
  Main prediction notebooks, result tables, and exported figures for the classification workflow.
- `0-complete_literature_data/`
  Literature curation workbooks plus summary plots and Sankey-style visualization outputs.

## Key data products

| Path | Description |
| --- | --- |
| `data/MOF_data.csv` | Merged descriptor table produced from each MOF folder's main CSV plus `geo_pro/data.csv` |
| `data/MOF_factor.csv` | 45-dimensional MOF factor scores used in the prediction notebooks |
| `data/MOF_factors.csv` | Duplicate copy of `MOF_factor.csv` |
| `data/RACs.csv` | Reference RAC-style descriptor matrix used to derive factors |
| `data/geometric_properties.csv` | Geometric descriptor source table used in factor analysis |
| `data/literature_data.xlsx` | Curated literature dataset grouped by deposited metal |
| `0-complete_literature_data/data-20260306.xlsx` | Expanded literature working file used for the grouped visualizations |

## Notebook workflow

1. Build or inspect the merged MOF descriptor table.
   `data/merge_mof_data.py` merges each per-MOF CSV with `geo_pro/data.csv` into `data/MOF_data.csv`.

2. Derive MOF factors from the descriptor space.
   `data/MOFscreen_Factor_analysis.ipynb` and related notebooks combine `RACs.csv`, `geometric_properties.csv`, and `MOF_data.csv` to generate the 45-factor representation saved in `data/MOF_factor.csv`.

3. Use the `*_train.ipynb` factor-analysis variants for train-only factor construction.
   These notebooks exclude `UiO-66-F` and `UiO-66-I`, matching the external hold-out setup used later in the modeling workflow.

4. Explore the literature summary plots.
   `0-complete_literature_data/visualize.ipynb` normalizes metal, MOF, synthesis-method, and location labels and exports grouped PNG figures plus an HTML Sankey visualization.

5. Run the prediction notebooks.
   The modeling notebooks merge four metal-side descriptors:
   `BindingEnergy`, `DiffusionBarrier`, `QMO`, and `Noble`
   with the 45 MOF factors and evaluate logistic-regression and MLP classifiers.

6. Summarize full-model performance.
   `1-over_fitting_with_linear_model/1-get_model_performance.ipynb` reports 5-fold accuracy, balanced accuracy, ROC-AUC, and pooled out-of-fold metrics for the full metal-plus-factor feature set.

7. Review exported model benchmarks.
   `1-over_fitting_with_linear_model/1-feature_selection.ipynb` writes the `results_core_combos/` CSV files after enumerating core metal-descriptor subsets of size 2 to 4 with one added MOF factor.

8. Check the external-family comparison.
   `1-over_fitting_with_linear_model/1-metal_onlyvs_factor37_on_external_test.ipynb` trains on the 110-entry internal set and evaluates on 20 held-out `UiO-66-F` and `UiO-66-I` entries. The saved notebook output reports external-test accuracy of `0.75` for the `metal-related-descriptor-only` model and `0.85` for the `Factor37` model.

To rebuild the merged MOF descriptor table directly from the per-MOF folders:

```bash
python data/merge_mof_data.py --base ./data --output MOF_data.csv
```

## Main notebooks

- `data/MOFscreen_Factor_analysis.ipynb`
- `data/MOFscreen_Factor_analysis_train.ipynb`
- `data/MOFscreen_Factor_analysis-Factor19.ipynb`
- `data/MOFscreen_Factor_analysis-Factor19_trian.ipynb`
- `data/MOFscreen_Factor_analysis-Factor39.ipynb`
- `data/MOFscreen_Factor_analysis-Factor39_train.ipynb`
- `0-complete_literature_data/visualize.ipynb`
- `1-over_fitting_with_linear_model/0-if_linear_separatable.ipynb`
- `1-over_fitting_with_linear_model/0-feature_selection.ipynb`
- `1-over_fitting_with_linear_model/1-get_model_performance.ipynb`
- `1-over_fitting_with_linear_model/1-feature_selection.ipynb`
- `1-over_fitting_with_linear_model/1-compare_metal_vs_factor37.ipynb`
- `1-over_fitting_with_linear_model/1-metal_onlyvs_factor37_on_external_test.ipynb`
- `1-over_fitting_with_linear_model/additional_visualization/1-visualize_selected_features.ipynb`

## Environment

Python 3.10+ is recommended.

Install the notebook dependencies with:

```bash
pip install pandas numpy scipy scikit-learn matplotlib seaborn plotly jupyter openpyxl factor-analyzer
```

Launch Jupyter from the repository root:

```bash
jupyter notebook
```

## Git LFS

This repository uses Git LFS for large CSV, notebook, Excel, and PNG artifacts. After cloning, run:

```bash
git lfs install
git lfs pull
```

If Git LFS is not available locally, many tracked files will appear as pointer files instead of the full datasets and notebook outputs.

## Notes

- The modeling notebooks rename the Chinese Excel column for post-reaction surface nanoparticles to `ExternalNP`.
- The executed notebooks and exported CSV/PNG artifacts are part of the repository state; rerunning notebooks may overwrite them.
- Some notebook comments and spreadsheet headers are bilingual or Chinese-only. The saved code already standardizes the relevant columns during analysis.

## Contact

- `yibin_jiang@outlook.com`
- `wangchengxmu@xmu.edu.cn`
