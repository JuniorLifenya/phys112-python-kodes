import numpy as np
import matplotlib.pyplot as plt

#############################################################################################
#############################################################################################

# Constants

r21 = 6.4e6
m1 = 0.45    # mass
m2 = 5.97e24
G  = 6.674e-11
g= 9.81
omega_g = -G * m1*m2 / r21**3

# Initial conditions: [vx0, vy0, x0, y0]
state = np.array([5.0, 5.0, 0.0, 0.0])

# Time parameters
t0 = 0.0
tf = 25.0
h = 0.01
#n_steps = int((tf - t0) / h)
n_steps = int(input(f"Number of steps "))

#############################################################################################
#############################################################################################

# Right-hand side of the system: returns [dvx/dt, dvy/dt, dx/dt, dy/dt]
def simple_grav(state, t):

    vx, vy, x, y = state # A very cool way to define a vector right called UNPACKING
    # So really what we want in the end is state = [vx,vy,x,y] unpacking makes it possible 
    # Unpacking is super neat once you get used to it ! 
    
    dvx = 0*x
    dvy = -(g)
    dx = vx
    dy = vy

    return np.array([dvx, dvy, dx, dy])

# RK4 step for vector-valued state
def rk4_step(f, state, t, h):

    k1 = f(state, t)
    k2 = f(state + 0.5 * h * k1, t + 0.5 * h)
    k3 = f(state + 0.5 * h * k2, t + 0.5 * h)
    k4 = f(state + h * k3, t + h)
    return state + (h* (k1 + 2*k2 + 2*k3 + k4))/6

#############################################################################################
#############################################################################################



# Storage
trajectory = np.zeros((n_steps + 1, 4))
trajectory[0] = state
times = np.linspace(t0, tf, n_steps + 1)

# Run simulation
for i in range(n_steps):
    state = rk4_step(simple_grav, state, times[i], h)
    trajectory[i+1] = state

# Extract positions
x_vals = trajectory[:, 2]
y_vals = trajectory[:, 3]

#############################################################################################
#############################################################################################

print(state)
# Plot
plt.figure(figsize=(6, 6))
plt.plot(x_vals, y_vals)
plt.title("Charged Particle in Uniform Magnetic Field (Circular Motion)")
plt.xlabel("x")
plt.ylabel("y")
plt.grid(True)
plt.show()

##############################################################################################
# Moving animation man 
from matplotlib.animation import FuncAnimation
fig, ax = plt.subplots()
line, = ax.plot([], [], 'o-')
ax.set_xlim(-1, 8.5)
ax.set_ylim(-4, 4)

# Replace with:
def animate(i):
    line.set_data(x_vals[:i], y_vals[:i])
    return line,

ani = FuncAnimation(fig, animate, frames=len(times), interval=20)
plt.show()
# At 627 iterations, the particle makes a perfect circle revolution, But Ek_0 != EK_f still decimals
#############################################################################################
#############################################################################################


