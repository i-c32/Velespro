import itertools
import logging
import numpy as np

from src.parameter.Errors import SEA_tol
from src.parameter.Parameters import h_const, c_const

logger = logging.getLogger(__name__)

class Symmetry:
    def __init__(self, name: str = "Unknown"):
        self.rot_const = []
        self.SEA = []

    @staticmethod
    def inet_matrix(mol):
        x, y, z = mol.coords.T

        i_xx = np.sum(mol.at_mass * (y ** 2 + z ** 2))
        i_yy = np.sum(mol.at_mass * (x ** 2 + z ** 2))
        i_zz = np.sum(mol.at_mass * (x ** 2 + y ** 2))

        i_xy = -np.sum(mol.at_mass * x * y)
        i_xz = -np.sum(mol.at_mass * x * z)
        i_yz = -np.sum(mol.at_mass * y * z)

        return np.array([
            [i_xx, i_xy, i_xz],
            [i_xy, i_yy, i_yz],
            [i_xz, i_yz, i_zz]
        ])

    def rotation_const(self, mol):
        mat_in = self.inet_matrix(mol)
        eigvals, eigvecs = np.linalg.eig(mat_in)
        rot_const = h_const/8.0/np.pi**2/c_const/eigvals
        # Sort indices (descending order)
        idx = np.argsort(rot_const)[::-1]
        self.rot_const = rot_const[idx]
        return self

    def obt_sea(self, mol):
        # Se ordenan las distancias de la matriz
        m_dist_ord = np.sort(mol.m_dist, axis=1)

        usados = np.zeros(mol.n_at, dtype=bool)

        #Se obtienen los grupos de SEA
        for i in range(mol.n_at):
            if usados[i]:
                continue
            grupo = [i]
            usados[i] = True
            for j in range(i + 1, mol.n_at):
                if np.all(np.abs(m_dist_ord[i] - m_dist_ord[j]) < SEA_tol):
                    grupo.append(j)
                    usados[j] = True
            self.SEA.append(grupo)
        return self

    # Hay 3 comprobaciones para encontrar los atomos C2 de una molecula.
    def C2_rot_2at(self,mol_SEA):

        return 1

    def C2_rot_med_2at(self, mol_SEA):
        for i in range(mol_SEA.n_at-1):
            for j in range(mol_SEA.n_at):
                # Se calcula el punto medio.
                p_med = (mol_SEA.coords[i]-mol_SEA.coords[j])/2
                eje_C2 = p_med / np.linalg.norm(p_med)
                if self.comprobar_eje(mol_SEA,eje_C2, 180):
                    print(eje_C2)
        return 1

    def C2_rot_atraves(self, mol_SEA):
        return 1

    @staticmethod
    def comprobar_eje(mol_SEA, eje, angulo):
        """
        Rota una molécula y comprueba si la rotación produce la misma estructura.
        """
        mol_SEA_rot = Symmetry.rotar_molecula(mol_SEA.coords,eje,angulo)
        return Symmetry.son_moleculas_equivalentes(mol_SEA.atoms, mol_SEA.coords, mol_SEA.atoms, mol_SEA_rot)

    @staticmethod
    def matriz_rot(vector, angulo):
        """
        Compute a 3x3 rotation matrix given a rotation axis (vector) and an angle (in degrees).

        Parameters
        ----------
        vector : array-like of shape (3,)
            Rotation axis (not necessarily normalized).
        angulo : float
            Rotation angle in degrees.

        Returns
        -------
        m_rot : ndarray of shape (3, 3)
            Rotation matrix.
        """

        angulo_rad = np.deg2rad(angulo)
        cos_a = np.cos(angulo_rad)
        sin_a = np.sin(angulo_rad)

        x, y, z = vector

        m_rot = np.array([
            [x ** 2 * (1 - cos_a) + cos_a, x * y * (1 - cos_a) - z * sin_a, x * z * (1 - cos_a) + y * sin_a],
            [x * y * (1 - cos_a) + z * sin_a, y ** 2 * (1 - cos_a) + cos_a, y * z * (1 - cos_a) - x * sin_a],
            [x * z * (1 - cos_a) - y * sin_a, y * z * (1 - cos_a) + x * sin_a, z ** 2 * (1 - cos_a) + cos_a]
        ])

        return m_rot

    @staticmethod
    def son_moleculas_equivalentes(atoms1, coord1, atoms2, coord2, tol=1e-3):
        atoms1 = np.array(atoms1)
        atoms2 = np.array(atoms2)
        coord1 = np.array(coord1)
        coord2 = np.array(coord2)

        # Calcular matrices de distancia
        dist1 = np.linalg.norm(coord1[:, None, :] - coord1[None, :, :], axis=2)
        dist2 = np.linalg.norm(coord2[:, None, :] - coord2[None, :, :], axis=2)

        # Comprobar dimensiones
        if dist1.shape != dist2.shape or len(atoms1) != len(atoms2):
            return False

        n = len(atoms1)

        # Probar todas las permutaciones posibles de los átomos
        for perm in itertools.permutations(range(n)):
            perm = np.array(perm)

            # Comprobar que las etiquetas de los átomos coinciden
            if not np.array_equal(atoms1, atoms2[perm]):
                continue

            # Reordenar matriz de distancias
            dist2_perm = dist2[np.ix_(perm, perm)]

            # Comparar con tolerancia numérica
            if np.allclose(dist1, dist2_perm, atol=tol):
                return True

        return False

    @staticmethod
    def rotar_molecula(mol_coord, vector, angulo):
        """
        Aplica una rotación a una molécula.

        Parámetros
        ----------
        mol_coord : ndarray de forma (num_at, 3)
            Coordenadas originales de los átomos.
        vector : array-like de 3 elementos
            Eje de rotación.
        angulo : float
            Ángulo en grados.

        Retorna
        -------
        new_coord : ndarray de forma (num_at, 3)
            Coordenadas rotadas.
        """
        rotacion = Symmetry.matriz_rot(vector, angulo)

        # Aplica la rotación a cada coordenada (vector columna)
        new_coord = (rotacion @ mol_coord.T).T

        return new_coord