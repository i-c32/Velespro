"""This is the main file of the project.

Reads a TOML configuration file, builds molecular structures,
computes symmetry properties, and writes a full report.
"""
import argparse
import logging
import sys

from pathlib import Path
from config_mod import setup_logging
from in_out import save_full_report, load_config
from src.molecule.molecule import Molecule
from src.symmetry.symmetry import Symmetry

setup_logging()
logger = logging.getLogger("vel_app")


def parse_args() -> argparse.Namespace:
    """Parse and return command-line arguments."""
    parser = argparse.ArgumentParser(
        description="Quantum chemistry program driven by TOML configuration files.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument(
        "input",
        type=Path,
        help="Path to the input TOML configuration file.",
    )
    parser.add_argument(
        "output",
        type=Path,
        nargs="?",
        help="Path to the output report file (optional).",
    )
    return parser.parse_args()

def run(input_file: Path, output_file: Path) -> int:
    """Execute the full computational chemistry pipeline.

    Args:
        input_file: Path to the TOML configuration file.
        output_file: Path to the output report file.

    Returns:
        Exit code: 0 on success, 1 on handled error, 2 on unexpected error.
    """
    try:
        mol_config = load_config(input_file)
        #molecules = build_molecules(config)
    except FileNotFoundError as e:
        logger.error("Input file not found: %s", e)
        return 1
    except ValueError as e:
        logger.error("Invalid configuration: %s", e)
        return 1
    except Exception as e:
        logger.critical("Unexpected error while loading configuration: %s", e, exc_info=True)
        return 2

    # For the Symmetry
    try:
        sym = Symmetry()
#        for mol in molecules:
#            logger.info("Processing molecule: %s", mol.name)
#            sym.rotation_const(mol)

            # sym.C2_rot_med_2at(molecs)

            # sym.obt_sea(mol)
            # logger.debug(f"SEA: {sym.SEA})")
    except Exception as e:
        logger.critical("Pipeline failed during processing: %s", e, exc_info=True)
        return 2

    # Final report
#    try:
#        molec = molecules[0]
#        save_full_report(output_file, molec, sym)
#    except Exception as e:
#        logger.critical("Pipeline failed during processing: %s", e, exc_info=True)
#        return 2

    logger.info("Report successfully written to: %s", output_file)
    return 0


def main() -> None:
    """Parse arguments and run the pipeline."""
    args = parse_args()

    input_file: Path = args.input
    output_file: Path = args.output or input_file.with_suffix(".out")

    if not args.output:
        logger.warning("Output file not specified, defaulting to: %s", output_file)

    exit_code = run(input_file, output_file)

    if exit_code == 0:
        logger.info("Pipeline completed successfully.")
    elif exit_code == 1:
        logger.error("Pipeline finished with configuration errors.")
    else:
        logger.critical("Pipeline aborted due to an unexpected error.")

    sys.exit(exit_code)


if __name__ == "__main__":
    setup_logging()
    main()
