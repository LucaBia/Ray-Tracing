from gl import Raytracer, color
from obj import Obj, Texture, Envmap
from sphere import *


gray = Material(diffuse = color(0.4, 0.4, 0.4 ), spec = 64)
metallicSeaweed = Material(diffuse = color(0.031, 0.255, 0.361), spec = 64)
etonBlue = Material(diffuse = color(0.537, 0.808, 0.580), spec = 64)
wall = Material(diffuse = color(0.996, 0.996, 0.996), spec = 64)
floor = Material(diffuse = color(0.851, 0.851, 0.851), spec = 64)



rayTracer = Raytracer(500, 500)


rayTracer.pointLight = PointLight(position = (0,0,0), intensity = 1)
rayTracer.ambientLight = AmbientLight(strength = 0.1)


# Cuarto
rayTracer.scene.append( Plane((0, -3, 0), (0,1,0), wall)) # Pared izquierda
rayTracer.scene.append( Plane((0, 0, -10), (0,0,1), gray)) # Pared enfrente 
rayTracer.scene.append( Plane(( 3, 0,0), (-1,0,0), wall)) # Pared derecha
rayTracer.scene.append( Plane(( -3,0, 0), (1,0,0), floor)) # Suelo
rayTracer.scene.append( Plane((0, 3, 0), (0,-1,0), wall) ) # Techo 

# Cubos
rayTracer.scene.append(AABB((-1, -2.3, -7), 1, metallicSeaweed))
rayTracer.scene.append(AABB((1, -2.3, -7), 1, etonBlue))


rayTracer.rtRender()
rayTracer.glFinish('output.bmp')

print("El bitmap se ha generado con exito, revisa la carpeta contenedora")





