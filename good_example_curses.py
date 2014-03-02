#!/usr/bin/env python2
import socket
from struct import *
import curses
from curses import panel
import os

def recvpackage(socket_cliente,size_package):
    package = ''
    while len(package) < size_package:
        chunk = socket_cliente.recv(size_package - len(package))
        if chunk == '':
            print 'Connection broken'  # raise ...
            break
        package += chunk
    return package


class Menu(object):

    def __init__(self, items, stdscreen, select_menu):
        self.window = stdscreen.subwin(0,0)
        self.window.keypad(1)
        self.panel = panel.new_panel(self.window)
        self.panel.hide()
        panel.update_panels()

        self.position = 0
        self.items = items
        if select_menu == 1:
            server_list = self.request_server()
            self.items.append(("Name server",curses.flash,"a","t","maps"))
            for server in server_list:
                self.items.append((server[2].split('\x00')[0],"start",server[3],server[4],server[5],server[0].split('\x00')[0], server[1]))
        else:
            self.items.append(('exit','exit'))

    def request_server(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect(("masteroids.no-ip.org", int(8004)))
        #mode
        mode = 1
        server_list = []
        s.send(pack('i', mode))
        longitud = unpack('i', recvpackage(s, 4))[0]
        for k in range(longitud):
            server_list.append(unpack('15si32siii',recvpackage(s,64)))
        return server_list

    def navigate(self, n):
        self.position += n
        if self.position < 0:
            self.position = 0
        elif self.position >= len(self.items):
            self.position = len(self.items)-1

    def display(self):
        self.panel.top()
        self.panel.show()
        self.window.clear()

        while True:
            self.window.refresh()
            curses.doupdate()
            for index, item in enumerate(self.items):
                if index == self.position:
                    mode = curses.A_REVERSE
                else:
                    mode = curses.A_NORMAL

                name_server = '%s' % (item[0])
                self.window.addstr(1+index, 1, str(name_server), mode)
                if 3 < len(item): #server list
                    self.window.addstr(1+index, 64, str(item[2])+"/"+str(item[3]), mode)
                    self.window.addstr(1+index, 70, str(item[4]), mode)

            key = self.window.getch()

            if key in [curses.KEY_ENTER, ord('\n')]:
                if self.position == len(self.items)-1:
                    break
                else:
                    if self.items[self.position][1] == "start":
                        ip = self.items[self.position][5]
                        port = self.items[self.position][6]
                        os.chdir('client')
                        print ip, port
                        #os.system('python start.py '+str(ip)+' '+str(port))
                        break
                        #pass #init server
                    else:
                        self.items[self.position][1]()


            elif key == curses.KEY_UP:
                self.navigate(-1)

            elif key == curses.KEY_DOWN:
                self.navigate(1)

        self.window.clear()
        self.panel.hide()
        panel.update_panels()
        curses.doupdate()

class MyApp(object):

    def __init__(self, stdscreen):
        self.screen = stdscreen
        curses.curs_set(0)
        multiplayer_items = []
        multiplayer = Menu(multiplayer_items, self.screen, 1)

        main_menu_items = [
                ('multiplayer', multiplayer.display)
                ]
        main_menu = Menu(main_menu_items, self.screen, 0)

        multiplayer_items.append(('back', main_menu.display))
        main_menu.display()

if __name__ == '__main__':
    curses.wrapper(MyApp)