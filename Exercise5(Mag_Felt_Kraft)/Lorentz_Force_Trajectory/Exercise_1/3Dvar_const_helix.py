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
# Constants
q = 1.0 # Positive ladninger følger høyre håndsregelen her, negative følger venstre håndsregelen
m1 = .45
B0 = 1.0

# Initial values
v0 = np.array([0.0, 12.0, 2.0])  # vx, vy, vz
r0 = np.array([7.0, 0.0, 0.0])  # x, y, z

t0 = 0.0
tf = 8.0  # End time
h = 0.1
n= int((tf - t0) / h) #Alternative 
#############################################################################################
#############################################################################################
# Define the functions for the system of ODEs

def B_felt(t,r):
    x, y , z= r
    const_B = [0.0, 0.0, -B0]
    var_B= [0.0,0.0,1 + 0.5 * np.sin(x) + 0.3 * np.cos(y)]
    return np.array(var_B)  # Constant B in z# Lorentz force
def f(t, r, v):  
    B = B_felt(t, r)
    return (q / m1) * np.cross(v, B)

#############################################################################################
#############################################################################################

def g(t, r, v): #drdt really 
    return v

def Runge_Kutta_system(t0,r0,v0,h,n):
    
    t = np.zeros(n+1)
    r = np.zeros((n+1,3))
    v = np.zeros((n+1,3))

    t[0],r[0],v[0] = t0,r0,v0
    
    for i in range (n):
        ti,ri,vi = t[i], r[i], v[i]
       

        K1, G1 = f(ti,ri,vi), g(ti,ri,vi)

        K2 = f(ti + h/2, ri + h*G1/2, vi + h*K1/2)
        G2 = g(ti + h/2, ri + h*G1/2, vi + h*K1/2)

        K3 = f(ti + h/2, ri + h*G2/2, vi + h*K2/2)
        G3 = g(ti + h/2, ri + h*G2/2, vi + h*K2/2)

        K4 = f(ti + h , ri + h*G3, vi + h*K3)
        G4 = g(ti + h , ri + h*G3, vi + h*K3)

        t[i+1] = t[i] + h 
        v[i+1] = v[i] + h/6 * (K1 + 2*K2 + 2*K3 + K4)
        r[i+1] = r[i] + h/6 * (G1 + 2*G2 + 2*G3 + G4)
        
    return t,r,v

#############################################################################################
#############################################################################################

############################# For perfect sircle motion #####################################

#period = 2 * np.pi / (q * B0 / m)  # 2*pi / omega_c
#tf = period * 1  # for one full circle
#h = 0.01
#n = int(tf / h)
#################################################################

# Run simulation
t_vals, r_vals, v_vals = Runge_Kutta_system(t0, r0, v0, h,n) # Tilstanden etter n steg

# Plot trajectory
x_vals = r_vals[:, 0]
y_vals = r_vals[:, 1]
z_vals = r_vals[:, 2]

def kinetic_energy(v):
    return 0.5 * m1 * np.dot(v, v)

print("Initial KE:", kinetic_energy(v0))
print("Final KE:", kinetic_energy(v_vals[-1]))

# Plotting og animasjon
#############################################################################################
#############################################################################################

from mpl_toolkits.mplot3d import Axes3D
from matplotlib.animation import FuncAnimation

# 3D Plotting
fig = plt.figure(figsize=(10, 8))
ax = fig.add_subplot(111, projection='3d')

# Plot trajectory
ax.plot(x_vals, y_vals, z_vals, 'g-', linewidth=1.5, label='Trajectory')
ax.scatter([r0[0]], [r0[1]], [r0[2]], c='r', s=50, label='Start')
ax.scatter([x_vals[-1]], [y_vals[-1]], [z_vals[-1]], c='b', s=50, label='End')

# Animation setup
line, = ax.plot([], [], [], 'o-', color="r", markersize=6)
def animate(i):
    line.set_data(r_vals[:i, 0], r_vals[:i, 1])
    line.set_3d_properties(r_vals[:i, 2])
    return line,

# Create animation
ani = FuncAnimation(fig, animate, frames=len(t_vals), interval=30, blit=True)

ax.set_xlabel('X (m)')
ax.set_ylabel('Y (m)')
ax.set_zlabel('Z (m)')
ax.set_title(f'3D Charged Particle Motion in non-constant Magnetic Field after {tf} seconds')

# Set viewing angle for better perspective
ax.view_init(elev=30, azim=45)  # Elevation and azimuth angles

ax.legend()
ax.grid(True)
ani.save('3D_Partikkkel_Bane_varB.gif', writer='pillow', fps=20)
plt.show()


# At 627 iterations, the particle makes a perfect circle revolution, But Ek_0 != EK_f still decimals
#############################################################################################
#############################################################################################