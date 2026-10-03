# Artifact Manifest

Every AMTDAN research-preview result should remain traceable while patient data and implementation stay outside the public release.

| Artifact | Visibility | Required identity |
|:---|:---:|:---|
| Cohort inventory | Private | Criteria, site, patient count, content hash |
| Patient split manifest | Private | Role, task support, split hash |
| Input schema | Public-safe | Visual, clinical, quality, and missingness fields |
| Label registry | Public-safe | Seventeen tasks and five-level definitions |
| Model checkpoint | Withheld | Module config, loss weights, seed, weight hash |
| Prediction table | Private | Patient key, task, probabilities, label |
| Evaluation table | Public-safe | Checkpoint, cohort, metric and uncertainty method |
| Figure | Public | Source-table hash and rendering revision |

## Required metadata

Each record stores `artifact_id`, parent IDs, Git revision, schema and registry versions, configuration hash, content hash, creation time, governance state, and access class.

## Lineage rule

Aggregate metrics must resolve to task-level tables produced from one frozen checkpoint and split manifest. Preview figures may expose only publication-safe summaries and cannot substitute for executable evidence.

## Integrity checks

- All tasks and severity levels map to the frozen label registry.
- Patient and site identifiers remain outside public artifacts.
- Aggregate values reproduce task-level source tables.
- Replaced artifacts receive new IDs rather than overwriting history.
