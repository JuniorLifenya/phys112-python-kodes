import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation



# Initialize plot. Size and restricted area
fig, ax = plt.subplots(figsize=(6, 6))
ax.set_xlim(-5, 5)
ax.set_ylim(-5, 5)
ax.set_xlabel("x")
ax.set_ylabel("y")

# Define charge properties
q = 1  # Charge magnitude, needed for later
v = np.array([1, 0])  # Velocity vector (moving to the right)
pos = np.array([-5, 0])  # Initial position



# Store all dots and crosses
dots = []  # Stores (x, y) positions of dots
crosses = []  # Stores (x, y) positions of crosses


# Animation update function
def update(frame):
    global pos, dots, crosses # Allows us to directly modify the external variables. Without it changes would not affect the actual pos,dots,cross. Each update would start from scratch without it

    # Update charge position
    pos[0] += v[0]  # Move charge to the right
    if pos[0] >= 4:  # Stop at x = 5
        pos[0] = 4

    # Clear the plot
    ax.clear()
    ax.set_xlim(-5, 5) #Calling them in each frame in case they change( they dont ), needed for more adbanced code. 
    ax.set_ylim(-5, 5)
    ax.set_xlabel("x")
    ax.set_ylabel("y")

    # Plot the moving charge
    ax.plot(pos[0], pos[1], "ro", markersize=10, label="Moving Charge")

    # Add dots above and crosses below the charge's current location
    y_dots = np.arange(pos[1] + 0.5, 5, 1)  # Dots above the charge
    y_crosses = np.arange(pos[1] - 0.5, -5, -1)  # Crosses below the charge

    for y in y_dots:
        dots.append((pos[0], y))  # Store dot positions

    for y in y_crosses:
        crosses.append((pos[0], y))  # Store cross positions

    # Plot all dots and crosses
    for dot in dots:
        ax.text(
            dot[0], dot[1], "•", fontsize=12, ha="center", va="center", color="blue"
        )  # Dots

    for cross in crosses:
        ax.text(
            cross[0], cross[1], "×", fontsize=12, ha="center", va="center", color="red"
        )  # Crosses

    ax.legend() #Also added in every frame but not needed really. 


# Run animation
ani = animation.FuncAnimation(fig, update, frames=50, interval=200, repeat=False)
plt.show()
