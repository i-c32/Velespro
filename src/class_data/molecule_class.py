from dataclasses import dataclass
import numpy as np

@dataclass(frozen=True, slots=True)
class MoleculeEngine:
    name: str
    n_at: int
    at_symbols: list[str]
    at_mass: list[float]
    geometry: np.ndarray  # Matriz de NumPy (N, 3)
    molec_mass: float
    center_mass: np.ndarray
    elec_repusion: float
    matrix_dist: np.ndarray
