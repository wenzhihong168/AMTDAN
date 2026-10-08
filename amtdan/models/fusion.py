"""Quality-aware modality gating without framework dependencies."""

from __future__ import annotations

from dataclasses import dataclass
from math import exp, isfinite
from typing import Sequence

from ..datasets.schema import ModalityState


@dataclass(frozen=True, slots=True)
class GateWeights:
    visual: float
    clinical: float

    def __post_init__(self) -> None:
        if any(not isfinite(value) or value < 0 for value in (self.visual, self.clinical)):
            raise ValueError("gate weights must be finite and non-negative")
        if abs(self.visual + self.clinical - 1.0) > 1e-9:
            raise ValueError("gate weights must sum to one")


def compute_gate(
    state: ModalityState,
    visual_logit: float = 0.0,
    clinical_logit: float = 0.0,
    *,
    quality_floor: float = 0.05,
) -> GateWeights:
    if not all(isfinite(value) for value in (visual_logit, clinical_logit, quality_floor)):
        raise ValueError("gate inputs must be finite")
    if not 0 < quality_floor <= 1:
        raise ValueError("quality_floor must lie in (0, 1]")
    if state.visual_available and not state.clinical_available:
        return GateWeights(1.0, 0.0)
    if state.clinical_available and not state.visual_available:
        return GateWeights(0.0, 1.0)
    quality = state.visual_quality if state.visual_quality is not None else 1.0
    visual_score = exp(visual_logit - max(visual_logit, clinical_logit)) * max(quality, quality_floor)
    clinical_score = exp(clinical_logit - max(visual_logit, clinical_logit))
    total = visual_score + clinical_score
    return GateWeights(visual_score / total, clinical_score / total)


def _vector(values: Sequence[float] | None, name: str) -> tuple[float, ...] | None:
    if values is None:
        return None
    result = tuple(values)
    if not result or any(not isfinite(value) for value in result):
        raise ValueError(f"{name} must contain finite values")
    return result


def fuse_embeddings(
    visual: Sequence[float] | None,
    clinical: Sequence[float] | None,
    weights: GateWeights,
) -> tuple[float, ...]:
    visual_values, clinical_values = _vector(visual, "visual"), _vector(clinical, "clinical")
    if weights.visual > 0 and visual_values is None:
        raise ValueError("visual embedding is required by the gate")
    if weights.clinical > 0 and clinical_values is None:
        raise ValueError("clinical embedding is required by the gate")
    available = [values for values in (visual_values, clinical_values) if values is not None]
    if not available or len({len(values) for values in available}) != 1:
        raise ValueError("available embeddings must have one shared dimension")
    dimension = len(available[0])
    return tuple(
        weights.visual * (visual_values[index] if visual_values else 0.0)
        + weights.clinical * (clinical_values[index] if clinical_values else 0.0)
        for index in range(dimension)
    )
