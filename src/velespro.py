"""This is the main file of the project.

It reads the configuration file, creates the molecule, and writes the output file.
"""
import argparse
import logging

import src.io.read_file as rf
from pathlib import Path
from config_mod import setup_logging
from src.io.write_file import write_input, write_intro, write_prop_molec, write_rot_const
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

    #Obtain the name of the molecules
    keys = list(config.keys())

    mol = Molecule(keys[0]).from_hocon(config, keys[0])

    # Write the output file
    write_intro(output_file)
    write_input(output_file, mol)
    write_prop_molec(output_file, mol)

    sym = Symmetry()
    sym.rotation_const(mol)
    write_rot_const(output_file,sym.rot_const)

    sym.C2_rot_med_2at(mol)

    sym.obt_sea(mol)
    logger.debug(f"SEA: {sym.SEA})")


if __name__ == "__main__":
    main()
