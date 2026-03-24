```python
#!/usr/bin/env python3
import numpy as np
import matplotlib.pyplot as plt
from scipy.ndimage import gaussian_filter

def create_landscape(size=100):
    """Generate synthetic performance landscape with multiple basins and a ridge."""
    x = np.linspace(-5, 5, size)
    y = np.linspace(-5, 5, size)
    X, Y = np.meshgrid(x, y)
    # Multi-modal: multiple optima and a low-dimensional ridge
    Z = (np.exp(-(X**2 + Y**2)) +
         0.5*np.exp(-((X-2)**2 + (Y+2)**2)) +
         0.5*np.exp(-((X+2)**2 + (Y-2)**2)) +
         0.2*np.sin(2*X) * np.cos(2*Y))
    Z = gaussian_filter(Z, sigma=2)  # smooth
    return X, Y, Z

def domain_prior(X, Y):
    """Domain knowledge: promising region near (1,1) with some uncertainty."""
    prior = np.exp(-((X-1)**2 + (Y-1)**2) / 2)
    return prior

def acquisition(Z, prior, beta=0.5):
    """Combine exploitation (Z) and exploration (prior uncertainty)."""
    return beta * prior + (1 - beta) * Z

def tune(X, Y, Z, prior, steps=20):
    """Hill climbing guided by acquisition function."""
    idx = np.random.randint(0, X.shape[0])
    idy = np.random.randint(0, Y.shape[1])
    path = [(X[idx, idy], Y[idx, idy], Z[idx, idy])]
    for _ in range(steps):
        neighbors = []
        for dx, dy in [(-1,0),(1,0),(0,-1),(0,1)]:
            ni, nj = idx+dx, idy+dy
            if 0 <= ni < X.shape[0] and 0 <= nj < Y.shape[1]:
                neighbors.append((Z[ni,nj], ni, nj))
        if not neighbors:
            break
        acq_vals = [acquisition(Z[i,j], prior[i,j]) for _, i, j in neighbors]
        best = np.argmax(acq_vals)
        _, idx, idy = neighbors[best]
        path.append((X[idx, idy], Y[idx, idy], Z[idx, idy]))
    return np.array(path)

def main():
    X, Y, Z = create_landscape()
    prior = domain_prior(X, Y)
    paths = []
    for i in range(5):
        path = tune(X, Y, Z, prior, steps=30)
        paths.append(path)
        print(f"Run {i+1}: performance={path[-1,2]:.3f} at ({path[-1,0]:.2f}, {path[-1,1]:.2f})")
    plt.figure(figsize=(8,6))
    plt.contourf(X, Y, Z, levels=20, cmap='viridis')
    plt.colorbar(label='Performance')
    for i, path in enumerate(paths):
        plt.plot(path[:,0], path[:,1], 'w-', linewidth=1.5, alpha=0.8)
        plt.scatter(path[0,0], path[0,1], c='red', s=50, label='Start' if i==0 else "")
        plt.scatter(path[-1,0], path[-1,1], c='yellow', s=50, label='End' if i==0 else "")
    plt.title('Domain-Spatiality Guided Configuration Tuning')
    plt.xlabel('Param 1'); plt.ylabel('Param 2')
    plt.legend()
    plt.tight_layout()
    plt.savefig('tuning_paths.png', dpi=150)
    print("\nPlot saved as tuning_paths.png")

if __name__ == "__main__":
    main()
```