import unittest

from amtdan.datasets import ExaminationRecord, ModalityState, TaskRegistry, TaskSpec
from amtdan.evaluation import expected_calibration_error, ordinal_metrics
from amtdan.models import GateWeights, compute_gate, fuse_embeddings


def registry() -> TaskRegistry:
    labels = ("none", "mild", "moderate", "marked", "severe")
    return TaskRegistry(tuple(TaskSpec(f"task-{index:02d}", labels) for index in range(17)))


class SchemaTests(unittest.TestCase):
    def test_registry_and_examination_record(self):
        tasks = registry()
        record = ExaminationRecord(
            "patient-1",
            "exam-1",
            "site-a",
            ModalityState(True, True, 0.8),
            {"age": 65.0, "marker": None},
            {tasks.tasks[0].name: 3},
        )
        self.assertEqual(len(tasks.tasks), 17)
        self.assertEqual(record.labeled_task_count, 1)
        self.assertEqual(tasks.by_name("task-00").name, "task-00")

    def test_invalid_severity_is_rejected(self):
        with self.assertRaises(ValueError):
            ExaminationRecord(
                "patient-1",
                "exam-1",
                "site-a",
                ModalityState(True, False, 0.8),
                severity_labels={"task-00": 5},
            )


class MetricTests(unittest.TestCase):
    def test_ordinal_metrics_capture_distance(self):
        metrics = ordinal_metrics([0, 1, 2, 3, 4], [0, 2, 2, 2, 4])
        self.assertAlmostEqual(metrics.accuracy, 0.6)
        self.assertAlmostEqual(metrics.mean_absolute_grade_error, 0.4)
        self.assertAlmostEqual(metrics.within_one_grade, 1.0)
        self.assertGreater(metrics.quadratic_weighted_kappa, 0.0)

    def test_calibration_error_is_bounded(self):
        value = expected_calibration_error([1, 1, 0, 0], [0.9, 0.7, 0.8, 0.6], bins=4)
        self.assertGreaterEqual(value, 0.0)
        self.assertLessEqual(value, 1.0)


class FusionTests(unittest.TestCase):
    def test_single_modality_is_not_diluted(self):
        weights = compute_gate(ModalityState(False, True))
        self.assertEqual(weights, GateWeights(0.0, 1.0))
        self.assertEqual(fuse_embeddings(None, [1.0, 2.0], weights), (1.0, 2.0))

    def test_visual_quality_changes_gate_weight(self):
        high = compute_gate(ModalityState(True, True, 1.0))
        low = compute_gate(ModalityState(True, True, 0.2))
        self.assertGreater(high.visual, low.visual)
        fused = fuse_embeddings([1.0, 0.0], [0.0, 1.0], low)
        self.assertAlmostEqual(sum(fused), 1.0)


if __name__ == "__main__":
    unittest.main()
