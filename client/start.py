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
from PIL.Image import open
import sys

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

def enable_vsync():
    pass
    #glEnable(GL_VSYNC)
        # set v to 1 to enable vsync, 0 to disable vsync


def loadImage(imageName):
    im = open(imageName)
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

def create_camera(zoom_lock):
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



def object_select():
    v_object_select[0] = int((player.get_position()[0][0]+0.16) * 3.125)
    v_object_select[1] = int((player.get_position()[0][1]+0.16) * 3.125)
    #tmp = math.degrees(radians)
    #position = (player.get_position()[0][0]+(math.cos(radians)*0.5),player.get_position()[0][1]+(math.sin(radians)*0.5))
    #print "init"
    #print v_object_select
    #v_object_select[0] = int((position[0]+0.16) * 3.125)
    #v_object_select[1] = int((position[1]+0.16) * 3.125)
    #print tmp
    #90 top
    #if tmp > 0 and tmp < 45:
    #    v_object_select[1] += 1
    #    v_object_select[0] += 1
    #    #print "right top"
    #if tmp > 45 and tmp < 90:
    #    v_object_select[1] += 1
    #    #print "top"
    #if tmp > 90 and tmp < 135:
    #    v_object_select[1] += 1
    #    v_object_select[0] -= 1
    #    #print "left top"
    #if tmp > 135 and tmp < 180:
    #    v_object_select[0] -= 1
    #    #print "left"
    #if tmp > 180 and tmp < 225:
    #    v_object_select[1] -= 1
    #    v_object_select[0] -= 1
    #    #print "left bottom"
    #if tmp > 225 and tmp < 270:
    #    v_object_select[1] -= 1
    #    #print "bottom"
    #if tmp > 270 and tmp < 315:
    #    v_object_select[1] -= 1
    #    v_object_select[0] += 1
    #    #print "right bottom"
    #if tmp > 315 and tmp < 360:
    #    v_object_select[0] += 1
    #    #print "right"


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
def draw_posible_options():
    Lchunk[0].check_object(v_object_select)

def glut_print( x,  y,  font,  text, r,  g , b , a):

    #glEnable(GL_BLEND)
    glColor3f( r,  g , b)
    glRasterPos2d(x,y+0.02)
    #glWindowPos2d(x,y)
    for ch in text :
        glutBitmapCharacter( font , ctypes.c_int( ord(ch) ) )
    glColor3f( 1, 1, 1)

def initFun():
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
    global vida_DL
    global energy_DL
    global trenecito
    global naves
    global current_fps
    current_fps = 0
    naves = dict()
    vida_DL = glGenLists(1)
    energy_DL = glGenLists(1)
    global_DL = glGenLists(256)
    print "aqui", global_DL
    tmp2 = 0
    for taa in range(global_DL,256 + global_DL):
        glNewList(global_DL+tmp2, GL_COMPILE)
        basicas.draw_cube(0.16, tmp2)
        glEndList()
        tmp2 += 1

    textures.append(loadImage('assets/stGrid1.png'))
    textures.append(loadImage('assets/player.png'))
    textures.append(loadImage('assets/bullet.png'))
    textures.append(loadImage('assets/stGriddeco.png'))
    textures.append(loadImage('assets/icons.png'))
    textures.append(loadImage('assets/tren_1.png'))
    textures.append(loadImage('assets/inicio.png'))
    textures.append(loadImage('assets/gameover.png'))
    textures.append(loadImage('assets/frases1.png'))

    player = player(global_DL)
        #thread sockets
    online = update_dates(player)
    online.start()

    enable_vsync()
    getDelta()

    #glEnable(GL_CULL_FACE)
    #glCullFace(GL_BACK )

