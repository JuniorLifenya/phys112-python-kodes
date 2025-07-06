import matplotlib.pyplot as plt
import numpy as np

X = np.arange(-10, 11, 2)   # Fewer points for clarity
Y = np.arange(-10, 11, 2)
X, Y = np.meshgrid(X, Y)

fig, ax = plt.subplots()
ax.set_aspect('equal')

# Plot crosses to represent field going into the screen
for i in range(X.shape[0]):
    for j in range(X.shape[1]):
        ax.text(X[i, j], Y[i, j], '×', fontsize=14, ha='center', va='center', color='blue')

ax.set_xlim(-11, 11)
ax.set_ylim(-11, 11)
ax.set_xlabel('x')
ax.set_ylabel('y')
ax.set_title('Magnetic Field Into the Screen (× symbols)')
plt.grid(True)
plt.show()
