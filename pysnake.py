from tkinter import *
import random as rand

canvasSize = 500
cellSize = 20
cellCount = canvasSize/cellSize
Snake = [] 

# Window frame
class Window(Frame):

    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.master = master 

# Class for each body part object
class snakePart():
    def __init__(self):
        self.x = 0
        self.y = 0
        self.oldx = 0
        self.oldy = 0

        self.direction = int

# Class for each food object
class food():
    def __init__(self):
        self.x = 0
        self.y = 0

def startGame():
    global Snake # Allows us to read and write from the snake object list created above
    
    snakeHead = snakePart() # Creates head object
    Snake.append(snakeHead) # Adds head object to list of snake parts

# Starting the window
root = Tk()
root.geometry((str(canvasSize)+"x"+str(canvasSize)))
root.title("PySnake")
root.configure(background='black')
app = Window(root)

# Creates the canvas
g = Canvas(root, width=canvasSize, height=canvasSize)
g.pack()

# Creates the grid
for i in range(int(cellCount)):
    # Horizontal lines
    g.create_line(0, i*cellSize, canvasSize, i*cellSize, width=1)

    # Vertical lines
    g.create_line(i*cellSize, 0, i*cellSize, canvasSize)



# Window mainloop 
root.mainloop()