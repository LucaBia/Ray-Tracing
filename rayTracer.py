from gl import Raytracer, color
from obj import Obj, Texture, Envmap
from forms import *
import random

print("\nCargando ...\n")

# c2a472 - 194, 164, 114
colosseum1 = Material(diffuse = color(0.761, 0.643, 0.447), spec = 16)
# 9a7445 - 154, 116, 69
colosseum2 = Material(diffuse = color(0.604, 0.455, 0.271), spec = 16)
# b88f57 - 184, 143, 87
colosseum3 = Material(diffuse = color(0.722, 0.561, 0.341), spec = 16)
# feda9c - 254, 218, 156
colosseum4 = Material(diffuse = color(0.996, 0.855, 0.612), spec = 16)
# 42692f - 66, 105, 47
treeGreen = Material(diffuse = color(0.259, 0.412, 0.184), spec = 16)
# 765c48 - 118, 92, 72
treeBrown = Material(diffuse = color(0.463, 0.361, 0.282), spec = 16)

floor = Material(texture = Texture('floor.bmp'))

mirror = Material(diffuse = color(0.4, 0.4, 0.4), spec = 64, matType = REFLECTIVE)
glass = Material(spec = 32, ior = 1.5, matType= TRANSPARENT) 


raytracer = Raytracer(700, 512)

raytracer.envmap = Envmap('envmap.bmp')

# Lights
# raytracer.pointLights.append( PointLight(position = (-4,4,0), intensity = 0.5))
# raytracer.pointLights.append( PointLight(position = ( 4,0,0), intensity = 0.5))
# raytracer.dirLight = Directi.onalLight(direction = (1, -1, -2), intensity = 1)
raytracer.ambientLight = AmbientLight(strength = 1)


raytracer.scene.append( AABB((0, -3, -20), (40, 0.1, 40), floor))
raytracer.scene.append( AABB((0, -1, -30), (50, 5, 0.1), mirror))

# Columnas
raytracer.scene.append(AABB((-7.4, -0.09, -10), (0.2, 4.86, 0), colosseum3))
raytracer.scene.append(AABB((-6.65, -0.5, -10), (0.1, 4, 0), colosseum3))
raytracer.scene.append(AABB((-5.95, -0.7, -10), (0.1, 3.6, 0), colosseum3))
raytracer.scene.append(AABB((-5.26, -0.7, -10), (0.1, 3.6, 0), colosseum3))
raytracer.scene.append(AABB((-4.57, -1.25, -10), (0.1, 2.53, 0), colosseum3))

# Horizontales
raytracer.scene.append(AABB((-5.4, -1.3, -9), (2.5, 0.2, 0), colosseum3))
raytracer.scene.append(AABB((-5.4, -0.08, -9), (2.5, 0.2, 0), colosseum3))
raytracer.scene.append(AABB((-5.7, 1.05, -9), (2, 0.2, 0), colosseum3))
raytracer.scene.append(AABB((-6.1, 2, -9), (1.2, 0.2, 0), colosseum3))

# Primera fila 
raytracer.scene.append(AABB((-7, -2, -10), (0.6, 1, 0) , colosseum1)) #Rectangulo vertical mayor
raytracer.scene.append(AABB((-6.93, -1.67, -9.9), (0.6, 0.4, 0) , colosseum2))
raytracer.scene.append(Sphere((-4.2, -1.2, -6), 0.15, colosseum1))

raytracer.scene.append(AABB((-6.31, -2, -10), (0.6, 1, 0) , colosseum1)) 
raytracer.scene.append(AABB((-6.23, -1.67, -9.9), (0.6, 0.4, 0) , colosseum2))
raytracer.scene.append(Sphere((-3.79, -1.2, -6), 0.15, colosseum1))

raytracer.scene.append(AABB((-5.6, -2, -10), (0.6, 1, 0), colosseum1)) 
raytracer.scene.append(AABB((-5.54, -1.67, -9.9), (0.6, 0.4, 0), colosseum2))
raytracer.scene.append(Sphere((-3.37, -1.2, -6), 0.15, colosseum1))

raytracer.scene.append(AABB((-4.9, -2, -10), (0.6, 1, 0), colosseum1)) 
raytracer.scene.append(AABB((-4.86, -1.67, -9.9), (0.6, 0.4, 0), colosseum2))
raytracer.scene.append(Sphere((-2.95, -1.2, -6), 0.15, colosseum1))


