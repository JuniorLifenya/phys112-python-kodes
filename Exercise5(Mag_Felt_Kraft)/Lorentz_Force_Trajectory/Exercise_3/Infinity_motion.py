import numpy as np
import matplotlib.pyplot as plt
#############################################################################################

# Constants
q = 1.0
m = 1.0
omega = 1.0  # Angular frequency for the figure-eight

# Time parameters
t0 = 0.0
tf = 4 * np.pi  # Two full cycles of the figure-eight
h = 0.01
n_steps = int((tf - t0) / h)

#############################################################################################

# Field functions
def E_field(t):
    Ex = -m/q * omega**2 * np.sin(omega*t)
    Ey = -m/q * 2 * omega**2 * np.sin(2*omega*t)
    return np.array([Ex, Ey])

def B_field(t, r):
    return np.array([0.0, 0.0, 0.0])

# Equations of motion
def f(t, r, v):  # dv/dt = q/m (E + v × B)
    E = E_field(t)
    B = B_field(t, r)
    v3d = np.array([v[0], v[1], 0.0])
    cross = np.cross(v3d, B)
    return (q/m) * (E + cross[:2])

def g(t, r, v):  # dr/dt = v
    return v

#############################################################################################
#############################################################################################
# Runge-Kutta solver
def rk4_system(t0, r0, v0, h, n):
    t = np.zeros(n+1)
    r = np.zeros((n+1, 2))
    v = np.zeros((n+1, 2))
    
    t[0] = t0
    r[0] = r0
    v[0] = v0
    
    for i in range(n):
        ti = t[i]
        ri = r[i]
        vi = v[i]
        
        K1 = f(ti, ri, vi)
        G1 = g(ti, ri, vi)
        
        K2 = f(ti + h/2, ri + h*G1/2, vi + h*K1/2)
        G2 = g(ti + h/2, ri + h*G1/2, vi + h*K1/2)
        
        K3 = f(ti + h/2, ri + h*G2/2, vi + h*K2/2)
        G3 = g(ti + h/2, ri + h*G2/2, vi + h*K2/2)
        
        K4 = f(ti + h, ri + h*G3, vi + h*K3)
        G4 = g(ti + h, ri + h*G3, vi + h*K3)
        
        t[i+1] = ti + h
        v[i+1] = vi + (h/6) * (K1 + 2*K2 + 2*K3 + K4)
        r[i+1] = ri + (h/6) * (G1 + 2*G2 + 2*G3 + G4)
        
    return t, r, v

# Initial conditions (match parametric equations)
r0 = np.array([0.0, 0.0])
v0 = np.array([omega, omega])  # dx/dt = ω, dy/dt = ω at t=0
t0 = 0.0

# Run simulation
t_vals, r_vals, v_vals = rk4_system(t0, r0, v0, h, n_steps)

from matplotlib.animation import FuncAnimation


fig, ax = plt.subplots()
line, = ax.plot([], [], 'o-')
ax.set_xlim(-1.5, 1.5)
ax.set_ylim(-1.5, 1.5)

#############################################################################################
#############################################################################################

# Auto animation man###########################################

def animate(i):
    line.set_data(r_vals[:i,0], r_vals[:i,1])
    return line,

ani = FuncAnimation(fig, animate, frames=len(t_vals), 
                    interval=20, blit=True)
plt.show()

#############################################################################################
#############################################################################################

# Plot
plt.figure(figsize=(10, 5))
plt.plot(r_vals[:, 0], r_vals[:, 1], 'b-')
plt.title("Infinity Sign Trajectory")
plt.xlabel("x")
plt.ylabel("y")
plt.gca().set_aspect('equal')
plt.grid(True)

plt.show()

#############################################################################################
#############################################################################################