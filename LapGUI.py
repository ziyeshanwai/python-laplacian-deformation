import sys
sys.path.append("S3DGLPy")
import wx
from Primitives3D import *
from PolyMesh import *
from LaplacianMesh import *
from Cameras3D import *
from MeshCanvas import *
import numpy as np
import os
import math
from pylab import cm
import matplotlib.pyplot as plt

#LAPLACIAN MESH CONSTANTS
SPECTRUM_K = 20
LOWPASS_K = 20
HEAT_K = 200
HKS_K = 200
HKS_T = 20

#GUI States
(STATE_NORMAL, STATE_CHOOSELAPLACEVERTICES, STATE_CHOOSECOLORVERTICES, STATE_ANIMATEHEAT) = (0, 1, 2, 3)
#Laplacian substates
(SUBSTATE_NONE, CHOOSELAPLACE_WAITING, CHOOSELAPLACE_PICKVERTEX) = (0, 1, 2)
#Color picking substates
(COLORPICK_NONE, COLORPICK_WAITING, COLORPICK_PICKVERTEX, COLORPICK_PICKCOLOR) = (0, 1, 2, 3)

class MeshViewerCanvas(BasicMeshCanvas):
    def clearAllSelections(self):
        #State variables for laplacian mesh operations
        self.laplacianConstraints = {} #Elements will be key-value pairs (idx, Point3D(new position))
        self.laplaceCurrentIdx = -1
        self.laplacianSelections = [] #Stores an ordered list of the selections (used for flattening)

    def __init__(self, parent):
        super(MeshViewerCanvas, self).__init__(parent)
        self.clearAllSelections()
    
    def getAnchors(self):
        anchors = np.zeros((len(self.laplacianConstraints), 3))
        i = 0
        anchorsIdx = []
        for anchor in self.laplacianConstraints:
            anchorsIdx.append(anchor)
            anchors[i, :] = self.laplacianConstraints[anchor]
            i += 1
        anchorsIdx = np.array(anchorsIdx)
        return (anchors, anchorsIdx)

    def doLaplacianSolveWithConstraints(self, evt):
        (anchors, anchorsIdx) = self.getAnchors()        
        solveLaplacianMesh(self.mesh, anchors, anchorsIdx)
    
    def doLaplacianSmooth(self, evt):
        doLaplacianSmooth(self.mesh)
        self.mesh.needsDisplayUpdate = True
        self.Refresh()

    def doLaplacianSharpen(self, evt):
        doLaplacianSharpen(self.mesh)
        self.mesh.needsDisplayUpdate = True
        self.Refresh()
    
    def doMinimalSurface(self, evt):
        (anchors, anchorsIdx) = self.getAnchors()        
        makeMinimalSurface(self.mesh, anchors, anchorsIdx)


if __name__ == '__main__':
    viewer = MeshViewer()