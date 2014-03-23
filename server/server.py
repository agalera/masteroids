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
import random
from random import randint
import sys
from clases.chunk import chunk
from clases.disparos import disparos
from clases.asteroids import asteroids
from clases.myContactListener import myContactListener
from clases.myDestructionListener import myDestructionListener


from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
from clases.player import player
from PIL.Image import open as pil_open
import csv

import clases.basicas as basicas
from threading import Thread

#import os
import os.path
#################################### Functions network ####################################
def recvpackage(socket_cliente,size_package):
    package = ''
    while len(package) < size_package:
        chunk = socket_cliente.recv(size_package - len(package))
        if chunk == '':
            print 'Connection broken'  # raise ...
            break
        package += chunk
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
    def __init__(self, clientes, port, server_name):
        Thread.__init__(self)
        self.clientes = clientes
        self.port = port
        self.register(server_name)

    def connect(self):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.connect(("masteroids.no-ip.org", int(8004)))
    def run(self):
        while True:
            time.sleep(60)
            self.connect()
            self.s.send(pack('iiiiii', 2, self.unique_id, self.port, len(self.clientes), 0, self.id_random))
    def register(self, server_name):
        self.id_random = randint(-sys.maxint,sys.maxint)
        self.connect()
        self.s.send(pack('ii32siiii', 0, self.port, server_name, len(self.clientes), 10, 0,self.id_random))
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
        glutInit()
        glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB)
        glutInitWindowSize(resolution[0],resolution[1])
        glutCreateWindow("Masteroids")

        #glutSpecialFunc(ControlFlechas)

        #glutSpecialUpFunc(ControlFlechasUp)
        #glutTimerFunc(16,update, 1)

        glutDisplayFunc(self.game)
        glutIdleFunc(self.game)
        glutReshapeFunc(self.reshapeFun)
        glutMouseFunc(self.ControlRaton)
        glutPassiveMotionFunc(self.ControlRatonPos)
        glutMotionFunc(self.ControlRatonPos)
        self.initFun()
        glutMainLoop()

    def initFun(self):
        print "initFun"
        glEnable(GL_AUTO_NORMAL)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
        glEnable(GL_BLEND)
        glClearColor(0.0,0.0,0.0,0.0)
        #reshapeFun(resolution[0],resolution[1])
        ### load textures and initial chunk
        global textures
        global Lchunk
        global player
        global world

        global global_DL

        global_DL = glGenLists(256)

        print "aqui", global_DL
        for taa in range(256):
            glNewList(global_DL+taa, GL_COMPILE)
            basicas.draw_cube(0.16, taa)
            glEndList()

        textures.append(self.loadImage('assets/stGrid1.png'))
        textures.append(self.loadImage('assets/player.png'))
        textures.append(self.loadImage('assets/bullet.png'))
        textures.append(self.loadImage('assets/stGriddeco.png'))
        textures.append(self.loadImage('assets/icons.png'))
        textures.append(self.loadImage('assets/tren_1.png'))
        textures.append(self.loadImage('assets/inicio.png'))
        textures.append(self.loadImage('assets/gameover.png'))
        textures.append(self.loadImage('assets/frases1.png'))
        textures.append(self.loadImage('assets/stGrid2.png'))

        player = player(global_DL)


        self.enable_vsync()
        self.load_map()
    def game(self):
        global t_delta
        global timeStep

        #recorre la lista de clientes
        updateFPS()
        t_delta = getDelta()
        if len(self.clientes) == 0:
            timeSleep = 0.02 - (t_delta / 1000.0 )
            if timeSleep > 0.0:
                time.sleep(timeSleep)
        else:
            timeStep = t_delta*0.0004
            #borrar_bullet bullet colisionados
            if (len(self.borrar_bullet) != 0):
                for taa in self.borrar_bullet:
                    self.bullet.remove(taa.userData)
                    world.DestroyBody(taa)
                    self.borrar_bullet.remove(taa)
                    print "remove time"

            #borrar_bullet bullet colisionados
            if (len(self.borrar_asteroids) != 0):
                for taa in self.borrar_asteroids:
                    self.asteroids_dic.pop(taa.userData.get_id(), None)
                    world.DestroyBody(taa)
                    self.borrar_asteroids.remove(taa)
                    print "remove time2"

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


            #A PINTAR!
            #---- Init Experimental zone ----
            global animate
            animate +=float(t_delta)/60.0
            if animate > 16:
                animate = 0.0

            #---- End Experimental zone ----
            #Init Frame
            glClearColor(0.3,0.3,0.3,0.0)
            glClear(GL_COLOR_BUFFER_BIT)
            glLoadIdentity()

            player.set_position(self.clientes[0])

            self.create_camera(False)

            self.setupTexture(6)
            self.background()
            self.setupTexture(9)
            glCallList(chunkDisplayList)
            #draw time (optional)

            self.setupTexture(0)
            self.draw_naves()
            self.draw_bullet()

            #setupTexture(2)

            #GUI
            self.create_camera(True)
            #self.draw_fps()
            #FIN GUI

            #draw_select()
            #go to gpu
            glutSwapBuffers()
            #timeSleep = 0.03 - (t_delta / 1000.0 )
            #if timeSleep > 0.0:
            #    time.sleep(timeSleep)

            #crea un paquete
            #package = pack('i', int(len(self.clientes)+len(self.bullet)+len(self.asteroids_dic)))
            #for taa in self.clientes:
            #    try:
            #        tmp = taa.get_position()
            #        package += pack('iifff',tmp[0],0,tmp[1],tmp[2], tmp[3] )
            #    except:
            #        pass
            #for taa in self.bullet:
            #    pos_tmp, angle_tmp = taa.get_position()
            #    package += pack('iifff',-1,-1,pos_tmp[0],pos_tmp[1], angle_tmp)
