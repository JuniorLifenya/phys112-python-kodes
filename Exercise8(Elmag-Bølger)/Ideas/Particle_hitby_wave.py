import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

# Constants
q = 1.0  # Particle charge
m = 1.0  # Particle mass
c = 1.0  # Speed of light (simplified units)

# Wave parameters
amplitude = 15.0  # Increased field strength for stronger interaction
wavelength = 1.0
k = 2 * np.pi / wavelength  # Wave number
omega = k * c  # Angular frequency (since ω = ck for EM waves)

# Time parameters
t0 = 0.0
tf = 15.0  # Longer simulation time
h = 0.005  # Time step
n_steps = int((tf - t0) / h)

# Field functions - modified to have particle hit by wave
def E_field(t, r):
    """Electric field of a plane wave propagating in x-direction"""
    x, y = r
    # Shift wave so particle starts at a field maximum
    phase = k * (x - 5) - omega * t  # Wave starts 5 units away
    Ex = 0.0
    Ey = amplitude * np.sin(phase)
    return np.array([Ex, Ey])

def B_field(t, r):
    """Magnetic field of a plane wave propagating in x-direction"""
    x, y = r
    phase = k * (x - 5) - omega * t  # Same phase shift
    Bz = amplitude * np.sin(phase) / c  # B = E/c for EM wave
    return np.array([0.0, 0.0, Bz])

# Equations of motion (unchanged)
def f(t, r, v):
    """dv/dt = (q/m)(E + v × B)"""
    E = E_field(t, r)
    B = B_field(t, r)
    v3d = np.array([v[0], v[1], 0.0])
    v_cross_B = np.cross(v3d, B)
    force = q * (E + v_cross_B[:2])
    return force / m

def g(t, r, v):
    """dr/dt = v"""
    return v

# Runge-Kutta solver (unchanged)
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

# Initial conditions - particle at rest, waiting to be hit by wave
r0 = np.array([0.0, 0.0])
v0 = np.array([0.0, 0.0])  # Particle starts at rest

# Run simulation
print("Simulating particle motion in EM wave...")
t_vals, r_vals, v_vals = rk4_system(t0, r0, v0, h, n_steps)
print("Simulation complete")

# Create figure for animation
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))

# Set up trajectory plot
ax1.set_xlim(-1, 10)
ax1.set_ylim(-5, 5)
ax1.set_title("Particle Trajectory in EM Wave")
ax1.set_xlabel("x position")
ax1.set_ylabel("y position")
ax1.grid(True)
trajectory_line, = ax1.plot([], [], 'b-', lw=1, alpha=0.7)
particle_point, = ax1.plot([], [], 'ro', markersize=6)

# Set up phase space plot
ax2.set_xlim(-10, 10)
ax2.set_ylim(-10, 10)
ax2.set_title("Phase Space (Velocity vs Position)")
ax2.set_xlabel("x velocity")
ax2.set_ylabel("y velocity")
ax2.grid(True)
phase_line, = ax2.plot([], [], 'g-', lw=1, alpha=0.5)
phase_point, = ax2.plot([], [], 'bo', markersize=6)

# Add wave visualization
x_wave = np.linspace(-1, 10, 300)
wave_line, = ax1.plot(x_wave, np.zeros_like(x_wave), 'r-', alpha=0.3)

# Add text for time display
time_text = ax1.text(0.02, 0.95, '', transform=ax1.transAxes)

# Add field display at particle position
field_text = ax1.text(0.02, 0.85, '', transform=ax1.transAxes)

def init():
    trajectory_line.set_data([], [])
    particle_point.set_data([], [])
    phase_line.set_data([], [])
    phase_point.set_data([], [])
    time_text.set_text('')
    field_text.set_text('')
    wave_line.set_ydata(np.zeros_like(x_wave))
    return trajectory_line, particle_point, phase_line, phase_point, time_text, field_text, wave_line

def animate(i):
    # Only plot every 5th frame to make animation smoother
    idx = i * 5
    if idx >= len(t_vals):
        idx = len(t_vals) - 1
    
    # Update trajectory plot
    trajectory_line.set_data(r_vals[:idx, 0], r_vals[:idx, 1])
    particle_point.set_data([r_vals[idx, 0]], [r_vals[idx, 1]])
    
    # Update phase space plot
    phase_line.set_data(v_vals[:idx, 0], v_vals[:idx, 1])
    phase_point.set_data([v_vals[idx, 0]], [v_vals[idx, 1]])
    
    # Update wave visualization
    t_current = t_vals[idx]
    wave_phase = k * (x_wave - 5) - omega * t_current
    wave_line.set_ydata(0.5 * np.sin(wave_phase))
    
    # Update text
    time_text.set_text(f'Time: {t_current:.2f} s')
    
    # Calculate field at particle position
    E = E_field(t_current, r_vals[idx])
    B = B_field(t_current, r_vals[idx])
    field_text.set_text(f'Ey: {E[1]:.2f}, Bz: {B[2]:.2f}')
    
    # Highlight when wave hits particle
    if 4.5 < r_vals[idx, 0] < 5.5:
        ax1.set_facecolor((1.0, 0.9, 0.9))  # Light red background
    else:
        ax1.set_facecolor('white')
    
    return trajectory_line, particle_point, phase_line, phase_point, time_text, field_text, wave_line

# Create animation
print("Creating animation...")
ani = FuncAnimation(fig, animate, frames=len(t_vals)//5, 
                   init_func=init, blit=True, interval=20)

plt.tight_layout()
plt.show()