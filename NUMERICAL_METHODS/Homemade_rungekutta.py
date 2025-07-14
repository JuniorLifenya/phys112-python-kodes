import math as m 
import numpy as np 
import matplotlib.pyplot as plt


#####################################################################################################

## Now we use the example from the geeks for geeks website #############

# dy/dx = (x-y)/2 Example #
# x0 = 0, y0 = 1, xf = 2, h = 0.2; #


#####################################################################################################

def f(x,y): #dydx
    return (x-y)/2

def runge_kutta_calc(x0 ,y0,x1 ,h ): # Alternative specify the datatype x0 : float

    delta = (x1-x0)/h
    n = int ((delta))
    
    y = y0 
    for i in range(n):
    
        k1 = f(x0,y)

        k2 = f(x0 + h/2, y + h*k1/2)
        k3 = f(x0 + h/2, y + h*k2/2)
        k4 = f(x0 + h , y + h*k3)

        y += h*(k1 + 2*k2 + 2*k3 + k4)/6.0
        x0 += h 
    return y
    
# Now we test 

print(runge_kutta_calc(0,1,2,0.2))
    
# Expected output:  1.10364 


#####################################################################################################
## Now Extended for stuff like dydx = (sinx-5y^2)/3
# Expected output: Scalar RK4: y(0.9) = -1261.5, The code over will be reused also

import numpy as np
import matplotlib.pyplot as plt

# Differensialligning: dy/dx = (sin(x) - 5y^2)/3
def f(x, y):
    return (np.sin(x) - 5 * y**2) / 3

# RK4 vektorimplementering
def rungeKuttaVector(x0, y0, xf, h):
    n = int((xf - x0) / h)
    x = np.zeros(n + 1)
    y = np.zeros(n + 1)
    x[0] = x0
    y[0] = y0
    for i in range(n):
        xi = x[i]
        yi = y[i]
        k1 = f(xi, yi)
        k2 = f(xi + h/2, yi + h*k1/2)
        k3 = f(xi + h/2, yi + h*k2/2)
        k4 = f(xi + h, yi + h*k3)
        y[i + 1] = yi + h * (k1 + 2*k2 + 2*k3 + k4) / 6.0
        x[i + 1] = xi + h
    return x, y

# Testverdier
x0, y0, xf, h = 0.3, 5.0, 0.9, 0.1  # Mindre h for bedre nøyaktighet
x, y = rungeKuttaVector(x0, y0, xf, h)
ha = 0.01 # Forbedret h verdi 
xa, ya = rungeKuttaVector(x0, y0, xf, ha) # Forbedret RK4
print(f"Vector RK4: y({xf}) = {y[-1]:.4f}")


#####################################################################################################
# Plotting
plt.figure(figsize=(10, 6))
plt.plot(x, y, label=f"RK4-løsning(h = {h})", color="blue", marker='o', markersize=3)
plt.plot(xa, ya, label=f"Forbedret_RK4-løsning(h = {ha})", color="red", marker='o', markersize=3)
plt.title(r"Solving $\frac{dy}{dx} = \frac{\sin(x) - 5y^2}{3}$ with RK4")
plt.xlabel("x")
plt.ylabel("y")
plt.grid(True)
plt.legend()
plt.show()

#####################################################################################################