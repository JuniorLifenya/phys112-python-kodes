import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from mpl_toolkits.mplot3d import Axes3D

# Define charge properties
q = 1  # Charge magnitude
v = np.array([0, 1, 0])  # Velocity vector (moving to the right along y-axis in 3D)
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


# Function to calculate magnetic field due to moving charge (simplified for point charge)
def magnetic_field(r, v, q):
    r_vec = r - pos  # Vector from charge to observation point
    r_mag = np.linalg.norm(r_vec)  # Magnitude of the distance
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
    if pos[1] >= 4:
        v[1] = -v[1]  # Reverse direction
    if pos[1] <= -4:
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
    ax.scatter(pos[0], pos[1], pos[2], color="red", s=100, label="Moving Charge")

    # Plot magnetic field lines around the charge (circular loops in the x-y plane)
    for phi in np.linspace(
        0, 2 * np.pi, 20
    ):  # Create circular field lines in the x-y plane
        for r_val in np.linspace(1, 3, 5):  # Radius of the magnetic field loops
            r = np.array(
                [pos[0] + r_val * np.cos(phi), pos[1] + r_val * np.sin(phi), pos[2]]
            )
            B = magnetic_field(r, v, q)  # Magnetic field at this point
            ax.quiver(
                r[0],
                r[1],
                r[2],
                B[0],
                B[1],
                B[2],
                length=0.5,
                normalize=True,
                color="green",
                alpha=0.5,
            )
    
    
    ax.legend()


# Run animation
ani = animation.FuncAnimation(fig, update, frames=50, interval=200, repeat=True)
plt.show()
