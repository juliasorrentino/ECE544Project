import random
import queue
from tkinter import *
import time
import math


class Block:
    def __init__(self, x1, y1, x2, y2):
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2
        self.marked = 0
        self.ship = 0
        self.colour = "white"

    def checkClick(self, x, y):
        if((x >= self.x1) and (x <= self.x2) and (x >= self.x1) and (x <= self.x2)):
            return 1
        else:
            return 0

    def markBlock(self, canvas):
        if(self.ship == 0):
            canvas.create_line(self.x1, self.y1, self.x2,
                               self.y2, fill="red", width=2)
            canvas.create_line(self.x1+50, self.y1, self.x2 -
                               50, self.y2, fill="red", width=2)
        else:
            canvas.create_rectangle(
                self.x1, self.y1, self.x2, self.y2, fill=self.colour)
            canvas.create_line(self.x1, self.y1, self.x2,
                               self.y2, fill="white", width=2)
            canvas.create_line(self.x1+50, self.y1, self.x2 -
                               50, self.y2, fill="white", width=2)
            print(self.x1, self.y1, self.x2, self.y2)
        self.marked = 1

    def markTarget(self, canvas):
        canvas.create_rectangle(self.x1, self.y1, self.x2,
                                self.y2, fill=self.colour)
        self.marked = 1

    def markPerson(self, canvas):
        canvas.create_oval(self.x1, self.y1, self.x2, self.y2,
                           fill="", outline="blue", width=4)
        self.marked = 1

    def setShip(self, x, canvas):
        print(x)
        self.ship = x
        if(x == 1):
            self.colour = "green"
        elif(x == 2):
            self.colour = "violet"
        elif(x == 3):
            self.colour = "blue"
        elif(x == 4):
            self.colour = "orange"
        elif(x == 5):
            self.colour = "black"


class RootClass:
    def __init__(self, name):
        self.Blocks = []
        self.canvas = 0
        self.name = name
        self.x = 0
        self.y = 0
        self.clickedFlag = 0
        self.rows = 0
        self.cols = 0

    def getCanvas(self):
        return self.canvas

    def getClickedBox(self, event):
        self.clickedFlag = 0
        for i in range(0, self.rows):
            for j in range(0, self.cols):
                if((self.Blocks[i][j].marked == 0)and(self.Blocks[i][j].checkClick(event.x, event.y) == 1)):
                    self.x = i
                    self.y = j
                    self.clickedFlag = 1

    def create_grid(self, rows, columns, event=None):
        w = self.canvas.winfo_width()
        h = self.canvas.winfo_height()
        self.canvas.delete('grid_line')
        for i in range(0, w, int(w/rows)):
            self.canvas.create_line([(i, 0), (i, h)], tag='grid_line', width=2)
        for i in range(0, h, int(h/columns)):
            self.canvas.create_line([(0, i), (w, i)], tag='grid_line', width=2)

    def getBlocks(self):
        return self.Blocks

    def makeRoot(self, matrix, root):
        rows = len(matrix)
        root.title(self.name)
        columns = len(matrix[0])
        self.rows = rows
        self.cols = columns
        self.canvas = Canvas(root, height=500, width=500, bg='white')
        self.canvas.pack(fill=BOTH, expand=True)
        w = 500
        h = 500
        self.canvas.bind(
            '<Configure>', lambda X: self.create_grid(rows, columns))
        for i in range(0, rows):
            self.Blocks.append([0, 0, 0, 0, 0, 0, 0, 0, 0, 0])

        for i in range(0, w, int(w/rows)):
            for j in range(0, h, int(h/columns)):
                self.Blocks[int(i/50)][int(j/50)] = Block(i, j, i+50, j+50)

        for i in range(0, rows):
            for j in range(0, columns):
                if(matrix[i][j] != 0):
                    self.Blocks[i][j].setShip(matrix[i][j], self.canvas)

    def Update(self, root):
        root.update()


def makeMatrix(shipPosition):
    matrix = list()
    for i in range(0, 10):
        matrix.append([0, 0, 0, 0, 0, 0, 0, 0, 0, 0])
    num = 1
    for i in shipPosition:
        for j in i:
            matrix[j[0]][j[1]] = num
        num = num+1
    return matrix

#if shot is within 1 block of a "person" stop operation
def safety(place):
    shot = place
    p1 = [2, 2]
    p2 = [5, 7]
    distance1 = math.sqrt(((shot[0]-p1[0])**2)+((shot[1]-p1[1])**2))
    distance2 = math.sqrt(((shot[0]-p2[0])**2)+((shot[1]-p2[1])**2))
    if distance1 < 2:
        print("Unable to fire, unknown object detected")
        safeEnable = 1
    elif distance2 < 2:
        print("Unable to fire, unknown object detected")
        safeEnable = 1
    else:
        safeEnable = 0
    return safeEnable

