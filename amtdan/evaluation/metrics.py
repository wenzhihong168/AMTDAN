"""Dependency-light metrics for five-level ordinal classification."""

from __future__ import annotations

from dataclasses import dataclass
from math import isfinite
from typing import Iterable, Sequence


def _labels(values: Iterable[int], classes: int) -> tuple[int, ...]:
    result = tuple(values)
    if not result or any(value not in range(classes) for value in result):
        raise ValueError(f"labels must be non-empty integers in [0, {classes - 1}]")
    return result


@dataclass(frozen=True, slots=True)
class OrdinalMetrics:
    accuracy: float
    macro_f1: float
    mean_absolute_grade_error: float
    within_one_grade: float
    quadratic_weighted_kappa: float
    confusion_matrix: tuple[tuple[int, ...], ...]


def _quadratic_weighted_kappa(matrix: Sequence[Sequence[int]]) -> float:
    classes = len(matrix)
    total = sum(sum(row) for row in matrix)
    true_hist = [sum(matrix[row]) for row in range(classes)]
    pred_hist = [sum(matrix[row][column] for row in range(classes)) for column in range(classes)]
    observed, expected = 0.0, 0.0
    denominator = (classes - 1) ** 2
    for row in range(classes):
        for column in range(classes):
            weight = (row - column) ** 2 / denominator
            observed += weight * matrix[row][column] / total
            expected += weight * true_hist[row] * pred_hist[column] / (total * total)
    if expected == 0:
        return 1.0 if observed == 0 else 0.0
    return 1 - observed / expected


def ordinal_metrics(y_true: Iterable[int], y_pred: Iterable[int], classes: int = 5) -> OrdinalMetrics:
    truth = _labels(y_true, classes)
    predicted = _labels(y_pred, classes)
    if len(truth) != len(predicted):
        raise ValueError("y_true and y_pred must have equal length")
    matrix = [[0 for _ in range(classes)] for _ in range(classes)]
    for actual, guess in zip(truth, predicted):
        matrix[actual][guess] += 1
    f1_values = []
    for label in range(classes):
        tp = matrix[label][label]
        fp = sum(matrix[row][label] for row in range(classes) if row != label)
        fn = sum(matrix[label][column] for column in range(classes) if column != label)
        precision = tp / (tp + fp) if tp + fp else 0.0
        recall = tp / (tp + fn) if tp + fn else 0.0
        f1_values.append(2 * precision * recall / (precision + recall) if precision + recall else 0.0)
    distances = [abs(actual - guess) for actual, guess in zip(truth, predicted)]
    return OrdinalMetrics(
        accuracy=sum(distance == 0 for distance in distances) / len(distances),
        macro_f1=sum(f1_values) / classes,
        mean_absolute_grade_error=sum(distances) / len(distances),
        within_one_grade=sum(distance <= 1 for distance in distances) / len(distances),
        quadratic_weighted_kappa=_quadratic_weighted_kappa(matrix),
        confusion_matrix=tuple(tuple(row) for row in matrix),
    )


def expected_calibration_error(
    correctness: Sequence[bool | int], confidence: Sequence[float], bins: int = 10
) -> float:
    if not correctness or len(correctness) != len(confidence):
        raise ValueError("correctness and confidence must be non-empty and aligned")
    if bins <= 0 or any(not isfinite(value) or not 0 <= value <= 1 for value in confidence):
        raise ValueError("bins must be positive and confidence must lie in [0, 1]")
    total, result = len(confidence), 0.0
    for index in range(bins):
        low, high = index / bins, (index + 1) / bins
        members = [i for i, value in enumerate(confidence) if low <= value <= high if index == bins - 1 or value < high]
        if members:
            accuracy = sum(bool(correctness[i]) for i in members) / len(members)
            mean_confidence = sum(confidence[i] for i in members) / len(members)
            result += len(members) / total * abs(accuracy - mean_confidence)
    return result
