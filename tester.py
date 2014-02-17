#By Alberto Galera
import sys
import random
import socket
from struct import *
import time
import random
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

def add_server():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(("127.0.0.1", int(8004)))
    #mode
    mode = 0
    port = 8003
    name = "sasas"
    players = 0
    total_players = 32
    id_map = 1
    id_random = random.randint(-12222222,122222222)
    s.send(pack('ii32siiii', mode, port, name, players, total_players, id_map,id_random))
    return unpack('i', s.recv(4))[0], id_random

def update_server(id_unique, id_random):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(("127.0.0.1", int(8004)))
    #mode
    mode = 2
    port = 8003
    players = 0
    id_map = 2
    s.send(pack('iiiiii', mode, id_unique, port, players, id_map, id_random))
def request_server():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(("127.0.0.1", int(8004)))
    #mode
    mode = 1
    server_list = []
    s.send(pack('i', mode))
    longitud = unpack('i', recvpackage(s, 4))[0]
    print longitud
    for k in range(longitud):
        server_list.append(unpack('15si32siii',recvpackage(s,64)))
    print server_list
unique_id, id_random = add_server()
update_server(unique_id, id_random)
request_server()
