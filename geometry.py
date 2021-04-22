# Author: ROK, Rippmann Oesterle Knauss GmbH, Silvan Oesterle
# Web: http://www.rok-office.com
# Description: Pure python geometry library. Fast 3d Vector classes. 
# Based on ROK designlib.geometry. No binary dependencies allowed.

import math
import random


EPSILON = 1e-10


class __Object3Base__(object):
    __slots__ = ('x', 'y', 'z')
    __hash__ = None
    
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

    def __copy__(self):
        return self.__class__(self.x, self.y, self.z)
    
    def __eq__(self, other):
        return self.x == other.x and self.y == other.y and self.z == other.z

    def __ne__(self, other):
        return not self.__eq__(other)
    
    def __len__(self):
        """Returns the number of elements."""
        return 3
    
    def __iter__(self):
        return iter((self.x, self.y, self.z))
    
    def __getitem__(self, i):
        if i == 0:
            return self.x
        elif i == 1:
            return self.y
        elif i == 2:
            return self.z
        else:
            raise IndexError('Index out of range')

    def __setitem__(self, i, val):
        if i == 0:
            self.x = val
        elif i == 1:
            self.y = val
        elif i == 2:
            self.z = val
        else:
            raise IndexError('Index out of range')

    
class Vector3(__Object3Base__):    
    """
    x,y,z (float): Vector components
    """
    def __repr__(self):
        return u'Vector3: <{0}, {1}, {2}>'.format(
            self.x, self.y, self.z)
    
    def __nonzero__(self):
        """A zero vector will return None."""
        return self.x != 0 or self.y != 0 or self.z != 0    
    
    def __add__(self, other):
        """Return new Vector3 added self + other.""" 
        return Vector3(self.x + other.x, self.y + other.y, self.z + other.z)
    
    def __iadd__(self, other):
        """Adds other to self in place and returns self."""
        self.x += other.x
        self.y += other.y
        self.z += other.z
        return self
    
    def __sub__(self, other):
        """Return new Vector3 subtracted self - other."""
        return Vector3(self.x - other.x, self.y - other.y, self.z - other.z)
    
    def __isub__(self, other):
        """Subtracts other from self in place and returns self."""
        self.x -= other.x
        self.y -= other.y
        self.z -= other.z
        return self
    
    def __mul__(self, scalar):
        """
        Returns new Vector3. Scales the vector by scalar.
        scalar (int, float)
        return (Vector3)
        """
        return Vector3(self.x * scalar, self.y * scalar, self.z * scalar)
    
    __rmul__ = __mul__
    
    def __imul__(self, scalar):
        """Multiplies self in place with scalar and returns self."""
        self.x *= scalar
        self.y *= scalar
        self.z *= scalar
        return self
    
    def __neg__(self):
        """Unary -. Returns reversed version of self."""
        return Vector3(-self.x, -self.y, -self.z)
    
    @property
    def length_sqrd(self):
        """Squared length of the vector (faster than length)."""
        return self.x ** 2 + self.y ** 2 + self.z ** 2
    
    @property
    def length(self):
        """Length of the vector."""
        return math.sqrt(self.x ** 2 + self.y ** 2 + self.z ** 2)

    def dot(self, other):
        """
        Dot prodct of the vector with other vector.
        other (Vector3)
        return (int, float)
        """
        return self.x * other.x + self.y * other.y + self.z * other.z

    def cross(self, other):
        """
        Cross product of the vector with other vector.
        other (Vector3)
        return (Vector3)
        """
        return Vector3(self.y * other.z - self.z * other.y,
                       -self.x * other.z + self.z * other.x,
                       self.x * other.y - self.y * other.x)
    
    def scale(self, scalar):
        """In place scaling of the vector."""
        self.x *= scalar
        self.y *= scalar
        self.z *= scalar
        return self
    
    def normalize(self):
        """In place normalization of the vector (unit vector)."""
        d = self.length
        if d:
            self.x /= d
            self.y /= d
            self.z /= d
            return self
        raise RuntimeError('Zero vector, can not be normalized')
    
    def normalized(self):
        """Returns a normalized (unit vector) copy of self"""
        d = self.length
        if d:
            return Vector3(self.x / d, 
                           self.y / d,
                           self.z / d)
        raise RuntimeError('Zero vector, can not be normalized')
        
    def angle_rad(self, other):
        """
        Angle between two vectors in radians (0-180).
        other (Vector3)
        return (float)
        """
        d = self.dot(other.normalized())
        # Fixes floating point arithmetic errors that could lead to the dot being
        # out of bounds -1, 1. This clamps to the bounds
        if d < -1: d = -1
        elif d > 1: d = 1
        return math.acos(d)
    
    def angle_deg(self, other):
        """
        Angle between two vectors in degress (0-180).
        other (Vector3)
        return (float)
        """
        return self.angle_rad(other) * (180/math.pi)

    def rotate(self, angle, axis):
            """
            Rotation via Rodriguez formula.
            angle (double): The rotation angle in radians.
            axis (Vector3): Has to be normalized (unitized).
            """
            c = math.cos(angle)
            s = math.sin(angle)
            return c * self + s * axis.cross(self) + self.dot(axis) * (1-c) * axis    


