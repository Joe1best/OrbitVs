import numpy as np
import matplotlib.pyplot as plt

def magnitude(v1):
    """
    Calculates the magnitude of v1 (vector)
    """
    return np.sqrt(v1[0]**2+v1[1]**2)

def vectorBtw(pos1,pos2):
    """
    Calculates and returns the vector between object one and object two. 
    """
    return [pos2[0]-pos1[0],pos2[1]-pos1[1]]

class Planet:
    def __init__(self,mass,ecc,r0,w,star,radius):
        self.mass = mass
        self.ecc = ecc
        self.r0 = r0
        self.w = w
        self.star = star
        self.radius = radius
    
    def orbit(dt,e,f):
        return 0 

class Star: 
    def __init__(self,mass,radius):
        self.mass = mass
        self.radius = radius