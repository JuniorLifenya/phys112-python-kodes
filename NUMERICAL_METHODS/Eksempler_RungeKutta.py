import numpy as np


def f(x,y): #dydx
    return (x-y)/2

def runge_kutta_calc(x0 ,y0,x1 ,h ): # Alternative specify the datatype x0 : float

    delta = (x1-x0)/h
    n = int ((delta))
    
    y = y0 
    for i in range(n) : 
    
        k1 = f(x0,y)
        k2 = f(x0 + h/2, y + h*k1/2)
        
        y += (h/2.0)*(k1 + k2 )
        x0 +=  h 
    return y
    
# Now we test 

print(runge_kutta_calc(0,1,2,0.2))
# Expected output:  1.07546

################################################################################################

import numpy as np
import matplotlib.pyplot as plt

# Differensialligning: dy/dx = (sin(x) - 5y^2)/3
def dydx(x, y):
    return (np.sin(x) - 5 * y**2) / 3

# RK4 vektorimplementering
def rungeKuttaVector(x0, y0, x1, h):
    n = int((x1- x0) / h)
    x = np.zeros(n + 1)
    y = np.zeros(n + 1)
    x[0] = x0
    y[0] = y0
    for i in range(n):
        xi = x[i]
        yi = y[i]

        k1 = dydx(xi, yi)
        k2 = dydx(xi + h/2, yi + h*k1/2)
        k3 = dydx(xi + h/2, yi + h*k2/2)
        
        y[i + 1] = yi + h * (k1 + 4*k2 + k3 ) / 6.0
        x[i + 1] = xi + h
    return x, y

# Testverdier
x0, y0, x1, h = 0.3, 5.0, 0.9, 0.3  # Mindre h for bedre nøyaktighet
x, y = rungeKuttaVector(x0, y0, x1, h)
print(f"Vector RK4: y({x1}) = {y[-1]:.4f}")

################################################################################################

## Nå utvider vi til x'' = -x' + 6x til systemet:
# x' = v 
# v' = -y + 6x

import numpy as np
import matplotlib.pyplot as plt

def f(t,x, v): # dx/dt = v 
    return v
def g(t,x, v): # dy/dt = -v + 6x
    return -v + 6 * x
# RK4 vektorimplementering
def rungeKuttaVector(t0,t1,x0,v0, h):
    n = int((t1 - t0) / h)
    t = np.zeros(n+1)
    x = np.zeros(n+1)
    v = np.zeros(n+1)

    t[0] = t0
    x[0] = x0 
    v[0] = v0
    for i in range (n):
        ti = t[i]
        xi = x[i]
        vi = v[i]

        K1 = f(ti,xi,vi)
        G1 = g(ti,xi,vi)

        K2 = f(ti + h/2, xi + h*K1/2, vi + h*G1/2)
        G2 = g(ti + h/2, xi + h*K1/2, vi + h*G1/2)

        K3 = f(ti + h/2, xi + h*K2/2, vi + h*G2/2)
        G3 = g(ti + h/2, xi + h*K2/2, vi + h*G2/2)

        K4 = f(ti + h , xi + h*K3, vi + h*G3)
        G4 = g(ti + h , xi + h*K3, vi + h*G3)

        x[i+1] = x[i] + h/6 * (K1 + 2*K2 + 2*K3 + K4)
        v[i+1] = v[i] + h/6 * (G1 + 2*G2 + 2*G3 + G4)
        t[i+1] = t[i] + h 
    return t,x,v

# Initialverdier
t0, t1 = 0.0, 2.0
x0, v0 = 0.0, 1.0
h = 0.5

# Løsning med grov h
t, x, v = rungeKuttaVector(t0, t1, x0, v0, h) # Der [x,v] er tilstanden 2 sekunder
print(f"RK4 med h = {h}: x'({t1}) = {v[-1]:.4f}")

################################################################################################
# Plotting
plt.figure(figsize=(10, 6))
plt.plot(t, 2/5*np.exp(2*t)+3/5*np.exp(-3*t), label='v(t): Faktisk funk.')
plt.plot(t, v, label=f"v(t), RK4 metod(h={h})", linestyle='--', marker='x')
plt.plot(t, 1/5*np.exp(2*t)-1/5*np.exp(-3*t), label='x(t): Faktisk funk.', )
plt.plot(t, x, label=f'x(t): RK4 metode(h={h})', linestyle='dashed', marker='x')

plt.title(r"Løsning av $x'' = -x' + 6x$ med RK4")
plt.xlabel("t")
plt.ylabel("x(t) og x'(t)")
plt.grid(True)
plt.legend()
plt.show()