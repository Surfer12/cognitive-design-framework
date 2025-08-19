"""
therapeutic_fractal_framework.py
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

High-level utilities that operationalise the theoretical extensions proposed
by the user.  The focus is on three pieces of functionality:

1.  An *enhanced cognitive-memory metric*  \(d_{MC}\) that includes a
    cross-modal interference term capturing the interaction between symbolic
    and neural processing streams.

2.  A *consciousness-emergence functional*  \(E[\Psi]\) expressed as a simple
    variational energy integral that can be evaluated on discretised data.

3.  Lightweight **topological-coherence checks** that act as stubs for more
   sophisticated homotopy / covering-space verification.

The implementation purposefully keeps numerical machinery minimal – the code
is *not* a full scientific package.  Instead it provides reference
implementations that can be swapped out for domain-specific versions once the
research programme matures.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Callable, Sequence, Tuple

import numpy as np

# ---------------------------------------------------------------------------
# Data modelling helpers
# ---------------------------------------------------------------------------


@dataclass
class MemoryEntry:
    """A minimal abstraction of a memory trace.

    Parameters
    ----------
    time : float
        Timestamp (seconds since an agreed epoch).
    content_vector : Sequence[float]
        Embedding or other content descriptor living in *any* latent space.
    energy : float
        A task-specific scalar – e.g. arousal, affect level, or log-surprise.
    alpha : float
        Resource-allocation scalar in \[0, 1].  Semantically this is the
        symbolic/neural blending coefficient.
    symbolic_signal : Callable[[float], float]
        Function returning the symbolic activity *S(t)* at time *t*.
    neural_signal : Callable[[float], float]
        Function returning the neural activity *N(t)* at time *t*.
    """

    time: float
    content_vector: Sequence[float] = field(repr=False)
    energy: float
    alpha: float
    symbolic_signal: Callable[[float], float] = field(repr=False)
    neural_signal: Callable[[float], float] = field(repr=False)

    # Make life easier by materialising the embedding as a NumPy array.
    def __post_init__(self):
        self._vec = np.asarray(self.content_vector, dtype=np.float64)

    @property
    def vector(self) -> np.ndarray:  # noqa: D401 – simple property wrapper
        """Return the latent embedding as *NumPy* array (read-only view)."""
        return self._vec

# ---------------------------------------------------------------------------
# Enhanced cognitive-memory metric (Definition 1 extension)
# ---------------------------------------------------------------------------


def _content_distance(m1: MemoryEntry, m2: MemoryEntry) -> float:
    """Plain Euclidean distance between memory embeddings."""

    diff = m1.vector - m2.vector
    return float(np.dot(diff, diff) ** 0.5)


def _cross_modal_interference(
    m1: MemoryEntry,
    m2: MemoryEntry,
    t_range: Tuple[float, float] | None = None,
    steps: int = 128,
) -> float:
    """Numerically integrate the *cross-modal* interference term.

    The integrand is   **S(m₁)·N(m₂) − S(m₂)·N(m₁)**  evaluated across a sampled
    time window.  A very small trap-rule is all that is required for proof-of
    concept.
    """

    if t_range is None:
        t_range = (min(m1.time, m2.time), max(m1.time, m2.time))

    ts = np.linspace(*t_range, steps)
    integrand = [
        m1.symbolic_signal(t) * m2.neural_signal(t)
        - m2.symbolic_signal(t) * m1.neural_signal(t)
        for t in ts
    ]
    return float(np.trapz(integrand, ts))


def cognitive_memory_distance(
    m1: MemoryEntry,
    m2: MemoryEntry,
    *,
    w_t: float = 1.0,
    w_c: float = 1.0,
    w_e: float = 1.0,
    w_alpha: float = 1.0,
    w_cross: float = 1.0,
    t_range: Tuple[float, float] | None = None,
    steps: int = 128,
) -> float:
    """Compute the *enhanced* cognitive-memory metric **dₘ꜀**.

    Parameters
    ----------
    m1, m2 : MemoryEntry
        The memory traces being compared.
    w_* : float
        Non-negative weights matching the notation in the user specification.
        They need ***not*** sum to one – scaling is application dependent.
    t_range : tuple(float, float) | None
        Optional integration limits for the cross-modal term.  Defaults to the
        time span spanned by *m₁* and *m₂*.
    steps : int
        Number of samples used in the simple trapezoid integration.
    """

    dt2 = (m1.time - m2.time) ** 2
    dc2 = _content_distance(m1, m2) ** 2
    de2 = (m1.energy - m2.energy) ** 2
    da2 = (m1.alpha - m2.alpha) ** 2
    cross_term = _cross_modal_interference(m1, m2, t_range=t_range, steps=steps)

    return (
        w_t * dt2
        + w_c * dc2
        + w_e * de2
        + w_alpha * da2
        + w_cross * cross_term
    )

# ---------------------------------------------------------------------------
# Consciousness-emergence functional  E[Ψ]
# ---------------------------------------------------------------------------


def emergence_functional(
    psi: np.ndarray,
    *,
    lambda_: float = 1.0,
    mu: float = 1.0,
    d_t: float = 1.0,
    d_m: float = 1.0,
    d_s: float = 1.0,
) -> float:
    """Evaluate the discretised emergence functional *E[Ψ]*.

    The tensor *psi* is expected to have dimensions `(T, M, S)` corresponding
    to time, memory-space, and *s-space* (symbolic/neural allocation) axes.  A
    crude finite-difference approximation of the gradient terms is sufficient
    for exploratory analysis.
    """

    # Finite differences along each axis.
    dpsi_dt = np.gradient(psi, d_t, axis=0)
    dpsi_dm = np.gradient(psi, d_m, axis=1)
    dpsi_ds = np.gradient(psi, d_s, axis=2)

    integrand = (dpsi_dt**2) + lambda_ * (dpsi_dm**2) + mu * (dpsi_ds**2)
    return float(np.sum(integrand) * d_t * d_m * d_s)

# ---------------------------------------------------------------------------
# Topological coherence – extremely light placeholders
# ---------------------------------------------------------------------------


def homotopy_invariant(path1: np.ndarray, path2: np.ndarray) -> bool:
    """Placeholder: are *path₁* and *path₂* homotopic with fixed endpoints?"""

    # A *real* implementation would involve persistent-homology or numerical
    # homotopy checks.  We merely assert equal endpoints here.
    return np.allclose(path1[[0, -1]], path2[[0, -1]])


def is_covering_space(alpha_path: np.ndarray) -> bool:
    """Placeholder covering-space validation for the allocation manifold.*"""

    # The covering-space property is non-trivial.  As a stub we ensure the path
    # lives in the open interval (0, 1) ⊂ ℝ which *could* be a covering of S¹
    # under the exponential map.  A full check would require far richer data.
    return np.all((alpha_path > 0.0) & (alpha_path < 1.0))

# ---------------------------------------------------------------------------
# Convenience stubs – these will be fleshed out in downstream research code.
# ---------------------------------------------------------------------------

__all__ = [
    "MemoryEntry",
    "cognitive_memory_distance",
    "emergence_functional",
    "homotopy_invariant",
    "is_covering_space",
]