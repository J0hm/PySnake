from tkinter import *
import random as rand
import time
import threading

canvasSize = 500
cellSize = 20
cellCount = canvasSize/cellSize
Snake = [] 
snakeDirection = int
tps = 10
running = False


class App(threading.Thread):

    def __init__(self):
        threading.Thread.__init__(self)
        self.start()

    def callback(self):
        self.root.quit()

    def run(self):
        self.root = Tk()
        self.root.protocol("WM_DELETE_WINDOW", self.callback)
        self.root.bind("<Key>", key)
        
        self.root.geometry((str(canvasSize)+"x"+str(canvasSize)))
        self.root.title("PySnake")
        self.root.configure(background='black')

        # Creates the canvas
        self.g = Canvas(self.root, width=canvasSize, height=canvasSize)
        self.g.pack()

        # Creates the grid
        for i in range(int(cellCount)):
            # Horizontal lines
            self.g.create_line(0, i*cellSize, canvasSize, i*cellSize, width=1)
            # Vertical lines
            self.g.create_line(i*cellSize, 0, i*cellSize, canvasSize)

        self.root.mainloop()
    
    def drawSnakePart(self, part):
        global cellSize

        # Sets the two points for the rectangle, top left and bottom left coords
        x1 = (part.x - 1) * cellSize
        y1 = (part.y - 1) * cellSize
        x2 = part.x * cellSize
        y2 = part.y * cellSize

        # Sets the ID of the part so it can be modifided/deleted later
        part.id = self.g.create_rectangle(x1, y1, x2, y2, fill=part.fillColor)

    def tick(self):
        if snakeDirection == 1:
            self.g.move(Snake[0], 0, 20)
        elif snakeDirection == 2:
            self.g.move(Snake[0], 0, -20)
        elif snakeDirection == 3:
            self.g.move(Snake[0], -20, 0)
        elif snakeDirection == 4:
            self.g.move(Snake[0], 20, 0)
        else: 
            print("nomove")

def runGame():
    running = True
    while running == True:
        app.tick()


def key(event):
    global snakeDirection
    keyPressed = str(event.char)
    
    if keyPressed == 'w':
        snakeDirection = 1
    elif keyPressed == 's':
        snakeDirection = 2
    elif keyPressed == 'a':
        snakeDirection = 3
    elif keyPressed == 'd':
        snakeDirection = 4
    else:
        return # Marginally improved efficiency 
    
    # Temp, used for debug
    print(snakeDirection)



app = App()
runGame()
