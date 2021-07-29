import matplotlib.pyplot as plt
color=[0,255,0]
x=df[0, 1]
y=df[1, 0]
plt.scatter(x, y, c=color, alpha=1,s=234)
plt.show()
