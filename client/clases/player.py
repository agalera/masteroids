from __future__ import division

import math
from Box2D import *
import copy
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import clases.audio

size_tile = 0.16

class player:
    def __init__ (self, global_DL):
        self.position = [0.0, 0.0, 0.0]
        self.global_DL = global_DL

    def add_damage(self, damage):
        self.damage -= damage
    def add_hp(self, hp):
        self.damage += hp
    def distance(self, p0, p1):
        return math.hypot(p1[0] - p0[0], p1[1] - p0[1])

    def get_position(self):
        return self.position

    def set_position(self, new_position):
        self.position = new_position[1:4]