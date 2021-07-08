from flask import Flask, render_template
import os
app = Flask(__name__)

file1 = "dir.txt"
file2 = "coordX.txt"
file3 = "coordY.txt"
file4 = "cycs.txt"
@app.route('/')
def audio():
    return render_template('saw.html')

di = ""
@app.route('/<mn>/giveVal')
def giveVal(mn):
    with open(file1, 'w') as filetowrite:
        filetowrite.write(mn)
    return mn

@app.route('/<n>/coordX')
def poseX(n):
    with open(file2, 'w') as filetowrite:
        filetowrite.write(n)
    return n
@app.route('/<n>/cycs')
def cycle(n):
    with open(file4, 'w') as filetowrite:
        filetowrite.write(n)
    return n
@app.route('/<n>/coordY')
def poseY(n):
    with open(file3, 'w') as filetowrite:
        filetowrite.write(n)
    return n

@app.route('/<x>/<y>/coords')
def coords(x, y):
    with open(file2, 'w') as filetowrite:
        filetowrite.write(x)
    with open(file3, 'w') as filetowrite:
        filetowrite.write(y)
    return x


@app.route('/getVal')
def getVal():
    f = open("dir.txt", "r")
    return f.read()


@app.route('/getCoord')
def getCoord():
    f = open(file2, "r")
    l = open(file3, "r")
    return l.read()
