import math
import cmath
import time

W = [] # Your tuple of complex numbers, I'm just going to put values from cos(x)+jsin(x) into it
for x in range(-180,180):
    W.append(complex(math.cos(x*math.pi/180), math.sin (x*math.pi/180)))

mag = [] # Instantiating the mag list
o = math.pi/180 # Radians to degrees conversion factor
p = [] # Instantiating the list of phase angles


for z in W:
    mag.append(abs(z)) # Adding the magnitudes to mag
    p.append(180 - cmath.phase(z)/o) # Adding the phase angles to p (in degrees, in the range [0,360]

# Instantiating r, g, b arrays
r = [None] * len(W)
g = [None] * len(W)
b = [None] * len(W)

# The three main MATLAB code blocks, in order
for i in range(0, len(p)):
    if (p[i] < 144 and p[i] >= 0):
        r[i] = p[i] / 144
        g[i] = (144 - p[i]) / 144
        b[i] = 0
    elif (p[i] >= 144 and p[i] < 288):
        r[i] = (288 - p[i]) / 144
        g[i] = 0
        b[i] = (p[i] - 144) / 144
    else:
        r[i] = 0
        g[i] = (p[i] - 288) / 72
        b[i] = (360 - p[i]) / 72

# Instantiating R, G, B arrays
R = [None] * len(r)
B = [None] * len(b)
G = [None] * len(g)

# The last MATLAB code block
for i in range(0, len(r)):
    R[i] = math.floor(r[i] * mag[i] * 255.99)
    G[i] = math.floor(g[i] * mag[i] * 255.99)
    B[i] = math.floor(b[i] * mag[i] * 255.99)

for i in range(0, len(R)):
    print("R: " + str(R[i]) + " G: " + str(G[i]) + " B: " + str(B[i]))
    time.sleep(0.1)
