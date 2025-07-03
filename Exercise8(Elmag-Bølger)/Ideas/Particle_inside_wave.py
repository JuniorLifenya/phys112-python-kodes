import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

# Constants
q = 1.0  # Particle charge
m = 1.0  # Particle mass
c = 1.0  # Speed of light (simplified units)

# Wave parameters
amplitude = 5.0  # Field strength
wavelength = 1.0
k = 2 * np.pi / wavelength  # Wave number
omega = k * c  # Angular frequency (since ω = ck for EM waves)

# Time parameters
t0 = 0.0
tf = 10.0  # Simulation time
h = 0.005  # Time step
n_steps = int((tf - t0) / h)

# Field functions
def E_field(t, r):
    """Electric field of a plane wave propagating in x-direction"""
    x, y = r
    phase = k * x - omega * t
    Ex = 0.0
    Ey = amplitude * np.sin(phase)
    return np.array([Ex, Ey])

def B_field(t, r):
    """Magnetic field of a plane wave propagating in x-direction"""
    x, y = r
    phase = k * x - omega * t
    Bz = amplitude * np.sin(phase) / c  # B = E/c for EM wave
    return np.array([0.0, 0.0, Bz])

# Equations of motion
def f(t, r, v):
    """dv/dt = (q/m)(E + v × B)"""
    E = E_field(t, r)
    B = B_field(t, r)
    v3d = np.array([v[0], v[1], 0.0])  # 3D velocity
    v_cross_B = np.cross(v3d, B)
    force = q * (E + v_cross_B[:2])  # Only need x,y components
    return force / m

def g(t, r, v):
    """dr/dt = v"""
    return v

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

# Initial conditions
r0 = np.array([0.0, 0.0])
v0 = np.array([0.1, 0.0])  # Small initial velocity in x-direction
t0 = 0.0

# Run simulation
print("Simulating particle motion in EM wave...")
t_vals, r_vals, v_vals = rk4_system(t0, r0, v0, h, n_steps)
print("Simulation complete")

# Create figure for animation
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))

# Set up trajectory plot
ax1.set_xlim(-2, 15)
ax1.set_ylim(-3, 3)
ax1.set_title("Particle Trajectory in EM Wave")
ax1.set_xlabel("x position")
ax1.set_ylabel("y position")
ax1.grid(True)
trajectory_line, = ax1.plot([], [], 'b-', lw=1, alpha=0.7)
particle_point, = ax1.plot([], [], 'ro', markersize=6)

# Set up phase space plot
ax2.set_xlim(-0.5, 0.5)
ax2.set_ylim(-3, 3)
ax2.set_title("Phase Space (Velocity vs Position)")
ax2.set_xlabel("x velocity")
ax2.set_ylabel("y velocity")
ax2.grid(True)
phase_line, = ax2.plot([], [], 'g-', lw=1, alpha=0.5)
phase_point, = ax2.plot([], [], 'bo', markersize=6)

# Add wave visualization
x_wave = np.linspace(-2, 15, 300)
wave_line, = ax1.plot(x_wave, np.zeros_like(x_wave), 'r-', alpha=0.3)

# Add text for time display
time_text = ax1.text(0.02, 0.95, '', transform=ax1.transAxes)

# Add energy display
energy_text = ax1.text(0.02, 0.85, '', transform=ax1.transAxes)

def init():
    trajectory_line.set_data([], [])
    particle_point.set_data([], [])
    phase_line.set_data([], [])
    phase_point.set_data([], [])
    time_text.set_text('')
    energy_text.set_text('')
    wave_line.set_ydata(np.zeros_like(x_wave))
    return trajectory_line, particle_point, phase_line, phase_point, time_text, energy_text, wave_line

# ... (rest of the code remains the same until animation section)

def animate(i):
    # Only plot every 5th frame to make animation smoother
    idx = i * 5
    if idx >= len(t_vals):
        idx = len(t_vals) - 1
    
    # Update trajectory plot - FIXED HERE
    trajectory_line.set_data(r_vals[:idx, 0], r_vals[:idx, 1])
    particle_point.set_data([r_vals[idx, 0]], [r_vals[idx, 1]])  # Wrap in lists
    
    # Update phase space plot - FIXED HERE
    phase_line.set_data(v_vals[:idx, 0], v_vals[:idx, 1])
    phase_point.set_data([v_vals[idx, 0]], [v_vals[idx, 1]])  # Wrap in lists
    
    # Update wave visualization
    t_current = t_vals[idx]
    wave_line.set_ydata(0.5 * np.sin(k * x_wave - omega * t_current))
    
    # Update text
    time_text.set_text(f'Time: {t_current:.2f} s')
    
    # Calculate energy
    kinetic = 0.5 * m * np.sum(v_vals[idx]**2)
    energy_text.set_text(f'Kinetic Energy: {kinetic:.4f}')
    
    return (trajectory_line, particle_point, phase_line, phase_point, 
            time_text, energy_text, wave_line)

# ... (rest of the code remains the same)
# Create animation
print("Creating animation...")
ani = FuncAnimation(fig, animate, frames=len(t_vals)//5, 
                   init_func=init, blit=True, interval=20)

plt.tight_layout()
plt.show()

# Save animation (optional)
# print("Saving animation...")
# ani.save('em_wave_particle.mp4', writer='ffmpeg', fps=30)
# print("Animation saved")