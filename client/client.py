#By Alberto Galera
import sys
import random
import socket
from struct import *
import time

def send_position():
    s.send(pack('ifff', 1,1.0,2222.1,44.23123123))
    time.sleep(0.03)
    
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
def update_info(socket_cliente):
    try:
        numero_datos = unpack("i", recvpackage(socket_client, 4))[0]
        tmp = []
        for taa in int(numero_datos):
            tmp.append(unpack("ifff", recvpackage(socket_cliente, numero_datos)))
        return tmp
    except:
        print "epic crash"

s = socket.socket(socket.SOCK_DGRAM)
s.connect(("127.0.0.1", int(8002)))
#mode
mode = 1
s.send(pack('i',mode))
#recv id
player_id = unpack('i', recvpackage(s,4))[0]
print "id: "+ str(player_id)

s.close()
