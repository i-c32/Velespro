"""Module to write the molecules and the output file."""
from src.parameter.Parameters import umu_const, c_const


def write_intro(name_output: str):
    """ Write the intro file.

    Args:
        name_output: output name for the file.
    """

    # Ensure the config file is read correctly, handling BOM if present
    with open(name_output, "w", encoding="utf-8") as f:
        f.write("""----------------------------------------------------------------------------------------------------------------
VVVVV           VVVVVVV            llllll EEEEEEEEEEEEEE  SSSSSSSSSSSS PPPPPPPPPPPPPP                           
V:::V           V:::::V            l::::l E::::::::::::E S::::::::::::SP:::::::::::::P
V:::V           V:::::V            l::::l E::::::::::::ES::::SSSSS::::SP:::::PPPPP::::P
V:::V           V:::::V            l::::l EE::::EEEEE::ES::::S    SSSSSPP::::P    P::::P
V:::V           V::::V eeeeeeeeee   l:::l   E:::E   EEEES::::S           P:::P    P::::Prrr   rrrrr     oooooo
V::::V         V::::Vee::::::::::e  l:::l   E:::E       S::::S           P:::P    P::::Pr::rrr:::::r   o::::::o
 V::::V       V::::Ve::::eeeee::::eel:::l   E::::EEEEEE  ::::SSS         P:::PPPPP::::P r:::::::::::r o::::::::o
  V::::V     V::::Ve::::e     e::::el:::l   E:::::::::E  SS:::::SSSS     P:::::::::::P  rr::::rrr::::ro:::oo:::o
   V::::V   V::::V e:::::eeeee:::::el:::l   E:::::::::E    SSS::::::S    P:::PPPPPPPP    r:::r   r:::ro::o  o::o
    V::::V V::::V  e::::::::::::::e l:::l   E::::EEEEEE       SSSSS::S   P:::P           r:::r   rrrrro::o  o::o
     V::::V::::V   e::::eeeeeeeeee  l:::l   E:::E                 S:::S  P:::P           r:::r        o::o  o::o
      V:::::::V    e:::::e          l:::l   E:::E   EEEE          S:::S  P:::P           r:::r        o::o  o::o
       V:::::V     e::::::e        l:::::lEE::::EEEE:::ESSSSSS    S:::SPP:::::PP         r:::r        o:::oo:::o
        V:::V       e::::::eeeeeee l:::::lE::::::::::::ES:::::SSSSS:::SP:::::::P         r:::r        o::::::::o
         V:V         ee::::::::::e l:::::lE::::::::::::ES::::::::::::S P:::::::P         r:::r         o::::::o
          V            eeeeeeeeeee lllllllEEEEEEEEEEEEEE SSSSSSSSSSSS  PPPPPPPPP         rrrrr          oooooo
----------------------------------------------------------------------------------------------------------------
Quantum chemistry program in python
""")

def write_input(name_output: str, mol):
    """
    Write the input file.
    :param name_output: output name for the file.
    :param mol: data of the input.
    """

    # Ensure the config file is read correctly, handling BOM if present
    with open(name_output, "a", encoding="utf-8") as f:
        lines = []
        # First two lines: atom count and name
        lines.append("%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")
        lines.append(str(len(mol.atoms)))
        lines.append(mol.name)
        # Atom lines
        for atom, (x, y, z) in zip(mol.atoms, mol.coords):
            lines.append(f"{atom:2s}  {x:10.6f}  {y:10.6f}  {z:10.6f}")
        lines.append("%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")
        f.write("\n".join(lines))

def write_prop_molec(name_output: str, mol):
    """
    Write the properties of the molecule.
    :param name_output: output name for the file.
    :param mol: data of the input.
    """

    # Ensure the config file is read correctly, handling BOM if present
    with open(name_output, "a", encoding="utf-8") as f:
        lines = [""]
        lines.append(f"The repulsion energy is: {mol.elec_rep} Hartrees")
        lines.append("%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")
        f.write("\n".join(lines))

def write_rot_const(name_output: str, rot_const):
    """
    Write the rotational constants.
    :param name_output: output name for the file.
    :param rot_const: rotational constants.
    """

    # Ensure the config file is read correctly, handling BOM if present
    with open(name_output, "a", encoding="utf-8") as f:
        conv_cm = 1/umu_const*1.0E11*c_const
        conv_ghz = 1/umu_const/100/1.0E-20
        rot_const_cm = rot_const*conv_cm
        rot_const_ghz = rot_const*conv_ghz
        lines = []
        # First two lines: atom count and name
        lines.append("")
        lines.append("The rotational constants in cm-1 are:")
        lines.append(f"A = {rot_const_cm[0]}   B = {rot_const_cm[1]}   C = {rot_const_cm[2]}")
        lines.append("")
        lines.append("The rotational constants in GHz are:")
        lines.append(f"A = {rot_const_ghz[0]}   B = {rot_const_ghz[1]}   C = {rot_const_ghz[2]}")
        lines.append("%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")
        f.write("\n".join(lines))
