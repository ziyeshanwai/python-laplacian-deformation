from S3DGLPy.PolyMesh import *
import numpy as np
from scipy import sparse
from scipy.sparse.linalg import lsqr, cg, eigsh

WEIGHT = 1


class LaplacianDeformation:
    """
    object of laplacian deformation
    """
    def __init__(self, mesh, WEIGHT):
        self.WEIGHT = WEIGHT
        self.L = None
        self.mesh = mesh

    def getLaplacianMatrixUmbrella(self, anchorsIdx):
        n = self.mesh.VPos.shape[0]  # N x 3
        k = anchorsIdx.shape[0]
        I = []
        J = []
        V = []

        # Build sparse Laplacian Matrix coordinates and values
        for i in range(n):
            neighbors = self.mesh.vertices[i].getVertexNeighbors()
            indices = list(map(lambda x: x.ID, neighbors))
            z = len(indices)
            I = I + ([i] * (z + 1))  # repeated row
            J = J + indices + [i]  # column indices and this row
            V = V + ([-1] * z) + [z]  # negative weights and row degree
        # augment Laplacian matrix with anchor weights
        for i in range(k):
            I = I + [n + i]
            J = J + [anchorsIdx[i]]
            V = V + [self.WEIGHT[i]]  # default anchor weight
        self.L = sparse.coo_matrix((V, (I, J)), shape=(n + k, n)).tocsr()

    # Purpose: To return a sparse matrix representing a laplacian matrix with
    # cotangent weights in the upper square part and anchors as the lower rows
    # Inputs: mesh (polygon mesh object), anchorsIdx (indices of the anchor points)
    # Returns: L (An (N+K) x N sparse matrix, where N is the number of vertices
    # and K is the number of anchors)
    def getLaplacianMatrixCotangent(self, anchorsIdx):
        n = self.mesh.VPos.shape[0]  # N x 3
        k = anchorsIdx.shape[0]
        I = []
        J = []
        V = []

        # Build sparse Laplacian Matrix coordinates and values
        for i in range(n):
            vertex = self.mesh.vertices[i]
            neighbors = vertex.getVertexNeighbors()
            indices = list(map(lambda x: x.ID, neighbors))  # python3 return list
            weights = []
            z = len(indices)
            I = I + ([i] * (z + 1))  # repeated row
            J = J + indices + [i]  # column indices and this row
            for j in range(0, z):
                neighbor = neighbors[j]
                edge = getEdgeInCommon(vertex, neighbor)
                faces = [edge.f1, edge.f2]
                cotangents = []

                for f in range(2):
                    if faces[f]:
                        P = self.mesh.VPos[list(filter(lambda v: v not in [neighbor, vertex], faces[f].getVertices()))[0].ID]
                        (u, v) = (self.mesh.VPos[vertex.ID] - P, self.mesh.VPos[neighbor.ID] - P)
                        cotangents.append(np.dot(u, v) / np.sqrt(np.sum(np.square(np.cross(u, v)))))

                weights.append(-1 / len(cotangents) * np.sum(cotangents))  # cotangent weights

            V = V + weights + [(-1 * np.sum(weights))]  # n negative weights and row vertex sum

        # augment Laplacian matrix with anchor weights
        for i in range(k):
            I = I + [n + i]
            J = J + [anchorsIdx[i]]
            V = V + [self.WEIGHT[i]]  # default anchor weight

        self.L = sparse.coo_matrix((V, (I, J)), shape=(n + k, n)).tocsr()

    # Purpose: Given a mesh, to perform Laplacian mesh editing by solving the system
    # of delta coordinates and anchors in the least squared sense
    # Inputs: mesh (polygon mesh object), anchors (a K x 3 numpy array of anchor
    # coordinates), anchorsIdx (a parallel array of the indices of the anchors)
    # Returns: Nothing (should update mesh.VPos)
    def solveLaplacianMesh(self, anchors, anchorsIdx):
        n = self.mesh.VPos.shape[0]  # N x 3
        k = anchorsIdx.shape[0]
        self.getLaplacianMatrixCotangent(anchorsIdx)  # get LaplacianMatrix   cotangent=True
        delta = np.array(self.L.dot(self.mesh.VPos))
        # augment delta solution matrix with weighted anchors
        for i in range(k):
            delta[n + i, :] = self.WEIGHT[i] * anchors[i, :]
        # update mesh vertices with least-squares solution
        for i in range(3):
            self.mesh.VPos[:, i] = lsqr(self.L, delta[:, i])[0]

if __name__ == '__main__':
    print("todo test")