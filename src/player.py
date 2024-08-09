import math
from math import floor
import numpy
from src.course import Block
from numpy import float32, float64, int32, uint64

class Input:
    def __init__(self, w = False, a = False, s = False, d = False, sprint = False, sneak = False, jump = False, rotation = 0.0):
        self.w = w;
        self.a = a;
        self.s = s;
        self.d = d;
        self.sprint = sprint;
        self.sneak = sneak;
        self.jump = jump;
        # clockwise in degrees
        self.rotation = rotation

class Player:
    PI = 3.14159265358979323846
    EPSILON = 0.000000001
    WIDTH = 0.30000001192092896
    HEIGHT = 1.7999999523162841796875

    def __init__(self, x = 0.0, y = 1.0, z = 0.0, facing = 0.0):
        # floats
        self.x = x
        self.y = y
        self.z = z
        self.vx = 0.0
        self.vy = 0.0
        self.vz = 0.0
        self.ground_slip = float32(0.6)
        self.slip = self.ground_slip
        self.facing = float32(facing)
        self.inertia = float32(0.005)
        
        # bools
        self.airborne = False
        self.sprinting = False
        self.stop_sprint = False
    
    def __str__(self):
        return f"x: {self.x}\ny: {self.y}\nz: {self.z}\nvx: {self.vx}\nvy: {self.vy}\nvz: {self.vz}\n"

    def mcsin(self, rad):
        index = int(rad * float32(10430.378)) & 65535
        return float32(math.sin(index * Player.PI * 2.0 / 65536))

    def mccos(self, rad):
        index = int(rad * float32(10430.378) + float32(16384.0)) & 65535
        return float32(math.sin(index * Player.PI * 2.0 / 65536))

    # thanks physiq
    def move(self, inpt, course):
        # y velocity
        if self.airborne:
            self.vy = (self.vy - 0.08) * 0.9800000190734863
            if abs(self.vy) < self.inertia:
                self.vy = 0.0
        elif inpt.jump:
            self.vy = float64(float32(0.42))
        else:
            self.vy = (0.0 - 0.08) * 0.9800000190734863

        # check y blockages
        next_airborne = True
        if self.vy <= 0.0:
            b1 = course.blocks.get((floor(self.x - Player.WIDTH), floor(self.y + self.vy), floor(self.z - Player.WIDTH)), Block.oob())
            b2 = course.blocks.get((floor(self.x - Player.WIDTH), floor(self.y + self.vy), floor(self.z + Player.WIDTH)), Block.oob())
            b3 = course.blocks.get((floor(self.x + Player.WIDTH), floor(self.y + self.vy), floor(self.z - Player.WIDTH)), Block.oob())
            b4 = course.blocks.get((floor(self.x + Player.WIDTH), floor(self.y + self.vy), floor(self.z + Player.WIDTH)), Block.oob())
            y_max = max(b1.y_max, b2.y_max, b3.y_max, b4.y_max)
            if y_max > 0.0 and self.vy < y_max - self.y:
                next_airborne = False
                # set vy to difference between current height and y_max (max height of block below) if player hits it
                self.vy = self.y
                self.y = y_max
                self.vy = self.y - self.vy
            else:
                self.y += self.vy
        else:
            b1 = course.blocks.get((floor(self.x - Player.WIDTH), floor(self.y + self.vy + Player.HEIGHT), floor(self.z - Player.WIDTH)), Block.oob())
            b2 = course.blocks.get((floor(self.x - Player.WIDTH), floor(self.y + self.vy + Player.HEIGHT), floor(self.z + Player.WIDTH)), Block.oob())
            b3 = course.blocks.get((floor(self.x + Player.WIDTH), floor(self.y + self.vy + Player.HEIGHT), floor(self.z - Player.WIDTH)), Block.oob())
            b4 = course.blocks.get((floor(self.x + Player.WIDTH), floor(self.y + self.vy + Player.HEIGHT), floor(self.z + Player.WIDTH)), Block.oob())
            y_min = min(b1.y_min, b2.y_min, b3.y_min, b4.y_min)
            if y_min < 257.0 and self.vy < y_min - self.y - Player.HEIGHT:
                # set vy to difference between current height and y_min (min height of block above) if player hits it
                self.vy = self.y
                self.y = y_min - Player.HEIGHT
                self.vy = self.y - self.vy
            else:
                self.y += self.vy
        
        self.facing += inpt.rotation
        # x,z velocity
        self.vx *= float32(0.91) * self.slip
        self.vz *= float32(0.91) * self.slip
        if abs(self.vx) < self.inertia:
            self.vx = 0.0
        if abs(self.vz) < self.inertia:
            self.vz = 0.0

        if self.airborne:
            movement = float32(0.02)
            if self.sprinting:
                movement = float32(movement + movement * float64(0.3))
        else:
            movement = float32(0.1)
            # +w+sprint -s-sneak
            if (self.sprinting or inpt.sprint) and inpt.w and not inpt.s and not inpt.sneak and not self.stop_sprint:
                movement = float32(movement * (float64(1.0) + float32(0.3)))
                if inpt.jump:
                    # pi / 180
                    facing_rad = float32(self.facing * float32(0.017453292))
                    self.vx -= self.mcsin(facing_rad) * float32(0.2)
                    self.vz += self.mccos(facing_rad) * float32(0.2)
            drag = float32(0.91) * float32(0.6)
            movement *= float32(0.16277136) / (drag * drag * drag)
            
        forward = float32(0.0)
        strafe = float32(0.0)
        if inpt.w and not inpt.s:
            forward = float32(1.0)
        elif inpt.s and not inpt.w:
            forward = float32(-1.0)
        if inpt.a and not inpt.d:
            strafe = float32(1.0)
        elif inpt.d and not inpt.a:
            strafe = float32(-1.0)

        if inpt.sneak:
            forward = float32(float64(forward) * float64(0.3))
            strafe = float32(float64(strafe) * float64(0.3))

        forward *= float32(0.98)
        strafe *= float32(0.98)
        distance = float32(strafe * strafe + forward * forward)
        
        # shitty mojang code
        if distance >= float32(0.0001):
            distance = float32(math.sqrt(float64(distance)))
            if distance < 1.0:
                distance = float32(1.0)

            distance = movement / distance
            forward = forward * distance
            strafe = strafe * distance

            sin_yaw = float32(self.mcsin(self.facing * float32(Player.PI) / float32(180.0)))
            cos_yaw = float32(self.mccos(self.facing * float32(Player.PI) / float32(180.0)))
            self.vx += float64(strafe * cos_yaw - forward * sin_yaw)
            self.vz += float64(forward * cos_yaw + strafe * sin_yaw)

        # x blockage (untested)
        collided = False
        if self.vx <= 0:
            b1 = course.blocks.get((floor(self.x + self.vx - Player.WIDTH), floor(self.y), floor(self.z - Player.WIDTH)), Block.oob())
            b2 = course.blocks.get((floor(self.x + self.vx - Player.WIDTH), floor(self.y) + 1, floor(self.z - Player.WIDTH)), Block.oob())
            b3 = course.blocks.get((floor(self.x + self.vx - Player.WIDTH), floor(self.y + Player.HEIGHT), floor(self.z - Player.WIDTH)), Block.oob())
            b4 = course.blocks.get((floor(self.x + self.vx - Player.WIDTH), floor(self.y), floor(self.z + Player.WIDTH)), Block.oob())
            b5 = course.blocks.get((floor(self.x + self.vx - Player.WIDTH), floor(self.y) + 1, floor(self.z + Player.WIDTH)), Block.oob())
            b6 = course.blocks.get((floor(self.x + self.vx - Player.WIDTH), floor(self.y + Player.HEIGHT), floor(self.z + Player.WIDTH)), Block.oob())
            x_max = max(b1.x_max, b2.x_max, b3.x_max, b4.x_max, b5.x_max, b6.x_max)
            if x_max > -30000001.0 and self.vx < x_max + Player.WIDTH - self.x:
                collided = True
                self.vx = self.x
                self.x = x_max + Player.WIDTH
                self.vx = self.x - self.vx
            else:
                self.x += self.vx
        else:
            b1 = course.blocks.get((floor(self.x + self.vx + Player.WIDTH), floor(self.y), floor(self.z - Player.WIDTH)), Block.oob())
            b2 = course.blocks.get((floor(self.x + self.vx + Player.WIDTH), floor(self.y) + 1, floor(self.z - Player.WIDTH)), Block.oob())
            b3 = course.blocks.get((floor(self.x + self.vx + Player.WIDTH), floor(self.y + Player.HEIGHT), floor(self.z - Player.WIDTH)), Block.oob())
            b4 = course.blocks.get((floor(self.x + self.vx + Player.WIDTH), floor(self.y), floor(self.z + Player.WIDTH)), Block.oob())
            b5 = course.blocks.get((floor(self.x + self.vx + Player.WIDTH), floor(self.y) + 1, floor(self.z + Player.WIDTH)), Block.oob())
            b6 = course.blocks.get((floor(self.x + self.vx + Player.WIDTH), floor(self.y + Player.HEIGHT), floor(self.z + Player.WIDTH)), Block.oob())
            x_min = min(b1.x_min, b2.x_min, b3.x_min, b4.x_min, b5.x_min, b6.x_min)
            if x_min < 30000001.0 and self.vx > x_min - Player.WIDTH - self.x:
                collided = True
                self.vx = self.x
                self.x = x_min - Player.WIDTH
                self.vx = self.x - self.vx
            else:
                self.x += self.vx

        # z blockage (untested)
        if self.vz <= 0:
            b1 = course.blocks.get((floor(self.x - Player.WIDTH), floor(self.y), floor(self.z + self.vz - Player.WIDTH)), Block.oob())
            b2 = course.blocks.get((floor(self.x - Player.WIDTH), floor(self.y) + 1, floor(self.z + self.vz - Player.WIDTH)), Block.oob())
            b3 = course.blocks.get((floor(self.x - Player.WIDTH), floor(self.y + Player.HEIGHT), floor(self.z + self.vz - Player.WIDTH)), Block.oob())
            b4 = course.blocks.get((floor(self.x + Player.WIDTH), floor(self.y), floor(self.z + self.vz - Player.WIDTH)), Block.oob())
            b5 = course.blocks.get((floor(self.x + Player.WIDTH), floor(self.y) + 1, floor(self.z + self.vz - Player.WIDTH)), Block.oob())
            b6 = course.blocks.get((floor(self.x + Player.WIDTH), floor(self.y + Player.HEIGHT), floor(self.z + self.vz - Player.WIDTH)), Block.oob())
            z_max = max(b1.z_max, b2.z_max, b3.z_max, b4.z_max, b5.z_max, b6.z_max)
            if z_max > -30000001.0 and self.vz < z_max + Player.WIDTH - self.z:
                collided = True
                self.vz = self.z
                self.z = z_max + Player.WIDTH
                self.vz = self.z - self.vz
            else:
                self.z += self.vz
        else:
            b1 = course.blocks.get((floor(self.x - Player.WIDTH), floor(self.y), floor(self.z + self.vz + Player.WIDTH)), Block.oob())
            b2 = course.blocks.get((floor(self.x - Player.WIDTH), floor(self.y) + 1, floor(self.z + self.vz + Player.WIDTH)), Block.oob())
            b3 = course.blocks.get((floor(self.x - Player.WIDTH), floor(self.y + Player.HEIGHT), floor(self.z + self.vz + Player.WIDTH)), Block.oob())
            b4 = course.blocks.get((floor(self.x + Player.WIDTH), floor(self.y), floor(self.z + self.vz + Player.WIDTH)), Block.oob())
            b5 = course.blocks.get((floor(self.x + Player.WIDTH), floor(self.y) + 1, floor(self.z + self.vz + Player.WIDTH)), Block.oob())
            b6 = course.blocks.get((floor(self.x + Player.WIDTH), floor(self.y + Player.HEIGHT), floor(self.z + self.vz + Player.WIDTH)), Block.oob())
            z_min = min(b1.z_min, b2.z_min, b3.z_min, b4.z_min, b5.z_min, b6.z_min)
            if z_min < 30000001.0 and self.vz > z_min - Player.WIDTH - self.z:
                collided = True
                self.vz = self.z
                self.z = z_min - Player.WIDTH
                self.vz = self.z - self.vz
            else:
                self.z += self.vz

        # cleanup
        if self.airborne:
            self.slip = 1.0
        else:
            self.slip = self.ground_slip
        self.airborne = next_airborne
        # +w+sprint -s
        if inpt.sprint and inpt.w and not inpt.s:
            self.sprinting = True
        if self.stop_sprint:
            self.sprinting = False
        if inpt.sprint and inpt.w and not inpt.s:
            self.stop_sprint = False
        if inpt.sneak or collided:
            self.stop_sprint = True