def draw_pantallazo(num):
    setupTexture(num)
    texture_info_temp = 2
    textureXOffset = 1
    textureYOffset = 1
    textureHeight  = 1
    textureWidth   = 1

    #glTranslatef( self.body.position[0] , self.body.position[1], 0.00)
    glClearColor(0.0,0.0,0.0,0.0)
    glClear(GL_COLOR_BUFFER_BIT)
    glRotate(0, 0, 0, 1)
    glBegin(GL_QUADS)
    glTexCoord2f(textureXOffset, textureYOffset - textureHeight)

    glVertex3f(-zoom, -zoom, 0)

    glTexCoord2f(textureXOffset + textureWidth, textureYOffset - textureHeight)
    glVertex3f(zoom, -zoom, 0)

    glTexCoord2f(textureXOffset + textureWidth, textureYOffset)
    glVertex3f( zoom,  zoom, 0)

    glTexCoord2f(textureXOffset,textureYOffset)
    glVertex3f(-zoom, zoom, 0)
    glEnd()
    glRotate(0, 0, 0, -1)
    #glTranslatef( -self.body.position[0] , -self.body.position[1], 0.00)

def reshapeFun(wi,he):
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

def setupTexture(imageID):
    glEnable(GL_TEXTURE_2D)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
    #glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
    #glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
    glBindTexture(GL_TEXTURE_2D, textures[imageID])
    #texCoordsFrame1 = [0.32]
    #glTexCoordPointer(2, GL_FLOAT, 0, textures[imageID])
    #glTexCoordPointer(2, GL_FLOAT, 1000, 1000)

def new_frame(init):
    if init == True:
        glMatrixMode(GL_TEXTURE)
        glPushMatrix()
        glTranslatef(0.0625*int(animate),0.0,0.0)
        glMatrixMode(GL_MODELVIEW)
    else:
        glMatrixMode(GL_TEXTURE)
        glPopMatrix()
        glMatrixMode(GL_MODELVIEW)

def background():
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

def RenderGLFun():
    if len(naves_new) == 0:
        return
    global status_global
    if status_global == 0 or status_global == 3:
        status_global = 1
        updateFPS()
        getDelta()
        glClearColor(0.0,0.0,0.0,0.0)
        glClear(GL_COLOR_BUFFER_BIT)
        glLoadIdentity()
        glPushMatrix()

        if status_global == 0:
            draw_pantallazo(6)
            if (wasd[0] == True):
                status_global = 1
        else:
            draw_pantallazo(7)
        glPopMatrix()
        glutSwapBuffers()

    #pepito
    elif status_global == 1:
        global t_delta
        updateFPS()
        t_delta = getDelta()

        #update()
        #---- Init Experimental zone ----
        global animate
        global naves
        animate +=float(t_delta)/60.0
        if animate > 16:
            animate = 0.0

        #---- End Experimental zone ----
        #Init Frame
        glClearColor(0.3,0.3,0.3,0.0)
        glClear(GL_COLOR_BUFFER_BIT)
        glLoadIdentity()
        naves = naves_new

        player.set_position(naves[player_id])

        create_camera(False)

        setupTexture(6)
        background()
        #draw time (optional)
        setupTexture(0)

        draw_naves()

        #player.draw() #components.py:31 opengl
        #setupTexture(2)

        #GUI
        create_camera(True)
        setupTexture(1)
        #draw_shield()
        draw_hp()
        draw_energy()
        draw_fps()
        #FIN GUI

        #draw_select()
        #go to gpu
        glutSwapBuffers()
        #timeSleep = 0.03 - (t_delta / 1000.0 )
        #if timeSleep > 0.0:
        #    time.sleep(timeSleep)
def draw_fps():
    bx = 1.5 * (aspect*2)
    by = 3.0 - 2/10.0
    glut_print( bx-0.25 , by , GLUT_BITMAP_HELVETICA_10 , str(int(current_fps)), 0.0 , 0.5 , 1.0 , 1.0 )
def draw_hp():
    global last_damage
    hp = player.get_hp()
    if hp != False:
        if hp > 0.0:
            glNewList(vida_DL, GL_COMPILE)
            draw_bar_opengl(1,hp)
            glEndList()
        else:
            global status_global
            status_global = 3
    glCallList(vida_DL)

def draw_energy():
    global last_damage
    energy = player.get_energy()
    if energy != False:
        if energy > 0.0:
            glNewList(energy_DL, GL_COMPILE)
            draw_bar_opengl(2,energy)
            glEndList()
        else:
            global status_global
            status_global = 3
    glCallList(energy_DL)

