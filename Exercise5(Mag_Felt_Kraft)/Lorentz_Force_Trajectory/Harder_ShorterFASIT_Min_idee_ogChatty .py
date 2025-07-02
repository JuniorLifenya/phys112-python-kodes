import numpy as np
import matplotlib.pyplot as plt

#############################################################################################
#############################################################################################

# Constants
q = 1.0     # charge
m = 1.0     # mass
B0 = 2.0     # magnetic field strength
omega_c = q * B0 / m

# Time parameters
t0 = 0.0
tf = 20.0
h = 0.01
#n_steps = int((tf - t0) / h)
n_steps = int(input(f"Number of steps "))

#############################################################################################
#############################################################################################

# Right-hand side of the system: returns [dvx/dt, dvy/dt, dx/dt, dy/dt]
def lorentz_rhs(state, t):

    vx, vy, x, y = state # A very cool way to define a vector right called UNPACKING
    # So really what we want in the end is state = [vx,vy,x,y] unpacking makes it possible 
    # Unpacking is super neat once you get used to it ! 
    
    dvx = omega_c * vy
    dvy = -omega_c * vx
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

# Initial conditions: [vx0, vy0, x0, y0]
state = np.array([0.0, 1.0, 0.0, 0.0])

# Storage
trajectory = np.zeros((n_steps + 1, 4))
trajectory[0] = state
times = np.linspace(t0, tf, n_steps + 1)

# Run simulation
for i in range(n_steps):
    state = rk4_step(lorentz_rhs, state, times[i], h)
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
plt.gca().set_aspect('equal')
plt.title("Charged Particle in Uniform Magnetic Field (Circular Motion)")
plt.xlabel("x")
plt.ylabel("y")
plt.grid(True)
plt.show()

# For perfect sircle : Number of steps 314 [-3.18531016e-03  9.99994927e-01  2.53662642e-06 -1.59265508e-03]
#############################################################################################
#############################################################################################