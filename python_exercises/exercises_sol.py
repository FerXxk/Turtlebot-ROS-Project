# %% [markdown]
# # Practical Session 2: Introduction to Python
# 
# ## Laboratorio de Robótica 
# ### Grado en Ingeniería Electrónica, Mecatrónica y Robótica
# ### Universidad de Sevilla

# %% [markdown]
# ## Objectives
# 
# The objective of this notebook is to propose some exercises to practise with Python and get familiar with data types, loops, functions, classes, and so on.
# 
# After completing the missing code in this notebook, export it as a Python script. You can do that both using Jupyther Notebook or through the Jupyter extension in VS Code. Then name your file `exercises_sol.py` and commit it to your course Github repository, into a folder named `python_exercises`.

# %% [markdown]
# ### Exercise 1
# 
# Define a function called `squares` that, given a list `sec` of numbers, returns a list with the squares of those numbers, in the same order.

# %%
# Examples:

# squares([2, -1.2, 3e2, 1j]) should return [4, 1.44, 90000.0, (-1+0j)]
# squares(i for i in range(10)) should return [0, 1, 4, 9, 16, 25, 36, 49, 64, 81]

# %%
def squares(k):
    l=[]
    for x in k:
        l.append(x**2)
    return l


squares([2,1,14,3,7])
squares(i for i in range(10))

# %% [markdown]
# ### Exercise 2
# 
# A positive integer is said to be perfect if it coincides with the sum of all its proper divisors (that is, other than itself). Define a function called `write_perfect` that, given two positive integers `m` $\leq$ `n`, returns a list with all the perfect numbers within the interval `[m, n]`. The function should also print on the screen each perfect number and its divisors. 

# %%
# Examples:

# write_perfect(1, 1000) should write on screen:
# Number 6 is perfect and its divisors are [1, 2, 3]
# Number 28 is perfect and its divisors are [1, 2, 4, 7, 14]
# Number 496 is perfect and its divisors are [1, 2, 4, 8, 16, 31, 62, 124, 248]

# %%
def write_perfect(m,n):
    
    for num in range(m,n+1):
        divisores = []
        
        for x in range(1,num):
            if(num % x == 0):
                divisores.append(x)
                
                   

        sum=0
        for x in divisores:
            sum+=x
    
        if(sum==num):
            print("Number "+ str(num) +" is perfect and its divisors are"+ str(divisores) )



write_perfect(1,1000)

# %% [markdown]
# ### Exercise 3
# 
# Consider a dictionary whose keys are character strings of length one and the associated values ​​are non-negative integers, such as the following dictionary `d`:

# %%
d = {'a': 5, 'b': 10, 'c': 12, 'd': 11, 'e': 15, 'f': 20, 'g': 15, 'h': 9, 'i': 7, 'j': 2}

# %% [markdown]
# Define a function called `horizontal_histogram` that, given a dictionary of the previous type, writes the associated histogram of horizontal bars on the screen, printing the bars from top to bottom in the order determined by the `sorted` function on the keys, as illustrated in the following example:

# %%
# horizontal_histogram(d)
# a: *****
# b: **********
# c: ************
# d: ***********
# e: ***************
# f: ********************
# g: ***************
# h: *********
# i: *******
# j: **

# %%
def horizontal_histogram(d):
    for i in d:
        h=d[i]
        l=i+": "
        for j in range(0,h):
            l+="*"
        print(l)


d = {'a': 5, 'b': 10, 'c': 12, 'd': 11, 'e': 15, 'f': 20, 'g': 15, 'h': 9, 'i': 7, 'j': 2}
horizontal_histogram(d)

# %% [markdown]
# ### Exercise 4
# 
# Suppose we want to simulate the trajectory of a drone that is launched at a given point with a certain initial height. The drone is launched forward with an initial speed and at a certain angle without propulsion motors on. Initially it will advance upwards, but due to the force of gravity, at a given moment it will begin to descend until it lands. For simplicity, we will assume that there is no friction or wind resistance.
# 
# Define a class `Drone` that represents the state of the drone at a given instant of time. At least, the class should include attributes to store the following data:
# + Traveled distance traveled (horizontally)
# + Height
# + Horizontal speed
# + Vertical speed
# 
# In addition, apart from its constructor, the class should have the following three methods:
# + `get_pos_x`: it returns the horizontal traveled distance 
# + `get_pos_y`: it returns the vertical traveled distance 
# + `update_position`: given a number `t` of seconds, it updates the position and velocity of the projectile after that time has elapsed
# 
# Once the `Drone` class is defined, define an external function called `land` that, given the `height` (meters), `velocity` (meters per second), `angle` (degrees) and time `step` (seconds), prints on the screen the different positions of a drone launched with that initial `height`, `velocity` and `angle`. The position of the drone should be displayed at each `step` of time, until it lands. The function should also print the maximum height reached by the drone, the total distance traveled horizontally and the time and number of steps that it took it to land.
# 
# Indications:
# 1. If the drone has an initial velocity $v$ and is launched at an angle $\theta$, the horizontal and vertical components of the initial velocity are $v \times \cos(\theta)$ and $v \times \ sin(\theta)$, respectively.
# 2. The horizontal component of velocity, in the absence of friction and wind, will remain constant.
# 3. The vertical component of the velocity evolves throughout time: if $vy_0$ is the initial vertical velocity, after a time step $t$, the velocity will be $vy_1 = vy_0 - 9.8 \times t$, due to the Earth's gravity.
# 4. Also, if $h_0$ is the initial drone height, after a time step $t$, the height will be $h_1 = h_0 + vm \times t$, where $vm$ is the average between the previous $vy_0$ and $vy_1$.

