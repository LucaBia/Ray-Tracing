# from gl import Raytracer, color
# from obj import Obj, Texture, Envmap
# from sphere import *


# gray = Material(diffuse = color(0.4, 0.4, 0.4 ), spec = 64)
# metallicSeaweed = Material(diffuse = color(0.031, 0.255, 0.361), spec = 64)
# etonBlue = Material(diffuse = color(0.537, 0.808, 0.580), spec = 64)
# wall = Material(diffuse = color(0.996, 0.996, 0.996), spec = 64)
# floor = Material(diffuse = color(0.851, 0.851, 0.851), spec = 64)



# rayTracer = Raytracer(500, 500)


# rayTracer.pointLight = PointLight(position = (0,0,0), intensity = 1)
# rayTracer.ambientLight = AmbientLight(strength = 0.1)


# # Cuarto
# rayTracer.scene.append( Plane((0, -3, 0), (0,1,0), wall)) # Pared izquierda
# rayTracer.scene.append( Plane((0, 0, -10), (0,0,1), gray)) # Pared enfrente 
# rayTracer.scene.append( Plane(( 3, 0,0), (-1,0,0), wall)) # Pared derecha
# rayTracer.scene.append( Plane(( -3,0, 0), (1,0,0), floor)) # Suelo
# rayTracer.scene.append( Plane((0, 3, 0), (0,-1,0), wall) ) # Techo 

# # Cubos
# rayTracer.scene.append(AABB((-1, -2.3, -7), 1, metallicSeaweed))
# rayTracer.scene.append(AABB((1, -2.3, -7), 1, etonBlue))


# rayTracer.rtRender()
# rayTracer.glFinish('output.bmp')

# print("El bitmap se ha generado con exito, revisa la carpeta contenedora")


from gl import Raytracer, color
from obj import Obj, Texture, Envmap
from sphere import *
import random

print("Cargando ...")

brick = Material(diffuse = color(0.8, 0.25, 0.25 ), spec = 16)
stone = Material(diffuse = color(0.4, 0.4, 0.4 ), spec = 32)
mirror = Material(spec = 64, matType = REFLECTIVE)
glass = Material(spec = 64, ior = 1.5, matType= TRANSPARENT) 

boxMat = Material(texture = Texture('box.bmp'))

earthMat = Material(texture = Texture('earthDay.bmp'))


width = 512
height = 512
r = Raytracer(width,height)
r.glClearColor(0.2, 0.6, 0.8)
r.glClear()

r.envmap = Envmap('envmap.bmp')

# Lights
#r.pointLights.append( PointLight(position = V3(-4,4,0), intensity = 0.5))
#r.pointLights.append( PointLight(position = V3( 4,0,0), intensity = 0.5))
r.dirLight = DirectionalLight(direction = (1, -1, -2), intensity = 0.5)
r.ambientLight = AmbientLight(strength = 0.1)

# Objects
#r.scene.append( Sphere(V3( 0, 0, -8), 2, brick) )
#r.scene.append( Sphere(V3( -0.5, 0.5, -5), 0.25, stone))
#r.scene.append( Sphere(V3( 0.25, 0.5, -5), 0.25, stone))


r.scene.append( AABB((0, -3, -10), (5, 0.1, 5) , boxMat ) )
#r.scene.append( AABB(V3(1.5, 1.5, -5), V3(1, 1, 1) , boxMat ) )
#r.scene.append( AABB(V3(-1.5, 0, -5), V3(1, 1, 1) , boxMat ) )

r.scene.append( Sphere(( 0, 0, -8), 2, earthMat))



r.rtRender()

r.glFinish('output.bmp')






