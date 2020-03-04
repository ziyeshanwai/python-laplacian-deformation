import sys
sys.path.append("S3DGLPy")
from S3DGLPy.PolyMesh import *
from LaplacianMesh import *
from Util.util import *


if __name__ == "__main__":
    file_name = r"./in.obj"
    polymesh = PolyMesh()
    polymesh.loadObjFile(file_name)
    v, f = loadObj(file_name)
    # for i in range(0, polymesh.VPos.shape[0]):
    #     vertex = polymesh.vertices[0]
    #     print(vertex.ID)
    #     neighbors = vertex.getVertexNeighbors()
    #     for nei in neighbors:
    #         print(nei.ID + 1)
    v = np.array(v) - np.mean(v, axis=0)
    anchors_ids = load_pickle_file(r"./anchor_id.pkl")
    anchors_ids = np.array(anchors_ids, dtype=np.int32)
    anchors = v[anchors_ids, :]
    WEIGHT = np.ones((anchors.shape[0],), dtype=np.float32)
    print("the origin index 2527 coordinates is {}".format(anchors[np.where(anchors_ids == 2527)[0], :]))
    target_points = np.array([[-0.00964538, 0.15759308*5, 2.204274]], dtype=np.float32)
    anchors[np.where(anchors_ids == 2527)[0], :] = target_points
    print("the changed index 2527 is {}".format(target_points))
    # anchors[np.where(anchors_ids == 2529)[0], :] = target_points
    # anchors[np.where(anchors_ids == 2531)[0], :] = target_points
    anchorsIdx = np.array(anchors_ids, dtype=np.int32)
    laplacian = LaplacianDeformation(polymesh, WEIGHT)
    laplacian.solveLaplacianMesh(anchors, anchorsIdx)
    laplacian.mesh.saveObjFile(r"./output.obj")