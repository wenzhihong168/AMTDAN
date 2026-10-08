# Release Checklist

Complete this checklist before publishing any AMTDAN research-preview update.

## Evidence

- [ ] The input schema and 17-task, five-level label registry are frozen.
- [ ] Patient-level partitions and class support are recorded.
- [ ] Per-task results precede macro and weighted summaries.
- [ ] Ablations use identical splits, preprocessing, and evaluation code.
- [ ] Every public figure resolves to a task-level evaluation artifact.

## Governance and privacy review

- [ ] The update remains within research-preview scope and makes no clinical-use claim.
- [ ] No ultrasound, clinical record, identifier, site mapping, or private manifest is exposed.
- [ ] Missing-modality, quality, domain-shift, and high-confidence failures are reviewed.
- [ ] Code, weights, and data remain withheld until their stated release gates are satisfied.

## Repository quality

- [ ] Module settings, loss weights, seeds, environment, and metric versions are recorded.
- [ ] Public examples are synthetic or separately approved.
- [ ] Model card, release scope, and README describe the same artifact boundary.
- [ ] Checkpoints, predictions, logs, and credentials are excluded.
- [ ] The tagged revision reproduces every released publication-safe summary.
