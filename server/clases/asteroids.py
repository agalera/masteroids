from __future__ import division
import math
from random import randint

size_tile = 0.16
class asteroids:
    def __init__ (self,world, pos, borrar_asteroids):
        self.world = world
        self.fixture = self.generate_asteroids(pos)
        self.body = self.fixture.body
        self.body.userData = self
        self.damage = 0.0
        self.body.ApplyTorque(randint(-100,100),1)
        self.borrar_asteroids = borrar_asteroids
        self.hp = 10.0
    def generate_asteroids(self, pos):
        tmp = self.world.CreateDynamicBody(position=(pos),bullet=False,angularDamping=0.01, linearDamping= 0.01, angle= 0,linearVelocity=(randint(-10000,10000)/2000,randint(-10000,10000)/2000))
        return tmp.CreateCircleFixture(radius=(size_tile/1.0),density=5, friction= 0)
    def get_body(self):
        return self.body
    def get_awake(self):
        return self.body.awake
    def touch(self, touch):
        pass
    def recv_damage(self, fl):
        self.hp -= fl
        if self.hp < 0:
            self.borrar_asteroids.append(self.body)

    def get_position(self):
        return self.body.position, self.body.angle
    def get_worldcenter(self):
        return self.body.worldCenter
    def get_type(self):
        return "asteroids"