# Segunda fila
raytracer.scene.append(AABB((-7, -0.82, -10), (0.6, 1, 0), colosseum1)) 
raytracer.scene.append(AABB((-6.93, -0.4, -9.9), (0.6, 0.4, 0), colosseum2))
raytracer.scene.append(Sphere((-4.2, -0.43, -6), 0.15, colosseum1))

raytracer.scene.append(AABB((-6.31, -0.82, -10), (0.6, 1, 0), colosseum1)) 
raytracer.scene.append(AABB((-6.23, -0.4, -9.9), (0.6, 0.4, 0), colosseum2))
raytracer.scene.append(Sphere((-3.79, -0.43, -6), 0.15, colosseum1))

raytracer.scene.append(AABB((-5.6, -0.82, -10), (0.6, 1, 0), colosseum1)) 
raytracer.scene.append(AABB((-5.54, -0.4, -9.9), (0.6, 0.4, 0), colosseum2))
raytracer.scene.append(Sphere((-3.37, -0.43, -6), 0.15, colosseum1))

raytracer.scene.append(AABB((-4.9, -0.82, -10), (0.6, 1, 0), colosseum1)) 
raytracer.scene.append(AABB((-4.86, -0.4, -9.9), (0.6, 0.4, 0), colosseum2))
raytracer.scene.append(Sphere((-2.95, -0.43, -6), 0.15, colosseum1))


# Tercera fila
raytracer.scene.append(AABB((-7, 0.36, -10), (0.6, 1, 0), colosseum1)) 
raytracer.scene.append(AABB((-6.93, 0.87, -9.9), (0.6, 0.4, 0), colosseum2))
raytracer.scene.append(Sphere((-4.2, 0.4, -6), 0.15, colosseum1))

raytracer.scene.append(AABB((-6.31, 0.36, -10), (0.6, 1, 0), colosseum1)) 
raytracer.scene.append(AABB((-6.23, 0.87, -9.9), (0.6, 0.4, 0), colosseum2))
raytracer.scene.append(Sphere((-3.79, 0.4, -6), 0.15, colosseum1))

raytracer.scene.append(AABB((-5.6, 0.36, -10), (0.6, 1, 0), colosseum1)) 
raytracer.scene.append(AABB((-5.54, 0.87, -9.9), (0.6, 0.4, 0), colosseum2))
raytracer.scene.append(Sphere((-3.37, 0.4, -6), 0.15, colosseum1))

# Cuarta fila 
raytracer.scene.append(AABB((-6.1, 1.5, -9), (1.2, 1, 0), colosseum1))

raytracer.scene.append(AABB((-6.1, 1.76, -8.5), (0.2, 0.1, 0), colosseum2))
raytracer.scene.append(AABB((-5.48, 1.76, -8.5), (0.2, 0.1, 0), colosseum2))

raytracer.scene.append(AABB((-6.1, 1.4, -8.5), (0.08, 0.65 , 0), colosseum2))
raytracer.scene.append(AABB((-5.49, 1.4, -8.5), (0.076, 0.65 , 0), colosseum2))

raytracer.scene.append(AABB((-5.8, 1.4, -8.5), (0.1, 0.17, 0), colosseum2))


# Parte derecha
raytracer.scene.append(AABB((-3.3, -1.17, -10), (2.4, 2.7 , 0), colosseum1))

# Arbol
raytracer.scene.append(Cylinder(0.23, 1.5, (2, -2.5, -9), treeBrown))

raytracer.scene.append(Pyramid([(3, -1.4, -8.5), (1.9, -0.1, -8.5), (0.8, -1.4, -8.5), (2.5, -1, -10)], treeGreen)) #  Pyramid( derecha, arriba, izquierda, atras)
raytracer.scene.append(Pyramid([(2.7, -0.7, -8), (1.8, 0.7, -8), (0.9, -0.7, -8), (2.2, -0.1, -10)], treeGreen))
raytracer.scene.append(Pyramid([(2.5, 0, -8), (1.8, 1.3, -8), (1.1, 0, -8), (1.9, 1, -10)], treeGreen))

raytracer.scene.append(AABB((0.65, -0.2, -3), (1, 1.4, 0.1), glass))


raytracer.rtRender()

raytracer.glFinish('output.bmp')

print("El bitmap se ha generado con exito, revisa la carpeta contenedora")






