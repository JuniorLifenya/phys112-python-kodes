import math as m 
import numpy as np 
import matplotlib.pyplot as plt

#############################################################################################
#############################################################################################

## Now ULTIMATELY we look at SYSTEMS of vector ode #############

# This code solves a system of ordinary differential equations using the Runge-Kutta method.
# For systems like this one here :
# dx/dt = f(t,x,y,z) = x + 2 * y
# dy/dt = g(t,x,y,z) = 3*x+2*y

#############################################################################################
#############################################################################################

q = 1.0
m = 0.45
B0 = 2.0 # Changes for how many steps with have full revolution
k = 0.2

# Initial values
v0 = np.array([0.0, 1.0])  # vx0, vy0
r0 = np.array([0.0, 0.0])  # x0, y0
t0 = 0.0
h = 0.05
tf = 10.0  # End time
n = int((tf - t0) / h)  # Number of steps
#############################################################################################
#############################################################################################
# Define the functions for the system of ODEs

def B_felt(t,r):
    x, y = r
    var_B= [0.0,0.0,1 + 0.5 * np.sin(x) + 0.3 * np.cos(y)] # Spiral motion 
    return np.array(var_B) 

def f(t, r, v): # dv/dt = (q/m) * v x B 
    B = B_felt(t, r)
    v3d = np.array([v[0], v[1], 0.0])
    bforce = q/m * np.cross(v3d, B)
    gravforce = np.array([0.0, 0.0, -9.81])  # Gravity force in z direction
    dragforce = k * v  # gamma = damping coefficient
    Ftot = bforce[:2] + gravforce[:2] + dragforce  # Total force including gravity and damping
    return Ftot
# This function returns the Lorentz force and damping force as a 2D vector, written as
# Ftot= (q/m) * v x B + (-gamma * v) + gforce

#############################################################################################
#############################################################################################

def g(t, r, v): #drdt really 
    return v

def Runge_Kutta_system(t0,r0,v0,h,n):

    #t0,tf = 0.0 , 20.0
    #n= int((tf - t0) / h) #Alternative 
    
    t = np.zeros(n+1)
    r = np.zeros((n+1,2))
    v = np.zeros((n+1,2))

    t[0] = t0
    r[0] = r0 
    v[0] = v0
    for i in range (n):
        ti = t[i]
        ri = r[i]
        vi = v[i]

        K1 = f(ti,ri,vi)
        G1 = g(ti,ri,vi)

        K2 = f(ti + h/2, ri + h*G1/2, vi + h*K1/2)
        G2 = g(ti + h/2, ri + h*G1/2, vi + h*K1/2)

        K3 = f(ti + h/2, ri + h*G2/2, vi + h*K2/2)
        G3 = g(ti + h/2, ri + h*K2/2, vi + h*G2/2)

        K4 = f(ti + h , ri + h*G3, vi + h*K3)
        G4 = g(ti + h , ri + h*G3, vi + h*K3)

        t[i+1] = t[i] + h 
        v[i+1] = v[i] + h/6 * (K1 + 2*K2 + 2*K3 + K4)
        r[i+1] = r[i] + h/6 * (G1 + 2*G2 + 2*G3 + G4)
        
    return t,r,v

#############################################################################################
#############################################################################################



# Run simulation
t_vals, r_vals, v_vals = Runge_Kutta_system(t0, r0, v0, h,n)

# Plot trajectory
x_vals = r_vals[:, 0]
y_vals = r_vals[:, 1]


#############################################################################################
     
fig, ax = plt.subplots(figsize=(10, 5))
# Moving animation man 
from matplotlib.animation import FuncAnimation
line, = ax.plot([], [], '-', color="green")
def animate(i):
    line.set_data(r_vals[:i,0], r_vals[:i,1])
    return line,

ani = FuncAnimation(fig, animate, frames=len(t_vals), 
                    interval=30, blit=True)

ax.plot(x_vals, y_vals, '-', linewidth=1.5, label='Trajectory', color  = "green")
ax.scatter([r0[0]], [r0[1]],c='red', s=50, label='Start')
ax.scatter([x_vals[-1]], [y_vals[-1]], c='b', s=50, label='End')
ax.legend()

plt.plot(x_vals, y_vals,color= "orange") # type: ignore
plt.title(f" Partikkel-varierende Bane med (h= {h}) etter {tf} sekunder")
plt.xlabel("x (m)")
plt.ylabel("y (m)")
plt.grid(True)
plt.savefig("Partikkel-drag_Bane(50s).png", dpi=300, bbox_inches='tight')
plt.show()


#############################################################################################
#############################################################################################

