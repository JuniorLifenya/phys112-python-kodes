
import numpy as np 

########################################################################

## Now ULTIMATELY we look at SYSTEMS of vector ode #############

# This code solves a system of ordinary differential equations using the Runge-Kutta method.
# For systems like this one here :
# dx/dt = f(t,x,y,z) = x + 2 * y
# dy/dt = g(t,x,y,z) = 3*x+2*y

########################################################################

# Define the function for the system of ODEs

def f(t,x,y):
    return 3*x +  y
def g(t,x,y):
    return x + 2 * y

def Runge_Kutta_system(t0,t1,x0,y0,h,n):

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

        K2 = f(ti + h/2, xi + h*K1/2, yi + h*G1)
        G2 = g(ti + h/2, xi + h*K1/2, yi + h*G1)


        x[i+1] = x[i] + h/2 * (K1 + K2)
        y[i+1] = y[i] + h/2 * (G1 + G2 )
        t[i+1] = t[i] + h 
    return t,x,y

t0 = 0.0
t1 = 0.9
x0 = 0.3
y0 = 5.0
h = 0.1
n = int ((t1 - t0) / h) # Antall steg

t_verdi,x_verdi,y_verdi = Runge_Kutta_system(t0,t1,x0,y0,h,n)
print("Tid:", t_verdi)

# Siste verdi av x og y etter siste iterasjon, altså etter t = 0.9 sekunder
print("x(t):", x_verdi[-1])  
print("y(t):", y_verdi[-1])  

