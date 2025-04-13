import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from mpl_toolkits.mplot3d import Axes3D

# Define charge properties
q = 1  # Charge magnitude
v = np.array([1, 0, 0])  # Velocity vector (moving to the right along x-axis)
pos = np.array([-4, 0, 0])  # Initial position (x, y, z)

# Initialize 3D plot
fig = plt.figure(figsize=(8, 8))
ax = fig.add_subplot(111, projection="3d")
ax.set_xlim(-5, 5)
ax.set_ylim(-5, 5)
ax.set_zlim(-5, 5)
ax.set_xlabel("x")
ax.set_ylabel("y")
ax.set_zlabel("z")

# Store all dots and crosses
dots = []  # Stores (x, y, z) positions of dots
crosses = []  # Stores (x, y, z) positions of crosses


# Animation update function
def update(frame):
    global pos, dots, crosses

    # Update charge position
    pos[0] += v[0]
    if pos[0] >= 4:
        v[0] = -v[0]  # Reverse direction
        dots.clear()  # Clear old dots
        crosses.clear()  # Clear old crosses
    if pos[0] <= -4:
        v[0] = -v[0]  # Reverse direction
        dots.clear()  # Clear old dots
        crosses.clear()  # Clear old crosses

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

    # Determine the positions of dots and crosses based on the direction of movement
    if v[0] > 0:  # Moving to the right
        z_dots = np.arange(pos[2] + 1.5, 5, 1)  # Dots above the charge (along z-axis)
        z_crosses = np.arange(
            pos[2] - 1.5, -5, -1
        )  # Crosses below the charge (along z-axis)
    else:  # Moving to the left
        z_dots = np.arange(pos[2] - 1.5, -5, -1)  # Dots below the charge (along z-axis)
        z_crosses = np.arange(
            pos[2] + 1.5, 5, 1
        )  # Crosses above the charge (along z-axis)

    for z in z_dots:
        dots.append((pos[0], pos[1], z))  # Store dot positions

    for z in z_crosses:
        crosses.append((pos[0], pos[1], z))  # Store cross positions

    # Plot all dots and crosses
    for dot in dots:
        ax.text(
            dot[0],
            dot[1],
            dot[2],
            "•",
            fontsize=15,
            ha="center",
            va="center",
            color="blue",
        )  # Dots

    for cross in crosses:
        ax.text(
            cross[0],
            cross[1],
            cross[2],
            "×",
            fontsize=15,
            ha="center",
            va="center",
            color="red",
        )  # Crosses

    ax.legend()


# Run animation
ani = animation.FuncAnimation(fig, update, frames=50, interval=200, repeat=True)
plt.show()
