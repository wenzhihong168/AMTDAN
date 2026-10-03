# Experiment Record

Use one immutable record for every AMTDAN research-preview experiment.

## Identity

| Field | Value |
|:---|:---|
| Experiment ID |  |
| Git revision |  |
| Input-schema version |  |
| Label-registry version |  |
| Patient-level split hash |  |
| Random seeds |  |
| Hardware and software environment |  |

## Model configuration

- Ultrasound representation and quality policy:
- Clinical feature and missingness policy:
- Multi-scale visual encoder:
- Dynamic-attention and graph-reasoning modules:
- Transformer fusion and task heads:
- Multi-task loss weighting and checkpoint rule:

## Evaluation record

Record per-task support, precision, recall, F1, AUC, ordinal agreement, calibration, and confusion matrices before aggregate summaries. Ablations use the same patient split, preprocessing, and evaluation code as the complete model.

## Release gate

- [ ] Repeated examinations remain in one patient partition.
- [ ] All 17 task results and five-level label definitions are present.
- [ ] Aggregate metrics can be traced to per-task artifacts.
- [ ] Claims remain within research-preview scope.
- [ ] No patient data, identifiers, weights, or private manifests are exported.
