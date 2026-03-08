"""Module to write the molecules and the output file."""
from src.parameter.Parameters import umu_const, c_const
from pathlib import Path
from typing import TextIO
from src.molecule.molecule import Molecule


def write_intro(f: TextIO) -> None:
    """Escribe la cabecera del software."""
    header = (
        f"{'='*70}\n"
        f" VELESPRO :: Quantum Chemistry Suite\n"
        f" Version 2026.1.0\n"
        f"{'='*70}\n\n"
    )
    f.write(header)

def write_molecule_data(f: TextIO, mol: Molecule) -> None:
    """Escribe las secciones de propiedades y geometría."""
    # Sección de Propiedades
    f.write("[PROPERTIES]\n")
    f.write(f"  Molecule:  {mol.name}\n")
    f.write(f"  Atoms:     {mol.n_at}\n")
    f.write("  Units:     Angstrom\n\n")

    # Sección de Geometría
    f.write("[GEOMETRY]\n")
    f.write(f"  {'Element':<7} {'X':>12} {'Y':>12} {'Z':>12}\n")
    f.write(f"  {'-'*50}\n")

    geometry_block = "".join(
        f"  {atom:<7} {x:12.6f} {y:12.6f} {z:12.6f}\n"
        for atom, (x, y, z) in zip(mol.atoms, mol.coords, strict=True)
    )
    f.write(geometry_block)
    f.write(f"  {'-'*50}\n\n")

def write_prop_molec(f: TextIO, mol: Molecule) -> None:
    """Write the properties of the molecule.

    :param name_output: output name for the file.
    :param mol: data of the input.
    """
    f.write("[RESULTS.Repulsion]\n")
    f.write(f"  Nuclear Repulsion Energy: {mol.elec_rep} Hartrees\n")
    f.write(f"  {'-'*50}\n\n")

def write_rot_const(f: TextIO, rot_const) -> None:
    """Write the rotational constants.

    :param name_output: output name for the file.
    :param rot_const: rotational constants.
    """
    conv_cm = 1/umu_const*1.0E11*c_const
    conv_ghz = 1/umu_const/100/1.0E-20
    rot_const_cm = rot_const*conv_cm
    rot_const_ghz = rot_const*conv_ghz

    f.write("[RESULTS.Rotational]\n")
    f.write("The rotational constants in cm-1 are:\n")
    f.write(f"A = {rot_const_cm[0]}   B = {rot_const_cm[1]}   C = {rot_const_cm[2]}\n")
    f.write("\n")
    f.write("The rotational constants in GHz are:\n")
    f.write(f"A = {rot_const_ghz[0]}   B = {rot_const_ghz[1]}   C = {rot_const_ghz[2]}\n")
    f.write(f"  {'-'*50}\n\n")

def save_full_report(output_path: Path, mol: Molecule, sym) -> None:
    """Gestiona la escritura de todo el fichero de salida."""
    try:
        with output_path.open("w", encoding="utf-8") as f:
            write_intro(f)
            write_molecule_data(f, mol)
            write_prop_molec(f, mol)
            write_rot_const(f,sym.rot_const)

            # Modeline para Neovim al final del archivo
            f.write(f"\n{'='*70}\n")
            f.write("# vim: set foldmethod=expr foldexpr=getline(v\\:lnum)=~'^\\['?'>1'\\:'=' :\n")

    except OSError as e:
        logger.error("Error al escribir el reporte en %s: %s", output_path, e)

