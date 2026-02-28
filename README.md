# NP_at_MOF

Machine-learning study and data release for the manuscript **"Machine Learning Reveals Metal-Support Interactions Governing Nanoparticle Localization in Metal-Organic Frameworks"**. The repo bundles the curated experimental dataset (10 transition metals on 11 (trian) + 2 (test) Zr-based MOFs synthesized via the double-solvent method), literature survey, descriptor tables, structural files, and the notebooks used to build and visualize the classification models that predict whether nanoparticles form inside or outside MOF pores.

## Repository layout
- `data/` - Core datasets and descriptor tables (RACs, geometric features from Zeo++, 45-factor MOF representations, experimental labels in `all_NPs.xlsx`, literature set in `literature_data.xlsx`) plus per-MOF subfolders with `*.cif`, `*_descriptors.csv`, and Zeo++ outputs. Also includes factor-contribution breakdowns (`full_contrib_factor19.csv`, `full_contrib_factor37.csv`, `full_contrib_factor39.csv`) and the merged feature matrix `MOF_data.csv`/`MOF_factors.csv`. Large raw descriptor dumps live here (`RACs.csv`, `geometric_properties.csv`).
- `cifs/` - Lightweight copy of the CIF structures for the studied MOFs (UiO-66 variants, DUT-51/67, MOF-801/808, MIL-140, PCN-700, Zr-FA, Zr12-BPDC).
- `0-over_fitting_with_linear_model/` - Main analysis notebooks and derived figures for feature selection, linear separability checks, and MLP classification (e.g., `0-feature_selection.ipynb`, `0-if_linear_separatable.ipynb`, `1-feature_selection.ipynb`). Results tables for metal-descriptor combinations sit in `results_core_combos/`; visualization outputs are saved as `*.png`.
- `1-literature_data/` - Literature-survey notebooks (`v1.ipynb`, `v2.ipynb`) and summary plots/Sankey diagram quantifying inside vs outside nanoparticle formation across 167 reported cases.
- `0-old/` - Archived intermediate data and legacy notebooks/plots kept for reference; not used in the final figures.

## Key files and what they contain
- `data/all_NPs.xlsx` - Experimental labels for the 10-by-13 metal/MOF grid (inside vs outside nanoparticle localization) measured by electron microscopy.
- `data/MOF_data.csv` - Merged RAC and geometric descriptors for each MOF (one row per MOF; produced with `data/merge_mof_data.py`).
- `data/MOF_factors.csv` - 45-factor low-dimensional representation from prior factor analysis over ~470k MOFs; these factors are the MOF-side features used in modeling.
- `data/full_contrib_factor19.csv`, `data/full_contrib_factor37.csv`, `data/full_contrib_factor39.csv` and `data/uio_factor*/` - Factor contribution analyses mapping factors back to chemically interpretable RAC/Zeo++ descriptors.
- `data/literature_data.xlsx` - Collated literature cases used for Figure 1 (inside/outside counts by synthesis route, metal, and MOF).
- `data/merge_mof_data.py` - Utility to stack per-MOF descriptor CSVs and Zeo++ outputs into a single table. Usage: `python data/merge_mof_data.py --base ./data --output MOF_data.csv` (defaults match repo layout). Requires `pandas`.
- `0-over_fitting_with_linear_model/NPs.xlsx` - Metal descriptor table (binding energy and diffusion barrier on graphene, QMO, noble indicator) used as the metal-side features.

## How to reproduce the analyses
1. Set up Python (tested with Python 3.10+). Install: `pip install pandas numpy scikit-learn matplotlib jupyter openpyxl` (add `seaborn` or `plotly` if you want extra styling).
2. Launch notebooks with `jupyter notebook` from the repo root. Recommended order:
   - `0-over_fitting_with_linear_model/0-feature_selection.ipynb` - Baseline feature selection and model comparison (logistic regression, random forest, gradient boosting, MLP).
   - `0-over_fitting_with_linear_model/0-if_linear_separatable.ipynb` - Linear separability check and justification for using a small MLP (hidden layers (10, 4) with tanh).
   - `0-over_fitting_with_linear_model/1-feature_selection.ipynb` - Exhaustive metal+MOF descriptor combinations and cross-validation; produces the accuracy/feature-importance figures.
   - `0-over_fitting_with_linear_model/additional_visualization/1-visualize_selected_features.ipynb` - Generates the phase-boundary plots and noble/non-noble panels.
   - `1-literature_data/v2.ipynb` - Rebuilds the literature Sankey and bar plots (Figure 1).
3. Intermediate/derived outputs are written alongside each notebook as CSV/PNG; rerunning a notebook regenerates its artifacts.

## Study highlights (context for the notebooks)
- Combining four metal migration descriptors (binding energy and diffusion barrier on graphene, affinity to O atoms QMO, noble indicator) with 45 low-dimensional MOF factors yields an interpretable classifier for nanoparticle localization (inside vs outside).
- Metal descriptors alone cap performance (~0.87 balanced accuracy) because they cannot distinguish different MOFs for a given metal; adding MOF factors (notably Factors 19, 37, 39) resolves MOF-specific behavior.
- A compact three-descriptor view captures the mechanism: weak metal affinity to C/O drives external deposition; stronger metal-support interactions and linker heteroatom character (Factor 37) steer nanoparticles into pores. External validation on UiO-66-F/I achieves ~85% accuracy.

## Notes on data size and provenance
- Some descriptor files are large (`data/RACs.csv` ~0.8 GB, `data/geometric_properties.csv` ~110 MB). Keep them on local storage; cloud-synced folders may throttle performance.
- MOF structures in `cifs/` mirror those in `data/<MOF>/` and can be used to recompute descriptors if needed.

## Citation and contact
If you use these data or notebooks, please cite the manuscript (authors: Zhaomin Su, Lingzhen Zeng, Yibin Jiang*, Cheng Wang*; iChem, Xiamen University).
Corresponding authors: `yibin_jiang@outlook.com`, `wangchengxmu@xmu.edu.cn`.
