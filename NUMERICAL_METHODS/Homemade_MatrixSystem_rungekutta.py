import math as m 
import numpy as np 
import matplotlib.pyplot as plt

########################################################################

## Now ULTIMATELY we look at SYSTEMS of vector ode #############

# This code solves a system of ordinary differential equations using the Runge-Kutta method.
# For systems like this one here :
# dx/dt = f(t,x,y,z) = x + 2 * y
# dy/dt = g(t,x,y,z) = 3*x+2*y

########################################################################

# Define the function for the system of ODEs

def f(t,x,y):
    return x + 2 * y
def g(t,x,y):
    return 3 * x + 2 * y



def Runge_Kutta_system(t0,t1,x0,y0,h,n):

    n = int ((t1 - t0) / h) # Antall steg
    
    t = np.zeros(n+1)
    x = np.zeros(n+1)
    y = np.zeros(n+1)

    t[0] = t0
    x[0] = x0 
    y[0] = y0
    for i in range (n):
        ti = t[i]
        xi = x[i]
        yi = y[i]

        K1 = f(ti,xi,yi)
        G1 = g(ti,xi,yi)

        K2 = f(ti + h/2, xi + h*K1/2, yi + h*G1/2)
        G2 = g(ti + h/2, xi + h*K1/2, yi + h*G1/2)

        K3 = f(ti + h/2, xi + h*K2/2, yi + h*G2/2)
        G3 = g(ti + h/2, xi + h*K2/2, yi + h*G2/2)

        K4 = f(ti + h , xi + h*K3, yi + h*G3)
        G4 = g(ti + h , xi + h*K3, yi + h*G3)

        x[i+1] = x[i] + h/6 * (K1 + 2*K2 + 2*K3 + K4)
        y[i+1] = y[i] + h/6 * (G1 + 2*G2 + 2*G3 + G4)
        t[i+1] = t[i] + h 
    return t,x,y

t,t1,x, y = Runge_Kutta_system(0.0,5.0, 6.0,4.0, 0.02)

# Convert to Python lists
t_list = t.tolist()
x_list = x.tolist()
y_list = y.tolist()
print("t =", t_list[:20])
print("x =", x_list[:20])
print("y =", y_list[:20])

#####################################################################