import os
import pickle
import json
import numpy as np


def load_pts(path):
    if not os.path.exists(path):
        return []
    with open(path, 'r') as f:
        lines = [l.strip() for l in f.readlines()]
    line = lines[0]
    while not line.startswith('{'):
        line = lines.pop(0)

    data = []
    for line in lines:
        if not line.strip().startswith('}'):
            xpos, ypos = line.split()[:2]
            data.append((float(xpos), float(ypos)))

    return data



def save_pickle_file(filename, file):
    with open(filename, 'wb') as f:
        pickle.dump(file, f)
        print("save {}".format(filename))


def load_pickle_file(filename):
    if os.path.exists(filename):
        with open(filename, "rb") as f:
            file = pickle.load(f)
        return file
    else:
        print("{} not exist".format(filename))


def loadObj(path):
    """Load obj file
    读取三角形和四边形的mesh
    返回vertex和face的list
    """
    if path.endswith('.obj'):
        f = open(path, 'r')
        lines = f.readlines()
        vertics = []
        faces = []
        vts = []
        for line in lines:
            if line.startswith('v') and not line.startswith('vt') and not line.startswith('vn'):
                line_split = line.split()
                ver = line_split[1:4]
                ver = [float(v) for v in ver]
                vertics.append(ver)
            else:
                if line.startswith('f'):
                    line_split = line.split()
                    if '/' in line:  # 根据需要这里补充obj的其他格式解析
                        tmp_faces = line_split[1:]
                        f = []
                        for tmp_face in tmp_faces:
                            f.append(int(tmp_face.split('/')[0]))
                        faces.append(f)
                    else:
                        face = line_split[1:]
                        face = [int(fa) for fa in face]
                        faces.append(face)

        return (vertics, faces)

    else:
        print('格式不正确，请检查obj格式')
        return


def writeObj(file_name_path, vertexs, faces, vts=None):
    """write the obj file to the specific path
       file_name_path:保存的文件路径
       vertexs:顶点数组 list
       faces: 面 list
    """
    with open(file_name_path, 'w') as f:
        for v in vertexs:
            # print(v)
            f.write("v {} {} {}\n".format(v[0], v[1], v[2]))
        for face in faces:
            if len(face) == 4:
                f.write("f {} {} {} {}\n".format(face[0], face[1], face[2], face[3])) # 保存四个顶点
            if len(face) == 3:
                f.write("f {} {} {}\n".format(face[0], face[1], face[2]))  # 保存三个顶点
        if vts != None:
            for vt in vts:
                f.write("vt {} {}\n".format(vt[0], vt[1]))
        print("saved mesh to {}".format(file_name_path))