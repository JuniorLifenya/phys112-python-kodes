# Pseudo-code
def solve_waveguide_modes(epsilon_grid, k0):
    """
    Solves ∇²H = -ω²μϵH with PEC boundaries
    """
    # Construct sparse Laplacian matrix
    Nx, Ny = epsilon_grid.shape
    D2x = (np.eye(Nx-2, k=-1) - 2*np.eye(Nx-2) + np.eye(Nx-2, k=1))/dx**2
    D2y = (np.eye(Ny-2, k=-1) - 2*np.eye(Ny-2) + np.eye(Ny-2, k=1))/dy**2
    L = sparse.kronsum(D2x, D2y)
    
    # Solve eigenvalue problem
    evals, evecs = sparse.linalg.eigs(L + k0**2*sparse.diags(epsilon_grid[1:-1,1:-1].flatten()), 
                                      k=5, which='SM')
    return np.sqrt(-evals)  # Propagation constants

# Task: Find TE modes in rectangular waveguide
# Plot field distributions for fundamental mode