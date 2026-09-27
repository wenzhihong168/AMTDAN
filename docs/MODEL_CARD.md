# AMTDAN Model Card

## Summary

AMTDAN is a research-preview framework for five-level severity assessment across 17 cardiac conditions. It combines ultrasound-derived visual representations with clinical variables through multi-scale encoding, dynamic attention, graph reasoning, Transformer fusion, and task-specific heads.

| Item | Current public scope |
|:---|:---|
| Inputs | Ultrasound and structured clinical features |
| Outputs | Condition-specific five-level severity predictions |
| Tasks | 17 cardiac conditions |
| Release state | Architecture, aggregate results, and documentation |
| Not released | Model implementation, weights, data, and split manifests |

## Intended use

The artifact supports research discussion, protocol design, and future reproducibility work. It is not a clinical device and must not be used for diagnosis, triage, or treatment decisions.

## Evaluation expectations

Evaluate every task independently before reporting macro or weighted summaries. Preserve patient-level separation, quantify ordinal disagreement, report calibration, and include class support and confidence intervals. Follow [EVALUATION_PROTOCOL.md](EVALUATION_PROTOCOL.md) for the minimum protocol.

## Limitations

- Aggregate results cannot establish portability across institutions, devices, or populations.
- Five-level labels may reflect local annotation practice and class imbalance.
- Missing or low-quality modalities can alter dynamic-attention behavior.
- Public results are not independently reproducible until executable code and evaluation assets are released.

## Data and privacy

Patient data, identifiers, institution-specific mappings, and protected metadata must remain outside the repository. Any future public data interface should use de-identified examples or synthetic fixtures with explicit provenance.
