```python
#!/usr/bin/env python3
"""
yProv4DV Demo: Reproducible visualization with full provenance.
Generates a plot and saves execution context for perfect reproduction.
"""

import sys, platform, json, hashlib
from datetime import datetime
from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt

# Fixed random seed ensures identical data on every run
np.random.seed(42)

def gen_data():
    x = np.linspace(0, 10, 100)
    y = 2*x + 1 + np.random.normal(0, 1.5, 100)
    return x, y

def make_plot(x, y, meta):
    fig, ax = plt.subplots(figsize=(8,5))
    ax.scatter(x, y, alpha=0.6, s=50, edgecolors='w', label='Data')
    ax.plot(x, 2*x+1, 'r--', lw=2, label='True relation')
    coeffs = np.polyfit(x, y, 1)
    ax.plot(x, coeffs[0]*x+coeffs[1], 'g-', lw=2, label='Fit')
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_title('Reproducible Visualization')
    ax.legend()
    ax.grid(alpha=0.3)
    # Metadata box
    txt = '\n'.join([f'{k}: {v}' for k,v in meta.items()])
    ax.text(0.02, 0.98, txt, transform=ax.transAxes, fontsize=8,
            verticalalignment='top', bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))
    plt.tight_layout()
    return fig

def provenance():
    info = {
        'timestamp': datetime.utcnow().isoformat()+'Z',
        'python': sys.version.split()[0],
        'platform': platform.system(),
        'numpy': np.__version__,
        'script_hash': hashlib.sha256(Path(__file__).read_bytes()).hexdigest()[:12],
        'seed': 42,
        'N': 100
    }
    try:
        import matplotlib
        info['matplotlib'] = matplotlib.__version__
    except: pass
    return info

def main():
    outdir = Path('reproducible_output')
    outdir.mkdir(exist_ok=True)
    
    prov = provenance()
    with open(outdir/'provenance.json', 'w') as f:
        json.dump(prov, f, indent=2)
    
    x, y = gen_data()
    meta = {'N': len(x), 'Slope': f'{np.polyfit(x,y,1)[0]:.3f}'}
    fig = make_plot(x, y, meta)
    fig.savefig(outdir/'plot.png', dpi=300)
    plt.close(fig)
    
    print(f"✓ Saved plot to {outdir/'plot.png'}")
    print(f"✓ Provenance: {outdir/'provenance.json'}")
    print("\nReproduce with: python", __file__)

if __name__ == '__main__':
    main()
```