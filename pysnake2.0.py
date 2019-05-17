from tkinter import *
import random as rand
import time
import threading

# Constants
canvasSize = 500
cellSize = 20
cellCount = canvasSize/cellSize
Snake = [] 
snakeDirection = int
tps = 10
running = False

# Main class for everything tkinter (graphics library)
class App(threading.Thread):
    # Creates and starts a new thread. This is needed so that the tkinter mainloop() can run at the same time as our tick loop
    def __init__(self):
        threading.Thread.__init__(self)
        self.start()
    
    
    # Stops the tkinter loop and thread. Prevents issues when closing the program
    def callback(self):
        self.root.quit()
    
    
    # Main function, creates GUI and frame
    def run(self):
        self.root = Tk() # Creationg of main frame
        self.root.protocol("WM_DELETE_WINDOW", self.callback) # Window is closed
        self.root.bind("<Key>", key) # Keyboard event logging
        
        self.root.geometry((str(canvasSize)+"x"+str(canvasSize))) # Sets size of the window
        self.root.title("PySnake") # Sets window title
        self.root.configure(background='black') # Sets window background color

        # Creates the canvas
        self.g = Canvas(self.root, width=canvasSize, height=canvasSize)
        self.g.pack()

        # Creates the grid
        for i in range(int(cellCount)):
            # Horizontal lines
            self.g.create_line(0, i*cellSize, canvasSize, i*cellSize, width=1)
            # Vertical lines
            self.g.create_line(i*cellSize, 0, i*cellSize, canvasSize)
        
        # Main tkinter loop
        self.root.mainloop()
    
    
    # Draws a snake part to the canvas. Part must be a snakePart class object
    def drawSnakePart(self, part):
        global cellSize

        # Sets the two points for the rectangle, top left and bottom left coords
        x1 = (part.x - 1) * cellSize
        y1 = (part.y - 1) * cellSize
        x2 = part.x * cellSize
        y2 = part.y * cellSize

        # Sets the ID of the part so it can be modifided/deleted later
        part.id = self.g.create_rectangle(x1, y1, x2, y2, fill=part.fillColor)

        
    # Main tick function, called each tick 
    def tick(self):
        # Moves the snake head
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
          
            
# Main tick loop 
def runGame():
    running = True
    while running == True:
        app.tick()


# Sets snake direction on keypress
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
