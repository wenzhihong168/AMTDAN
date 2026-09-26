<div align="center">

# AMTDAN

**Adaptive multi-task dynamic attention for cardiac disease severity classification**

[![Status](https://img.shields.io/badge/Status-research_preview-D97706?style=flat-square)](#)
[![Modalities](https://img.shields.io/badge/Modalities-ultrasound_+_clinical-7C3AED?style=flat-square)](#architecture)
[![Code](https://img.shields.io/badge/Code-structure_only-6B7280?style=flat-square)](#repository-layout)

</div>

AMTDAN combines multi-scale visual encoding, dynamic attention, graph reasoning, and Transformer fusion for five-level severity assessment across 17 cardiac conditions.

## Architecture

<p align="center">
  <img src="assets/architecture.png" width="900" alt="AMTDAN architecture">
</p>

## Results

| Weighted precision | Weighted F1 | AUC | Cohen's κ |
|:---:|:---:|:---:|:---:|
| **90.5 ± 0.4%** | **90.0 ± 0.4%** | **93.8%** | **0.88 ± 0.02** |

<p align="center">
  <img src="assets/results.png" width="820" alt="AMTDAN severity classification results">
</p>

## Repository layout

```text
AMTDAN/
├── assets/                 # architecture and result figures
├── configs/                # task and experiment settings
├── data/                   # ultrasound and clinical interfaces
├── models/
│   ├── visual_encoder/     # multi-scale feature extraction
│   ├── dynamic_attention/  # quality-aware attention fusion
│   ├── graph_encoder/      # anatomical relation modeling
│   └── task_heads/         # disease-specific severity heads
├── evaluation/             # multi-task metrics and ablations
└── README.md
```

> Research preview. Model implementation is not included in this release.
