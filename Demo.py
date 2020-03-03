import sys
sys.path.append("S3DGLPy")
from S3DGLPy.PolyMesh import *
from LaplacianMesh import *
from Util.util import *


if __name__ == "__main__":
    file_name = r"D:\matab_code\lapcian_mesh_deformation\testfor_matlb_lapacian_deformation.obj"
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
    anchors = v[anchors_ids, :]
    WEIGHT = np.ones((anchors.shape[0],), dtype=np.float32)
    target_points = np.array([[-9.645, -1.08917, 2.4884]], dtype=np.float32)
    # anchors[np.where(anchors_ids == 2529)[0], :] = np.mean(v, axis=0)

    anchors[np.where(anchors_ids == 2528)[0], :] = target_points
    WEIGHT[np.where(anchors_ids == 2528)[0]] = 300
    anchors[np.where(anchors_ids == 2529)[0], :] = target_points
    WEIGHT[np.where(anchors_ids == 2529)[0]] = 300
    anchors[np.where(anchors_ids == 2530)[0], :] = target_points
    WEIGHT[np.where(anchors_ids == 2530)[0]] = 300
    anchorsIdx = np.array(anchors_ids, dtype=np.int32)
    l_polymesh = solveLaplacianMesh(polymesh, anchors, anchorsIdx, WEIGHT, cotangent=True)
    l_polymesh.saveObjFile(r"./output5.obj")