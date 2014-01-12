from __future__ import division
import math

size_tile = 0.16
class disparos:
    def __init__ (self, init_pos, body):
        self.body = body
        self.init_pos = init_pos
        self.body.userData = self
        self.hp = 100.0
    def get_body(self):
        return self.body
    def recv_damage(self, fl):
        self.hp -= fl
        if self.hp < 0:
            return True
        else:
            return False
    def get_position(self):
        return [self.body.position, self.body.angle]
    def get_init_post(self):
        return self.init_pos
    def get_type(self):
        return "disparos"