def draw_bar_opengl(tile, value):
    x = value / 100.0
    size_tile = 0.08
    bx = - 1.5 * (aspect*2)
    by = 3.0 - tile/10.0

    texture_info_temp = [int(tile), 0];
    textureXOffset = float(texture_info_temp[0]/16.0)+0.001
    textureYOffset = float(16 - int(texture_info_temp[0]/16)/16.0)-0.001
    textureHeight  = float(0.060)
    textureWidth   = float(0.060)
    glTranslatef(bx,by, 0)

    glBegin(GL_QUADS)
    glTexCoord2f(textureXOffset, textureYOffset - textureHeight)
    glVertex3f(0.0, 0.0, 0)

    glTexCoord2f(textureXOffset + textureWidth, textureYOffset - textureHeight)
    glVertex3f(x, 0.0, 0)

    glTexCoord2f(textureXOffset + textureWidth, textureYOffset)
    glVertex3f(x, +0.1, 0)

    glTexCoord2f(textureXOffset,textureYOffset)
    glVertex3f(0.0, +0.1, 0)

    glEnd()
    glTranslatef(-bx,-by, 0)

    glut_print( bx , by , GLUT_BITMAP_HELVETICA_10 , str(int(value))+" / 100" , 0.0 , 1.0 , 1.0 , 1.0 )

def draw_naves():
    for key in naves.keys():
        draw_nave(naves[key])

def draw_nave(position):
    size_tile = 0.32
    glTranslatef( position[2] , position[3], 0.0)
    glRotate(math.degrees(position[4]), 0, 0, 1)
    if position[1] < 253:
        glCallList(global_DL+position[1]+4)
    else:
        glCallList(global_DL)
    glRotate(math.degrees(position[4]), 0, 0, -1)
    glTranslatef( -position[2] , -position[3], -0.0)

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
        global current_fps
        current_fps = fps / (time.time() - last_time)
        fps = 0
        last_time = time.time()

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
        while True:
            global naves_new
            tmp = self.update_info()
            if (tmp != True):
                naves_new = tmp
            if cambios:
                print "envio teclas"
                self.s.send(pack('?????', wasd[0], wasd[1], wasd[2], wasd[3], wasd[4]))
                global cambios
                cambios = False

    def update_info(self):
        try:
            numero_datos = unpack("i", recvpackage(self.s, 4))[0]
            if (numero_datos < 0):
                #hp
                if numero_datos == -1:
                    player.set_hp(unpack("f", recvpackage(self.s, 4))[0])
                #energy
                elif numero_datos == -2:
                    player.set_energy(unpack("f", recvpackage(self.s, 4))[0])
                #hp y energy
                elif numero_datos == -3:
                    player.set_hp(unpack("f", recvpackage(self.s, 4))[0])
                    player.set_energy(unpack("f", recvpackage(self.s, 4))[0])
                return True
            else:
                var = -10
                tmp = dict()
                for taa in range(int(numero_datos)):
                    tmp2 = unpack("iifff", recvpackage(self.s, 20))
                    player_pos = player.get_position()

                    if(math.hypot(player_pos[0] - tmp2[2], player_pos[1] - tmp2[3])<20):
                        if tmp2[0] == -2:
                            ids = var
                            var -= 1
                        else:
                            ids = tmp2[0]
                        tmp[tmp2[0]] = [ids, tmp2[1], tmp2[2], tmp2[3], tmp2[4]]
                return tmp
        except:
            print "error network"
            print "len", numero_datos
            return True

if __name__ == '__main__':
    glutInit()
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB)
    glutInitWindowSize(resolution[0],resolution[1])
    glutCreateWindow("Masteroids")

    #glutSpecialFunc(ControlFlechas)

    #glutSpecialUpFunc(ControlFlechasUp)
    #glutTimerFunc(16,update, 1)

    glutDisplayFunc(RenderGLFun)
    glutIdleFunc(RenderGLFun)
    glutReshapeFunc(reshapeFun)
    glutKeyboardFunc(ControlTeclado)
    glutKeyboardUpFunc(ControlTecladoUp)
    glutMouseFunc(ControlRaton)
    glutPassiveMotionFunc(ControlRatonPos)
    glutMotionFunc(ControlRatonPos)
    initFun()
    glutMainLoop()