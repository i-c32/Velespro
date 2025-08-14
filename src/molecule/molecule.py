import numpy as np

class Molecule:
    def __init__(self, name: str = "Unknown"):
        self.name = name
        self.atoms: []
        self.coords = np.array([])

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
        return self