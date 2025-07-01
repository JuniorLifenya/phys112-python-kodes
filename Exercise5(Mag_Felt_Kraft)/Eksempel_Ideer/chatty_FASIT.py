import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

# Fysiske konstanter
dt = 0.01       # tidssteg
tot_steps = 1000
q = 1.0         # ladning
m = 1.0         # masse
B0 = 1.0        # konstant magnetfelt i z

# Initialbetingelser
pos = np.array([0.0, 0.0])        # startposisjon i xy
vel = np.array([0.0, 1.0])        # startfart i xy

# Lorentz-kraft i 2D
def lorentz(v, Bz):
    # v = [vx, vy], B = [0,0,Bz]
    return np.array([ q/m * v[1] * Bz,
                      -q/m * v[0] * Bz ])

# RK4-integrator
def step_rk4(r, v, Bz):
    k1_v = lorentz(v, Bz)
    k1_r = v
    k2_v = lorentz(v + 0.5 * dt * k1_v, Bz)
    k2_r = v + 0.5 * dt * k1_v
    k3_v = lorentz(v + 0.5 * dt * k2_v, Bz)
    k3_r = v + 0.5 * dt * k2_v
    k4_v = lorentz(v + dt * k3_v, Bz)
    k4_r = v + dt * k3_v

    v_new = v + dt / 6 * (k1_v + 2*k2_v + 2*k3_v + k4_v)
    r_new = r + dt / 6 * (k1_r + 2*k2_r + 2*k3_r + k4_r)
    return r_new, v_new

# Beregn bane
trajectory = np.zeros((tot_steps, 2))
trajectory[0] = pos.copy()
for i in range(1, tot_steps):
    pos, vel = step_rk4(pos, vel, B0)
    trajectory[i] = pos

# Oppsett for animasjon
fig, ax = plt.subplots()
ax.set_aspect('equal', 'box')
ax.set_xlim(-5, 5)
ax.set_ylim(-5, 5)
line, = ax.plot([], [], 'r-', lw=2, label='Bane')
point, = ax.plot([], [], 'bo', ms=6, label='Partikkel')
ax.legend(loc='upper right')

# Initialiseringsfunksjon
def init():
    line.set_data([], [])
    point.set_data([], [])
    return line, point

# Oppdateringsfunksjon
def update(frame):
    # Plott banen opp til frame
    line.set_data(trajectory[:frame, 0], trajectory[:frame, 1])
    # Bruk sekvens når punkt oppdateres
    x, y = trajectory[frame]
    point.set_data([x], [y])
    return line, point

ani = animation.FuncAnimation(
    fig, update, frames=tot_steps,
    init_func=init, blit=True, interval=20
)
plt.show()

##################################################################################################
##################################################################################################

# 3D Versjonen av koden over : 

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from mpl_toolkits.mplot3d import Axes3D

# Fysiske konstanter
dt = 0.01       # tidssteg
tot_steps = 1000
q = 1.0         # ladning
m = 1.0         # masse
B0 = np.array([0.0, 0.0, 1.0])  # konstant magnetfelt i z-retning

# Initialbetingelser
pos = np.array([0.0, 0.0, 0.0])   # startposisjon i xyz
vel = np.array([0.1, 0.5, 0.2])   # startfart i xyz

# Lorentz-kraft i 3D
def lorentz(v, B):
    # F = q(v × B)
    return (q/m) * np.cross(v, B)

# RK4-integrator for 3D
def step_rk4(r, v, B):
    # Akselerasjon ved startpunkt
    a = lorentz(v, B)
    
    # RK4-trinn for hastighet
    k1v = a
    k1r = v
    
    k2v = lorentz(v + 0.5 * dt * k1v, B)
    k2r = v + 0.5 * dt * k1v
    
    k3v = lorentz(v + 0.5 * dt * k2v, B)
    k3r = v + 0.5 * dt * k2v
    
    k4v = lorentz(v + dt * k3v, B)
    k4r = v + dt * k3v
    
    # Oppdater hastighet og posisjon
    v_new = v + (dt / 6.0) * (k1v + 2*k2v + 2*k3v + k4v)
    r_new = r + (dt / 6.0) * (k1r + 2*k2r + 2*k3r + k4r)
    
    return r_new, v_new

# Beregn bane i 3D
trajectory = np.zeros((tot_steps, 3))
trajectory[0] = pos.copy()
for i in range(1, tot_steps):
    pos, vel = step_rk4(pos, vel, B0)
    trajectory[i] = pos

# Oppsett for 3D-animasjon
fig = plt.figure(figsize=(10, 8))
ax = fig.add_subplot(111, projection='3d')

# Beregn dynamiske grenser basert på banen
max_range = 1.1 * np.max(np.abs(trajectory))
ax.set_xlim([-max_range, max_range])
ax.set_ylim([-max_range, max_range])
ax.set_zlim([-max_range, max_range])
ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Z')
ax.set_title('Partikkelbane i magnetfelt', fontsize=14)
ax.grid(True)

# Initialiser grafikkobjekter
line, = ax.plot([], [], [], 'r-', lw=2, label='Bane')
point, = ax.plot([], [], [], 'bo', ms=8, label='Partikkel')
ax.legend(loc='upper right')

# Initialiseringsfunksjon
def init():
    line.set_data([], [])
    line.set_3d_properties([])
    point.set_data([], [])
    point.set_3d_properties([])
    return line, point

# Oppdateringsfunksjon for animasjon
def update(frame):
    # Plott banen opp til nåværende tidspunkt
    line.set_data(trajectory[:frame, 0], trajectory[:frame, 1])
    line.set_3d_properties(trajectory[:frame, 2])
    
    # Plott partikkelens nåværende posisjon
    x, y, z = trajectory[frame]
    point.set_data([x], [y])
    point.set_3d_properties([z])
    
    return line, point

# Lag animasjon
ani = animation.FuncAnimation(
    fig, update, frames=range(0, tot_steps, 5),  # Hopp over noen rammer for raskere visning
    init_func=init, blit=True, interval=20
)

plt.tight_layout()
plt.show()

# For å lagre animasjonen (fjern kommentar hvis ønskelig)
# ani.save('partikkelbane_3D.gif', writer='pillow', fps=30)