import sys
import numpy as np
import logging


logger = logging.getLogger(__name__)

class Molecule:
    def __init__(self, name: str = "Unknown"):
        self.name = name
        self.atoms = []
        self.coords = np.array([])
        self.at_n = []
        self.at_mass = []

    def __repr__(self):
        return f"<Molecule {self.name} with {len(self.atoms)} atoms>"


    def from_hocon(self, config, molecule_key: str):
        """
        :param config:
        :param molecule_key:
        :return:
        """
        raw_coords = config[molecule_key]["coord"]
        # Separate atoms and coordinates
        self.atoms = [row[0] for row in raw_coords]
        self.coords = np.array([row[1:] for row in raw_coords], dtype=float)

        # Compute atomic numbers and mass
        try:
            self.at_n = [self.atomic_num(atom) for atom in self.atoms]
            self.at_mass = [self.atomic_mass(at) for at in self.at_n]
        except ValueError as e:
            logging.error(f"Invalid atom: {e}")
            sys.exit(1)

        return self

    def atomic_num(self, atomos):
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

    def atomic_mass(self, n_at):
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
