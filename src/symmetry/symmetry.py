import logging
import numpy as np
from scipy.spatial.distance import pdist, squareform

from src.parameter.Errors import SEA_tol
from src.parameter.Parameters import h_const, c_const

logger = logging.getLogger(__name__)

class Symmetry:
    def __init__(self, name: str = "Unknown"):
        self.rot_const = []
        self.SEA = []
        
    def inet_matrix(self, mol):
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
        # Se calcula la matriz de distancia para la molecula
        m_dist = squareform(pdist(mol.coords))
        # Se ordenan las distancias de la matriz
        m_dist_ord = np.sort(m_dist, axis=1)

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


        


    
