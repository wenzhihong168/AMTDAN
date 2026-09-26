# Research preview scope

AMTDAN is presented as a research preview. The repository documents the intended system design and preliminary evaluation while keeping implementation and restricted data outside the public release.

## Public artifacts

- Project overview and model architecture
- Publication-safe result figures
- Planned package layout
- Contribution and release-boundary guidance

## Excluded artifacts

- Patient-level ultrasound or clinical data
- Identifiers and private split manifests
- Model checkpoints and experiment logs
- Implementation code pending release review

## Future release gates

1. Freeze the task and label specification.
2. Verify data provenance and privacy controls.
3. Reproduce all reported metrics from immutable split manifests.
4. Add tests for data schemas, model outputs, and evaluation metrics.
5. Publish implementation only after manuscript and governance review.
