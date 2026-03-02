"""Module to read the files."""
import tomllib
from pathlib import Path
from typing import TYPE_CHECKING

# [TC003] Any solo se usa en la firma de la función, se mueve aquí
if TYPE_CHECKING:
    from typing import Any


class ConfigNotFoundError(FileNotFoundError):
    """Excepción lanzada cuando el archivo de configuración no existe."""

    def __init__(self, path: Path) -> None:
        self.message = "No se encontró el archivo en la ruta: %s", path.resolve()
        super().__init__(self.message)

def config_man(input_file: Path) -> dict[str, Any]:
    """Read the hocon file for the input.

    Args:
        input_file(Path): input name for the file.

    Return:
        config of the job.
    """
    if not input_file.exists():
        raise ConfigNotFoundError(input_file)


    with input_file.open("rb") as f:
        return tomllib.load(f)
