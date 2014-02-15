# -*- coding: utf-8 -*-
#By Alberto Galera
from __future__ import division
import codecs
import json
import copy
import hashlib
import time
import datetime
import socket
from struct import pack, unpack
from threading import Thread
from Box2D import *
import math
from random import randint
import sys
from clases.chunk import chunk
from clases.disparos import disparos
from clases.asteroids import asteroids
from clases.myContactListener import myContactListener
from clases.myDestructionListener import myDestructionListener

#import os
import os.path
#################################### Functions network ####################################
def recvpackage(socket_cliente,size_package):
    package = socket_cliente.recv(int(size_package))
    if (len(package) != size_package):
        print "fragment buffer"
        Esperando = True
        while Esperando:
            if (len(package) != size_package):
                package = package + socket_cliente.recv(size_package - len(package))
                if (package == ""):
                    print "conexion broken"
                    break
            else:
                Esperando = False
    return package

def getDelta():
    global lastFrame
    #time = 7.000.000
    time = getTime()
    delta = float(time - lastFrame)
    lastFrame = time
    return delta

def getTime():
    return (time.time() * 1000)

def updateFPS():
    global fps
    global last_time
    fps += 1
    if time.time() - last_time >= 1:
        current_fps = fps / (time.time() - last_time)
        print current_fps, 'fps'
        fps = 0
        last_time = time.time()
        #print last_time
class updateLobby(Thread):
    def __init__(self, clientes, port):
        Thread.__init__(self)
        self.clientes = clientes
        self.port = port
        self.register()

    def connect(self):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.connect(("127.0.0.1", int(8004)))
    def run(self):
        while True:
            time.sleep(60)
            self.connect()
            self.s.send(pack('iiiiii', 2, self.unique_id, self.port, len(self.clientes), 0, self.id_random))
    def register(self):
        self.id_random = randint(-sys.maxint,sys.maxint)
        self.connect()
        self.s.send(pack('ii32siiii', 0, self.port, "Pepito server", len(self.clientes), 32, 0,self.id_random))
        self.unique_id = unpack('i', self.s.recv(4))[0]

class mainProcess(Thread):
    def __init__(self, clientes, bullet, borrar_bullet ,borrar_asteroids, asteroids_dic):
        Thread.__init__(self)
        self.clientes = clientes
        self.bullet = bullet
        self.borrar_bullet = borrar_bullet
        self.borrar_asteroids = borrar_asteroids
        self.asteroids_dic = asteroids_dic

    def run(self):
        global t_delta
        global timeStep
        while True:
            #recorre la lista de clientes

            if len(self.clientes) == 0:
                updateFPS()
                t_delta = getDelta()
                timeSleep = 0.02 - (t_delta / 1000.0 )
                if timeSleep > 0.0:
                    time.sleep(timeSleep)
            else:
                updateFPS()
                t_delta = getDelta()
                timeStep = t_delta*0.0004
                #borrar_bullet bullet colisionados
                if (len(self.borrar_bullet) != 0):
                    for taa in list(set(self.borrar_bullet)):
                        self.bullet.remove(taa.userData)
                        world.DestroyBody(taa)
                        self.borrar_bullet.remove(taa)
                        print "remove time"
                if (len(self.borrar_bullet) != 0):
                    print "duplicate items"
                    for taa in self.borrar_bullet:
                        self.borrar_bullet.remove(taa)

                #borrar_bullet bullet colisionados
                if (len(self.borrar_asteroids) != 0):
                    for taa in list(set(self.borrar_asteroids)):
                        self.asteroids_dic.pop(taa.userData.get_id(), None)
                        world.DestroyBody(taa)
                        self.borrar_asteroids.remove(taa)
                        print "remove time2"
                if (len(self.borrar_asteroids) != 0):
                    print "duplicate items2"
                    for taa in self.borrar_asteroids:
                        self.borrar_asteroids.remove(taa)


                #clear bullet much range
                for taa in self.bullet:
                    actual_pos = taa.get_position()
                    init_pos = taa.get_init_post()
                    #print math.hypot(init_pos[0][0] - actual_pos[0][0], init_pos[0][1] - actual_pos[0][1])
                    if(math.hypot(init_pos[0] - actual_pos[0][0], init_pos[1] - actual_pos[0][1])>50):
                        world.DestroyBody(taa.get_body())
                        self.bullet.remove(taa)
                for taa in self.clientes:
                    taa.move(t_delta)
                    #mueve las mierdas
                #calcula las mierdas
                world.Step(timeStep, vel_iters, pos_iters)
                world.ClearForces()
                #crea un paquete
                package = pack('i', int(len(self.clientes)+len(self.bullet)+len(self.asteroids_dic)))
                for taa in self.clientes:
                    try:
                        tmp = taa.get_position()
                        package += pack('iifff',tmp[0],0,tmp[1],tmp[2], tmp[3] )
                    except:
                        pass
                for taa in self.bullet:
                    pos_tmp, angle_tmp = taa.get_position()
                    package += pack('iifff',-1,-1,pos_tmp[0],pos_tmp[1], angle_tmp)

                for key in self.asteroids_dic.keys():
                    pos_tmp, angle_tmp = self.asteroids_dic[key].get_position()
                    package += pack('iifff',key,-2,pos_tmp[0],pos_tmp[1],0)

                #envia las mierdas
                for taa in self.clientes:
                    try:
                        taa.send_package(package)
                        taa.recv_package()
                    except:
                        print "remove 2"
                        taa.remove()
                        self.clientes.remove(taa)

                timeSleep = 0.01 - (t_delta / 1000.0 )
                if timeSleep > 0.0:
                    time.sleep(timeSleep)

