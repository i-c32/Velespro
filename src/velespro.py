"""This is the main file of the project.

It reads the configuration file, creates the molecule, and writes the output file.
"""
import argparse
import logging

import src.io.read_file as rf
from pathlib import Path
from config_mod import setup_logging
from src.io.write_file import save_full_report
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
    config = rf.config_man(input_file)

    #Obtain the molecules
    molecules = config.get("molecule", [])

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
