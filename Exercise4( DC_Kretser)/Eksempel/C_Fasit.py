
import numpy as np 

########################################################################

## Now ULTIMATELY we look at SYSTEMS of vector ode #############

# This code solves a system of ordinary differential equations using the Runge-Kutta method.
# For systems like this one here :

# dy/dt = f(t,x,y,z) = 3x + y
# dx/dt = g(t,x,y,z) = x + 2y

########################################################################

# B) med Huens metode
def f(t,x,y):
    return 3*x +  y
def g(t,x,y):
    return x + 2 * y

def Huens_system(t0,t1,x0,y0,h,n):

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

        y_gjett = yi + h*K1
        x_gjett = xi + h*G1
        
        K2 = f(ti + h, x_gjett, y_gjett)
        G2 = g(ti + h, x_gjett, y_gjett)


        x[i+1] = xi + h/2 * (K1 + K2)
        y[i+1] = yi + h/2 * (G1 + G2 )
        t[i+1] = ti + h 
    return t,x,y

t0 = 0.0
t1 = 0.9
x0 = 0.3
y0 = 5.0
h = 0.1
n = int ((t1 - t0) / h) # Antall steg

t_verdi,x_verdi,y_verdi = Huens_system(t0,t1,x0,y0,h,n)
print("Tid:", t_verdi)

# Siste verdi av x og y etter siste iterasjon, altså etter t = 0.9 sekunder
print("x(t):", x_verdi[-1])  
print("y(t):", y_verdi[-1])  

######################################################################################################

# A) med Huens metode
import numpy as np


def f(x,y): #dydx = (3x-2y)/(x+2y)
    return (3*x+y)/(x+2*y)

def Huens_calc(x0,y0,x1 ,h ): # Her definerer vi metoden som skal brukes

    n = int ((x1-x0)/h)
    
    y = y0 
    for i in range(n) : 
    
        k1 = f(x0,y)
        y_gjett = y + h*k1

        k2 = f(x0 + h, y_gjett)
        
        y += (h/2.0)*(k1 + k2 )
        x0 +=  h # Siden vi ikke har en x-variabel i arrayet, så må vi oppdatere den manuelt,
        #I tillegg fordi antall steg n er definert av x1-x0/h så må x oppdateres
    return y
    
# Nå tester vis

print(Huens_calc(0.3,5.0,0.9,0.1))

#################################################################################

# Visualisering #

import matplotlib.pyplot as plt
plt.plot(t_verdi, x_verdi, label='x(t)')
plt.plot(t_verdi, y_verdi, label='y(t)')
plt.legend()
plt.grid(True)
plt.xlabel('Tid t')
plt.ylabel('Verdi')
plt.title('Løsning av systemet med Heun\'s metode')
plt.show()
