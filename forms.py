from gl import color
from mathLib import * 
from numpy import arccos, arctan2

from math import sqrt, inf # Utilizadas unicamente para el cilindro


OPAQUE = 0
REFLECTIVE = 1
TRANSPARENT = 2

WHITE = color(1,1,1)

class AmbientLight(object):
    def __init__(self, strength = 0, _color = WHITE):
        self.strength = strength
        self.color = _color

class PointLight(object):
    def __init__(self, position = (0,0,0), _color = WHITE, intensity = 1):
        self.position = position
        self.intensity = intensity
        self.color = _color

class DirectionalLight(object):
     def __init__(self, direction = (0,-1,0), _color = WHITE, intensity = 1):
        # self.direction = direction / frobeniusNorm(direction)
        self.direction = divVN(direction, frobeniusNorm(direction)) 
        self.intensity = intensity
        self.color = _color

class Material(object):
    def __init__(self, diffuse = WHITE, spec = 0, ior = 1, texture = None, matType = OPAQUE):
        self.diffuse = diffuse
        self.spec = spec

        self.matType = matType
        self.ior = ior

        self.texture = texture


class Intersect(object):
    def __init__(self, distance, point, normal, texCoords, sceneObject):
        self.distance = distance
        self.point = point
        self.normal = normal
        self.texCoords = texCoords
        self.sceneObject = sceneObject


class Sphere(object):
    def __init__(self, center, radius, material):
        self.center = center
        self.radius = radius
        self.material = material

    def ray_intersect(self, orig, dir):
        L = subVectors(self.center, orig)
        tca = dotVectors(L, dir)
        l = frobeniusNorm(L) 
        d = (l**2 - tca**2) ** 0.5
        if d > self.radius:
            return None


        thc = (self.radius** 2 - d**2) ** 0.5
        t0 = tca - thc
        t1 = tca + thc
        if t0 < 0:
            t0 = t1

        if t0 < 0: 
            return None
        
        hit = sumVectors(orig, multiply(t0, dir))
        norm = subVectors( hit, self.center )
        norm = norm / frobeniusNorm(norm)

        u = 1 - (arctan2( norm[2], norm[0]) / (2 * pi) + 0.5)
        v =  arccos(-norm[1]) / pi

        uvs = [u, v]

        return Intersect(distance = t0,
                         point = hit,
                         normal = norm,
                         texCoords = uvs,
                         sceneObject = self)

# Plano
class Plane(object):
    def __init__(self, position, normal, material):
        self.position = position
        self.normal = divVN(normal, frobeniusNorm(normal))
        self.material = material

    def ray_intersect(self, orig, dir):
        denom = dotVectors(dir, self.normal)

        if abs(denom) > 0.0001:
            t = dotVectors(self.normal, subVectors(self.position, orig)) / denom
            if t > 0:
                # hit = sumVectors(orig, t * dir)
                hit = sumVectors(orig, multiply(t, dir))

                return Intersect(distance = t,
                                 point = hit,
                                 normal = self.normal,
                                 texCoords = None,
                                 sceneObject = self)

        return None


# Cubos
class AABB(object):
    def __init__(self, position, size, material):
        self.position = position
        self.size = size
        self.material = material
        self.planes = []

        halfSizeX = size[0] / 2
        halfSizeY = size[1] / 2
        halfSizeZ = size[2] / 2

        self.planes.append( Plane( sumVectors(position, (halfSizeX, 0, 0)), (1, 0, 0), material))
        self.planes.append( Plane( sumVectors(position, (-halfSizeX, 0, 0)), (-1, 0, 0), material))

        self.planes.append( Plane( sumVectors(position, (0, halfSizeY, 0)), (0, 1, 0), material))
        self.planes.append( Plane( sumVectors(position, (0, -halfSizeY, 0)), (0, -1, 0), material))

        self.planes.append( Plane( sumVectors(position, (0, 0, halfSizeZ)), (0, 0, 1), material))
        self.planes.append( Plane( sumVectors(position, (0, 0, -halfSizeZ)), (0, 0, -1), material))


    def ray_intersect(self, orig, dir):

        epsilon = 0.001

        boundsMin = [0,0,0]
        boundsMax = [0,0,0]

        for i in range(3):
            boundsMin[i] = self.position[i] - (epsilon + self.size[i] / 2)
            boundsMax[i] = self.position[i] + (epsilon + self.size[i] / 2)

        t = float('inf')
        intersect = None
        uvs = None

        for plane in self.planes:
            planeInter = plane.ray_intersect(orig, dir)

            if planeInter is not None:
                if planeInter.point[0] >= boundsMin[0] and planeInter.point[0] <= boundsMax[0]:
                    if planeInter.point[1] >= boundsMin[1] and planeInter.point[1] <= boundsMax[1]:
                        if planeInter.point[2] >= boundsMin[2] and planeInter.point[2] <= boundsMax[2]:
                            if planeInter.distance < t:
                                t = planeInter.distance
                                intersect = planeInter

                                if abs(plane.normal[0]) > 0:
                                    u = (planeInter.point [1] - boundsMin[1]) / (boundsMax[1] - boundsMin[1])
                                    v = (planeInter.point [2] - boundsMin[2]) / (boundsMax[2] - boundsMin[2])

                                elif abs(plane.normal[1]) > 0:
                                    u = (planeInter.point [0] - boundsMin[0]) / (boundsMax[0] - boundsMin[0])
                                    v = (planeInter.point [2] - boundsMin[2]) / (boundsMax[2] - boundsMin[2])

                                elif abs(plane.normal[2]) > 0:
                                    u = (planeInter.point [0] - boundsMin[0]) / (boundsMax[0] - boundsMin[0])
                                    v = (planeInter.point [1] - boundsMin[1]) / (boundsMax[1] - boundsMin[1])

                                uvs = [u, v]

        if intersect is None:
            return None

        return Intersect(distance = intersect.distance,
                         point = intersect.point,
                         normal = intersect.normal,
                         texCoords = uvs,
                         sceneObject = self)


