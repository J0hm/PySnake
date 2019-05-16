from tkinter import *
import random as rand


canvasSize = 500
cellSize = 20
cellCount = canvasSize/cellSize
Snake = [] 
snakeDirection = int

# Window frame
class Window(Frame):

    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.master = master 
        master.bind("<Key>", key) # Key press handler


# Class for each body part object
class snakePart():
    def __init__(self):
        # x and y are the cell, not the
        self.x = 0
        self.y = 0
        self.oldx = 0
        self.oldy = 0
        self.id = int
        self.fillColor = "green" # Default for body - head would be changed to black


# Class for each food object
class food():
    def __init__(self):
        self.x = 0
        self.y = 0


# Starts the game (initilization)
def startGame():
    # Defines which varibles are the globals used above and not local
    global Snake 
    global cellCount 

    g.delete("all") # Resets canvas

    # Creates the grid
    for i in range(int(cellCount)):
        # Horizontal lines
        g.create_line(0, i*cellSize, canvasSize, i*cellSize, width=1)

        # Vertical lines
        g.create_line(i*cellSize, 0, i*cellSize, canvasSize)

    snakeHead = snakePart() # Creates head object
    Snake.append(snakeHead) # Adds head object to list of snake parts

    # Sets snake head properties 
    Snake[0].color = "black"

    # Draws off center if there is no exact center
    if (cellCount % 2) == 0:
        Snake[0].x = cellCount/2
        Snake[0].y = cellCount/2
    else:
        Snake[0].x = (cellCount-1)/2
        Snake[0].y = (cellCount-1)/2

    drawSnakePart(Snake[0])


def drawSnakePart(part):
    global cellSize

    # Sets the two points for the rectangle, top left and bottom left coords
    x1 = (part.x - 1) * cellSize
    y1 = (part.y - 1) * cellSize
    x2 = part.x * cellSize
    y2 = part.y * cellSize

    # Sets the ID of the part so it can be modifided/deleted later
    part.id = g.create_rectangle(x1, y1, x2, y2, fill=part.fillColor)


def key(event):
    global snakeDirection
    keyPressed = str(event.char)
    
    if keyPressed == 'w':
        snakeDirection = 1
    elif keyPressed == 's':
        snakeDirection = 2
    elif keyPressed == 'a':
        snakeDirection = 3
    else:
        snakeDirection = 4
    
    
    print(snakeDirection)
        


# Starts the window and sets properties 
root = Tk()
root.geometry((str(canvasSize)+"x"+str(canvasSize)))
root.title("PySnake")
root.configure(background='black')
app = Window(root)

# Creates the canvas
g = Canvas(root, width=canvasSize, height=canvasSize)
g.pack()

startGame()

# Window mainloop 
root.mainloop()