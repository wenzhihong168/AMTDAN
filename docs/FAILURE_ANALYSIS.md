# Failure Analysis

AMTDAN failure analysis should distinguish data-quality, modality, fusion, and task-specific errors before interpreting aggregate scores.

## Error taxonomy

| Failure class | Diagnostic view | Minimum context |
|:---|:---|:---|
| Visual-quality failure | Metric versus quality grade | View and device family |
| Missing-modality failure | Performance by availability pattern | Modality mask |
| Ordinal near miss | Adjacent-grade confusion | Task and class support |
| Ordinal severe miss | Severity-distance distribution | Full probability vector |
| Site or device shift | Stratified metric and calibration | Domain support |
| Task imbalance | Per-class recall and precision | Prevalence and loss weight |

## Required stratification

Report all 17 conditions separately by severity level, modality availability, quality grade, and evaluation domain when support permits. Weighted summaries are accompanied by macro and per-class results.

## Case review

For every high-confidence or distant-grade error, record task, input-availability mask, quality flags, calibrated probabilities, attention or graph diagnostics when available, label-review status, and whether the case lies outside training support.

## Corrective-action rule

Changes to modality handling, attention, graph structure, loss weighting, or calibration must use the frozen patient split. Findings remain research hypotheses until executable evaluation assets are released.
