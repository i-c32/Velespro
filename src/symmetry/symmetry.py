import logging
import numpy as np

logger = logging.getLogger(__name__)

class Symmetry:
    def __init__(self, name: str = "Unknown"):
        self.rot_const = []
        
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
        # Sort indices (descending order)
        idx = np.argsort(eigvals)[::-1]
        self.rot_const = eigvals[idx]
        return self


        


    
