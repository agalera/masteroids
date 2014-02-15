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
import math
from random import randint


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

class Cliente(Thread):
    def __init__(self, socket_cliente, servers):
        Thread.__init__(self)
        self.socket = socket_cliente
        self.servers = servers

    def run(self):
        package = pack('i', len(self.servers))
        for key in self.servers.keys():
            tmp = self.servers[key]
            package += pack('15si32siii',tmp[0],tmp[1],tmp[2],tmp[3],tmp[4],tmp[5])
        self.socket.send(package)
        self.socket.close()

#################################### Init code ####################################
if __name__ == '__main__':
    servers = dict()
    global_id = 1
    # Se prepara el servidor
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    #server = socket.socket(socket.SOCK_DGRAM)

    server.bind(("", 8004))
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
            hilo3 = Cliente(socket_cliente, servers)
            hilo3.start()
        elif(package[0] == 0):
            package = unpack('i32siiii', recvpackage(socket_cliente,52))
            #id_random = package[5]
            #ip = datos_cliente[0]
            #port = package[0]
            servers[global_id] = [datos_cliente[0],package[0], package[1], package[2],package[3],package[4],package[5]]
            socket_cliente.send(pack('i', global_id))
            global_id += 1
            socket_cliente.close()
            print package
            print "server anadido a la lista", global_id-1
        elif(package[0] == 2):
            package = unpack('iiiii', recvpackage(socket_cliente,20))
            select_server = servers[package[0]]
            if select_server[0] == datos_cliente[0] and select_server[1] == package[1] and select_server[6] == package[4]:
                servers[package[0]][3] = package[2]
                servers[package[0]][4] = package[3]
                print "update ok", package[0]
            else:
                print "intento de falseo"
            socket_cliente.close()
            #id_random = package[5]
            #ip = datos_cliente[0]
            #port = package[0]