class Point3(__Object3Base__):
    def __repr__(self):
        return u'Point3: <{0}, {1}, {2}>'.format(
            self.x, self.y, self.z)


# ------------------------------------------------------------------------------
# 3d Vector functions
def vect3_divide(v1, f):
    """
    Divides vector v1 by scalar f.
    v1 (3-tuple): 3d vector
    f (float): Scalar
    return (3-tuple): 3d vector
    """
    return (v1[0] / f, v1[1] / f, v1[2] / f)
    
    
def vect3_add(v1, v2):
    """
    Adds two 3d vectors.
    v1, v2 (3-tuple): 3d vectors
    return (3-tuple): 3d vector
    """ 
    return (v1[0]+v2[0], v1[1]+v2[1], v1[2]+v2[2])


def vect3_subtract(v1, v2):
    """
    Subtracts one 3d vector from another.
    v1, v2 (3-tuple): 3d vectors
    return (3-tuple): 3d vector
    """ 
    return (v1[0]-v2[0], v1[1]-v2[1], v1[2]-v2[2])


def vect3_pow(v):
    """
    Vector power.
    v (3-tuple): 3d vector
    return (float): the dot product of v.v
    """
    return vect3_dot(v, v)


def vect3_cross(u, v):
    """
    Cross product.
    u, v (3-tuple): 3d vectors
    return (3-tuple): 3d vector
    """
    return (u[1] * v[2] - u[2] * v[1], 
            u[2] * v[0] - u[0] * v[2], 
            u[0] * v[1] - u[1] * v[0])


def vect3_dot(u, v):
    """
    u.v, dot (scalar) product.
    u, v (3-tuple): 3d vectors
    return (float): dot product
    """
    return u[0] * v[0] + u[1] * v[1] + u[2] * v[2]


def vect3_length(v):
    """
    True length of a 3d vector.
    v (3-tuple): 3d vector
    return (float): length
    """ 
    return math.sqrt(v[0] ** 2 + v[1] ** 2 + v[2] ** 2)


def vect3_length_sqrd(v):
    """
    Squared length of a 3d vector.
    v (3-tuple): 3d vector
    return (float): squared length
    """ 
    return v[0] ** 2 + v[1] ** 2 + v[2] ** 2


def vect3_scale(v, f):
    """
    Scales a vector by factor f.
    v (3-tuple): 3d vector
    f (float): scale factor
    return (3-tuple): 3d vector
    """
    return (v[0]*f, v[1]*f, v[2]*f)


def vect3_normalized(v):
    """
    Normalize a vector.
    v (3-tuple): 3d vector
    return (3-tuple): 3d vector
    """
    d = float(vect3_length(v))
    return (v[0]/d, v[1]/d, v[2]/d)


def vect3_angle_rad(u, v):
    """
    Angle between two vectors in radians (0-180).
    v1, v2 (3-tuple): 3d vectors
    return (float): angle
    """
    d = vect3_dot(vect3_normalized(u), vect3_normalized(v))
    # Fixes floating point arithmetic errors that could lead to the dot being
    # out of bounds -1, 1. This clamps to the bounds
    if d < -1: d = -1
    elif d > 1: d = 1
    return math.acos(d)


def vect3_angle_deg(u, v):
    """
    Angle between two vectors in degress (0-180).
    v1, v2 (3-tuple): 3d vectors
    return (float): angle
    """
    return vect3_angle_rad(u, v) * (180/math.pi)


def vect3_reverse(v):
    """
    Reverses a 3d vector.
    v (3-tuple): 3d vector
    return (3-tuple): 3d vector
    """
    return (v[0]*-1, v[1]*-1, v[2]*-1)


def vect3_bisector(v1, v2):
    """
    Gives the bisector vector of v1, v2
    v1, v2 (3-tuple): 3d vectors
    return (3-tuple): 3d vector
    """
    return vect3_add(vect3_normalized(v1), vect3_normalized(v2))


def vect3_rotate(v, angle, axis):
        """
        Rotation via Rodriguez formula.
        v (3-tuple): The vector to rotate
        angle (double): The rotation angle in radians.
        axis (3-tuple): Has to be normalized (unitized).
        """
        v = Vector3(*v)
        v.rotate(angle, Vector3(*axis))
        return (v.x, v.y, v.z)
