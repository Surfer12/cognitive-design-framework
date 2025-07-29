### =============================================================
### therapeutic_fractal_framework.mojo
### =============================================================
### A *Mojo* port of the reference implementation added in the
### companion Python module.  The code purposefully leans on Python
### inter-operability (`from python import ...`) so that the same NumPy
### routines can be reused while we gradually migrate numeric kernels
### to pure Mojo.
###
### NOTE: This is still *research-grade* code – the emphasis is on
### correctness + clarity rather than raw performance.
### =============================================================

from python import numpy as np

# ---------------------------------------------------------------
# Data modelling helpers
# ---------------------------------------------------------------

struct MemoryEntry:
    """A minimal abstraction of a memory trace for experimentation."""

    var time: Float64 = 0.0
    var _vector: np.ndarray  # latent embedding (NumPy)
    var energy: Float64 = 0.0
    var alpha: Float64  # symbolic / neural allocation coefficient in [0, 1] = 0.0
    var symbolic_signal  # Python callable   S(t)
    var neural_signal  # Python callable   N(t)

    fn __init__(
        self,
        time: Float64,
        content_vector,
        energy: Float64,
        alpha: Float64,
        symbolic_signal,
        neural_signal,
    ):
        self.time = time
        self._vector = np.asarray(content_vector, dtype=np.float64)
        self.energy = energy
        self.alpha = alpha
        self.symbolic_signal = symbolic_signal
        self.neural_signal = neural_signal

    @property
    fn vector(self) -> np.ndarray:
        ### Return the latent representation as a NumPy array (read-only view).
        return self._vector

# ---------------------------------------------------------------
# Metric helpers
# ---------------------------------------------------------------

def _content_distance(m1: MemoryEntry, m2: MemoryEntry) -> Float64:
    """Euclidean distance between memory embeddings."""
    var diff = m1.vector - m2.vector
    return Float64(np.linalg.norm(diff))

def _cross_modal_interference(
    m1: MemoryEntry,
    m2: MemoryEntry,
    t_range: (Float64, Float64) = None,
    steps: Int = 128,
) -> Float64:
    """Numerically integrate  S₁·N₂ − S₂·N₁  on a uniform grid."""
    if t_range is None:
        t_range = (min(m1.time, m2.time), max(m1.time, m2.time))

    var ts = np.linspace(t_range[0], t_range[1], steps)
    var vals = [
        m1.symbolic_signal(t) * m2.neural_signal(t)
        - m2.symbolic_signal(t) * m1.neural_signal(t)
        for t in ts
    ]
    return Float64(np.trapz(vals, ts))

def cognitive_memory_distance(
    m1: MemoryEntry,
    m2: MemoryEntry,
    *,
    w_t: Float64 = 1.0,
    w_c: Float64 = 1.0,
    w_e: Float64 = 1.0,
    w_alpha: Float64 = 1.0,
    w_cross: Float64 = 1.0,
    t_range: (Float64, Float64) = None,
    steps: Int = 128,
) -> Float64:
    """Enhanced cognitive-memory metric  d_MC  (Mojo version)."""
    var dt2 = (m1.time - m2.time) ** 2
    var dc2 = _content_distance(m1, m2) ** 2
    var de2 = (m1.energy - m2.energy) ** 2
    var da2 = (m1.alpha - m2.alpha) ** 2
    var cross_val = _cross_modal_interference(
        m1, m2, t_range=t_range, steps=steps
    )

    return (
        w_t * dt2 + w_c * dc2 + w_e * de2 + w_alpha * da2 + w_cross * cross_val
    )

# ---------------------------------------------------------------
# Emergence functional  E[Ψ]
# ---------------------------------------------------------------

def emergence_functional(
    psi,
    *,
    lambda_: Float64 = 1.0,
    mu: Float64 = 1.0,
    d_t: Float64 = 1.0,
    d_m: Float64 = 1.0,
    d_s: Float64 = 1.0,
) -> Float64:
    """Evaluate a discretised version of  E[Ψ].

    *psi* is expected to be a 3-D NumPy array with axes (T, M, S).
    var dpsi_dt = np.gradient(psi, d_t, axis=0)
    var dpsi_dm = np.gradient(psi, d_m, axis=1)
    var dpsi_ds = np.gradient(psi, d_s, axis=2)

    var integrand = (
        (dpsi_dt**2) + lambda_ * (dpsi_dm**2) + mu * (dpsi_ds**2)
    )
    var total = Float64(np.sum(integrand) * d_t * d_m * d_s)
    return total

# ---------------------------------------------------------------
# Topological coherence stubs
# ---------------------------------------------------------------

def homotopy_invariant(path1, path2) -> Bool:
    """Very rough check: same endpoints  => treat as homotopic."""
    return Bool(np.allclose(path1[[0, -1]], path2[[0, -1]]))

def is_covering_space(alpha_path) -> Bool:
    """Placeholder covering-space verification for α(t) trajectories."""
    return Bool(np.all((alpha_path > 0.0) & (alpha_path < 1.0)))

# ---------------------------------------------------------------
# Public API symbols
# ---------------------------------------------------------------

__all__: (String, ...) = (
)
