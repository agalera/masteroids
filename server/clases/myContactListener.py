from __future__ import division
from Box2D import *
import math
class myContactListener(b2ContactListener):
    def __init__(self, borrar):
        super(myContactListener, self).__init__()
        self.borrar = borrar

    def BeginContact(self, var):
        pass
    def EndContact(self, var):
        pass

    def PostSolve(self, var, var2):

        if var.fixtureA.body.bullet == True:
            print "remove A"
            self.borrar.append(var.fixtureA.body)
        else:
            var.fixtureA.body.userData.recv_damage(var2.normalImpulses[0])
        if var.fixtureB.body.bullet == True:
            print "remove B"
            self.borrar.append(var.fixtureB.body)
        else:
            var.fixtureB.body.userData.recv_damage(var2.normalImpulses[0]*2)



        #if var.fixtureB.body.bullet == True:
        #    if (var.fixtureA.body.userData != None):
        #        var.fixtureA.body.userData.add_damage(var2.normalImpulses[0] / 2)
        #    if var.fixtureB.body not in self.borrar:
        #        self.borrar.append(var.fixtureB.body)
        #if var.fixtureA.body.bullet == True:
        #    if (var.fixtureB.body.userData != None):
        #        var.fixtureB.body.userData.add_damage(var2.normalImpulses[0] / 2)
        #    if var.fixtureA.body not in self.borrar:
        #        self.borrar.append(var.fixtureA.body)

        #var.fixtureA.body #golpea
        #var.fixtureB.body #recibe

    def Add(self, point):
        """Called when a contact point is created"""
        print "Add:", point
    def Persist(self, point):
        """Called when a contact point persists for more than a time step"""
        print "Persist:", point
    def Remove(self, point):
        """Called when a contact point is removed"""
        print "Remove:",point