# Documentation

Technical notes for the AMTDAN research-preview repository.

| Document | Purpose |
|:---|:---|
| [Model card](MODEL_CARD.md) | Summarizes intended use, current scope, limitations, and privacy boundary |
| [Data interface](DATA_INTERFACE.md) | Defines multimodal examination records and the 17-task label registry |
| [Experiment record](EXPERIMENT_RECORD.md) | Captures module, loss, split, and environment settings |
| [Evaluation protocol](EVALUATION_PROTOCOL.md) | Defines patient-level partitioning and minimum reporting |
| [Artifact manifest](ARTIFACT_MANIFEST.md) | Links schemas, withheld models, evaluation tables, and public figures |
| [Failure analysis](FAILURE_ANALYSIS.md) | Reviews modality, quality, ordinal, domain, and imbalance failures |
| [Release scope](RELEASE_SCOPE.md) | Defines public artifacts, exclusions, and future release gates |
| [Release checklist](RELEASE_CHECKLIST.md) | Verifies preview claims, governance, privacy, and task-level evidence |

## Recommended order

Confirm research-preview scope and governance first, freeze input and label definitions, record every experiment, evaluate all tasks independently, bind aggregate claims to task-level artifacts, then review high-confidence and domain-shift failures.
