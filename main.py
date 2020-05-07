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
    def __init__(self,typeOfOrbit,star,frequency,initCond,name,eccen=None):
        self.typeOfOrbit = typeOfOrbit
        self.star = star
        self.frequency = frequency
        self.name = name
        if (typeOfOrbit == 'circular'):
            self.eccen = 0
        elif (typeOfOrbit == 'elliptical'):
            if (eccen==None):
                self.eccen = random()
            else: 
                self.eccen = eccen
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
    def __init__(self,starSystem,nsteps,duration,connectingPlanets = None,saveFile=None):
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
        fig = plt.figure(figsize=(20,15))
        ax = plt.axes(xlim=(self.limits[0]+0.1*self.limits[0],self.limits[2]+0.1*self.limits[2]),
                ylim=(self.limits[1]+0.1*self.limits[1],self.limits[3]+0.1*self.limits[3]))
        
         #Hiding the axes
        ax.axes.xaxis.set_visible(False)
        ax.axes.yaxis.set_visible(False)
        
        #Drawing the outline of the trajectory 
        data = [p.drawOrbit() for p in self.ss.planets]

        for (i,p) in zip(range(len(self.ss.planets)),self.ss.planets):
            plt.plot(data[i][0],data[i][1],'--',color = self.colors[i])
        
        #Drawing the star
        plt.plot(0,0,'*',color = 'orange',markeredgecolor='black',markersize=13)
        
        #Title depending on the purpose of the plot
        if (connectingPlanets==None):
            plt.title("Random Solar System",fontsize=25)
        else:
            plt.title(connectingPlanets[0].name+ " and "+connectingPlanets[1].name+" orbit",fontsize=25)
        
        #The object in our plot that will be animated
        ptcls = [ax.plot([],[],'.',markersize=20,color=self.colors[_],markeredgecolor='black',zorder=10)[0] for _ in range(len(self.ss.planets))]

        t = np.linspace(0,self.duration,self.nsteps)
    
        def init():
            for ptcl in ptcls:
                ptcl.set_data([], [])
            return ptcls
        
        def animate(i):
            #Updates the figure with the new points for each planet
            for (p,ptcl) in zip(self.ss.planets,ptcls): 
                xdata = p.orbit(t[i])[0] 
                ydata = p.orbit(t[i])[1] 
                ptcl.set_data(xdata,ydata)

            if (connectingPlanets != None):
                #gets all the current data on the graph 
                data = np.zeros([len(self.ss.planets),2])
                for (i,ptcl) in zip(range(len(self.ss.planets)),ptcls):
                    data[i][0] = ptcl.get_xdata()
                    data[i][1] = ptcl.get_ydata()

                #Figures out which index the planets that we want to connect are in 
                #the data array 
                index = []
                for i in range(len(self.ss.planets)):
                    if (self.ss.planets[i]==connectingPlanets[0] or self.ss.planets[i] == connectingPlanets[1]):
                        index.append(i)

                #Gives us the line equation parameters
                a,b = self.connectTwoPlanets(data[index[0]],data[index[1]],t[i])
                
                minx = min([data[index[0]][0],data[index[1]][0]])
                maxx = max([data[index[0]][0],data[index[1]][0]])
                x = np.linspace(minx,maxx,100,endpoint=True)
                plt.plot(x,a*x+b,'-',color='black')
            

            return ptcls
        ani = an.FuncAnimation(fig,animate,init_func = init,interval=1,frames=nsteps,blit=True)
         #If we do not want to save, just show the animation
        if (saveFile!=None):
            #Saves the animation
            ani.save(save+".gif",writer="pillow")

            #Saves the last snapshot of the figure
            fig.savefig(save+".svg", format='svg', dpi=1200)
            fig.savefig(save+".png", format='png', dpi=1200)

            plt.close()
        else:
            plt.show()
        
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
    
    def connectTwoPlanets(self,p1,p2,t):
        """
        Function that will draw a line between two given planet coordinates p1 and p2 at time t
        returns the parameters (a,b) in the line equation ax+b that passes through both points
        """

        a = (p2[1]-p1[1])/(p2[0]-p1[0])
        b = p2[1]- a*p2[0]
        return a,b




s = Star(1,1)
#plt.ion()

numPlanets = 10
typeOforbit = ['circular', 'elliptical']
#Frequencies of planets relative to Earth (which is 1)
freq1 = 4.15   #Mercury
freq2 = 1.62   #Venus
freq3 = 1      #Earth
freq4 = 0.53   #Mars
freq5 = 0.084  #Jupiter
freq6 = 0.0344 #Saturn
#Eccentricity values were googled and inputted here. 
a = Planet(typeOforbit[1],s,freq1,[0,0],"Mercury",eccen=0.206)
b = Planet(typeOforbit[1],s,freq2,[0,0],"Venus",eccen=0.007)
c = Planet(typeOforbit[1],s,freq3,[0,0],"Earth",eccen = 0.017)
d = Planet(typeOforbit[1],s,freq4,[0,0],"Mars",eccen = 0.093)
e = Planet(typeOforbit[1],s,freq5,[0,0],"Jupiter",eccen = 0.0484)
f = Planet(typeOforbit[1],s,freq6,[0,0],"Saturn",eccen = 0.054)
#Mars duration
#Resolution; the more, the longer it takes! 
#nsteps = 1100

#Duration of the simulation
#duration= 17

#Venus duration
#nsteps = 1100
#duration = 15

#Mercury duration
#nsteps = 1100
#duration = 7

#Jupiter duration
#nsteps = 1100
#duration = 24

#Saturn duration
nsteps = 600
duration = 30

ss = System([a,b,c,d,e,f],s)
save = "Saturn-Jupiter"
Plotting(ss,nsteps,duration,connectingPlanets=[e,f],saveFile=save)