#Update the failure rate for use of the second system
def availability(time2, currentFailRate):
    '''if time.time() - time2 < 5:
        print("System 2 is offline")
        time.sleep(0.5)
        fail = currentFailRate
    else:
        '''
    print("System 2 will be used")
    avail2 = 1
    fail = 0.4
    return fail

#Calculate if the system will fail based on a constant failure rate
def calcFail(fail):
    rand = random.randint(1, 100)
    #print statements for debugging
    #print(rand)
    #print(100*fail)
    if rand < (100*fail):

        print("System failure")
        return True
    else:
        return False

#Calculate the type of failure the system experiences
def calcError(pos):
    rand = random.randint(0, 1)

    if rand == 0:   # Does not fire
        pos = (99, 99)
    else: #misses target
        randx = random.randint(0, 9)
        randy = random.randint(0, 9)
        pos = (randx, randy)
    
    return pos

#Function to shoot a specific position
def shoot(p):
    while(matrix[p[0]][p[1]] == -1):
        print(p, "has already been hit")
        temp = input("Enter a new x,y coordinate: ")
        x = int(temp[0])
        y = int(temp[1])
        p = (x, y)
    flag = matrix[p[0]][p[1]]
    matrix[p[0]][p[1]] = -1

    Window.Update(root)
    Blocks = Window.getBlocks()
    Blocks[p[0]][p[1]].markBlock(Window.getCanvas())
    if(flag > 0):
        hitFlag = (p[0], p[1])
        print("System has hit the target")
        targetLengths[flag-1] -= 1
        if(targetLengths[flag-1] == 0):
            targetSunk.append(flag)
            print("Target fully hit")
    else:
        hitFlag = (-1, -1)
        print("System has Missed")
        print()

#Initialize Variables
Window = RootClass("Tracking System")
targetPositions = [[(5, 6), (4, 6), (3, 6), (2, 6)], [(7, 5), (7, 4)]]
print(targetPositions)
matrix = makeMatrix(targetPositions)
root = Tk()
targetLengths = [4, 2]
targetSunk = list()
sEnable = 0
count = 0
avail1 = 0
avail2 = 0
last1 = time.time() - 10
last2 = time.time() - 10
failRate = 0.1

#Initialize GUI
Window.makeRoot(matrix, root)
Blocks = Window.getBlocks()
Blocks[5][6].markTarget(Window.getCanvas())
Blocks[4][6].markTarget(Window.getCanvas())
Blocks[3][6].markTarget(Window.getCanvas())
Blocks[2][6].markTarget(Window.getCanvas())
Blocks[7][5].markTarget(Window.getCanvas())
Blocks[7][4].markTarget(Window.getCanvas())
person1 = Blocks[2][2].markPerson(Window.getCanvas())
person2 = Blocks[5][7].markPerson(Window.getCanvas())

#Allow the user to select the critical element for a given simulation
print("Select critical element for the system: ")
print("0: Reliability")
print("1: Saftey")
print("2: Availability")
crit = int(input(""))
# while (crit != 0):
#    crit=int(input("Not a valid choice please try again: "))

while((len(targetSunk) != 2)):

    #Take position of anticipated shot
    position = input("\nEnter x,y coordinates of your desired target: ")
    x = int(position[0])
    y = int(position[2])
    position = (x, y)

    #Check if system 1 is available
    while time.time() - last1 < 10:
        print("System 1 unavailable")
        if crit == 2:
            #failRate = availability(last2)
            failRate = 0.4
            break
        else:
            while (time.time() - last1 < 10):
                print("Waiting for system 1 to be back online")
                time.sleep(0.5)
            failRate = 0.1
            avail1 = 0

    #Determine if the system will experience a failure
    fail = calcFail(failRate)

    if fail == False:
        #Perform functions specific to safety or availability
        if(crit == 1):
            sEnable = safety(position)
        elif(crit == 2):
            if(avail1 == 1):
                print("System 1 unavailable")
                if(avail2 == 0):
                    print("Using system 2")

        #if safety is not enabled
        if(sEnable == 0):
            #set the time each launcher was last used
            if avail1 == 0:
                avail1 = 1
                last1 = time.time()
            else:
               #avail2 = 1
                last2 = time.time()

            shoot(position)

            print()
            time.sleep(0.5)
            Window.Update(root)

        else:
            continue
    else:
        #Perform failure actions
        position = calcError(position)
        if position == (99, 99):
            print("Info - unable to fire")
        else:
            print("Info - inaccurate shot")
            shoot(position)