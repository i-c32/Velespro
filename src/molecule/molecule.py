"""Module to manage the properties of the molecule."""

import logging
import sys

import numpy as np
from typing import Any
from scipy.spatial import distance_matrix

logger = logging.getLogger(__name__)


class Molecule:
    """Represent a molecular system and its physical properties."""
    name: str
    n_at: int

    def __init__(self, name: str = "Unknown") -> None:
        """Initialize a new Molecule instance.

        Args:
            name: The identifier of the molecule. Defaults to "Unknown".
        """
        self.name = name
        self.n_at = 0
        self.atoms = []
        self.coords = np.array([])
        self.at_n = np.array([])
        self.at_mass = np.array([])
        self.molec_mass = 0
        self.cm = np.array([])
        self.m_dist = np.array([])
        self.elec_rep = 0

    def __repr__(self) -> str:
        """Return the cartesian coordinates of the molecule in XYZ format.

        Returns:
            The formatted string representation of the molecule.
        """
        lines = []
        # First two lines: atom count and name
        lines.append(str(len(self.atoms)))
        lines.append(self.name)
        # Atom lines
        for atom, (x, y, z) in zip(self.atoms, self.coords):
            lines.append(f"{atom:2s}  {x:10.6f}  {y:10.6f}  {z:10.6f}")
        return "\n".join(lines)


    def from_config(self, config: dict[str, Any]) -> Molecule:
        """Build molecule from config dict with coordinate and atom data."""
        raw_coords: list[list[Any]] = config["coord"]
        atoms_raw, *xyz = zip(*raw_coords, strict=True)
        # Separate atoms and coordinates
        self.atoms = list(atoms_raw)
        self.coords = np.array(xyz, dtype=float).T

        # Compute molecule properties
        try:
            self.at_n = np.array([self.atomic_num(atom) for atom in self.atoms])
            self.n_at = len(self.atoms)
            self.at_mass = np.array([self.atomic_mass(at) for at in self.at_n])
            self.molec_mass = self.at_mass.sum()
            # La molecula se centra en su centro de masas.
            self.coords -= self.center_of_mass(self.at_mass, self.coords, self.molec_mass)
            self.m_dist = distance_matrix(self.coords, self.coords)

            self.electronic_repulsion(self.at_n,self.m_dist)

        except ValueError as e:
            logging.error(f"Invalid atom: {e}")
            sys.exit(1)

        return self

    @staticmethod
    def atomic_num(atomos: str) -> int:
        """Obtain the atomic number for the name of the atom.

        Args:
            atomos: Name of the atom.

        Returns:
            Number of the atomic number
        """
        atoms = [
            "X", "H", "He", "Li", "Be", "B", "C", "N", "O", "F", "Ne", "Na",
            "Mg", "Al", "Si", "P", "S", "Cl", "Ar", "K", "Ca", "Sc", "Ti", "V", "Cr", "Mn",
            "Fe", "Co", "Ni", "Cu", "Zn", "Ga", "Ge", "As", "Se", "Br", "Kr", "Rb", "Sr",
            "Y", "Zr", "Nb", "Mo", "Tc", "Ru", "Rh", "Pd", "Ag", "Cd", "In", "Sn", "Sb",
            "Te", "I", "Xe", "Cs", "Ba", "La", "Ce", "Pr", "Nd", "Pm", "Sm", "Eu", "Gd",
            "Tb", "Dy", "Ho", "Er", "Tm", "Yb", "Lu", "Hf", "Ta", "W", "Re", "Os", "Ir",
            "Pt", "Au", "Hg", "Tl", "Pb", "Bi", "Po", "At", "Rn", "Fr", "Ra", "Ac", "Th",
            "Pa", "U", "Np", "Pu", "Am", "Cm", "Bk", "Cf", "Es", "Fm", "Md", "No", "Lw"
        ]

        return atoms.index(atomos)

    @staticmethod
    def atomic_mass(n_at: int) -> float:
        """Obtain the atomic mass for the name of the atom.

        Args:
            n_at: Name of the atom.

        Returns:
            Mass of the atom
        """
        mass = [
            0.0, 1.00797, 4.0026, 6.939, 9.0122, 10.811, 12.01115, 14.0067,
            15.9994, 18.9984032, 20.183, 22.98976928, 24.312, 26.9815386, 28.0855, 30.9737620, 32.064,
            35.4527, 39.948, 39.102, 40.08, 44.956, 47.90, 50.942, 51.996, 54.938, 55.847, 58.933,
            58.71, 63.54, 65.37, 69.72, 72.59, 74.922, 78.96, 79.909, 83.80, 85.47, 87.62,
            88.905, 91.22, 92.906, 95.94, 98.00, 101.07, 102.905, 106.4, 107.870, 112.40, 114.82,
            118.69, 121.75, 127.60, 126.904, 131.30, 132.90545, 137.34, 138.90547, 140.116,
            140.90765, 144.242, 145.0, 150.36, 151.964, 157.25, 158.92535, 162.500, 164.93032,
            167.259, 168.93421, 173.054, 174.9668, 178.49, 180.948, 183.85, 186.2, 190.2, 192.2,
            195.09, 196.967, 200.59, 204.37, 207.19, 208.980, 209.0, 210.0, 222.0, 223.0, 226.0,
            227.0, 232.038, 231.036, 238.029, 237.0, 244.0, 243.0, 247.0, 247.0, 251.0,
            252.0, 257.0, 258.0, 259.0, 262.0
        ]

        return mass[n_at]

    @staticmethod
    def center_of_mass(m_at: np.ndarray, coords: np.ndarray, t_mass: float) -> np.ndarray:
        """Compute the center of mass of a molecule.

        Args:
            m_at: Numpy array with the mass of each atom.
            coords: Array with the coords of the molecule
            t_mass: Mass of the molecule

        Returns:
            The cartesian coordiantes for the center of mass
        """
        return (coords.T * m_at).sum(axis=1) / t_mass

    def electronic_repulsion(self, num_at: np.ndarray, dist_mat: np.ndarray) -> Molecule:
        """Obtain the electronic repulsion.

        Args:
            num_at: Array con los numeros atomicos.
            dist_mat: Matriz con las distancias entre las moleculas.

        Returns:
            Energia de repulsion electronica
        """
        i, j = np.triu_indices(len(num_at), k=1)
        self.elec_rep = np.sum((num_at[i] * num_at[j]) / dist_mat[i, j])

        return self
