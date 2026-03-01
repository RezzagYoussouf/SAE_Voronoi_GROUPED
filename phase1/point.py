from math import sqrt
import matplotlib.pyplot as plt
import numpy as np

class Point:

    def __init__(self, x, y, name=None):
        self._x = x
        self._y = y
        self._name = name
    
    def return_distance (self,autre_point):
        distance = sqrt((autre_point.x - self._x)**2 + (autre_point.y - self._y)**2)
        return distance
    
    @property
    def x(self):
        return self._x
    
    @property
    def y(self):
        return self._y
    
    @x.setter
    def x(self, value):
        self._x = value
    
    @y.setter
    def y(self, value):
        self._y = value
    
    def __str__(self):
        return f"Point({self._x}, {self._y})"
    