#
            #for key in self.asteroids_dic.keys():
            #    pos_tmp, angle_tmp = self.asteroids_dic[key].get_position()
            #    package += pack('iifff',key,-2,pos_tmp[0],pos_tmp[1],0)
#
            ##envia las mierdas
            #for taa in self.clientes:
            #    try:
            #        taa.send_package(package)
            #        taa.recv_package()
            #    except:
            #        print "remove 2"
            #        taa.remove()
            #        self.clientes.remove(taa)
#
            #timeSleep = 0.01 - (t_delta / 1000.0 )
            #if timeSleep > 0.0:
            #    time.sleep(timeSleep)
    def draw_naves(self):
        for cliente in self.clientes:
            if cliente.get_borrame():
                cliente.remove()
                self.clientes.remove(cliente)
            else:
                self.draw_object(cliente.get_position(),0)

    def draw_bullet(self):
        for bullet in self.bullet:
            tmp = bullet.get_position()
            self.draw_object([6, tmp[0][0], tmp[0][1], tmp[1]], 6)

    def draw_object(self,position, value): #value is a temp
        size_tile = 0.32
        glTranslatef( position[1] , position[2], 0.0)
        glRotate(math.degrees(position[3]), 0, 0, 1)
        glCallList(global_DL+abs(value))

        glRotate(math.degrees(position[3]), 0, 0, -1)
        glTranslatef( -position[1] , -position[2], -0.0)

    def background(self):
        texture_info_temp = 2
        textureXOffset = 1
        textureYOffset = 1
        textureHeight  = 1
        textureWidth   = 1

        #glTranslatef( self.body.position[0] , self.body.position[1], 0.00)
        glRotate(0, 0, 0, 1)
        glBegin(GL_QUADS)
        glTexCoord2f(textureXOffset, textureYOffset - textureHeight)

        glVertex3f(-100, -100, 0)

        glTexCoord2f(textureXOffset + textureWidth, textureYOffset - textureHeight)
        glVertex3f(100, -100, 0)

        glTexCoord2f(textureXOffset + textureWidth, textureYOffset)
        glVertex3f( 100,  100, 0)

        glTexCoord2f(textureXOffset,textureYOffset)
        glVertex3f(-100, 100, 0)
        glEnd()
        glRotate(0, 0, 0, -1)

    def setupTexture(self,imageID):
        glEnable(GL_TEXTURE_2D)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
        #glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
        #glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
        glBindTexture(GL_TEXTURE_2D, textures[imageID])
        #texCoordsFrame1 = [0.32]
        #glTexCoordPointer(2, GL_FLOAT, 0, textures[imageID])
        #glTexCoordPointer(2, GL_FLOAT, 1000, 1000)

    def enable_vsync(self):
        pass
        #glEnable(GL_VSYNC)
            # set v to 1 to enable vsync, 0 to disable vsync

    def loadImage(self,imageName):
        im = pil_open(imageName)
        try:
            ix, iy, image = im.size[0], im.size[1], im.tostring("raw", "RGBA", 0, -1)
        except SystemError:
            ix, iy, image = im.size[0], im.size[1], im.tostring("raw", "RGBX", 0, -1)
        ID = glGenTextures(1)
        glBindTexture(GL_TEXTURE_2D, ID)
        glPixelStorei(GL_UNPACK_ALIGNMENT,4)
        glTexImage2D(
            GL_TEXTURE_2D, 0, GL_RGBA, ix, iy, 0, GL_RGBA, GL_UNSIGNED_BYTE, image
        )
        return ID

    def create_camera(self,zoom_lock):
        glLoadIdentity()
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        if(zoom_lock):
            zoom_tmp = 3.0
        else:
            zoom_tmp = zoom
        if (aspect >= 1.0):
            glOrtho(-zoom_tmp * aspect, zoom_tmp * aspect, -zoom_tmp, zoom_tmp, -zoom_tmp, zoom_tmp)
        else:
            print "wtf"
            glOrtho(-zoom_tmp, zoom_tmp, -zoom_tmp / aspect, zoom_tmp / aspect, -zoom_tmp, zoom_tmp)
        glMatrixMode(GL_MODELVIEW)
        if (zoom_lock == False):
            glRotate(0, 0, 0, 0)
            glRotate(0, 1, 0, 0)
            glRotate(0, 0, 0, 1)
            camera = player.get_position()
            glTranslate( -camera[0] , -camera[1], 0)

    def ControlRatonPos(self,x,y):
        global radians
        radians = (math.atan2(-((resolution[1]/2)-y), (resolution[0]/2)-x)+ 3.14159266)

    def ControlRaton(self,key,leave,x,y):
        global wasd
        global zoom
        if key <= 2 :
            self.ControlRatonPos(x,y)
            wasd[5][key] = not leave
        if (key == 3):
            zoom -= 0.32
            reshapeFun(resolution[0], resolution[1])
        if (key == 4):
            zoom += 0.32
            reshapeFun(resolution[0], resolution[1])

    def object_select(self):
        v_object_select[0] = int((player.get_position()[0][0]+0.16) * 3.125)
        v_object_select[1] = int((player.get_position()[0][1]+0.16) * 3.125)
    def reshapeFun(self,wi,he):
        global resolution
        resolution = [wi,he]
        global aspect
        aspect = 1.9
        aspect = resolution[0] / resolution[1]
        glViewport(0, 0, wi, he)
        print "inv: " + str(aspect)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        if (aspect >= 1.0):
            print wi, he
            glOrtho(-zoom * aspect, zoom * aspect, -zoom, zoom, -zoom, zoom)
        else:
            print "wtf"
            glOrtho(-zoom, zoom, -zoom / aspect, zoom / aspect, -zoom, zoom)
        glMatrixMode(GL_MODELVIEW)
        print zoom
        #glMatrixMode(GL_MODELVIEW);

        #if w>h:
        #    glViewport((w-h)/2,0,h,h)
        #else:
        #    glViewport(0,(h-w)/2,w,w)

    def create_tile(self, bx,by,tile):
        size_tile = 0.64
        print "create_tile"
        bx = bx * size_tile
        by = by * size_tile

        texture_info_temp = [int(tile), 0];
        textureXOffset = float(texture_info_temp[0]/16.0)+0.001
        textureYOffset = float(16 - int(texture_info_temp[0]/16)/16.0)-0.001
        textureHeight  = float(0.060)
        textureWidth   = float(0.060)

        glBegin(GL_QUADS)
        glTexCoord2f(textureXOffset, textureYOffset - textureHeight)
        glVertex3f(bx-(size_tile/2), by-(size_tile/2), 0)

        glTexCoord2f(textureXOffset + textureWidth, textureYOffset - textureHeight)
        glVertex3f(bx + (size_tile/2), by-(size_tile/2), 0)

        glTexCoord2f(textureXOffset + textureWidth, textureYOffset)
        glVertex3f(bx + (size_tile/2), by+(size_tile/2), 0)

        glTexCoord2f(textureXOffset,textureYOffset)
        glVertex3f(bx-(size_tile/2),by+(size_tile/2), 0)

        glEnd()

    def load_map(self):
        size_tile = 0.64
        from clases.casilla import casilla
        from clases.objetos import objetos
        import copy
        #MatrixT = [[0 for x in xrange(30)] for x in xrange(400)]
        Matrix = []
        items = []
        itemsDisplayList = []
        global chunkDisplayList
        chunkDisplayList = glGenLists(2)

        mapa = list(csv.reader(open('assets/mapa.tmx')))
        estado = 0
        x = -1
        y = 29
        capa = -1
        #for taa in range(int(50)):
        #    self.items.append([])
        for pepe in mapa:
            if "orientation" in pepe[0]:
                pos_tmp = pepe[0].find('width="')
                string_tmp = pepe[0][pos_tmp+7:]
                pos_tmp = string_tmp.find('"')
                total_x = int(string_tmp[:pos_tmp])

                pos_tmp = pepe[0].find('height="')
                string_tmp = pepe[0][pos_tmp+8:]
                pos_tmp = string_tmp.find('"')
                total_y = int(string_tmp[:pos_tmp])
                y = total_y-1
                print total_x, total_y
                xasd = 0
                MatrixT = [[0 for xasd in xrange(total_y)] for xasd in xrange(total_x)]
                print "matrixt generado"

                for taa in range(int(total_x/8)):
                    items.append([])
                    itemsDisplayList.append((glGenLists(1)))

            if pepe[0] == '  <data encoding="csv">':
                capa +=1
                if (capa < 2):
                    glNewList(chunkDisplayList+capa, GL_COMPILE)
                estado = 1
            elif pepe[0] == '</data>':
                if (capa < 2):
                    glEndList()
                estado = 0
                Matrix.append(copy.deepcopy(MatrixT))
                x = -1
                y = total_y-1
            elif estado == 1:
                for taa in pepe:
                    if taa != "":
                        x +=1
                        if (capa == 2 and int(taa)-1 != -1):
                            tmpe = casilla(int(taa)-1, objetos(int(taa)-1, 1))
                        else:
                            tmpe = casilla(int(taa)-1)
                        if (int(taa)-1 != -1):
                            if (capa < 2):
                                self.create_tile(x,y,int(taa)-1)
                            if (capa == 2):
                                items[int(x/20)].append([x,y,tmpe])
                        MatrixT[x][y] = tmpe
                    else:
                        y -=1
                        x = -1

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
        self.borrame = False
        print "aqui estoy"

    def recv_package(self):
        result = self.socket.recv(5)
        if result != "":
            self.Vactual_info = unpack("?????",result)
        else:
            print "top else"
            raise "a tomar por culo"

    def run(self):
        try:
            while True:
                self.recv_package()
        except:
            self.borrame = True
    def get_borrame(self):
        return self.borrame
    def get_id(self):
        return self.datos



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

    #client
    resolution = [800,600]
    Lchunk = []
    size_tile = 0.16
    calculate_size = size_tile # deprecated
    v_object_select = [0,0]
    textures = []
    status_global = 0
    zoom = 3.0

    #server
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
    try:
        server_name = sys.argv[1]
    except:
        server_name = "Default name"
    try:
        thread_updateLobby = updateLobby(clientes, 8003, server_name)
        thread_updateLobby.start()
    except:
        print "lobby down"
    server.bind(("", 8003))
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
            client_pa_la_lista = Cliente(socket_cliente, datos_cliente, world, bullet)
            client_pa_la_lista.start()
            clientes.append(client_pa_la_lista)
        #elif(package[0] == 0):
        #   servers.append([socket_cliente,datos_cliente,'file_return',0,'hilo','frame'])
        #   print "server anadido a la lista"
        elif(package[0] == 9):
            print "test mode"
            #recvfile(socket_cliente,datos_cliente,'/tmp/test.tar.gz')
