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
m1 = 0.45
B0 = 1.0

# Initial values
v0 = np.array([0.0, 5.0])  # vx0, vy0
r0 = np.array([7.0, 0.0])  # x0, y0
t0 = 0.0
tf = 50.0  # End time
h = 0.1
n= int((tf - t0) / h) #Alternative 
#############################################################################################
#############################################################################################
# Define the functions for the system of ODEs

def B_felt(t,r):
    x, y = r
    var_B= [0.0,0.0,1+0.5 * np.sin(x) + 0.3 * np.cos(y)]
    return np.array(var_B)  # Constant B in z
def f(t, r, v):  # dv/dt = (q/m) * v x B
    B = B_felt(t, r)
    v3d = np.array([v[0], v[1], 0.0])  # pad v to 3D
    cross = np.cross(v3d, B)
    return (q / m1) * cross[:2] # return only x,y parts (2D vector)

def g(t, r, v): #drdt really 
    return v

#############################################################################################
#############################################################################################
def Runge_Kutta_system(t0,r0,v0,h,n):
    
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


def kinetic_energy(v):
    return 0.5 * m1 * np.dot(v, v)

KE_initial = kinetic_energy(v0)
KE_final = kinetic_energy(v_vals[-1])

print(f"Initial kinetic energy: {KE_initial:.6f} J")
print(f"Final kinetic energy: {KE_final:.6f} J")
print(f"Energy difference: {KE_final - KE_initial:.6f} J")
print(f"Absolute energy difference: {abs(KE_final - KE_initial):.6f} J")
print(f"Relative energy difference: {abs(KE_final - KE_initial)/KE_initial:.6%}")

# Plotting og animasjon
#############################################################################################
#############################################################################################

X = np.arange(-1, 15, 1)   # Fewer points for clarity
Y = np.arange(-5, 6, 1)
X, Y = np.meshgrid(X, Y)

fig, ax = plt.subplots()
ax.set_aspect('equal')

# Plot crosses to represent field going into the screen
for i in range(X.shape[0]):
    for j in range(X.shape[1]):
        ax.text(X[i, j], Y[i, j], '•', fontsize=14, ha='center', va='center', color='b')
        

# Moving animation man 
from matplotlib.animation import FuncAnimation
line, = ax.plot([], [], 'o-', color="r")
def animate(i):
    line.set_data(r_vals[:i,0], r_vals[:i,1])
    return line,

ani = FuncAnimation(fig, animate, frames=len(t_vals), 
                    interval=30, blit=True)

# For å vite start og sluttpunktet
ax.plot(x_vals, y_vals, 'g-', linewidth=1.5, label='Trajectory')
ax.scatter([r0[0]], [r0[1]], c='r', s=50, label='Start')
ax.scatter([x_vals[-1]], [y_vals[-1]], c='b', s=50, label='End')
ax.legend()

ax.set_xlim(-1, 14)
ax.set_ylim(-5, 5)
plt.plot(x_vals, y_vals,color= "g")
plt.title(f" Partikkel-varierende Bane med (h= {h}) etter {tf} sekunder")
plt.xlabel("x (m)")
plt.ylabel("y (m)")
plt.grid(True)
plt.savefig("Partikkel-varierende_Bane(50s).png", dpi=300, bbox_inches='tight')
plt.show()

# At 627 iterations, the particle makes a perfect circle revolution, But Ek_0 != EK_f still decimals
#############################################################################################
#############################################################################################