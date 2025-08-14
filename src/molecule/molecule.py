from typing import List, Tuple

class Molecule:
    def __init__(self, name: str = "Unknown"):
        self.name = name
        self.atoms: List[Tuple[str, float, float, float]] = []

    def add_atom(self, element: str, x: float, y: float, z: float):
        """Add an atom to the molecule."""
        self.atoms.append((element, x, y, z))

    def __repr__(self):
        return f"<Molecule {self.name} with {len(self.atoms)} atoms>"

    def to_xyz(self) -> str:
        """Return the XYZ format string for the molecule."""
        lines = [str(len(self.atoms)), self.name]
        for atom in self.atoms:
            lines.append(f"{atom[0]:<2} {atom[1]:>12.6f} {atom[2]:>12.6f} {atom[3]:>12.6f}")
        return "\n".join(lines)

    @classmethod
    def from_hocon(cls, config, molecule_key: str):
        coords = config[molecule_key]["coord"]
        mol = cls(name=molecule_key.capitalize())
        for element, positions in coords.items():
            for xyz in positions:
                mol.add_atom(element, *xyz)
        return mol