# %%
# Example:

# land(30, 1, 20, 0.1)
# Drone at position(0.0, 30.0)
# Drone at position(0.1, 30.0)
# Drone at position(0.2, 29.9)
# Drone at position(0.3, 29.7)
# Drone at position(0.4, 29.4)
# Drone at position(0.5, 28.9)
# Drone at position(0.6, 28.4)
# Drone at position(0.7, 27.8)
# Drone at position(0.8, 27.1)
# Drone at position(0.8, 26.3)
# Drone at position(0.9, 25.4)
# Drone at position(1.0, 24.4)
# Drone at position(1.1, 23.4)
# Drone at position(1.2, 22.2)
# Drone at position(1.3, 20.9)
# Drone at position(1.4, 19.5)
# Drone at position(1.5, 18.0)
# Drone at position(1.6, 16.4)
# Drone at position(1.7, 14.7)
# Drone at position(1.8, 13.0)
# Drone at position(1.9, 11.1)
# Drone at position(2.0, 9.1)
# Drone at position(2.1, 7.0)
# Drone at position(2.2, 4.9)
# Drone at position(2.3, 2.6)
# Drone at position(2.3, 0.2)

# After 26 steps of 0.1 seconds (2.6 seconds), the drone has landed.
# It has traveled a distance of 2.4 meters.
# It has reached a maximum height of 30.0 meters.

# %%

class Drone:
    def __init__(self, distance, height, xspeed, yspeed):
        
        self.distance = distance
        self.height = height
        self.xspeed = xspeed
        self.yspeed = yspeed


    def get_pos_x(self): 
        print(f"The horizontal travelled distance is {self.distance} metres")

    def get_pos_y(self): 
        print(f"The vertical travelled distance is {self.height} metres")

    def update_position(self,t): 
        y=self.height+self.yspeed*t
        x=self.distance + self.xspeed*t
        print(f"The position of the drone is ({x}, {y})")




Dron=Drone(20,30,40,50)
Dron.get_pos_x()
Dron.get_pos_y()
Dron.update_position(5)

import math
def land(h0,v0,theta,step):
    thetar=math.radians(theta)
    vx=v0*math.cos(thetar)
    vy=v0*math.sin(thetar)
    print(vx,vy)
    tmax=vy/9.8
    ymax=h0+vy*tmax- 4.9* (tmax**2)
    tcaida=(-vy-math.sqrt(vy*vy+4*4.9*h0))/(-2*4.9)
    y=h0
    t=0
    count=0
    while y>=0:
        
        x=vx*t
        y=h0+vy*t- 4.9* (t**2)
        t+=step
        if(y>=0):
            count+=1
            print(f"Drone at position( {x:.2f} ,{y:.2f})")

    print(f"After {count:.2f} steps of {step:.2f} seconds ({tcaida:.2f} seconds), the drone has landed.")
    print(f"It has traveled a distance of {vx*tcaida:.2f}  meters.")
    print(f"It has reached a maximum height of {ymax:.2f} meters.")
        


land(30, 1, 20, 0.1)



# %% [markdown]
# ### Exercise 5
# 
# Define a function called `matrix_operation` that receives an integer `n` as argument. The function should create a NumPy array (vector) with the integers within the interval $[n,n+25)$ and perform the following operations:
# 
# + Calculate the mean and standard deviation of the array and print it on the screen.
# + Reshape the array into a 5x5 matrix, calculate the determinant of the matrix and print the result on the screen.
# + Return a tuple with the three computed values `(mean, std, determinant)`.

# %%
# Example

# matrix_operation(1)
# The mean and standard deviation of the vector is 13.0 +/- 7.211102550927978.
# The determinant of the matrix is 0.0.

# %%
def matrix_operation(d):
    import numpy as np
    l=np.arange(d,d+25)
    m=np.mean(l)
    sd=np.std(l)
    print("The mean and standard deviation of the vector is ",m," +/- ",sd,".")
    l=np.reshape(l,(5,5))
    det=np.linalg.det(l)
    print("The determinant of the matrix is ",det,".")
    tp=(m,sd,det)
    return tp

import numpy as np



tp=matrix_operation(12)



# %% [markdown]
# ### Exercise 6
# 
# Create a function called `plot_functions` that makes a figure and plot the following functions over the range $[0, 10]$:
# 
# + $y_1 = sin(x)$
# + $y_2 = cos(x)$
# 
# The figure should also include appropriate labels, title, and a legend.

# %%


def plot_functions():

    import matplotlib.pyplot as plt
    import numpy as np
    x=np.linspace(0,10,100)
    y1=np.sin(x)
    y2=np.cos(x)

    plt.plot(x, y1)
    plt.plot(x,y2)
    plt.xlabel('Radianes')
    plt.xlim([0,10])
    plt.legend(['seno','coseno'])
    plt.title('Funciones trigonométricas')
    plt.grid('on')
    plt.show()

plot_functions()



# %%
