"""Module to read the files."""
import tomllib
from typing import TYPE_CHECKING
from class_data import ProjectInput

# [TC003] Any solo se usa en la firma de la función, se mueve aquí
if TYPE_CHECKING:
    from pathlib import Path
    from pydantic import BaseModel


class ConfigNotFoundError(FileNotFoundError):
    """Excepción lanzada cuando el archivo de configuración no existe."""

    def __init__(self, path: Path) -> None:
        """Se Compruba la existencia del fichero."""
        self.path = path
        message = f"No se encontró el archivo en la ruta: {path.resolve()}"
        super().__init__(message)

def load_config(input_file: Path) -> BaseModel:
    """Read a TOML configuration file.

    Args:
        input_file: Path to the TOML configuration file.

    Returns:
        The class with the molecules data.

    Raises:
        ConfigNotFoundError: If the file does not exist.
        tomllib.TOMLDecodeError: If the file is not valid TOML.
    """
    if not input_file.exists():
        raise ConfigNotFoundError(input_file)


    with input_file.open("rb") as f:
        raw_data = tomllib.load(f)

    # Validamos y transformamos en objetos
    try:
        project = ProjectInput(**raw_data)
        return project
    except Exception as e:
        print(f"Error de validación en el input:\n{e}")
        return None
