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

ax = fig.add_subplot(111,projection="3d")

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
    init_func=init, blit=True, interval=.50
)
plt.show()
