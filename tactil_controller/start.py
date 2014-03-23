from __future__ import division
import time
import random
import socket
from struct import *
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import math
from clases.player import player
from PIL.Image import open as pil_open
import sys
import csv

from random import randint
import clases.basicas as basicas
from threading import Thread

resolution = [800,600]
radians = 0
last_time = time.time()
t_delta = 0
fps = 0
lastFPS = 0
animate = 0.0
lastFrame = time.time()
test = 0.0
wasd = [0,0,0,0,0,[0,0,0]]
cambios = False
Lchunk = []
size_tile = 0.16
calculate_size = size_tile
v_object_select = [0,0]
borrar = []
textures = []
bullet = []
joints = []
status_global = 0
zoom = 3.0
naves_new = dict()

# Create a dynamic body at (0,4)


#body.fixedRotation = True


timeStep = 1.0 / 160
vel_iters, pos_iters = 6, 2



def ControlRatonPos(x,y):
    global radians
    radians = (math.atan2(-((resolution[1]/2)-y), (resolution[0]/2)-x)+ 3.14159266)

def ControlRaton(key,leave,x,y):
    global wasd
    global zoom
    if key <= 2 :
        ControlRatonPos(x,y)
        wasd[5][key] = not leave
    if (key == 3):
        zoom -= 0.32
        reshapeFun(resolution[0], resolution[1])
    if (key == 4):
        zoom += 0.32
        reshapeFun(resolution[0], resolution[1])





def ControlTeclado(key,x,y):
    global wasd
    global radians
    global cambios
    if (key == "w"):
        if wasd[0] == 0:
            wasd[0] = 1
            cambios = True
    if (key == "a"):
        if wasd[1] == 0:
            wasd[1] = 1
            cambios = True
    if (key == "s"):
        if wasd[2] == 0:
            wasd[2] = 1
            cambios = True
    if (key == "d"):
        if wasd[3] == 0:
            wasd[3] = 1
            cambios = True
    if (key == "q"):
        if wasd[4] == 0:
            wasd[4] = 1
            cambios = True

        #Lchunk[0].set_object(v_object_select, objetos(496,2.0))
def ControlTecladoUp(key,x,y):
    global wasd
    global cambios
    if (key == "w"):
        wasd[0] = 0
    if (key == "a"):
        wasd[1] = 0
    if (key == "s"):
        wasd[2] = 0
    if (key == "d"):
        wasd[3] = 0
    if (key == "q"):
        wasd[4] = 0
    cambios = True

def initFun():
    #thread sockets
    online = update_dates(player)
    online.start()

def recvpackage(socket_cliente,size_package):
    package = ''
    while len(package) < size_package:
        chunk = socket_cliente.recv(size_package - len(package))
        if chunk == '':
            print 'Connection broken'  # raise ...
            break
        package += chunk
    return package


class update_dates(Thread):
    def __init__(self, player):
        Thread.__init__(self)
        #self.s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.s = socket.socket(socket.SOCK_DGRAM)
        self.s.connect((sys.argv[1], int(sys.argv[2])))
        self.player = player
        #mode
        mode = 1
        self.s.send(pack('i',mode))
        global player_id
        player_id = unpack('i', recvpackage(self.s,4))[0]
        print "id: "+ str(player_id)

    def run(self):
        global cambios
        while True:
            if cambios:
                print "envio teclas"
                self.s.send(pack('?????', wasd[0], wasd[1], wasd[2], wasd[3], wasd[4]))
                cambios = False

    #def update_info(self):
    #    try:
    #        numero_datos = unpack("i", recvpackage(self.s, 4))[0]
    #        if (numero_datos < 0):
    #            #hp
    #            if numero_datos == -1:
    #                player.set_hp(unpack("f", recvpackage(self.s, 4))[0])
    #            #energy
    #            elif numero_datos == -2:
    #                player.set_energy(unpack("f", recvpackage(self.s, 4))[0])
    #            #hp y energy
    #            elif numero_datos == -3:
    #                player.set_hp(unpack("f", recvpackage(self.s, 4))[0])
    #                player.set_energy(unpack("f", recvpackage(self.s, 4))[0])
    #            return True
    #        else:
    #            var = -10
    #            tmp = dict()
    #            player_pos = player.get_position()
    #            for taa in range(int(numero_datos)):
    #                tmp2 = unpack("iifff", recvpackage(self.s, 20))
#
#
    #                if(math.hypot(player_pos[0] - tmp2[2], player_pos[1] - tmp2[3])<20):
    #                    if tmp2[0] == -2:
    #                        ids = var
    #                        var -= 1
    #                    else:
    #                        ids = tmp2[0]
    #                    tmp[tmp2[0]] = [ids, tmp2[1], tmp2[2], tmp2[3], tmp2[4]]
    #            return tmp
    #    except:
    #        print "error network"
    #        print "len", numero_datos
    #        return True

if __name__ == '__main__':
    glutInit()
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB)
    glutInitWindowSize(resolution[0],resolution[1])
    glutCreateWindow("Masteroids")

    #glutSpecialFunc(ControlFlechas)

    #glutSpecialUpFunc(ControlFlechasUp)
    #glutTimerFunc(16,update, 1)

    #glutDisplayFunc(RenderGLFun)
    #glutIdleFunc(RenderGLFun)
    #glutReshapeFunc(reshapeFun)
    glutKeyboardFunc(ControlTeclado)
    glutKeyboardUpFunc(ControlTecladoUp)
    glutMouseFunc(ControlRaton)
    glutPassiveMotionFunc(ControlRatonPos)
    glutMotionFunc(ControlRatonPos)
    initFun()
    glutMainLoop()