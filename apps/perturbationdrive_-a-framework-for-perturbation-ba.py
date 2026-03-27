```python
#!/usr/bin/env python3
"""
PerturbationDrive: ADAS Perturbation Testing Demo
Based on arXiv:2603.23661v1
"""

import numpy as np
import cv2

def make_scene():
    """Synthetic road with stop sign"""
    img = np.zeros((480, 640, 3), np.uint8)
    img[:200] = (135, 206, 235)  # Sky BGR
    img[200:] = (100, 100, 100)   # Road
    # Stop sign (red octagon)
    c = (480, 320)
    pts = np.array([[-40,-30],[-20,-50],[20,-50],[40,-30],
                    [40,30],[20,50],[-20,50],[-40,30]]) + c
    cv2.fillPoly(img, [pts], (0,0,255))
    cv2.polylines(img, [pts], True, (255,255,255), 3)
    return img

def detect_stop_sign(img):
    """Mock ADAS: color-based stop sign detector"""
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    m1 = cv2.inRange(hsv, (0,100,100), (10,255,255))
    m2 = cv2.inRange(hsv, (160,100,100), (180,255,255))
    red = np.sum(cv2.bitwise_or(m1, m2) > 0)
    return red / img.size

def gaussian_noise(img, s=25):
    n = np.random.randn(*img.shape) * s
    return np.clip(img.astype(np.float32)+n, 0, 255).astype(np.uint8)

def motion_blur(img, k=15):
    ker = np.zeros((k, k)); ker[k//2,:] = 1/k
    return cv2.filter2D(img, -1, ker)

def rain_effect(img, drops=50):
    r = img.copy()
    for _ in range(drops):
        x, y = np.random.randint(0, [img.shape[1], img.shape[0]])
        l = np.random.randint(10, 30)
        a = np.random.randint(-30, 30)
        ex, ey = int(x + l*np.cos(np.radians(a))), int(y + l*np.sin(np.radians(a)))
        cv2.line(r, (x,y), (ex,ey), (200,200,255), 1)
    return r

def occlusion(img, sz=80):
    o = img.copy()
    x, y = np.random.randint(0, [img.shape[1]-sz, img.shape[0]-sz])
    cv2.rectangle(o, (x,y), (x+sz, y+sz), (0,0,0), -1)
    return o

def main():
    print("🌧️ PerturbationDrive: ADAS Testing Framework")
    print("   arXiv:2603.23661v1 demo"); print("="*50)
    
    clean = make_scene()
    base = detect_stop_sign(clean)
    print(f"\n📸 Clean confidence: {base:.3f}")
    
    tests = [
        ("Gaussian σ=25", lambda i: gaussian_noise(i, 25)),
        ("Motion blur k=15", lambda i: motion_blur(i, 15)),
        ("Rain 50 drops", lambda i: rain_effect(i, 50)),
        ("Occlusion 80px", lambda i: occlusion(i, 80)),
        ("Combo noise+blur", lambda i: motion_blur(gaussian_noise(i, 20), 10))
    ]
    
    print("\n🧪 Perturbation results:"); print("-"*50)
    print(f"{'Perturbation':<25} {'Conf':<8} {'Drop':<8}")
    print("-"*50)
    
    drops = []
    for name, fn in tests:
        p = fn(clean)
        c = detect_stop_sign(p)
        d = (base - c) / base * 100 if base else 0
        drops.append(d)
        print(f"{name:<25} {c:.3f}  {d:>5.1f}%")
    
    print("-"*50)
    print(f"\n📊 Avg drop: {np.mean(drops):.1f}%")
    print(f"   Worst: {max(drops):.1f}%")
    print("\n💡 ADAS perception is fragile to common perturbations.")
    print("   Robustness testing essential before deployment.")
    print("="*50)

if __name__ == "__main__":
    main()
```