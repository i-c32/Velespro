"""This is the main file of the project.

It reads the configuration file, creates the molecule, and writes the output file.
"""
import argparse
import logging

from pathlib import Path
from config_mod import setup_logging
from in_out import save_full_report, config_man
from src.molecule.molecule import Molecule
from src.symmetry.symmetry import Symmetry

setup_logging()
logger = logging.getLogger(__name__)


def main():
    # Obtain the name of the configuration file
    parser = argparse.ArgumentParser(description="Quatum chemistry program with some config files.")
    parser.add_argument("input", type=Path, help="Path to the input configuration file")
    parser.add_argument("output", type=Path, nargs="?", help="Path to the output file (optional)")

    args = parser.parse_args()
    input_file = args.input
    # Logic: Use the provided output, or generate one from the input
    output_file = args.output or input_file.with_suffix(".out")
    if not args.output:
        logger.warning("Output file not specified. Using default: %s", {output_file})

    # Read the config
    config = config_man(input_file)

    #Obtain the molecules
    molecules = config.get("molecule", [])

    # Inicializamos como None o una instancia vacía
    molecs: Molecule | None = None

    for mol in molecules:
        molecs = Molecule(mol["name"]).from_config(mol)


    sym = Symmetry()
    sym.rotation_const(molecs)

    # Write the output file
    save_full_report(output_file, molecs, sym)

    # sym.C2_rot_med_2at(molecs)

    # sym.obt_sea(mol)
    # logger.debug(f"SEA: {sym.SEA})")


if __name__ == "__main__":
    main()