# https://github.com/tobycyanide/pytracer/blob/master/raytracer/shapes.py
class Cylinder(object):

    def __init__(self, radius, height, center, material):
        self.radius = radius
        self.height = height
        self.closed = False
        self.center = center
        self.material = material

    def ray_intersect(self, origin, direction):
        a = direction[0] ** 2 + direction[2] ** 2
        if abs(a) < 0.0001: #epsilon = 0.0001
            return None

        b = 2 * (
            direction[0] * (origin[0] - self.center[0])
            + direction[2] * (origin[2] - self.center[2])
        )
        c = (
            (origin[0] - self.center[0]) ** 2
            + (origin[2] - self.center[2]) ** 2
            - (self.radius ** 2)
        )

        discriminant = b ** 2 - 4 * (a * c)

        if discriminant < 0.0:
            return None

        t0 = (-b - sqrt(discriminant)) / (2 * a)
        t1 = (-b + sqrt(discriminant)) / (2 * a)

        if t0 > t1:
            t0, t1, t1, t0

        y0 = origin[1] + t0 * direction[1]
        if self.center[1] < y0 and y0 <= (self.center[1] + self.height):
            hit = sumVectors(origin, multiply(t0, direction))
            normal = frobeniusNorm(subVectors(hit, self.center))
            return Intersect(distance = t0,
                             point = hit,
                             normal = normal,
                             texCoords = None,
                             sceneObject = self)

        y1 = origin[1] + t1 * direction[1]
        if self.center[1] < y1 and y1 <= (self.center[1] + self.height):
            hit = sumVectors(origin, multiply(t1, direction))
            normal = frobeniusNorm(subVectors(hit, self.center))
            return Intersect(distance=t1,
                             point = hit,
                             normal = normal,
                             texCoords = None,
                             sceneObject = self)

        return self.intersect_caps(origin, direction)

    def check_cap(self, origin, direction, t):
        x = origin[0] + t * direction[0]
        z = origin[2] + t * direction[2]
        return (x ** 2 + z ** 2) <= abs(self.radius)

    def intersect_caps(self, origin, direction):
        if self.closed == False or abs(direction[1]) < 0.0001: #epsilon = 0.0001
            return None

        t_lower = (self.center[1] - origin[1]) / direction[1]
        if self.check_cap(origin, direction, t_lower):
            hit = sumVectors(origin, multiply(t_lower, direction))
            normal = frobeniusNorm(subVectors(hit, self.center))

            return Intersect(distance = t_lower,
                             point = hit,
                             normal = normal,
                             texCoords = None,
                             sceneObject = self)

        t_upper = ((self.center[1] + self.height) - origin[1]) / direction[1]
        if self.check_cap(origin, direction, t_upper):
            hit = sumVectors(origin, multiply(t_upper, direction))
            normal = frobeniusNorm(subVectors(hit, self.center))

            return Intersect(distance = t_upper,
                             point=hit,
                             normal=normal,
                             texCoords = None,
                             sceneObject = self)

        return None
        

class Triangle(object):

    def __init__(self, vertices, material):
        self.vertices = vertices
        self.material = material

    def ray_intersect(self, origin, direction):
        v0, v1, v2 = self.vertices
        normal = cross(subVectors(v1, v0), subVectors(v2, v0))
        determinant = dotVectors(normal, direction)

        if abs(determinant) < 0.0001:
            return None

        distance = dotVectors(normal, v0)
        t = (dotVectors(normal, origin) + distance) / determinant
        if t < 0:
            return None

        point = sumVectors(origin, multiply(t, direction))
        u, v, w = barycentric(v0, v1, v2, point)

        if w < 0 or v < 0 or u < 0:
            return None
        
        return Intersect(distance = distance,
                         point = point,
                         normal = frobeniusNorm(normal),
                         texCoords = None,
                         sceneObject = self)


class Pyramid(object):

    def __init__(self, vertices, material):
        self.sides = self.generate_sides(vertices, material)
        self.material = material

    def generate_sides(self, vertices, material):
        if len(vertices) != 4:
            return [None, None, None, None]

        v0, v1, v2, v3 = vertices
        sides = [
            Triangle([v0, v3, v2], material),
            Triangle([v0, v1, v2], material),
            Triangle([v1, v3, v2], material),
            Triangle([v0, v1, v3], material),
        ]
        return sides

    def ray_intersect(self, origin, direction):
        t = float("inf")
        intersect = None

        for triangle in self.sides:
            local_intersect = triangle.ray_intersect(origin, direction)
            if local_intersect is not None:
                if local_intersect.distance < t:
                    t = local_intersect.distance
                    intersect = local_intersect

        return intersect