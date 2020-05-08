import numpy as np
import matplotlib.pyplot as plt
from random import random
import matplotlib.animation as an 
import starSystems as st
import sys 

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
    
class Plotting:
    def __init__(self,starSystem,nsteps,duration,connectingPlanets = None,saveFile=True,ignorePlanet=None):
        #Declaring some variables
        self.ss = starSystem
        
        #Ignoring the planets that we want to ignore in the animation 
        newPlanets = self.ss.planets.copy()
        if (ignorePlanet!=None):
            [newPlanets.remove(ignorePlanet[i]) for i in range(len(ignorePlanet))]
        
        #Number of steps in the simulation
        self.nsteps = nsteps

        #How long the simulation lasts
        self.duration = duration

        #Parameters needed to calculate the length of the x and y axis 
        #for the animations
        par = self.findMaxMin(newPlanets)
        
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
        elif (ignorePlanet!=None):
            plt.title(connectingPlanets[0].name+ " and "+ connectingPlanets[1].name+" Orbit Closeup",fontsize=25)
        else:
            plt.title(connectingPlanets[0].name+ " and "+connectingPlanets[1].name+" orbit",fontsize=25)
        
        #The object in our plot that will be animated
        ptcls = [ax.plot([],[],'.',markersize=20,color=self.colors[_],markeredgecolor='black',zorder=10)[0] for _ in range(len(newPlanets))]

        t = np.linspace(0,self.duration,self.nsteps)
    
        def init():
            for ptcl in ptcls:
                ptcl.set_data([], [])
            return ptcls
        
        if (connectingPlanets!=None):
            #Will save all the data in there
            data = np.zeros([len(connectingPlanets),2])

        def animate(i):
            #Updates the figure with the new points for each planet
            
            for (p,ptcl) in zip(newPlanets,ptcls): 
                xdata = p.orbit(t[i])[0] 
                ydata = p.orbit(t[i])[1] 
                ptcl.set_data(xdata,ydata)

            if (connectingPlanets != None):
                
                #Figures out which index the planets that we want to connect are in 
                #the data array 
                index = []
                for cp in connectingPlanets:
                    index.append(self.ss.planets.index(cp))
                
                #gets all the current data on the graph for the two planets that we want to connect
                for (p,j,m) in zip(connectingPlanets,index,range(len(connectingPlanets))):
                    data[m][0] = self.ss.planets[j].orbit(t[i])[0]
                    data[m][1] = self.ss.planets[j].orbit(t[i])[1]

                #Gives us the line equation parameters
                a,b = self.connectTwoPlanets(data[0],data[1])
                minx = min([data[0][0],data[1][0]])
                maxx = max([data[0][0],data[1][0]])
                x = np.linspace(minx,maxx,100,endpoint=True)
                plt.plot(x,a*x+b,'-',color='black')
            
            return ptcls
        
        ani = an.FuncAnimation(fig,animate,init_func = init,interval=1,frames=nsteps,blit=True)
        
        #If we do not want to save, just show the animation. If we do not want to save, we can just look 
        #at the animation
        if (saveFile):
            
            #Saves the animation
            if (connectingPlanets==None):
                ani.save("Random Star System.gif",writer="pillow")
            else:
                save = connectingPlanets[0].name + "-" + connectingPlanets[1].name
                ani.save(save+".gif",writer="pillow")
                
                #Saves the last snapshot of the figure as an svg 
                fig.savefig(save+".svg", format='svg', dpi=1200)
            plt.close()
        else:
            plt.show()
        
    def findMaxMin(self,newPlanets):
        limits = np.zeros([4,len(newPlanets)])
        i = 0 
        for p in newPlanets:
            x,y = p.drawOrbit()
            limits[0][i] = min(x)
            limits[1][i] = min(y)
            limits[2][i] = max(x)
            limits[3][i] = max(y)
            i+=1
        return limits
    
    def connectTwoPlanets(self,p1,p2):
        """
        Function that will draw a line between two given planet coordinates p1 and p2 at time t
        returns the parameters (a,b) in the line equation ax+b that passes through both points
        """

        a = (p2[1]-p1[1])/(p2[0]-p1[0])
        b = p2[1]- a*p2[0]
        return a,b


#########
#Simulation example
#########
#star1 = st.Star(1,1,'S')
#typeOfOrbit = 'circular'
#planet1 = st.Planet(typeOfOrbit,star1,0.25,[0,0],'A')
#planet2 = st.Planet(typeOfOrbit,star1,0.75,[0,0],'B')
#ss = st.System([planet1,planet2],star1)

nsteps = 650
duration = 10
#Plotting(ss,nsteps,duration)

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
#nsteps = 600
#duration = 30

ss = st.System(name='HD 158259')
planets = ss.planets

Plotting(ss,nsteps,duration,connectingPlanets=[planets[1],planets[3]])
