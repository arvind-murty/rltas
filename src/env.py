import numpy as np
import numpy.linalg as la
import gymnasium as gym
from gymnasium import spaces
import math
from math import floor
from src.course import Block, Course
from numpy import float32, float64, int32, uint64

class CourseEnv(gym.Env):
    PI = 3.14159265358979323846
    WIDTH = 0.30000001192092896
    HEIGHT = 1.7999999523162841796875


    def __init__(self):
        super().__init__()
        self.action_space = spaces.Discrete(2)
        # x, y, z, vx, vy, vz, facing, airborne
        self.observation_space = spaces.Box(
            low=np.array([-np.inf]*7 + [-180, 0]),
            high=np.array([np.inf]*7 + [180, 1]),
            dtype=float32
        )
        self.reset()
    
    def _get_obs(self):
        return np.array([self.x, self.y, self.z, self.vx, self.vy, self.vz, float32(self.ticks), self.facing, float32(self.airborne)], dtype=float32)
    
    def _dist_from_goal(self):
        return max(0.0, 8.7 - self.z)

    def reset(self, seed=None, options=None):
        super().reset(seed=seed)

        self.course = Course([Block.block(0, 63, 0), Block.block(0, 63, 4), Block.block(0, 63, 9)])
        # floats
        self.x = float32(0.5)
        self.y = float32(64.0)
        self.z = float32(-0.3)
        self.vx = float32(0.0)
        self.vy = float32(0.0)
        self.vz = float32(0.0)
        self.ground_slip = float32(0.6)
        self.slip = self.ground_slip
        self.facing = float32(0.0)
        self.inertia = float32(0.005)
        self.ticks = 0
        
        # bools
        self.airborne = False
        self.sprinting = False
        self.stop_sprint = False

        return self._get_obs(), {}
    
    def _mcsin(self, rad):
        index = int(rad * float32(10430.378)) & 65535
        return float32(math.sin(index * CourseEnv.PI * 2.0 / 65536))

    def _mccos(self, rad):
        index = int(rad * float32(10430.378) + float32(16384.0)) & 65535
        return float32(math.sin(index * CourseEnv.PI * 2.0 / 65536))


    def step(self, action):
        jump = action
        rotation = float32(0.0)
        self.ticks += 1

        # y velocity
        if self.airborne:
            self.vy = (self.vy - 0.08) * 0.9800000190734863
            if abs(self.vy) < self.inertia:
                self.vy = 0.0
        elif jump:
            self.vy = float64(float32(0.42))
        else:
            self.vy = (0.0 - 0.08) * 0.9800000190734863

        # check y blockages
        next_airborne = True
        if self.vy <= 0.0:
            b1 = self.course.blocks.get((floor(self.x - CourseEnv.WIDTH), floor(self.y + self.vy), floor(self.z - CourseEnv.WIDTH)), Block.oob())
            b2 = self.course.blocks.get((floor(self.x - CourseEnv.WIDTH), floor(self.y + self.vy), floor(self.z + CourseEnv.WIDTH)), Block.oob())
            b3 = self.course.blocks.get((floor(self.x + CourseEnv.WIDTH), floor(self.y + self.vy), floor(self.z - CourseEnv.WIDTH)), Block.oob())
            b4 = self.course.blocks.get((floor(self.x + CourseEnv.WIDTH), floor(self.y + self.vy), floor(self.z + CourseEnv.WIDTH)), Block.oob())
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
            b1 = self.course.blocks.get((floor(self.x - CourseEnv.WIDTH), floor(self.y + self.vy + CourseEnv.HEIGHT), floor(self.z - CourseEnv.WIDTH)), Block.oob())
            b2 = self.course.blocks.get((floor(self.x - CourseEnv.WIDTH), floor(self.y + self.vy + CourseEnv.HEIGHT), floor(self.z + CourseEnv.WIDTH)), Block.oob())
            b3 = self.course.blocks.get((floor(self.x + CourseEnv.WIDTH), floor(self.y + self.vy + CourseEnv.HEIGHT), floor(self.z - CourseEnv.WIDTH)), Block.oob())
            b4 = self.course.blocks.get((floor(self.x + CourseEnv.WIDTH), floor(self.y + self.vy + CourseEnv.HEIGHT), floor(self.z + CourseEnv.WIDTH)), Block.oob())
            y_min = min(b1.y_min, b2.y_min, b3.y_min, b4.y_min)
            if y_min < 257.0 and self.vy < y_min - self.y - CourseEnv.HEIGHT:
                # set vy to difference between current height and y_min (min height of block above) if player hits it
                self.vy = self.y
                self.y = y_min - CourseEnv.HEIGHT
                self.vy = self.y - self.vy
            else:
                self.y += self.vy
        
        self.facing += rotation
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
            if not self.stop_sprint:
                movement = float32(movement * (float64(1.0) + float32(0.3)))
                if jump:
                    # pi / 180
                    facing_rad = float32(self.facing * float32(0.017453292))
                    self.vx -= self._mcsin(facing_rad) * float32(0.2)
                    self.vz += self._mccos(facing_rad) * float32(0.2)
            drag = float32(0.91) * self.ground_slip
            movement *= float32(0.16277136) / (drag * drag * drag)
            
        forward = float32(0.98)
        distance = forward * forward
        
        # shitty mojang code
        if distance >= float32(0.0001):
            distance = math.sqrt(distance)
            if distance < 1.0:
                distance = float32(1.0)

            distance = movement / distance
            forward = forward * distance

            sin_yaw = float32(self._mcsin(self.facing * float32(CourseEnv.PI) / float32(180.0)))
            cos_yaw = float32(self._mccos(self.facing * float32(CourseEnv.PI) / float32(180.0)))
            self.vx += float64(-1 * forward * sin_yaw)
            self.vz += float64(forward * cos_yaw)

        # x blockage (untested)
        collided = False
        if self.vx <= 0:
            b1 = self.course.blocks.get((floor(self.x + self.vx - CourseEnv.WIDTH), floor(self.y), floor(self.z - CourseEnv.WIDTH)), Block.oob())
            b2 = self.course.blocks.get((floor(self.x + self.vx - CourseEnv.WIDTH), floor(self.y) + 1, floor(self.z - CourseEnv.WIDTH)), Block.oob())
            b3 = self.course.blocks.get((floor(self.x + self.vx - CourseEnv.WIDTH), floor(self.y + CourseEnv.HEIGHT), floor(self.z - CourseEnv.WIDTH)), Block.oob())
            b4 = self.course.blocks.get((floor(self.x + self.vx - CourseEnv.WIDTH), floor(self.y), floor(self.z + CourseEnv.WIDTH)), Block.oob())
            b5 = self.course.blocks.get((floor(self.x + self.vx - CourseEnv.WIDTH), floor(self.y) + 1, floor(self.z + CourseEnv.WIDTH)), Block.oob())
            b6 = self.course.blocks.get((floor(self.x + self.vx - CourseEnv.WIDTH), floor(self.y + CourseEnv.HEIGHT), floor(self.z + CourseEnv.WIDTH)), Block.oob())
            x_max = max(b1.x_max, b2.x_max, b3.x_max, b4.x_max, b5.x_max, b6.x_max)
            if x_max > -30000001.0 and self.vx < x_max + CourseEnv.WIDTH - self.x:
                collided = True
                self.vx = self.x
                self.x = x_max + CourseEnv.WIDTH
                self.vx = self.x - self.vx
            else:
                self.x += self.vx
        else:
            b1 = self.course.blocks.get((floor(self.x + self.vx + CourseEnv.WIDTH), floor(self.y), floor(self.z - CourseEnv.WIDTH)), Block.oob())
            b2 = self.course.blocks.get((floor(self.x + self.vx + CourseEnv.WIDTH), floor(self.y) + 1, floor(self.z - CourseEnv.WIDTH)), Block.oob())
            b3 = self.course.blocks.get((floor(self.x + self.vx + CourseEnv.WIDTH), floor(self.y + CourseEnv.HEIGHT), floor(self.z - CourseEnv.WIDTH)), Block.oob())
            b4 = self.course.blocks.get((floor(self.x + self.vx + CourseEnv.WIDTH), floor(self.y), floor(self.z + CourseEnv.WIDTH)), Block.oob())
            b5 = self.course.blocks.get((floor(self.x + self.vx + CourseEnv.WIDTH), floor(self.y) + 1, floor(self.z + CourseEnv.WIDTH)), Block.oob())
            b6 = self.course.blocks.get((floor(self.x + self.vx + CourseEnv.WIDTH), floor(self.y + CourseEnv.HEIGHT), floor(self.z + CourseEnv.WIDTH)), Block.oob())
            x_min = min(b1.x_min, b2.x_min, b3.x_min, b4.x_min, b5.x_min, b6.x_min)
            if x_min < 30000001.0 and self.vx > x_min - CourseEnv.WIDTH - self.x:
                collided = True
                self.vx = self.x
                self.x = x_min - CourseEnv.WIDTH
                self.vx = self.x - self.vx
            else:
                self.x += self.vx

        # z blockage (untested)
        if self.vz <= 0:
            b1 = self.course.blocks.get((floor(self.x - CourseEnv.WIDTH), floor(self.y), floor(self.z + self.vz - CourseEnv.WIDTH)), Block.oob())
            b2 = self.course.blocks.get((floor(self.x - CourseEnv.WIDTH), floor(self.y) + 1, floor(self.z + self.vz - CourseEnv.WIDTH)), Block.oob())
            b3 = self.course.blocks.get((floor(self.x - CourseEnv.WIDTH), floor(self.y + CourseEnv.HEIGHT), floor(self.z + self.vz - CourseEnv.WIDTH)), Block.oob())
            b4 = self.course.blocks.get((floor(self.x + CourseEnv.WIDTH), floor(self.y), floor(self.z + self.vz - CourseEnv.WIDTH)), Block.oob())
            b5 = self.course.blocks.get((floor(self.x + CourseEnv.WIDTH), floor(self.y) + 1, floor(self.z + self.vz - CourseEnv.WIDTH)), Block.oob())
            b6 = self.course.blocks.get((floor(self.x + CourseEnv.WIDTH), floor(self.y + CourseEnv.HEIGHT), floor(self.z + self.vz - CourseEnv.WIDTH)), Block.oob())
            z_max = max(b1.z_max, b2.z_max, b3.z_max, b4.z_max, b5.z_max, b6.z_max)
            if z_max > -30000001.0 and self.vz < z_max + CourseEnv.WIDTH - self.z:
                collided = True
                self.vz = self.z
                self.z = z_max + CourseEnv.WIDTH
                self.vz = self.z - self.vz
            else:
                self.z += self.vz
        else:
            b1 = self.course.blocks.get((floor(self.x - CourseEnv.WIDTH), floor(self.y), floor(self.z + self.vz + CourseEnv.WIDTH)), Block.oob())
            b2 = self.course.blocks.get((floor(self.x - CourseEnv.WIDTH), floor(self.y) + 1, floor(self.z + self.vz + CourseEnv.WIDTH)), Block.oob())
            b3 = self.course.blocks.get((floor(self.x - CourseEnv.WIDTH), floor(self.y + CourseEnv.HEIGHT), floor(self.z + self.vz + CourseEnv.WIDTH)), Block.oob())
            b4 = self.course.blocks.get((floor(self.x + CourseEnv.WIDTH), floor(self.y), floor(self.z + self.vz + CourseEnv.WIDTH)), Block.oob())
            b5 = self.course.blocks.get((floor(self.x + CourseEnv.WIDTH), floor(self.y) + 1, floor(self.z + self.vz + CourseEnv.WIDTH)), Block.oob())
            b6 = self.course.blocks.get((floor(self.x + CourseEnv.WIDTH), floor(self.y + CourseEnv.HEIGHT), floor(self.z + self.vz + CourseEnv.WIDTH)), Block.oob())
            z_min = min(b1.z_min, b2.z_min, b3.z_min, b4.z_min, b5.z_min, b6.z_min)
            if z_min < 30000001.0 and self.vz > z_min - CourseEnv.WIDTH - self.z:
                collided = True
                self.vz = self.z
                self.z = z_min - CourseEnv.WIDTH
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
        self.sprinting = True
        if self.stop_sprint:
            self.sprinting = False
        self.stop_sprint = False
        if collided:
            self.stop_sprint = True

        reward = 0
        if collided:
            reward -= 100.0

        mult = 0.01
        reward -= mult * self.ticks * self.ticks
        dist = self._dist_from_goal()
        terminated = False
        if dist <= 0.0:
            reward += 500.0
            terminated = True
        else:
            reward -= dist
        
        observation = self._get_obs()
        truncated = False
        if reward < -50.0 or self.y < 64.0:
            truncated = True
        info = {}
        return observation, reward, terminated, truncated, info
    def render(self):
        print(f"(x, y, z, vx, vy, vz, ticks, facing, airborne): ({self.x}, {self.y}, {self.z}, {self.vx}, {self.vy}, {self.vz}, {self.ticks}, {self.facing}, {self.airborne}")

    def close(self):
        pass
