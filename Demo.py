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
    v = np.array(v)
    # v = np.array(v) - np.mean(v, axis=0)
    to_move_points_index = 2531
    anchors_ids = load_pickle_file(r"./anchor_id.pkl")
    anchors_ids = np.array(anchors_ids, dtype=np.int32)
    anchors = v[anchors_ids, :]
    WEIGHT = np.ones((anchors.shape[0],), dtype=np.float32)
    print("the origin index {} coordinates is {}".format(to_move_points_index, anchors[np.where(anchors_ids == to_move_points_index)[0], :]))
    tmp = anchors[np.where(anchors_ids == to_move_points_index)[0], :]
    tmp[:, 2] = tmp[:, 2] * 2.5
    target_points = tmp
    # target_points = np.array([[-0.00964538, 0.15759308, 2.204274*1.2]], dtype=np.float32)
    anchors[np.where(anchors_ids == to_move_points_index)[0], :] = target_points
    print("the changed index {} is {}".format(to_move_points_index, target_points))
    # anchors[np.where(anchors_ids == 2529)[0], :] = target_points
    # anchors[np.where(anchors_ids == 2531)[0], :] = target_points
    anchorsIdx = np.array(anchors_ids, dtype=np.int32)
    laplacian = LaplacianDeformation(polymesh, WEIGHT)
    laplacian.solveLaplacianMesh(anchors, anchorsIdx, True)
    laplacian.mesh.saveObjFile(r"./output.obj")