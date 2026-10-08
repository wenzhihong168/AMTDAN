"""Framework-independent components for multimodal research experiments."""

from .fusion import GateWeights, compute_gate, fuse_embeddings

__all__ = ["GateWeights", "compute_gate", "fuse_embeddings"]