class Cliente(Thread):
    def __init__(self, socket_cliente, datos_cliente, world, bullet):
        Thread.__init__(self)
        self.bullet = bullet
        self.world = world
        self.player = self.set_box2d()
        self.player.body.userData = self
        self.massData_default = self.player.body.massData
        #self.massData_default = b2MassData()
        #self.player.body.GetMassData(self.massData_default)
        self.socket = socket_cliente
        self.datos = datos_cliente
        #send id
        self.socket.send(pack("i", self.datos[1]))
        self.status = True
        self.Vactual_info = [False, False, False, False, False]
        self.block_fire = 0

        #Temporal hasta que tenga db
        self.hp = 100.0
        self.energy = 100.0
        self.change_hp = True
        self.change_energy = True
        self.buffer_message = ""
        self.fail_send = 0

    def recv_package(self):
        try:
            result = self.socket.recv(5)
            if result != "":
                try:
                    self.Vactual_info = unpack("?????",result)
                except:
                    pass
            else:
                print "top else"
                raise "a tomar por culo"

        except:
            pass


    def send_package(self, package):
        tmp = 0
        pack_tmp = ""
        if self.change_hp:
            tmp -= 1
            pack_tmp += pack('f', float(self.hp))
            self.change_hp = False
        if self.change_energy:
            tmp -= 2
            pack_tmp += pack('f', float(self.energy))
            self.change_energy = False
        if tmp != 0:
            pack_tmp = pack('i', tmp) + pack_tmp
            package += pack_tmp

        if (self.buffer_message != ""):
            package = self.buffer_message
        try:
            package = package[self.socket.send(package):]
            self.buffer_message = ""
            self.fail_send = 0
        except:
            self.buffer_message = package
            self.fail_send += 1
            if (self.fail_send > 600):
                raise "crash client"
            pass
        #self.socket.send(package)

    def recv_damage(self,dmg):
        self.hp -= dmg
        self.change_hp = True
        if self.hp < 0:
            return True
        else:
            return False

    def use_energy(self,value):
        if (self.energy > value):
            self.energy -= value
            self.change_energy = True
            return True
        else:
            return False

    def set_box2d(self):
        tmp = self.world.CreateDynamicBody(position=(0,0),angularDamping=30.0, linearDamping= 1.0, angle= 0)
        #return tmp.CreatePolygonFixture(box=(0.16*0.94,0.16*0.94),density=1, friction= 6)
        return tmp.CreatePolygonFixture(vertices=[(-0.08*2,-0.08*2),(0.0,0.08*2),(0.08*2,-0.08*2)],density=1, friction= 6)

    def get_position(self):
        return [self.datos[1], self.player.body.position[0],self.player.body.position[1],self.player.body.angle]

    def move(self, t_delta):

        #algunas funciones de movimiento no tienen en cuenta el delta, dejalo asi y luego lo arreglamos mas adelante
        if (self.block_fire >= 0):
            self.block_fire -= t_delta
        if (self.energy < 100):
            self.use_energy(-t_delta*0.01)
        if(self.Vactual_info[0] == True):
            if self.use_energy(0.2):
                massData_tmp = b2MassData()
                massData_tmp.I = self.massData_default.I * 1.5 #multiply per charge
                massData_tmp.center = self.massData_default.center
                massData_tmp.mass = self.massData_default.mass * 1.5 #multiply per charge
                self.player.body.massData = massData_tmp

                #self.player.body.ApplyLinearImpulse(b2Vec2(0.0,0.0015*t_delta), b2Vec2(self.player.body.position[0],2+self.player.body.position[1]),1)
                position_info = [0,0]
                position_info[0] -= (0.3 * math.sin(self.player.body.angle))*16
                position_info[1] += (0.3 * math.cos(self.player.body.angle))*16
                self.player.body.ApplyForce(b2Vec2(position_info), b2Vec2(self.player.body.position),1)
        if(self.Vactual_info[2] == True):
            if self.use_energy(0.1):
                #self.player.body.ApplyLinearImpulse(b2Vec2(-0.0015*t_delta,0.0000000), b2Vec2(2+self.player.body.position[0],self.player.body.position[1]),1)
                position_info = [0,0]
                position_info[0] += (0.1 * math.sin(self.player.body.angle))*16
                position_info[1] -= (0.1 * math.cos(self.player.body.angle))*16
                self.player.body.ApplyForce(b2Vec2(position_info), b2Vec2(self.player.body.position),1)
        if(self.Vactual_info[1] == True):
            #self.player.body.ApplyLinearImpulse(b2Vec2(0.0,-0.0015*t_delta), b2Vec2(self.player.body.position[0],2+self.player.body.position[1]),1)
            self.player.body.ApplyTorque(0.3,1)
        if(self.Vactual_info[3] == True):
            #self.player.body.ApplyLinearImpulse(b2Vec2(0.0015*t_delta,0.0000000), b2Vec2(2+self.player.body.position[0],self.player.body.position[1]),1)
            self.player.body.ApplyTorque(-0.3,1)
        if(self.Vactual_info[4] == True and self.block_fire <= 0):
            if self.use_energy(10):
                self.block_fire = 20
                position_info = copy.copy(self.player.body.linearVelocity)
                position_info[0] -= 80*math.sin(self.player.body.angle)
                position_info[1] += 80*math.cos(self.player.body.angle)
                print "creando bala"
                self.bullet.append(disparos(self.player.body.position, self.world.CreateDynamicBody(
                    position=(self.player.body.position[0]-(math.sin(self.player.body.angle)*0.8),self.player.body.position[1]+(math.cos(self.player.body.angle)*0.8)),
                    bullet=True,angle = self.player.body.angle,  angularDamping=5.0, linearDamping= 0.0,
                    fixtures=b2FixtureDef(shape=b2CircleShape(radius=(0.16/1.4)), density=50.0),
                    linearVelocity=(position_info))))

    def remove(self):
        self.world.DestroyBody(self.player.body)
        #return self.status

