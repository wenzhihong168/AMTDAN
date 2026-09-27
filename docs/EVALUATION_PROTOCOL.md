# Evaluation Protocol

AMTDAN is a research preview for five-level severity assessment across 17 cardiac conditions. Evaluation should remain task-aware, leakage-safe, and explicit about uncertainty.

## Data partitioning

- Split by patient before preprocessing, augmentation, or feature extraction.
- Keep repeated examinations from one patient in a single partition.
- Freeze the test cohort before architecture or threshold selection.
- Fit normalization and calibration using training or designated calibration data only.

## Required reporting

| Dimension | Minimum report |
|:---|:---|
| Task performance | Per-task precision, recall, F1, and confusion matrix |
| Discrimination | Macro and weighted AUC with confidence intervals |
| Ordinal agreement | Cohen's kappa and severity-distance error |
| Calibration | Reliability summary and expected calibration error |
| Aggregate results | Macro and support-weighted summaries with task support |

## Comparisons and ablations

Use identical patient splits for all baselines. Isolate the contribution of multi-scale encoding, dynamic attention, graph reasoning, Transformer fusion, and multi-task optimization. Report point estimates with variation across seeds or resamples.

## Release boundary

Values in the public README summarize the current research artifact. They should not be treated as independently reproduced until code, split manifests, and executable evaluation assets are released.
