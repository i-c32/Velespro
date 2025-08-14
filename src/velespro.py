import sys
import logging

from src.config_mod.logging_mod import setup_logging
import src.io.read_file as rf
from src.molecule.molecule import Molecule


setup_logging()
logger = logging.getLogger(__name__)

def main():
    # Obtain the name of the configuration file
    if len(sys.argv) < 2:
        logging.error("There are not a config file")
        sys.exit(1)

    name_input = sys.argv[1]

    # Read the config
    config = rf.config_man(name_input)

    #Obtain the name of the molecules
    keys = list(config.keys())

    mol = Molecule(keys[0]).from_hocon(config, keys[0])

    print(mol)
    print("Atoms:", mol.atoms)
    print("Coordinates:\n", mol.coords)


if __name__ == "__main__":
    main()