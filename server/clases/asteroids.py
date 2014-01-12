from __future__ import division
import math

size_tile = 0.16
class asteroids:
    def __init__ (self,world, pos):
        self.world = world
        self.fixture = self.generate_asteroids(pos)
        self.body = self.fixture.body
        self.body.userData = self
        self.damage = 0.0

    def generate_asteroids(self, pos):
        tmp = self.world.CreateDynamicBody(position=(pos),bullet=False,angularDamping=0.01, linearDamping= 0.01, angle= 0)
        return tmp.CreateCircleFixture(radius=(size_tile/1.2),density=100, friction= 0)
    def get_body(self):
        return self.body
    def get_awake(self):
        return self.body.awake
    def touch(self, touch):
        pass
    def recv_damage(self, fl):
        pass
    def get_position(self):
        return [self.body.position, self.body.angle]
    def get_worldcenter(self):
        return self.body.worldCenter
    def get_type(self):
        return "asteroids"