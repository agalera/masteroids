from __future__ import division
from clases.casilla import casilla
#from clases.asteroids import asteroids
from Box2D import *
from objetos import objetos
import copy

size_tile = 0.64
class chunk:
    def __init__ (self, x,y, worlds):
        self.dynamics = []
        self.x = x
        self.y = y
        self.Matrix = []
        self.items = []
        self.worlds = worlds
        self.load_map()

    def check_object(self, position):
        x = int(position[0])
        y = int(position[1])
        return self.Matrix[2][x][y].get_tile()
    def set_object(self,position, arma_objeto):

        x = int(position[0])
        y = int(position[1])
        self.Matrix[2][x][y].set_tile(arma_objeto.get_id(), arma_objeto)
        self.items[int(x/20)].append([x,y,self.Matrix[2][x][y]])

    def pick_object(self, position):

        try:
            x = int(position[0])
            y = int(position[1])
            xp = int(x/20)
            if (self.Matrix[2][x][y].get_tile() != -1):
                print x, y, xp
                tile = self.Matrix[2][x][y].get_tile()
                tmp = self.Matrix[2][x][y].get_object()
                self.Matrix[2][x][y].set_tile(-1)
                for taa in self.items[xp]:
                    if (x == taa[0] and y == taa[1]):
                        self.items[xp].remove(taa)

                return tmp
            else:
                return False
        except:
            return False

    def create_colision_triangle(self,xy,left):

        #    if (sa[1][0]-sa[0][0] == 0):
        #        x = size_tile/2
        #    else:
        #        x = ((sa[1][0]-sa[0][0])/2)* size_tile
#
        #    y = size_tile/2
        if (left):
            polydef = b2PolygonShape(vertices=[(size_tile/2,size_tile/2),(-size_tile/2,-size_tile/2),(size_tile/2,-size_tile/2)])
        else:
            polydef = b2PolygonShape(vertices=[(-size_tile/2,size_tile/2),(-size_tile/2,-size_tile/2),(size_tile/2,-size_tile/2)])


        #print "3"+ str(polydef)
        self.worlds.CreateStaticBody(
            position=(size_tile*xy[0],xy[1]*size_tile),
            shapes=polydef,
            #shapes=b2PolygonShape(box=(size_tile/2,size_tile/2)),
            )

#
            #            self.worlds.CreateStaticBody(
            #    position=(size_tile*bx,size_tile*by),
            #    shapes=b2PolygonShape(box=(size_tile/2,size_tile/2)),
            #    )
    def create_colision(self,shape):
        for sa in shape:

            longitud = (sa[1][0]-sa[0][0])/2.0

            self.worlds.CreateStaticBody(
                position=(size_tile*(longitud+sa[0][0]),(sa[0][1])*size_tile),
                shapes=b2PolygonShape(box=((longitud+0.5)*size_tile,size_tile/2)),
            )

    def load_map(self):
        #MatrixT = [[0 for x in xrange(30)] for x in xrange(400)]

        import csv
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
                self.total_x = int(string_tmp[:pos_tmp])

                pos_tmp = pepe[0].find('height="')
                string_tmp = pepe[0][pos_tmp+8:]
                pos_tmp = string_tmp.find('"')
                self.total_y = int(string_tmp[:pos_tmp])
                y = self.total_y-1
                print self.total_x, self.total_y
                xasd = 0
                MatrixT = [[0 for xasd in xrange(self.total_y)] for xasd in xrange(self.total_x)]
                print "matrixt generado"

                for taa in range(int(self.total_x/8)):
                    self.items.append([])

            if pepe[0] == '  <data encoding="csv">':
                capa +=1
                estado = 1
            elif pepe[0] == '</data>':
                estado = 0
                self.Matrix.append(copy.deepcopy(MatrixT))
                x = -1
                y = self.total_y-1
            elif estado == 1:
                for taa in pepe:
                    if taa != "":
                        x +=1
                        if (capa == 2 and int(taa)-1 != -1):
                            tmpe = casilla(int(taa)-1, objetos(int(taa)-1, 1))
                        else:
                            tmpe = casilla(int(taa)-1)
                        if (int(taa)-1 != -1):
                            if (capa == 2):
                                self.items[int(x/20)].append([x,y,tmpe])
                        MatrixT[x][y] = tmpe
                    else:
                        y -=1
                        x = -1

        shape = []

        posible_shape = [(-1,-1),(-1,-1)]
        for y in range(self.total_y):
            for x in range(self.total_x):
                s_y = (self.total_y-1) - int(y)
                tile = self.Matrix[0][x][y].get_tile()
                if (tile != -1):
                    if posible_shape[0][0] == -1 and posible_shape[0][1] == -1:
                        posible_shape[0] = (x,y)
                    else:
                        posible_shape[1] = (x,y)
                else:
                    if posible_shape[0][0] != -1 and posible_shape[0][0] != -1 and posible_shape[1][0] != -1 and posible_shape[1][1] != -1:
                        shape.append(posible_shape)
                    if posible_shape[0][0] != -1 and posible_shape[0][0] != -1 and posible_shape[1][0] == -1 and posible_shape[1][0] == -1:
                        posible_shape[1] = posible_shape[0]
                        shape.append(posible_shape)
                    posible_shape = [(-1,-1),(-1,-1)]
                    #if (tile == 4):
                    #    self.create_colision_triangle((x,y),True)
                    #if (tile == 5):
                    #    self.create_colision_triangle((x,y),False)
                #create dynamic bodys
                tile = self.Matrix[3][x][y].get_tile()
                #if (tile != -1):
                ##    pass
                #    self.dynamics.append(asteroids(self.worlds.CreateDynamicBody(position=(x*size_tile,y*size_tile), angularDamping=10.0, linearDamping= 10.0), tile, dl = self.global_DL))
        self.create_colision(shape)