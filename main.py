import numpy as np
import matplotlib.pyplot as plt
from random import random

#G = 6.674*10**(-11)
G = 1
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
    def __init__(self,typeOfOrbit,star,frequency):
        self.typeOfOrbit = typeOfOrbit
        self.star = star
        self.frequency = frequency
        if (typeOfOrbit == 'circular'):
            self.eccen = 0
        elif (typeOfOrbit == 'elliptical'):
            self.eccen = random()
        self.r = self.findR()
    
    def findR(self):
        """
        Function that calculates the radius given the type of orbit. This method only 
        accepts circular and elliptical type at the moment. If the orbit is elliptical
        it returns two parameters; the semi-major axis and the semi-minor axis.
        """
        T = self.frequency
        if (self.typeOfOrbit == 'circular'):
            return (T**2*G*self.star.mass/4*np.pi**2)**(1/3)
        elif (self.typeOfOrbit == 'elliptical'):
            return [(T**2*G*self.star.mass/4*np.pi**2)**(1/3), np.sqrt((T**2*G*self.star.mass/4*np.pi**2)**(2/3)*(1-self.eccen**2))]
        return [0,0]

    def orbit(self,t):   
        """
        Returns the orbit position as a function of time
        """ 
        if (self.typeOfOrbit == 'circular'):
            return [self.r*np.cos(2*np.pi*self.frequency*t), self.r*np.sin(2*np.pi*self.frequency*t)]
        elif (self.typeOfOrbit == 'elliptical'):
            return [self.r[0]*(1-self.eccen**2)/(1+self.eccen*np.cos(2*np.pi*self.frequency*t))*np.cos(2*np.pi*self.frequency*t),
                            self.r[0]*(1-self.eccen**2)/(1+self.eccen*np.cos(2*np.pi*self.frequency*t))*np.sin(2*np.pi*self.frequency*t)]

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
        self.planets = [Planet(planet[i][0],planet[i][1],planet[i][2]) for i in range(len(planet))]
        self.star = Star(star[0],star[1])

s = Star(1,1)
b = Planet('circular',s,2)
b2 = Planet('elliptical',s,2)
x=[]
y=[]

x2 = []
y2= []
t = np.linspace(0,1/2)
for time in t:
    x.append(b.orbit(time)[0])
    y.append(b.orbit(time)[1])
    x2.append(b2.orbit(time)[0])
    y2.append(b2.orbit(time)[1])
plt.plot(x,y)	
plt.plot(x2,y2)
plt.show()
