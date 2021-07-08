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

print(xCords)
print(yCords)
print(xTimes)
print("    ")
print(R)
print(G)
print(B)
print(rgTimes)
"""x = [1,2,3,4]
y = [4,1,3,6]

plt.plot(x, y, '--', color=[1.0, 0.5, 0.25])

x = [5,6,7,8]
y = [1,3,5,2]

plt.scatter(x, y, c='lightblue')

plt.title('Nuage de points avec Matplotlib')
plt.xlabel('x')
plt.ylabel('y')
plt.show()"""
