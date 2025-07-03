import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

# Constants
q = 1.0  # Particle charge
m = 1.0  # Particle mass
c = 1.0  # Speed of light

# Wave parameters
amplitude = 15.0  # Strong field for dramatic effect
wavelength = .57
k = 2 * np.pi / wavelength
omega = k * c

# Wave starting position (5 units away from particle)
wave_start_x = 5.0

# Time parameters
t0 = 0.0
tf = 15.0  # Simulation time
h = 0.005  # Time step
n_steps = int((tf - t0) / h)

# Field functions - wave starts at x = wave_start_x
def E_field(t, r):
    x, y = r
    # Calculate distance from wave starting point
    wave_distance = x - wave_start_x
    
    # Create a smooth transition using a sigmoid function
    transition = 1 / (1 + np.exp(-20*(wave_distance + c*t)))
    
    phase = k * (x - wave_start_x) - omega * t
    Ex = 0.0  # Only y-component for electric field
    Ey = amplitude * np.sin(phase) * transition
    return np.array([Ex, Ey])

def B_field(t, r):
    x, y = r
    # Calculate distance from wave starting point
    wave_distance = x - wave_start_x
    
    # Create a smooth transition using a sigmoid function
    transition = 1 / (1 + np.exp(-20*(wave_distance + c*t)))
    
    phase = k * (x - wave_start_x) - omega * t
    Bz = amplitude * np.sin(phase) * transition / c
    return np.array([0.0, 0.0, Bz])

# Equations of motion
def f(t, r, v):
    E = E_field(t, r)
    B = B_field(t, r)
    v3d = np.array([v[0], v[1], 0.0])
    v_cross_B = np.cross(v3d, B)
    force = q * (E + v_cross_B[:2])
    return force / m

def g(t, r, v):
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

# Initial conditions - particle moving straight to the right
r0 = np.array([2.0, 0.0])
v0 = np.array([0.5, 0.0])  # Initial velocity in x-direction
t0 = 0.0

# Run simulation
print("Simulating particle motion in EM wave...")
t_vals, r_vals, v_vals = rk4_system(t0, r0, v0, h, n_steps)
print("Simulation complete")

# Create figure for animation
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))

# Set up trajectory plot
ax1.set_xlim(-1, 15)
ax1.set_ylim(-5, 5)
ax1.set_title("Particle Trajectory: Straight Motion Until Wave Impact")
ax1.set_xlabel("x position")
ax1.set_ylabel("y position")
ax1.grid(True)
trajectory_line, = ax1.plot([], [], 'b-', lw=1, alpha=0.7)
particle_point, = ax1.plot([], [], 'ro', markersize=6)

# Set up phase space plot
ax2.set_xlim(-1, 1)
ax2.set_ylim(-5, 5)
ax2.set_title("Phase Space (x-velocity vs y-velocity)")
ax2.set_xlabel("x velocity")
ax2.set_ylabel("y velocity")
ax2.grid(True)
phase_line, = ax2.plot([], [], 'g-', lw=1, alpha=0.5)
phase_point, = ax2.plot([], [], 'bo', markersize=6)

# Add wave visualization
x_wave = np.linspace(-1, 15, 300)
wave_line, = ax1.plot(x_wave, np.zeros_like(x_wave), 'g-', alpha=0.8)

# Add vertical line to show wave starting point
wave_start_line = ax1.axvline(x=wave_start_x, color='r', linestyle='--', alpha=0.5)

# Add text for time display
time_text = ax1.text(0.02, 0.95, '', transform=ax1.transAxes)

# Add field display at particle position
field_text = ax1.text(0.02, 0.85, '', transform=ax1.transAxes)

# Add impact status
impact_text = ax1.text(0.02, 0.75, 'Wave approaching...', color='red', transform=ax1.transAxes)

def init():
    trajectory_line.set_data([], [])
    particle_point.set_data([], [])
    phase_line.set_data([], [])
    phase_point.set_data([], [])
    time_text.set_text('')
    field_text.set_text('')
    wave_line.set_ydata(np.zeros_like(x_wave))
    impact_text.set_text('Wave approaching...')
    impact_text.set_color('red')
    ax1.set_facecolor('white')
    return (trajectory_line, particle_point, phase_line, phase_point, 
            time_text, field_text, wave_line, impact_text)

def animate(i):
    # Only plot every 5th frame
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
    wave_phase = k * (x_wave - wave_start_x) - omega * t_current
    # Smooth transition for wave visualization
    wave_transition = 1 / (1 + np.exp(-20*((x_wave - wave_start_x) + c*t_current)))
    wave_line.set_ydata(0.5 * np.sin(wave_phase) * wave_transition)
    
    # Update text
    time_text.set_text(f'Time: {t_current:.2f} s')
    
    # Calculate field at particle position
    E = E_field(t_current, r_vals[idx])
    B = B_field(t_current, r_vals[idx])
    field_text.set_text(f'Ey: {E[1]:.2f}, Bz: {B[2]:.2f}')
    
    # Update impact status
    if r_vals[idx, 0] > wave_start_x - c*t_current:
        impact_text.set_text('WAVE IMPACT!')
        impact_text.set_color('green')
        # Add visual effect on impact
        ax1.set_facecolor((0.95, 1.0, 0.95))
    else:
        impact_text.set_text('Wave approaching...')
        impact_text.set_color('red')
        ax1.set_facecolor('white')
    
    return (trajectory_line, particle_point, phase_line, phase_point, 
            time_text, field_text, wave_line, impact_text)

# Create animation
print("Creating animation...")
ani = FuncAnimation(fig, animate, frames=len(t_vals)//5, 
                   init_func=init, blit=True, interval=20)

plt.tight_layout()
plt.show()