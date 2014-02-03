from __future__ import division

import math
import copy
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
#import clases.audio

size_tile = 0.16

class player:
    def __init__ (self, global_DL):
        self.position = [0.0, 0.0, 0.0]
        self.global_DL = global_DL
        self.shield = 100.0
        self.hp = 100.0
        self.energy = 100.0
        self.change_shield = True
        self.change_hp = True
        self.change_energy = True
    def set_shield(self, val):
        self.change_shield = True
        self.shield = val

    def set_hp(self, val):
        self.change_hp = True
        self.hp = val

    def set_energy(self, val):
        self.change_energy = True
        self.energy = val

    def get_shield(self):
        if self.change_shield == True:
            self.change_shield = False
            return self.shield
        return False

    def get_hp(self):
        if self.change_hp == True:
            self.change_hp = False
            return self.hp
        return False

    def get_energy(self):
        if self.change_energy == True:
            self.change_energy = False
            return self.energy
        return False

    def distance(self, p0, p1):
        return math.hypot(p1[0] - p0[0], p1[1] - p0[1])

    def get_position(self):
        return self.position

    def set_position(self, new_position):
        self.position = new_position[2:5]