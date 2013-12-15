# -*- coding: utf-8 -*-
#By Alberto Galera
from __future__ import division
import codecs
import json
import hashlib
import time
import datetime
import socket
import smtplib  #lib send mails
from struct import pack, unpack
from threading import Thread
from Box2D import *

from clases.myContactListener import myContactListener
from clases.myDestructionListener import myDestructionListener

#import os
import os.path
#################################### Functions network ####################################
def recvpackage(socket_cliente,size_package):
    package = socket_cliente.recv(int(size_package))
    if (len(package) != size_package):
        #fragment buffer
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
class mainProcess(Thread):
    def __init__(self, clientes):
        Thread.__init__(self)
        self.clientes = clientes

    def run(self):
        global t_delta
        global timeStep
        while True:
            #recorre la lista de clientes

            if len(self.clientes) == 0:
                updateFPS()
                t_delta = getDelta()
                timeSleep = 0.02 - (t_delta / 1000.0 )
                time.sleep(timeSleep)
            else:
                updateFPS()
                t_delta = getDelta()
                timeStep = t_delta*0.0004

                for taa in self.clientes:
                    try:
                        taa.move(t_delta)
                    except:
                        pass
                    #mueve las mierdas
                #calcula las mierdas
                world.Step(timeStep, vel_iters, pos_iters)
                world.ClearForces()
                #crea un paquete
                package = pack('i', int(len(self.clientes)))
                count = 0
                for taa in self.clientes:
                    try:
                        tmp = taa.get_position()
                        package += pack('ifff',tmp[0],tmp[1],tmp[2], tmp[3] )
                        count += 1
                    except:
                        pass
                #envia las mierdas
                for taa in self.clientes:
                    try:
                        taa.send_package(package)
                    except:
                        print "remove 2"
                        taa.remove()
                        self.clientes.remove(taa)
                timeSleep = 0.02 - (t_delta / 1000.0 )
                if timeSleep > 0.0:
                    time.sleep(timeSleep)
class Cliente(Thread):
    def __init__(self, socket_cliente, datos_cliente, world):
        Thread.__init__(self)
        self.world = world
        self.player = self.set_box2d()
        self.socket = socket_cliente
        self.datos = datos_cliente
        #send id
        self.socket.send(pack("i", self.datos[1]))
        self.status = True
        self.Vactual_info = [False, False, False, False, 0.0]

    def run(self):
        seguir = True
        while seguir:
            try:
                result = self.socket.recv(8)
                if result != "":
                    self.Vactual_info = unpack("????f",result)

            except:
                seguir = False
                print "leave client"
                break

    def set_box2d(self):
        tmp = self.world.CreateDynamicBody(position=(0,0),angularDamping=30.0, linearDamping= 10.0, angle= 0)
        return tmp.CreatePolygonFixture(box=(0.16*0.94,0.16*0.94),density=1, friction= 6)

    def get_position(self):
        return [self.datos[1], self.player.body.position[0],self.player.body.position[1],self.player.body.angle]
    def move(self, t_delta):
        if(self.Vactual_info[0] == True):
            self.player.body.ApplyLinearImpulse(b2Vec2(0.0,0.0015*t_delta), b2Vec2(self.player.body.position[0],2+self.player.body.position[1]),1)
        if(self.Vactual_info[1] == True):
            self.player.body.ApplyLinearImpulse(b2Vec2(-0.0015*t_delta,0.0000000), b2Vec2(2+self.player.body.position[0],self.player.body.position[1]),1)
        if(self.Vactual_info[2] == True):
            self.player.body.ApplyLinearImpulse(b2Vec2(0.0,-0.0015*t_delta), b2Vec2(self.player.body.position[0],2+self.player.body.position[1]),1)
        if(self.Vactual_info[3] == True):
            self.player.body.ApplyLinearImpulse(b2Vec2(0.0015*t_delta,0.0000000), b2Vec2(2+self.player.body.position[0],self.player.body.position[1]),1)
    def remove(self):
        return self.status

    def send_package(self, package):
        self.socket.send(package)

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
    borrar = []
    updateFPS()
    t_delta = getDelta()

    myListener = myContactListener(borrar)
    myDestructor = myDestructionListener()
    world=b2World(contactListener=myListener, destructorListener=myDestructor) # default gravity is (0,-10) and doSleep is True
    world.gravity = (0, 0)
    # Se prepara el servidor
    #server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server = socket.socket(socket.SOCK_DGRAM)
    global clientes
    clientes = []
    maestro = mainProcess(clientes)
    maestro.start()
    server.bind(("", 8002))
    server.listen(5)
    print "Wait clients..."
    while 1:
        # Se espera a un cliente
        socket_cliente, datos_cliente = server.accept()

        # Se escribe su informacion
        print "conectado "+str(datos_cliente)
        print datos_cliente

        # Se crea la clase con el hilo y se arranca.
        package = recvpackage(socket_cliente,4)
        package = unpack('i', package)
        if(package[0] == 1):
            hilo3 = Cliente(socket_cliente, datos_cliente, world)
            hilo3.start()
            clientes.append(hilo3)
        #elif(package[0] == 0):
        #   servers.append([socket_cliente,datos_cliente,'file_return',0,'hilo','frame'])
        #   print "server anadido a la lista"
        elif(package[0] == 9):
            print "test mode"
            #recvfile(socket_cliente,datos_cliente,'/tmp/test.tar.gz')