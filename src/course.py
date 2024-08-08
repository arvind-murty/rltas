import numpy
from numpy import float32

class Block:
    # for now only support (x,z)-centered cubes starting at integer height
    def __init__(self, x = 0, y = 0, z = 0, x_min = 0.0, y_min = 0.0, z_min = 0.0, x_max = 1.0, y_max = 1.0, z_max = 1.0):
        """
        int, int, int, float
        """
        self.x = x
        self.y = y
        self.z = z
        self.x_min = x_min
        self.y_min = y_min
        self.z_min = z_min
        self.x_max = x_max
        self.y_max = y_max
        self.z_max = z_max

    @classmethod
    def block(cls, x = 0, y = 0, z = 0, size = 1.0):
        return cls(x, y, z, float(x), float(y), float(z), float(x + size), float(y + size), float(z + size))
    
    # out of bounds constructor
    @classmethod
    def oob(cls):
        return cls(0, -1, 0, 30000001.0, 257.0, 30000001.0, -30000001.0, -1.0, -30000001.0)

class Course:
    def __init__(self, blocks):
        """
        blocks is a list of Blocks
        self.blocks is a dictionary mapping coordinates to Blocks
        """
        self.blocks = {}
        for b in blocks:
            self.blocks[(b.x, b.y, b.z)] = b
