import os
import sys
import logging

from src.config_mod.logging_mod import setup_logging
import src.io.read_file as rf
from src.io.write_file import write_intro, write_input, write_prop_molec, write_rot_const
from src.molecule.molecule import Molecule
from src.symmetry.symmetry import Symmetry

setup_logging()
logger = logging.getLogger(__name__)

def main():
    # Obtain the name of the configuration file
    if len(sys.argv) < 2:
        logging.error("There are not a config file")
        sys.exit(1)

    name_input = sys.argv[1]

    if len(sys.argv) < 3:
        logging.warning("The output file is not introduced. It uses the same name than the input.")
        name_output = os.path.splitext(sys.argv[1])[0] + ".out"
    else:
        name_output = sys.argv[2]

    # Read the config
    config = rf.config_man(name_input)

    #Obtain the name of the molecules
    keys = list(config.keys())

    mol = Molecule(keys[0]).from_hocon(config, keys[0])

    # Write the output file
    write_intro(name_output)
    write_input(name_output, mol)
    write_prop_molec(name_output, mol)

    sym = Symmetry()
    sym.rotation_const(mol)
    write_rot_const(name_output,sym.rot_const)

    sym.C2_rot_med_2at(mol)

    sym.obt_sea(mol)
    print(sym.SEA)


if __name__ == "__main__":
    main()