# OrbitVs

Generating some Lissajou Figures using orbital mechanics. Fun things to do when up late at night. We only assume elliptical and circular orbits as the other types of orbits will not be pertinent for the objective of this code.

## Generating a Star System 
A star system needs...well... a star first! We first generate a type **Star**. Then, we can start generating planets belonging to any star we created using the **Planet** class. Finally, using the Planets and star we have created, we can generate a type **System**. All of this can be found in [starSystems.py](https://github.com/Joe1best/OrbitVs/blob/master/starSystems.py). Using the **Plotting** class (which is essentially the main part of this project, found [here](https://github.com/Joe1best/OrbitVs/blob/master/main.py)) we can visualize the system that we have created. Below is an example of two planets having a frequency of rotation of 0.25Hz and 0.75Hz 

<img src = "https://github.com/Joe1best/OrbitVs/blob/master/README_examples/Random%20Star%20System.gif" width=500 height=400>

### Equations

We use kepler's third law, which states that the radius of orbit (or semi-major axis in case of an ellipse) <a href="https://www.codecogs.com/eqnedit.php?latex=a" target="_blank"><img src="https://latex.codecogs.com/gif.latex?a" title="a" /></a> is 

<a href="https://www.codecogs.com/eqnedit.php?latex=a\approx\left(\frac{GMT^2}{4\pi^2}\right)^{\frac{1}{3}}" target="_blank"><img src="https://latex.codecogs.com/gif.latex?a\approx\left(\frac{GMT^2}{4\pi^2}\right)^{\frac{1}{3}}" title="a\approx\left(\frac{GMT^2}{4\pi^2}\right)^{\frac{1}{3}}" /></a>,

where <a href="https://www.codecogs.com/eqnedit.php?latex=T" target="_blank"><img src="https://latex.codecogs.com/gif.latex?T" title="T" /></a> is the period of rotation (a given), <a href="https://www.codecogs.com/eqnedit.php?latex=G" target="_blank"><img src="https://latex.codecogs.com/gif.latex?G" title="G" /></a> the gravitational constant (which is always set to 1 because we dont care about units hehe), and <a href="https://www.codecogs.com/eqnedit.php?latex=M" target="_blank"><img src="https://latex.codecogs.com/gif.latex?M" title="M" /></a> is the mass of the star (again set to 1 because I am a physicist and I don't care about units). 

#### Cicular orbits 
Use polar coordinates now that we have the radius;

<a href="https://www.codecogs.com/eqnedit.php?latex=x&space;=&space;\left(\frac{GMT^2}{4\pi^2}\right)^{\frac{1}{3}}\cos\left(\frac{2\pi}{T}t&plus;\phi\right)&space;\quad&space;\quad&space;y&space;=&space;\left(\frac{GMT^2}{4\pi^2}\right)^{\frac{1}{3}}\sin\left(\frac{2\pi}{T}t&plus;\phi\right)" target="_blank"><img src="https://latex.codecogs.com/gif.latex?x&space;=&space;\left(\frac{GMT^2}{4\pi^2}\right)^{\frac{1}{3}}\cos\left(\frac{2\pi}{T}t&plus;\phi\right)&space;\quad&space;\quad&space;y&space;=&space;\left(\frac{GMT^2}{4\pi^2}\right)^{\frac{1}{3}}\sin\left(\frac{2\pi}{T}t&plus;\phi\right)" title="x = \left(\frac{GMT^2}{4\pi^2}\right)^{\frac{1}{3}}\cos\left(\frac{2\pi}{T}t+\phi\right) \quad \quad y = \left(\frac{GMT^2}{4\pi^2}\right)^{\frac{1}{3}}\sin\left(\frac{2\pi}{T}t+\phi\right)" /></a>.

#### Elliptical orbits
For this case, it is a lit bit more complicated than the circular case. Another variable has to be introduced which is the eccentricity, denote <a href="https://www.codecogs.com/eqnedit.php?latex=e" target="_blank"><img src="https://latex.codecogs.com/gif.latex?e" title="e" /></a>. The radius of orbit changes with angle with the following relationship,

<a href="https://www.codecogs.com/eqnedit.php?latex=r&space;=&space;\frac{a(1-e^2)}{1&plus;e\cos(\theta)}&space;=&space;\left(\frac{GMT^2}{4\pi^2}\right)^{\frac{1}{3}}\frac{(1-e^2)}{1&plus;e\cos(\theta)}" target="_blank"><img src="https://latex.codecogs.com/gif.latex?r&space;=&space;\frac{a(1-e^2)}{1&plus;e\cos(\theta)}&space;=&space;\left(\frac{GMT^2}{4\pi^2}\right)^{\frac{1}{3}}\frac{(1-e^2)}{1&plus;e\cos(\theta)}" title="r = \frac{a(1-e^2)}{1+e\cos(\theta)} = \left(\frac{GMT^2}{4\pi^2}\right)^{\frac{1}{3}}\frac{(1-e^2)}{1+e\cos(\theta)}" /></a>.

Finally, we can convert this to cartesian, 

<a href="https://www.codecogs.com/eqnedit.php?latex=x&space;=&space;\left(\frac{GMT^2}{4\pi^2}\right)^{\frac{1}{3}}\frac{(1-e^2)}{1&plus;e\cos(\frac{2\pi}{T}t&plus;\phi)}\cos\left(\frac{2\pi}{T}t&plus;\phi\right&space;)&space;\quad&space;\quad&space;y&space;=&space;\left(\frac{GMT^2}{4\pi^2}\right)^{\frac{1}{3}}\frac{(1-e^2)}{1&plus;e\cos(\frac{2\pi}{T}t&plus;\phi)}\sin\left(\frac{2\pi}{T}t&plus;\phi\right&space;)" target="_blank"><img src="https://latex.codecogs.com/gif.latex?x&space;=&space;\left(\frac{GMT^2}{4\pi^2}\right)^{\frac{1}{3}}\frac{(1-e^2)}{1&plus;e\cos(\frac{2\pi}{T}t&plus;\phi)}\cos\left(\frac{2\pi}{T}t&plus;\phi\right&space;)&space;\quad&space;\quad&space;y&space;=&space;\left(\frac{GMT^2}{4\pi^2}\right)^{\frac{1}{3}}\frac{(1-e^2)}{1&plus;e\cos(\frac{2\pi}{T}t&plus;\phi)}\sin\left(\frac{2\pi}{T}t&plus;\phi\right&space;)" title="x = \left(\frac{GMT^2}{4\pi^2}\right)^{\frac{1}{3}}\frac{(1-e^2)}{1+e\cos(\frac{2\pi}{T}t+\phi)}\cos\left(\frac{2\pi}{T}t+\phi\right ) \quad \quad y = \left(\frac{GMT^2}{4\pi^2}\right)^{\frac{1}{3}}\frac{(1-e^2)}{1+e\cos(\frac{2\pi}{T}t+\phi)}\sin\left(\frac{2\pi}{T}t+\phi\right )" /></a>,

and generate the orbits with different times <a href="https://www.codecogs.com/eqnedit.php?latex=t" target="_blank"><img src="https://latex.codecogs.com/gif.latex?t" title="t" /></a> and an initial condition <a href="https://www.codecogs.com/eqnedit.php?latex=\phi" target="_blank"><img src="https://latex.codecogs.com/gif.latex?\phi" title="\phi" /></a>.

## Lissajou Figures
This project serves to create Lissajou figures from orbits of various planets (some could be made-up and some could be real life planets in our solar system). How we do this? We just connect two planets together with a line and see what happens... Here is an example of the previous two planets but now with a line connecting them: 

<img src = "https://github.com/Joe1best/OrbitVs/blob/master/README_examples/A-B.gif" width=500 height=400>

Examples are now done with the Earth connected to different planets in our solar system, the final result can be seen in this [folder](https://github.com/Joe1best/OrbitVs/tree/master/Simulation_results_pics)
