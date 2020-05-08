import numpy as np

G = 1

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
    

    def __str__(self):
        return self.name

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
    def __init__(self,mass,radius,name):
        self.mass = mass
        self.radius = radius
        self.name = name

class System: 
    def __init__(self,p=None, s=None, name=None):
        """
        Input: Array of planet specifications (p)
               Array of star specifications (s)
               Name: A specific name of a solar system that exists out there.
        """
        if (p!=None and s!=None):
            self.numPlanets = len(p)
            self.planets = p
            self.star = s

        elif (name=='solar system'):
            #Dont really work in units here, so the sun is going to have a radius 1 and mass 1 
            self.star = Star(1,1,'Sun')
            self.numPlanets = 8
            #Frequencies of planets relative to Earth (which is 1)
            freq = [4.15,1.62,1,0.53,0.084,0.0344,0.01189,0.00606]   
            names = ['Mercury', 'Venus', 'Earth', 'Mars', 'Jupiter', 'Saturn', 'Uranus', 'Neptune']
            eccen = [0.206,0.007,0.017,0.093,0.048,0.056,0.047,0.009,0.248]
            #Eccentricity values were googled and inputted here. 
            self.planets = [Planet('elliptical',self.star,freq[i],[0,0],names[i],eccen=eccen[i]) for i in range(self.numPlanets)]
        elif (name=='HD 158259'):
            #Dont really work in units here, so the sun is going to have a radius 1 and mass 1 
            self.star = Star(1,1,'HD 158259')
            self.numPlanets = 5
            #Frequencies of planets relative to HD 158259 d (which is 1)
            freq = [2.3636,1.5294,1,0.65,0.43333]   
            names = ['HD 158259 b', 'HD 158259 c', 'HD 158259 d', 'HD 158259 e', 'HD 158259 f']
            #Eccentricity values were googled and inputted here. 
            self.planets = [Planet('circular',self.star,freq[i],[0,0],names[i]) for i in range(self.numPlanets)]

    def __str__(self):  
        """
        String method used when printing each system. This will print it in the form of 
        Star name: [STAR NAME]. Planets: [LIST OF PLANETS]
        #TO DO: 
            - make this print details about each planet. Need to re-implement the planet __str__ method 
        """
        string = "Star name: " + self.star.name + ". Planets names:" 
        for i in range(self.numPlanets):
            if (i == 0):
                string+=" "+ self.planets[0].name
            elif (i==self.numPlanets-1):
                string+= ", " + self.planets[-1].name
            else: 
                string+= ", " + self.planets[i].name
        return string