<div align="center">

# AMTDAN

**Adaptive multi-task dynamic attention for cardiac disease severity classification**

[![Status](https://img.shields.io/badge/Status-research_preview-D97706?style=flat-square)](#release-status)
[![Tasks](https://img.shields.io/badge/Tasks-17-8B5CF6?style=flat-square)](#task-formulation)
[![Severity](https://img.shields.io/badge/Severity-5_levels-B45309?style=flat-square)](#task-formulation)
[![Modalities](https://img.shields.io/badge/Modalities-ultrasound_+_clinical-0F766E?style=flat-square)](#multimodal-input-contract)
[![Code](https://img.shields.io/badge/Code-public_utilities-2563EB?style=flat-square)](#public-utility-layer)

<sub>multi-scale visual encoding · quality-aware dynamic attention · cardiac graph reasoning · Transformer fusion</sub>

</div>

AMTDAN is a multimodal, multi-task research framework for five-level severity assessment across 17 cardiac conditions. It combines ultrasound-derived visual representations with 39 structured clinical measurements, then uses image-quality-aware attention, anatomical graph reasoning, and global Transformer integration to produce condition-specific severity probabilities.

Developed in collaboration with **PLA General Hospital**, the project focuses on a problem that is broader than single-disease image classification. A cardiac examination can contain several coexisting abnormalities, each with an ordered severity scale and a different evidential basis. The system must preserve local image detail, account for examination quality, integrate quantitative clinical measurements, represent relationships among cardiac regions, and avoid allowing a well-represented task to dominate the remaining outputs.

This repository is a **research preview**. It documents the system architecture, aggregate results, evaluation contract, failure-analysis framework, and a dependency-light public utility layer. It does not release patient data, private split manifests, trained weights, or the complete experimental implementation. Reported values describe the current research artifact and should not be interpreted as independently reproduced results.

## At a glance

<table align="center">
  <tr align="center">
    <th>Visual input</th><th>Clinical input</th><th>Prediction space</th><th>Core reasoning</th>
  </tr>
  <tr align="center">
    <td>Cardiac ultrasound<br>representations</td>
    <td><b>39</b> structured<br>measurements</td>
    <td><b>17</b> conditions ×<br><b>5</b> severity levels</td>
    <td>Dynamic attention · GCN<br>Transformer integration</td>
  </tr>
</table>

<table align="center">
  <tr align="center">
    <th>Weighted precision</th><th>Weighted F1</th><th>AUC</th><th>Cohen's κ</th>
  </tr>
  <tr align="center">
    <td><b>90.5 ± 0.4%</b></td><td><b>90.0 ± 0.4%</b></td><td><b>93.8%</b></td><td><b>0.88 ± 0.02</b></td>
  </tr>
</table>

## Research overview

Cardiac ultrasound interpretation is intrinsically multimodal. Image appearance describes chamber morphology, wall motion, valve structure, and flow-related patterns. Quantitative measurements provide dimensions, velocities, gradients, functional indices, and pressure-related variables. Neither source is uniformly reliable in every examination: visual quality varies across views and devices, while structured variables may be missing, noisy, or only indirectly related to a particular disease.

Severity assessment adds an ordinal constraint. Confusing adjacent grades is different from confusing a mild case with a severe case, yet a conventional categorical loss treats both errors as equally distant. The challenge becomes more complex when 17 conditions are predicted jointly. Some tasks share anatomical or physiologic information, while others require highly specific evidence. A useful model must exploit related tasks without collapsing their individual decision boundaries.

AMTDAN is organized around this structure. A multi-scale visual encoder extracts patterns at several spatial resolutions. A dynamic-attention module modifies visual attention using an image-quality score. A graph-based branch represents predefined cardiac regions and their relationships while aligning structured clinical variables with regional embeddings. A global integration module then uses positional encoding and multi-head attention to combine local and global evidence before producing a five-class probability distribution for each condition.

The framework is intended to support research on standardized severity assessment. It is not presented as a clinical device, and the public artifact is not sufficient for diagnostic use. Its value at the current stage is to make the model logic, evaluation requirements, privacy boundary, and future release gates explicit.

## Task formulation

For each examination, AMTDAN produces a condition-specific probability vector over five ordered severity levels:

1. **Mild**
2. **Mild–moderate**
3. **Moderate**
4. **Moderate–severe**
5. **Severe**

The label registry treats these classes as ordered values rather than arbitrary category names. Every task must define the same five-position output contract, but the clinical meaning and sample support of each severity level remain task-specific. Unknown labels are retained as unknown and are not replaced by a normal or mild category.

All 17 conditions are evaluated independently before aggregate summaries are formed. This prevents a high-support or easier task from masking poor performance elsewhere. The minimum result record for each condition includes class support, precision, recall, F1, discrimination, ordinal agreement, calibration, and a five-by-five confusion matrix.

The model is multi-label at the examination level and ordinal within each task. One examination may contain several conditions simultaneously, and each condition receives its own severity distribution. The framework therefore differs from a single 85-class classifier: the task identity remains explicit, related conditions can share representations, and missing labels can be handled without redefining the complete output space.

## Multimodal input contract

### Visual representation

The visual branch receives a versioned ultrasound representation with view and quality metadata. Images are resized and normalized according to the frozen preprocessing specification before entering the multi-scale encoder. View identity, device family, and quality information remain attached to the examination so that performance can later be stratified rather than averaged across heterogeneous acquisition conditions.

The public contract does not prescribe redistribution of raw clinical images. Ultrasound, identifiers, and institution-specific metadata remain outside the repository. Future executable releases should use governed local data or explicitly de-identified synthetic fixtures while preserving the same schema.

### Structured clinical representation

The clinical branch receives 39 structured variables. Each variable must retain its name, unit, missingness state, and examination window. Normalization parameters are fitted on the training partition only. Missing measurements are represented explicitly and must never be replaced by undocumented constants that could be interpreted as physiologic values.

The structured vector complements rather than duplicates the visual branch. It provides quantitative context that may be difficult to infer consistently from one image, while the visual representation preserves spatial patterns that are not fully summarized by tabular measurements.

### Modality state and quality

Every examination records whether visual and clinical modalities are available and, when applicable, a bounded image-quality score. At least one modality must be present. The public utility layer uses this state to compute normalized fusion weights: a missing branch receives zero weight, and a low-quality visual branch can be down-weighted without silently discarding it.

This quality-aware policy is important for robustness. A model that assumes every ultrasound image is equally informative may become overconfident on poorly visualized anatomy. AMTDAN instead makes modality availability and visual quality part of the fusion contract so that their effects can be evaluated directly.

## Architecture

<p align="center">
  <img src="assets/architecture.png" alt="AMTDAN multimodal architecture"><br>
  <sub>Figure 1. Multi-scale visual encoding, dynamic attention, cardiac graph reasoning, and global severity prediction.</sub>
</p>

### 1. Multi-scale feature extraction

The visual encoder processes the normalized ultrasound representation through parallel convolutional paths with different receptive fields. The illustrated 3×3, 5×5, and 7×7 branches capture fine boundaries, intermediate structures, and broader cardiac context. Batch normalization stabilizes the feature distributions, while scale and translation transformations support variation in anatomy and acquisition.

The branch outputs are aligned and concatenated into a shared multi-scale feature map. This design avoids forcing one spatial resolution to represent every condition. Fine-scale features may be important for a localized structural change, whereas chamber-level remodeling or global function requires a wider receptive field.

### 2. Dynamic attention fusion

Self-attention models relationships among visual locations by constructing query, key, and value representations. AMTDAN augments this attention map with an image-quality score. The quality branch summarizes the reliability of the current visual input and interpolates between learned attention and a more uniform allocation when quality is reduced.

The resulting attention is dynamic in two senses: it depends on the content of the examination and on the estimated quality of the image. This helps prevent a small, high-response region in a poor-quality frame from dominating the complete representation. Multiple attended feature blocks are retained for subsequent regional reasoning and global fusion.

### 3. Graph-based structural encoding

The graph branch represents cardiac regions as nodes and anatomical or functional relationships as edges. An adjacency matrix defines which regions can exchange information, and normalized graph propagation aggregates neighboring evidence. Graph convolution therefore imposes a structured inductive bias: related cardiac regions communicate through an explicit topology rather than only through unconstrained dense layers.

Structured clinical measurements are normalized, embedded, and projected to the graph feature dimension. The clinical embedding is concatenated with the regional graph representation to form a multimodal structural feature. This design connects quantitative measurements to an anatomy-aware latent space while preserving the missingness and modality information declared by the input contract.

### 4. Global feature integration and prediction

The fused regional representation is converted into an ordered feature sequence and combined with positional encoding. Multi-head attention and feed-forward blocks integrate information across regions, modalities, and tasks. The global feature is then mapped to five logits for each condition, followed by a softmax probability distribution over severity levels.

Task-specific prediction heads retain the identity of all 17 conditions. Multi-task optimization allows shared visual, graph, and clinical representations to learn from correlated outcomes, while the separate heads preserve condition-specific class distributions. The final result for one examination is therefore a matrix of task-by-severity probabilities rather than a single diagnosis.

## Model design principles

1. **Multi-scale perception** — different receptive fields preserve both local structural detail and global cardiac context.
2. **Quality-aware attention** — visual evidence is weighted according to examination content and image quality.
3. **Anatomical structure** — graph propagation encodes relationships among cardiac regions instead of relying only on generic feature fusion.
4. **Multimodal alignment** — clinical measurements are projected into the same representational space as graph-derived visual features.
5. **Task-specific outputs** — every condition retains its own five-level probability distribution.
6. **Ordinal evaluation** — adjacent-grade and distant-grade errors are distinguished during analysis.
7. **Missing-modality transparency** — availability and quality states are explicit inputs to the fusion policy.

## Reported results

The current research artifact reports a weighted precision of 90.5 ± 0.4%, weighted F1 of 90.0 ± 0.4%, AUC of 93.8%, and Cohen's κ of 0.88 ± 0.02. These values summarize the multi-task experiment and should be read together with per-task support, severity distributions, calibration, and confusion matrices when the complete evaluation artifacts become available.

Weighted metrics emphasize tasks and classes with greater support. They are useful for summarizing the overall experiment but can underrepresent rare conditions or severity levels. Cohen's κ adds agreement information beyond raw accuracy, while task-level confusion matrices show whether errors are concentrated near the diagonal or span several severity grades.

### Severity error structure

The preview figure presents representative confusion matrices for pulmonary regurgitation, pulmonary artery pressure, aortic regurgitation, and left-ventricular diastolic dysfunction. Diagonal concentration indicates exact-grade agreement, while off-diagonal cells reveal the direction and distance of misclassification.

Pulmonary regurgitation is shown as a higher-performing task, with strong diagonal values across the five grades. Pulmonary artery pressure is presented as a more difficult task, with greater confusion between adjacent levels. Aortic regurgitation and diastolic dysfunction occupy an intermediate range. Across the examples, most visible errors remain near the diagonal, but this qualitative pattern must be confirmed for all 17 tasks using the frozen task-level result tables.

<p align="center">
  <img src="assets/results.png" alt="AMTDAN representative five-level confusion matrices"><br>
  <sub>Figure 2. Representative severity confusion matrices illustrating task heterogeneity and adjacent-grade error.</sub>
</p>

### How the metrics should be read

Precision describes the reliability of assigned severity labels under the observed class distribution. F1 balances precision and recall but does not encode how far an incorrect grade lies from the reference. AUC evaluates discrimination over decision thresholds and should be reported by task and class. Cohen's κ measures agreement beyond chance but remains sensitive to prevalence and label distribution.

For an ordinal problem, these measures should be complemented by mean absolute grade error, the proportion of predictions within one grade, quadratic-weighted κ, calibration error, and class-specific support. The public metric utilities implement these ordinal summaries so that future results can distinguish a near miss from a clinically distant error.

## Evaluation protocol

### Leakage-safe partitioning

All examinations from one patient must remain in the same partition. The split is frozen before normalization, augmentation, feature extraction, architecture selection, threshold selection, or calibration. Repeated examinations are never divided across training and test sets. This rule prevents patient-specific anatomy or acquisition signatures from inflating generalization performance.

### Task-aware reporting

Every condition is evaluated separately before computing macro and support-weighted summaries. The minimum report includes per-class precision and recall, task-level F1, ROC analysis, a full five-level confusion matrix, ordinal distance, quadratic-weighted κ, and calibration. Aggregate results must resolve to the same frozen checkpoint, task registry, and patient split.

### Ablation design

Ablations should remove one component at a time while preserving the split, preprocessing, optimization budget, and evaluation code. The planned comparisons isolate multi-scale extraction, quality-aware attention, graph reasoning, Transformer integration, and multi-task optimization. Variation across seeds or resamples should accompany point estimates.

### Domain and quality stratification

Performance should be stratified by site, device family, view, visual-quality grade, modality-availability pattern, condition, and severity when sample support permits. A high aggregate score can coexist with failure on low-quality images or a specific device domain. Calibration should be repeated within important deployment strata rather than assumed from the pooled cohort.

## Failure analysis

AMTDAN uses an explicit error taxonomy so that different failure mechanisms are not merged into one metric:

- **Visual-quality failure** — performance changes with image quality, view, or device family.
- **Missing-modality failure** — predictions degrade when one branch is unavailable or poorly represented.
- **Ordinal near miss** — the predicted grade is adjacent to the reference.
- **Ordinal severe miss** — the prediction differs by several severity levels.
- **Domain shift** — performance or calibration changes across sites or devices.
- **Task imbalance** — rare conditions or severity levels have unstable recall and precision.

High-confidence errors and distant-grade errors require case-level review. The review record should include task identity, full probability vector, modality state, visual-quality flags, graph or attention diagnostics when available, class support, and label-review status. Changes made after failure analysis must be evaluated on the original frozen split to avoid converting error inspection into test-set tuning.

## Public utility layer

The current repository includes tested, dependency-light components that make the future experimental release easier to audit:

- validated multimodal examination records;
- an immutable 17-task registry with five ordered labels per task;
- explicit modality-availability and visual-quality states;
- quality-aware fusion weights for visual and clinical embeddings;
- accuracy, macro F1, grade-distance, within-one-grade, and quadratic-weighted κ metrics;
- expected calibration error;
- model-card, evaluation, data-interface, artifact-lineage, and failure-analysis documentation;
- continuous integration for the public utilities.

These components define interfaces and evaluation behavior. They are not the full AMTDAN training implementation and cannot reproduce the reported aggregate results without the withheld architecture, governed data, split manifests, and model artifacts.

## Repository layout

```text
AMTDAN/
├── assets/
│   ├── architecture.png            # multimodal model architecture
│   └── results.png                 # representative ordinal results
├── amtdan/
│   ├── datasets/
│   │   ├── schema.py               # examination, modality, and task contracts
│   │   └── registry/               # planned task and label registries
│   ├── models/
│   │   ├── visual/                 # planned multi-scale visual encoder
│   │   ├── attention/              # planned quality-aware attention
│   │   ├── graph/                  # planned cardiac graph reasoning
│   │   ├── transformer/            # planned global feature integration
│   │   ├── heads/                  # planned 17 ordinal prediction heads
│   │   └── fusion.py               # public modality-gating utility
│   ├── training/
│   │   ├── objectives/             # planned multi-task and ordinal losses
│   │   ├── sampling/               # planned imbalance-aware sampling
│   │   └── callbacks/              # planned checkpoint and audit hooks
│   ├── evaluation/
│   │   ├── metrics.py              # public ordinal and calibration metrics
│   │   ├── stratification/         # planned quality and domain analyses
│   │   └── reporting/              # planned task-level reports
│   └── utils/                       # planned provenance and IO helpers
├── configs/
│   ├── data/                        # future cohort and preprocessing profiles
│   ├── model/                       # future module configuration
│   └── experiment/                  # future training and ablation protocols
├── data/
│   ├── synthetic/                   # future public schema fixtures only
│   └── private/                     # local governed data; never committed
├── docs/
│   ├── DATA_INTERFACE.md
│   ├── EVALUATION_PROTOCOL.md
│   ├── FAILURE_ANALYSIS.md
│   ├── MODEL_CARD.md
│   ├── ARTIFACT_MANIFEST.md
│   └── RELEASE_SCOPE.md
├── tests/
│   └── unit/                        # executable public-utility tests
├── pyproject.toml
└── README.md
```

## Release status

The architecture diagram and result figure are provided for transparent research communication. The public package currently validates data contracts, ordinal metrics, calibration summaries, and quality-aware fusion behavior. It does not include the complete visual encoder, graph network, Transformer stack, training loop, model weights, clinical data, private configurations, or patient-level predictions.

Future implementation release is gated on a frozen task registry, verified artifact lineage, reproducible task-level results, privacy and governance review, executable evaluation assets, and confirmation that no patient or institution-sensitive information is exposed. New public artifacts should be linked to a Git revision, schema version, configuration identity, and source-table hash.

## Scope and responsible use

AMTDAN is intended for research discussion, protocol development, and future reproducibility work. It is not approved for diagnosis, triage, treatment selection, or autonomous report generation. The reported aggregate metrics do not establish portability across hospitals, devices, populations, or annotation practices.

Five-level labels may reflect local reporting conventions, and some tasks may have limited examples at the extreme grades. Visual quality, missing modalities, class imbalance, and domain shift can change both accuracy and calibration. Any clinical investigation must include independent target-site validation, prospective workflow assessment, and human review of all outputs.

> **Research-preview boundary:** public figures and summary values document the current project state. They do not substitute for executable reproduction, external validation, or prospective clinical evaluation.
