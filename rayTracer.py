from gl import Raytracer, color
from obj import Obj, Texture, Envmap
from sphere import *
import random

print("\nCargando ...\n")

brick = Material(diffuse = color(0, 0, 0 ), spec = 16)
stone = Material(diffuse = color(0.4, 0.4, 0.4 ), spec = 32)
mirror = Material(spec = 64, matType = REFLECTIVE)
glass = Material(spec = 64, ior = 1.5, matType= TRANSPARENT) 

# c2a472 - 194, 164, 114
colosseum1 = Material(diffuse = color(0.761, 0.643, 0.447), spec = 16)
# 9a7445 - 154, 116, 69
colosseum2 = Material(diffuse = color(0.604, 0.455, 0.271), spec = 16)
# b88f57 - 184, 143, 87
colosseum3 = Material(diffuse = color(0.722, 0.561, 0.341), spec = 16)
# feda9c - 254, 218, 156
colosseum4 = Material(diffuse = color(0.996, 0.855, 0.612), spec = 16)

boxMat = Material(texture = Texture('box.bmp'))
sanpietrini = Material(texture = Texture('sanpietrini.bmp'))

earthMat = Material(texture = Texture('earthDay.bmp'))


r = Raytracer(736, 512)
r.glClearColor(0.2, 0.6, 0.8)
r.glClear()

r.envmap = Envmap('env2.bmp')

# Lights
#r.pointLights.append( PointLight(position = V3(-4,4,0), intensity = 0.5))
#r.pointLights.append( PointLight(position = V3( 4,0,0), intensity = 0.5))
# r.dirLight = DirectionalLight(direction = (1, -1, -2), intensity = 1)
r.ambientLight = AmbientLight(strength = 1)


r.scene.append( AABB((0, -3, -20), (40, 0.1, 40) , brick))
r.scene.append( AABB((0, -1, -30), (50, 5, 0.1) , stone))

r.scene.append( AABB((0, 0, -10), (1, 1.4, 0) , colosseum1))
r.scene.append( AABB((0, 0.73, -9.9), (1, 0.5, 0) , colosseum2))
r.scene.append( Sphere(( 0, 0.3, -6), 0.2, colosseum1))

# r.scene.append( Plane(( 0, -10, -20), (0, 1, 0.01), stone)) # Suelo

# r.scene.append(Cylinder(0.15, 1.8, (0, 1, -10), colosseum1))



r.rtRender()

r.glFinish('output.bmp')

print("El bitmap se ha generado con exito, revisa la carpeta contenedora")






