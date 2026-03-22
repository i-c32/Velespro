from typing import Literal
from pydantic import BaseModel, Field, field_validator

# Definimos un tipo para el átomo: Un String seguido de 3 Floats
AtomRow = tuple[str, float, float, float]
ALLOWED_SYMBOLS = [
            "X", "H", "He", "Li", "Be", "B", "C", "N", "O", "F", "Ne", "Na",
            "Mg", "Al", "Si", "P", "S", "Cl", "Ar", "K", "Ca", "Sc", "Ti", "V", "Cr", "Mn",
            "Fe", "Co", "Ni", "Cu", "Zn", "Ga", "Ge", "As", "Se", "Br", "Kr", "Rb", "Sr",
            "Y", "Zr", "Nb", "Mo", "Tc", "Ru", "Rh", "Pd", "Ag", "Cd", "In", "Sn", "Sb",
            "Te", "I", "Xe", "Cs", "Ba", "La", "Ce", "Pr", "Nd", "Pm", "Sm", "Eu", "Gd",
            "Tb", "Dy", "Ho", "Er", "Tm", "Yb", "Lu", "Hf", "Ta", "W", "Re", "Os", "Ir",
            "Pt", "Au", "Hg", "Tl", "Pb", "Bi", "Po", "At", "Rn", "Fr", "Ra", "Ac", "Th",
            "Pa", "U", "Np", "Pu", "Am", "Cm", "Bk", "Cf", "Es", "Fm", "Md", "No", "Lw"
        ]

class SimulationConfig(BaseModel):
    name: str
    method: Literal["DFT", "HF", "MP2"]
    basis_set: Literal["STO-3G"]

class SystemConfig(BaseModel):
    charge: int = 0
    multiplicity: int = Field(1, ge=1)
    units: Literal["angstrom", "bohr"] = "angstrom"
    geometry: list[AtomRow]  # Pydantic valida automáticamente que sean 4 elementos

    # Propiedades para facilitar la extracción sin "ensuciar" el modelo con NumPy
    @property
    def symbols(self) -> list[str]:
        extracted = [row[0] for row in self.geometry]

        # Aquí realizamos la comparación/validación
        for s in extracted:
            if s not in ALLOWED_SYMBOLS:
                raise ValueError(f"Símbolo no permitido: {s}")

        return extracted

    @property
    def raw_coords(self) -> list[list[float]]:
        return [list(row[1:]) for row in self.geometry]

    @field_validator('geometry')
    @classmethod
    def validate_geometry(cls, v: list[AtomRow]):
        if not v:
            raise ValueError("La geometría no puede estar vacía")
        return v

class OptionConfig(BaseModel):
    # Usamos Literal para restringir los valores permitidos
    print_integral: Literal["all", "minimal", "none"] = "all"

class MoleculeConfig(BaseModel):
    simulation: SimulationConfig
    system: SystemConfig
    option: OptionConfig

class ProjectInput(BaseModel):
    molecule: list[MoleculeConfig]
