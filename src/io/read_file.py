"""Module to read the files."""
from pathlib import Path
from pyhocon import ConfigFactory


def config_man(input_file: Path):
    """Read the hocon file for the input.

    Args:
        name_input(Path): input name for the file.

    Return:
        config of the job.
    """

    # Ensure the config file is read correctly, handling BOM if present
    with open(input_file, "r", encoding="utf-8") as f:
        content = f.read()

    if content.startswith("\ufeff"):
        content = content[1:]

    return ConfigFactory.parse_string(content).get("Velespro")
