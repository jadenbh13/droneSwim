import numpy as np
from scipy.interpolate import griddata
import matplotlib.pyplot as plt

import time

numbList = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '.']
def onlyNumbs(st):
    mnS = ""
    for t in st:
        if t in numbList:
            mnS += t
    if mnS != "":
        return float(mnS)

xFile = "demo.txt"
colFile = "demo2.txt"

xCords = []
yCords = []
xTimes = []

with open(xFile, "r") as fileRead:
    re = fileRead.read()
    real = re.split("\n")
    for g in real:
        rL = g.split(',')
        #print(g)
        print(rL)
        try:
            if len(rL) > 1:
                xCords.append(onlyNumbs(rL[0]))
                yCords.append(onlyNumbs(rL[1]))
                xTimes.append(onlyNumbs(rL[2]))
        except:
            print("Could not convert")

R = []
G = []
B = []
rgTimes = []

with open(colFile, "r") as fileRead:
    re = fileRead.read()
    real = re.split("\n")
    #print(real)
    for g in real:
        rL = g.split(',')
        #print(g)
        print(rL)
        if len(rL) > 1:
            R.append(onlyNumbs(rL[0]))
            G.append(onlyNumbs(rL[1]))
            B.append(onlyNumbs(rL[2]))
            rgTimes.append(onlyNumbs(rL[3]))

x = np.linspace(-1, 1, 100)
y =  np.linspace(-1, 1, 100)
print(x)
print(y)
X, Y = np.meshgrid(x,y)

def f(x, y):
    s = np.hypot(x, y)
    phi = np.arctan2(y, x)
    tau = s + s*(1-s)/5 * np.sin(6*phi)
    return 5*(1-tau) + tau

T = f(X, Y)
npts = 400
px, py = np.random.choice(x, npts), np.random.choice(y, npts)

plt.contourf(X, Y, T)
plt.scatter(px, py, c='k', alpha=0.2, marker='.')

plt.show()
