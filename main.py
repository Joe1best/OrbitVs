import numpy as np
import matplotlib.pyplot as plt

G = 6.674*10**(-11)

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
    def __init__(self,mass,ecc,r0,star,radius,v0):
        self.mass = mass
        self.r0 = r0
        self.v0 = v0
        self.star = star
        self.l = self.mass*self.r0**2*(self.v0/self/r0)
        self.radius = radius
        self.ecc = self.eccen(self.totalEnergy(),self.l,self.mass,G*self.star.mass)

    def totalEnergy(self):
        return (1/2)*self.mass*self.v0**2 - G*self.star.mass*self.mass/self.r0

    def orbit(self,dtheta,l,m,u,E):   
        """
        Returns the orbit as a function of theta depending on the physical 
        parameters of the planet
        Input: dtheta (float): true anomaly of the system
               m (float): mass of the body 
               u: G*M (float) where G is the gravitational constant and M is the mass of the star
               E: total energy of the system
        """     
        c = l**2/(m**2*u)
        e = self.ecc
        return c*(1/(1+e*np.cos(dtheta)))

    def eccen(self,E,l,m,u):
        """
        Returns the eccentricity of the planet 
        Input: l (float) angular momentum of the body
               m (float) mass of the body 
               u: G*M (float) where G is the gravitational constant and M is the mass of the star
        """
        return np.sqrt(1+(2*E*l**2/(m**3*u**2)))

class Star: 
    def __init__(self,mass,radius):
        self.mass = mass
        self.radius = radius

class system: 
    def __init__(self,planet,star):
        """
        Input: Array of planet specifications (planet)
               Array of star specifications (star)
        """
        self.planets = [Planet(planet[i][0],planet[i][1],planet[i][2],planet[i][3],planet[i][4],planet[i][5]) for i in range(len(planet))]
        self.star = Star(star[0],star[1])