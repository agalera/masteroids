from __future__ import division
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *


def put_texture(init, tile = 0):
    if init == True:
        glMatrixMode(GL_TEXTURE)
        glPushMatrix()
        textureXOffset = float(tile/16.0)+0.001
        textureYOffset = float(16 - int(tile/16)/16.0)-0.001
        glTranslatef(textureXOffset,textureYOffset,0.0)
        glMatrixMode(GL_MODELVIEW)
    else:
        glMatrixMode(GL_TEXTURE)
        glPopMatrix()
        glMatrixMode(GL_MODELVIEW)
def draw_cube(size_tile, tile = 0):
    texture_info_temp = [int(tile), 0];
    textureXOffset = float(texture_info_temp[0]/16.0)+0.001
    textureYOffset = float(16 - int(texture_info_temp[0]/16)/16.0)-0.001
    textureHeight  = float(0.060)
    textureWidth   = float(0.060)


    glBegin(GL_QUADS)
    glTexCoord2f(textureXOffset, textureYOffset - textureHeight)
    glVertex3f(-size_tile, -size_tile, 0.0)

    glTexCoord2f(textureXOffset + textureWidth, textureYOffset - textureHeight)
    glVertex3f(size_tile, -size_tile, 0.0)

    glTexCoord2f(textureXOffset + textureWidth, textureYOffset)
    glVertex3f( size_tile,  size_tile, 0.0)

    glTexCoord2f(textureXOffset,textureYOffset)
    glVertex3f(-size_tile, size_tile, 0.0)
    glEnd()
