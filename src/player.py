from math import atan2, degrees, radians, sqrt, copysign, atan, asin, acos, sin, cos
from numpy import float32, int32, uint64

class Input:
    def __init__(self, w = False, a = False, s = False, d = False, sprint = False, sneak = False, jump = False):
        """
        all bools
        """
        self.w = w;
        self.a = a;
        self.s = s;
        self.d = d;
        self.sprint = sprint;
        self.sneak = sneak;
        self.jump = jump;

class Player:
    pi = 3.14159265358979323846

    def __init__(self, x = 0.0, z = 0.0, y = 0.0):
        """
        all floats
        """
        self.x = x
        self.y = y
        self.z = z
        self.vx = 0.0
        self.vy = 0.0
        self.vz = 0.0
        self.prev_slip = None
        self.ground_slip = float32(0.6)

    def move(self, inpt):
        print("asd")
