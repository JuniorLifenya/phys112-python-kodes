import math as m 
import numpy as np 
import matplotlib.pyplot as plt


#####################################################################################################

## Now we use the example from the geeks for geeks website #############

# dy/dx = (x-y)/2 Example #
# x0 = 0, y0 = 1, xf = 2, h = 0.2; #


#####################################################################################################

def dydx(x,y):
    return (x-y)/2

def runge_kutta_calc(x0 ,y0,xf ,h ): # Alternative specify the datatype x0 : float

    delta = (xf-x0)/h
    n = int ((delta))
    
    y = y0 
    for i in range(1, n+1,1) : 
    
        k1 = float(h*dydx(x0,y))
        k2 = float(h* dydx(x0 + h/2, y + k1/2))
        k3 = float(h*dydx(x0 + h/2, y + k2/2))
        k4 = float(h* dydx(x0 + h, y+k3))
        
        y += (k1 + 2*k2 + 2*k3 + k4)/6.0
        x0 +=  h 
    return y
    
# Now we test 

print(runge_kutta_calc(0,1,2,0.2))
    
# Expected output:  1.10364 


#####################################################################################################
## Now Extended for stuff like dydx = (sinx-5y^2)/3
# Expected output: Scalar RK4: y(0.9) = -1261.5, The code over will be reused also

# Vector‐based RK4 storing t[0…n], y[0…n]
def dydx(x,y):
    return (m.sin(x)-5*y**2)/3

def rungeKuttaVector(x0,y0,xf,h):
    # Initialize the arrays for the output
    n = int((xf-x0)/h)
    t = np.zeros(n+1) # Instead of including them as vector-arguments in the functions
    y = np.zeros(n+1) # This is how YOU INITIALIZE EMPTY ARRAYS in python , they become filled later

    t[0] = x0
    y[0] = y0 

    for i in range(0,n,1): # Could have just written range(n) also hehe 
        ti = t[i]
        yi = y[i]
        k1 = dydx(ti,yi)
        k2 = dydx(ti + h/2, yi + k1/2)
        k3 = dydx(ti + h/2, yi + k2/2)
        k4 = dydx(ti + h, yi + h*k3)
        y[i+1] = yi + h* (k1 + 2*k2 + 2*k3 + k4)/6.0
        t[i+1] = ti + h
    return t,y

# Now we test
x0, y0, xf, h = 0.3 , 5.0 , 0.9 , 0.3

t , y = rungeKuttaVector(x0, y0, xf, h) # This returns a two things vector like stuff like v = (t,y)
print(f" Vector RK4: y({xf}) = {y}") # Prints out vector state for a give time value 

y_scalar = runge_kutta_calc(x0, y0, xf, h) # Vector code using 
print (f"Scalar RK4: y(0.9) = {y_scalar}")

#####################################################################################################
plt.plot(t, y, marker='o')
plt.title("RK4: Solving dy/dx = (sin(x) - 5y²)/3")
plt.xlabel("x")
plt.ylabel("y")
plt.grid(True)
plt.show()

#####################################################################################################