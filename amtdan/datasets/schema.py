"""Validated contracts for AMTDAN multimodal, ordinal research inputs."""

from __future__ import annotations

from dataclasses import dataclass, field
from math import isfinite
from types import MappingProxyType
from typing import Mapping


@dataclass(frozen=True, slots=True)
class ModalityState:
    visual_available: bool
    clinical_available: bool
    visual_quality: float | None = None

    def __post_init__(self) -> None:
        if not self.visual_available and not self.clinical_available:
            raise ValueError("at least one modality must be available")
        if self.visual_quality is not None and (
            not isfinite(self.visual_quality) or not 0 <= self.visual_quality <= 1
        ):
            raise ValueError("visual_quality must be between 0 and 1")


@dataclass(frozen=True, slots=True)
class TaskSpec:
    name: str
    severity_labels: tuple[str, ...]

    def __post_init__(self) -> None:
        if not self.name.strip():
            raise ValueError("task name must not be empty")
        if len(self.severity_labels) != 5 or len(set(self.severity_labels)) != 5:
            raise ValueError("each task requires five unique ordered severity labels")


@dataclass(frozen=True, slots=True)
class TaskRegistry:
    tasks: tuple[TaskSpec, ...]

    def __post_init__(self) -> None:
        names = [task.name for task in self.tasks]
        if len(names) != 17 or len(set(names)) != 17:
            raise ValueError("AMTDAN requires exactly 17 unique tasks")

    def by_name(self, name: str) -> TaskSpec:
        for task in self.tasks:
            if task.name == name:
                return task
        raise KeyError(name)


@dataclass(frozen=True, slots=True)
class ExaminationRecord:
    patient_id: str
    exam_id: str
    site: str
    modality: ModalityState
    clinical_features: Mapping[str, float | None] = field(default_factory=dict)
    severity_labels: Mapping[str, int | None] = field(default_factory=dict)

    def __post_init__(self) -> None:
        for name in ("patient_id", "exam_id", "site"):
            value = getattr(self, name)
            if not value.strip() or (name != "site" and any(ch.isspace() for ch in value)):
                raise ValueError(f"{name} must be a non-empty study value")
        features: dict[str, float | None] = {}
        for name, value in self.clinical_features.items():
            if not name.strip() or (value is not None and not isfinite(value)):
                raise ValueError("clinical features require names and finite values or None")
            features[name] = value
        labels: dict[str, int | None] = {}
        for task, label in self.severity_labels.items():
            if not task.strip() or (label is not None and label not in range(5)):
                raise ValueError("severity labels must be integers from 0 to 4 or None")
            labels[task] = label
        object.__setattr__(self, "clinical_features", MappingProxyType(features))
        object.__setattr__(self, "severity_labels", MappingProxyType(labels))

    @property
    def labeled_task_count(self) -> int:
        return sum(label is not None for label in self.severity_labels.values())
