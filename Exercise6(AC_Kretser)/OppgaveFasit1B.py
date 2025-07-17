
import numpy as np
import matplotlib.pyplot as plt

# Definerer kretsparametere
R = 10  # Motstand i ohm
C = 300e-6  # Kapasitans i farad
L = 0.2      # Induktans i henry
C = 100e-6   # Kapasitans i farad
t_slutt = 0.5  # Sluttidspunkt i sekunder

t0 = 0.0
q0 = 0.0
i0 = 1.0  
h = 0.01  # Steglengde i sekunder
n = int((t_slutt-t0) / h)  # Antall tidspunkter
##################################################################################################
def f(t, state):
    x, y = state
    dxdt = y 
    dydt = -R/L*y - x/(L*C)
    return np.array([dxdt, dydt])

# RK4‐step:
def rk4_step(f, t, state, h):
    K1 = f(t, state)
    K2 = f(t+h/2, state + h*K1/2)
    K3 = f(t+h/2, state + h*K2/2)
    K4 = f(t+h,   state + h*K3)
    return state + h*(K1 + 2*K2 + 2*K3 + K4)/6

# Simuler:
t, state = 0.0, np.array([q0, i0])
for i in range(n):
    state = rk4_step(f, t, state, h)
    t += h
# state inneholder [q(2.5), dq/dt(2.5)]

print(f"Q(2.5) = {state[0]:.2f} C", f"I(2.5) = {state[1]:.2f} A")

##########################################################################################################

### Alternative fasit #######################

def f(t,x,y): #dydt
    return -R/L*y - x/(L*C)
def g(t,x,y): #dxdt
    return y
    
def Runge_Kutta_system(t0,t_slutt,q0,i0,h,n):

    n = int ((t_slutt - t0) / h) # Antall steg
    t = np.zeros(n+1) 
    x = np.zeros(n+1) 
    y = np.zeros(n+1)  

    t[0],x[0],y[0] = t0 , q0 , i0
    
    for i in range (n):

        ti,xi,yi = t[i], x[i],  y[i]

        K1 = f(ti,xi,yi)
        G1 = g(ti,xi,yi)

        K2 = f(ti + h/2, xi + h*G1/2, yi + h*K1/2)
        G2 = g(ti + h/2, xi + h*G1/2, yi + h*K1/2)

        K3 = f(ti + h/2, xi + h*G2/2, yi + h*K2/2)
        G3 = g(ti + h/2, xi + h*G2/2, yi + h*K2/2)

        K4 = f(ti + h, xi + h*G3, yi + h*K3)
        G4 = g(ti + h, xi + h*G3, yi + h*K3)

        y[i+1] = yi + h/6 * (K1 + 2*K2 + 2*K3 + K4)
        x[i+1] = xi + h/6 * (G1 + 2*G2 + 2*G3 + G4)
        t[i+1] = ti + h 

    return t,x,y


t_verdier , x_verdier , y_verdier = Runge_Kutta_system(0.0,t_slutt, q0,i0,h,n)
print(f"Ønsket Q(2.5) = {x_verdier[-1]:.2f} C, Ønsket I(2.5) = {y_verdier[-1]:.2f} A")