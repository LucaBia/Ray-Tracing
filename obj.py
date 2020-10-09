# Gian Luca Rivera - 18049

import struct
from mathLib import *
from numpy import arccos, arctan2 



def color(r, g, b):
    return bytes([int(b * 255), int(g * 255), int(r * 255)])

    
# carga e identifica los elemetnos de un archivo obj
class Obj(object):
    def __init__(self, filename):
        with open(filename, 'r') as file:
            self.lines = file.read().splitlines()

        self.vertices = []
        self.normals = []
        self.texcoords = []
        self.faces = []

        self.read()

    def read(self):
        for line in self.lines:
            if line:
                if (len(line.split(" ")) > 1) :

                    prefix, value = line.split(' ', 1)

                    if prefix == 'v': # Vertices
                        self.vertices.append(list(map(float,value.split(' '))))
                    elif prefix == 'vn': # Vertives normales
                        self.normals.append(list(map(float,value.split(' '))))
                    elif prefix == 'vt': #Coordenada de texturas 
                        self.texcoords.append(list(map(float,value.split(' '))))
                    elif prefix == 'f': #Cara del poligono
                        self.faces.append([list(map(int,vert.split('/'))) for vert in value.split(' ')])

            # print(line)

# Clase para colocar una textura al obj en formato bmp
class Texture(object):
    def __init__(self, path):
        self.path = path
        self.read()
        
    def read(self):
        image = open(self.path, 'rb')
        image.seek(10)
        headerSize = struct.unpack('=l', image.read(4))[0]

        image.seek(14 + 4)
        self.width = struct.unpack('=l', image.read(4))[0]
        self.height = struct.unpack('=l', image.read(4))[0]
        image.seek(headerSize)

        self.pixels = []

        for y in range(self.height):
            self.pixels.append([])
            for x in range(self.width):
                b = ord(image.read(1)) / 255
                g = ord(image.read(1)) / 255
                r = ord(image.read(1)) / 255
                self.pixels[y].append(color(r,g,b))

        image.close()

    def getColor(self, tx, ty):
        if tx >= 0 and tx <= 1 and ty >= 0 and ty <= 1:
            x = int(tx * self.width)
            y = int(ty * self.height)

            return self.pixels[y][x]
        else:
            return color(0,0,0)
            

class Envmap(object):
    def __init__(self, path):
        self.path = path
        self.read()
        
    def read(self):
        image = open(self.path, 'rb')
        image.seek(10)
        headerSize = struct.unpack('=l', image.read(4))[0]

        image.seek(14 + 4)
        self.width = struct.unpack('=l', image.read(4))[0]
        self.height = struct.unpack('=l', image.read(4))[0]
        image.seek(headerSize)

        self.pixels = []

        for y in range(self.height):
            self.pixels.append([])
            for x in range(self.width):
                b = ord(image.read(1)) / 255
                g = ord(image.read(1)) / 255
                r = ord(image.read(1)) / 255
                self.pixels[y].append(color(r,g,b))

        image.close()

    def getColor(self, direction):

        direction = direction / frobeniusNorm(direction)

        x = int( (arctan2( direction[2], direction[0]) / (2 * pi) + 0.5) * self.width)
        y = int( arccos(-direction[1]) / pi * self.height )

        return self.pixels[y][x]

