import numpy as np
import matplotlib.pyplot as plt
from random import random
import matplotlib.animation as an 


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
    def __init__(self,typeOfOrbit,star,frequency,initCond,name):
        self.typeOfOrbit = typeOfOrbit
        self.star = star
        self.frequency = frequency
        self.name = name
        if (typeOfOrbit == 'circular'):
            self.eccen = 0
        elif (typeOfOrbit == 'elliptical'):
            self.eccen = random()
        self.r = self.findR()
        self.initCond = initCond
    
    def findR(self):
        """
        Function that calculates the radius given the type of orbit. This method only 
        accepts circular and elliptical type at the moment. If the orbit is elliptical
        it returns two parameters; the semi-major axis and the semi-minor axis.
        """
        T = 1/self.frequency
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
            return [self.r*np.cos(2*np.pi*self.frequency*t+self.initCond[0]), self.r*np.sin(2*np.pi*self.frequency*t+self.initCond[1])]
        elif (self.typeOfOrbit == 'elliptical'):
            return [self.r[0]*(1-self.eccen**2)/(1+self.eccen*np.cos(2*np.pi*self.frequency*t+self.initCond[0]))*np.cos(2*np.pi*self.frequency*t+self.initCond[0]),
                            self.r[0]*(1-self.eccen**2)/(1+self.eccen*np.cos(2*np.pi*self.frequency*t+self.initCond[1]))*np.sin(2*np.pi*self.frequency*t+self.initCond[1])]
    def drawOrbit(self):
        time = np.linspace(0,1/self.frequency,300)
        xdata, ydata = [], []
        for t in time: 
            xdata.append(self.orbit(t)[0])
            ydata.append(self.orbit(t)[1])
        return xdata,ydata



class Star: 
    def __init__(self,mass,radius):
        self.mass = mass
        self.radius = radius

class System: 
    def __init__(self,planets,star):
        """
        Input: Array of planet specifications (planet)
               Array of star specifications (star)
        """
        self.planets = planets
        self.star = star
    
class Plotting:
    def __init__(self,starSystem,nsteps,duration):
        #Declaring some variables
        self.ss = starSystem

        #Number of steps in the simulation
        self.nsteps = nsteps

        #How long the simulation lasts
        self.duration = duration

        #Parameters needed to calculate the length of the x and y axis 
        #for the animations
        par = self.findMaxMin()
        
        #Setting the limits 
        self.limits = [min(par[0,:]), min(par[1,:]), max(par[2,:]), max(par[3,:])]
        
        #Colors for each planet
        self.colors = plt.cm.rainbow(np.linspace(0,1,len(self.ss.planets)))
    
        #Animation stuffs 
        fig = plt.figure()
        ax = plt.axes(xlim=(self.limits[0]+0.1*self.limits[0],self.limits[2]+0.1*self.limits[2]),
                ylim=(self.limits[1]+0.1*self.limits[1],self.limits[3]+0.1*self.limits[3]))
        #Drawing the outline of the trajectory 
        data = [p.drawOrbit() for p in self.ss.planets]

        for (i,p) in zip(range(len(self.ss.planets)),self.ss.planets):
            plt.plot(data[i][0],data[i][1],'--',color = self.colors[i])
        
        #Drawing the star
        plt.plot(0,0,'*',color = 'orange',markeredgecolor='black',markersize=13)
        
        ptcls = [ax.plot([],[],'.',markersize=10,color=self.colors[_],markeredgecolor='black')[0] for _ in range(len(self.ss.planets))]

        t = np.linspace(0,self.duration,self.nsteps)
    
        def init():
            for ptcl in ptcls:
                ptcl.set_data([], [])
            return ptcls
        
        def animate(i):
            for (p,ptcl) in zip(self.ss.planets,ptcls): 
                xdata = p.orbit(t[i])[0] 
                ydata = p.orbit(t[i])[1] 
                ptcl.set_data(xdata,ydata)
            return ptcls

        ani = an.FuncAnimation(fig,animate,init_func = init,interval=15,frames=200,blit=True)
        ani.save("test.gif",writer="pillow")

    def findMaxMin(self):
        limits = np.zeros([4,len(self.ss.planets)])
        i = 0 
        for p in self.ss.planets:
            x,y = p.drawOrbit()
            limits[0][i] = min(x)
            limits[1][i] = min(y)
            limits[2][i] = max(x)
            limits[3][i] = max(y)
            i+=1
        return limits

s = Star(1,1)
#plt.ion()

numPlanets = 10
typeOforbit = ['circular', 'elliptical']
freq1 = 2
freq2 = 5
freq3 = 4
freq4 = 30
b = Planet('elliptical',s,freq1,[0,0],"Planet A")
c = Planet('circular',s,freq2,[2,2],"Planet B")
d = Planet('circular',s,freq3,[1.4,1.4],"Planet C")
e = Planet('circular',s,freq4,[5,5],"Planet D")

nsteps = 400
duration= 1
ss = System([b,c,d,e],s)

Plotting(ss,nsteps,duration)
