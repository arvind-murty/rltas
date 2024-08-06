from src.block import Block
import numpy
from numpy import float32
from pyoctree import pyoctree

class Course:
    def __init__(self, blocks):
        """
        blocks is a list of Blocks
        """
        allPts = []
        allTriangles = []
        for i in range(len(blocks)):
            b = blocks[i]

            # create 8 vertices
            pts = []

            # upper face clockwise
            pts.append([b.x - 0.300000011921, b.y + b.size, b.z - 0.300000011921])
            pts.append([b.x + b.size + 0.300000011921, b.y + b.size, b.z - 0.300000011921])
            pts.append([b.x + b.size + 0.300000011921, b.y + b.size, b.z + b.size + 0.300000011921])
            pts.append([b.x - 0.300000011921, b.y + b.size, b.z + b.size + 0.300000011921])

            # lower face clockwise
            pts.append([b.x - 0.300000011921, b.y - 1.8, b.z - 0.300000011921])
            pts.append([b.x + b.size + 0.300000011921, b.y - 1.8, b.z - 0.300000011921])
            pts.append([b.x + b.size + 0.300000011921, b.y - 1.8, b.z + b.size + 0.300000011921])
            pts.append([b.x - 0.300000011921, b.y - 1.8, b.z + b.size + 0.300000011921])

            # create 12 triangles
            triangles = []

            # top face
            triangles.append([0 + 8 * i, 1 + 8 * i, 2 + 8 * i])
            triangles.append([0 + 8 * i, 2 + 8 * i, 3 + 8 * i])
            
            # back face
            triangles.append([0 + 8 * i, 2 + 8 * i, 4 + 8 * i])
            triangles.append([2 + 8 * i, 4 + 8 * i, 5 + 8 * i])

            # left face
            triangles.append([0 + 8 * i, 3 + 8 * i, 4 + 8 * i])
            triangles.append([3 + 8 * i, 4 + 8 * i, 7 + 8 * i])

            # right face
            triangles.append([1 + 8 * i, 2 + 8 * i, 5 + 8 * i])
            triangles.append([2 + 8 * i, 5 + 8 * i, 6 + 8 * i])

            # front face
            triangles.append([2 + 8 * i, 3 + 8 * i, 6 + 8 * i])
            triangles.append([3 + 8 * i, 6 + 8 * i, 7 + 8 * i])

            # bottom face
            triangles.append([4 + 8 * i, 5 + 8 * i, 6 + 8 * i])
            triangles.append([4 + 8 * i, 6 + 8 * i, 7 + 8 * i])
            
            allPts.extend(pts)
            allTriangles.extend(triangles)
        
        ndPts = numpy.array(allPts, dtype=float)
        ndTriangles = numpy.array(allTriangles, dtype=numpy.int32)
        # print(ndPts)
        # print('{0:.16f}'.format(ndPts[0][0]))
        # print('{0:.16f}'.format(ndPts[8][2]))
        # print(ndTriangles)
        self.tree = pyoctree.PyOctree(ndPts, ndTriangles)
