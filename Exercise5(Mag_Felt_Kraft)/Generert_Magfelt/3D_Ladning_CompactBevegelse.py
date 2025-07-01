import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from mpl_toolkits.mplot3d import Axes3D

# Define charge properties
q = 1  # Charge magnitude
v = np.array([0, 1, 0])  # Velocity vector (moving along y-axis)
pos = np.array([0, 0, 0])  # Initial position (x, y, z)

# Constants
mu_0 = 4 * np.pi * 1e-7  # Permeability of free space

# Initialize 3D plot
fig = plt.figure(figsize=(8, 8))
ax = fig.add_subplot(111, projection="3d")
ax.set_xlim(-5, 5)
ax.set_ylim(-5, 5)
ax.set_zlim(-5, 5)
ax.set_xlabel("x")
ax.set_ylabel("y")
ax.set_zlabel("z")

# Function to calculate magnetic field due to moving charge
def magnetic_field(r, v, q):
    r_vec = r - pos  # Vector from charge to observation point
    r_mag = np.linalg.norm(r_vec)  # Magnitude of the distance
    if r_mag == 0:
        return np.array([0, 0, 0])  # Avoid division by zero
    r_hat = r_vec / r_mag  # Unit vector in the direction of r
    
    # Biot-Savart law (simplified for point charge)
    cross_product = np.cross(v, r_vec)
    B = (mu_0 * q / (4 * np.pi)) * (cross_product) / (r_mag**2)
    return B

# Animation update function
def update(frame):
    global pos

    # Update charge position
    pos[1] += v[1]
    if pos[1] >= 4 or pos[1] <= -4:
        v[1] = -v[1]  # Reverse direction

    # Clear the plot
    ax.clear()
    ax.set_xlim(-5, 5)
    ax.set_ylim(-5, 5)
    ax.set_zlim(-5, 5)
    ax.set_xlabel("x")
    ax.set_ylabel("y")
    ax.set_zlabel("z")

    # Plot the moving charge
    ax.scatter(pos[0], pos[1], pos[2], color="red", s=200, label="Moving Charge")

    # Plot magnetic field lines around the charge (3D circular loops)
    for theta in np.linspace(0, np.pi, 4):  # Latitude angle
        for phi in np.linspace(0, 2*np.pi, 15):  # Azimuthal angle
            r_val = 2  # Fixed radius for visualization
            x = pos[0] + r_val * np.sin(theta) * np.cos(phi)
            y = pos[1] + r_val * np.sin(theta) * np.sin(phi)
            z = pos[2] + r_val * np.cos(theta)
            r = np.array([x, y, z])
            B = magnetic_field(r, v, q)  # Magnetic field at this point
            ax.quiver(
                x, y, z, B[0], B[1], B[2],
                length=0.6, normalize=True, color="green", alpha=0.5
            )
    
    ax.legend()

# Run animation
ani = animation.FuncAnimation(fig, update, frames=120, interval=10, repeat=True)
plt.show()