#################################### Init code ####################################
if __name__ == '__main__':
    last_time = time.time()
    t_delta = 0
    fps = 0
    lastFPS = 0
    animate = 0.0
    lastFrame = time.time()
    timeStep = 1.0 / 160
    vel_iters, pos_iters = 6, 2
    borrar_bullet = []
    borrar_asteroids = []
    updateFPS()
    t_delta = getDelta()
    bullet = []
    asteroids_dic = dict()
    myListener = myContactListener(borrar_bullet)
    myDestructor = myDestructionListener()
    world=b2World(gravity=(0,0),contactListener=myListener, destructorListener=myDestructor)
    mapa = chunk(0,0,world)
    #generate asteroids
    for ids in range(10):
        asteroids_dic[ids] = asteroids(world, [randint(-10000,10000)/100,randint(-10000,10000)/100], borrar_asteroids, ids)

    # Se prepara el servidor
    #server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server = socket.socket(socket.SOCK_DGRAM)
    global clientes
    clientes = []
    maestro = mainProcess(clientes, bullet, borrar_bullet, borrar_asteroids,  asteroids_dic)
    maestro.start()
    thread_updateLobby = updateLobby(clientes, 8003)
    thread_updateLobby.start()
    server.bind(("", 8003))
    server.listen(5)
    print "Wait clients..."
    while 1:
        # Se espera a un cliente
        socket_cliente, datos_cliente = server.accept()
        socket_cliente.setblocking(0)
        # Se escribe su informacion
        print "conectado "+str(datos_cliente)
        print datos_cliente

        # Se crea la clase con el hilo y se arranca.
        package = recvpackage(socket_cliente,4)
        package = unpack('i', package)
        if(package[0] == 1):
            clientes.append(Cliente(socket_cliente, datos_cliente, world, bullet))
        #elif(package[0] == 0):
        #   servers.append([socket_cliente,datos_cliente,'file_return',0,'hilo','frame'])
        #   print "server anadido a la lista"
        elif(package[0] == 9):
            print "test mode"
            #recvfile(socket_cliente,datos_cliente,'/tmp/test.tar.gz')
