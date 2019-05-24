from tkinter import *
import random as rand
import time
import threading
from tkinter import messagebox

# Constants
canvasSize = 900
cellSize = 30
cellCount = canvasSize/cellSize
Snake = [] 
secondSnake = []
FoodObjectList = [] # Only using one food object so this isnt necessary, but it allows for more if you want
snakeDirection = int
secondSnakeDirection = int
tps = 20
running = False
U1Score = 0
U2Score = 0
highScore = 0
padding = 50 # Amount of pixels for the padding under the canvas

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
        self.root.bind("<Key>", self.key) # Keyboard event logging
        
        self.root.geometry((str(canvasSize+6)+"x"+str(canvasSize+padding))) # Sets size of the window
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

        self.scoreLabel = Label(self.root, text="Score: " + str(U1Score) +" vs " + str(U2Score) + "          Total: " + str(U1Score+U2Score), font=("Helvetica", 16), fg="white", bg="black")
        self.scoreLabel.place(x=0, y=canvasSize+10)
        self.highScoreLabel = Label(self.root, text="High Score: " + str(highScore), font=("Helvetica", 16), fg="white", bg="black")
        self.highScoreLabel.place(x=300, y=canvasSize+10)

        snakeHead = snakePart() # Creates head object
        Snake.append(snakeHead) # Adds head object to list of snake parts

        secondSnakeHead = snakePart()
        secondSnake.append(secondSnakeHead)

        # Sets snake head properties 
        Snake[0].fillColor = "black"
        secondSnake[0].fillColor = "black"

        # Draws off center if there is no exact center
        if (cellCount % 2) == 0:
            Snake[0].x = cellCount/2
            Snake[0].y = cellCount/2
            secondSnake[0].x = Snake[0].x - 5
            secondSnake[0].y = Snake[0].y - 5
        else:
            Snake[0].x = (cellCount-1)/2
            Snake[0].y = (cellCount-1)/2
            secondSnake[0].x = Snake[0].x - 5
            secondSnake[0].y = Snake[0].y - 5

        self.drawSnakePart(Snake[0]) # Draws head
        self.drawSnakePart(secondSnake[0])

        FoodObjectList.append(food())

        # Main tkinter loop
        self.root.mainloop()
        
        
    # Resets the varibles, wipes Snake[]
    def reset(self):
        global Snake
        global secondSnake
        global snakeDirection
        global secondSnakeDirection
        global U1Score
        global U2Score
        global FoodObjectList

        for i in Snake:
            self.g.delete(i.id)

        for i in secondSnake:
            self.g.delete(i.id)

        secondSnake.clear()
        Snake.clear()

        snakeDirection = int
        secondSnakeDirection = int
       
        U1Score = 0
        U2Score = 0
        self.scoreLabel.config(text="Score: " + str(U1Score) +" vs " + str(U2Score) + "          Total: " + str(U1Score+U2Score))
        
        snakeHead = snakePart() # Creates head object
        Snake.append(snakeHead) # Adds head object to list of snake parts

        snakeHead2 = snakePart()
        secondSnake.append(snakeHead2)

        # Sets snake head properties 
        Snake[0].fillColor = "black"
        secondSnake[0].fillColor = "black"

        # Draws off center if there is no exact center
        if (cellCount % 2) == 0:
            Snake[0].x = cellCount/2
            Snake[0].y = cellCount/2
            secondSnake[0].x = Snake[0].x - 5
            secondSnake[0].y = Snake[0].y - 5
        else:
            Snake[0].x = (cellCount-1)/2
            Snake[0].y = (cellCount-1)/2
            secondSnake[0].x = Snake[0].x - 5
            secondSnake[0].y = Snake[0].y - 5

        self.drawSnakePart(Snake[0]) # Draws head
        self.drawSnakePart(secondSnake[0])

        self.g.delete(FoodObjectList[0].id)
        
        newFood = food()
        FoodObjectList[0] = newFood

        runGame()

        
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


    # Spawns a new food object
    def spawnNewFood(self):
        global FoodObjectList
        global Snake

        # Python does not have a do-while loop, so I made one 
        # This is supposed to ensure that no food spawns inside the snake: it must take an open spot
        while True:
            badSpawn = False
            self.g.delete(FoodObjectList[0].id)
            FoodObjectList[0] = food()

            for i in Snake:
                if FoodObjectList[0].x == i.x and FoodObjectList[0].y == i.y:
                    badSpawn = True
            
            if badSpawn == False:
                break


    # On key press...
    def key(self, event):
        global snakeDirection
        global secondSnakeDirection
        global tps
        keyPressed = str(event.char)

        # Sets snake direction. And statements are a failsafe to make it so you cant turn 180 degrees back into yourself
        if keyPressed == 'w' and snakeDirection != 2:
            snakeDirection = 1
            time.sleep(1/tps)
        elif keyPressed == 's' and snakeDirection != 1:
            snakeDirection = 2
            time.sleep(1/tps)
        elif keyPressed == 'a' and snakeDirection != 4:
            snakeDirection = 3
            time.sleep(1/tps)
        elif keyPressed == 'd' and snakeDirection != 3:
            snakeDirection = 4
            time.sleep(1/tps)
        elif keyPressed == "i" and secondSnakeDirection != 2:
            secondSnakeDirection = 1
        elif keyPressed == 'k' and secondSnakeDirection != 1:
            secondSnakeDirection = 2
            time.sleep(1/tps)
        elif keyPressed == 'j' and secondSnakeDirection != 4:
            secondSnakeDirection = 3
            time.sleep(1/tps)
        elif keyPressed == 'l' and secondSnakeDirection != 3:
            secondSnakeDirection = 4
            time.sleep(1/tps)
        else:
            return # Marginally improved efficiency 



    # Main tick function, called each tick 
    def tick(self):
        global tps
        global Snake
        global secondSnake
        global snakeDirection
        global secondSnakeDirection
        global running
        global U1Score
        global U2Score

        # Moves the snake head
        if snakeDirection == 1:
            self.g.move(Snake[0].id, 0, -cellSize)
            Snake[0].oldx = Snake[0].x
            Snake[0].oldy = Snake[0].y
            Snake[0].y = Snake[0].y - 1
        elif snakeDirection == 2:
            self.g.move(Snake[0].id, 0, cellSize)
            Snake[0].oldx = Snake[0].x
            Snake[0].oldy = Snake[0].y
            Snake[0].y = Snake[0].y + 1
        elif snakeDirection == 3:
            self.g.move(Snake[0].id, -cellSize, 0)
            Snake[0].oldx = Snake[0].x
            Snake[0].oldy = Snake[0].y
            Snake[0].x = Snake[0].x - 1
        elif snakeDirection == 4:
            self.g.move(Snake[0].id, cellSize, 0)
            Snake[0].oldx = Snake[0].x
            Snake[0].oldy = Snake[0].y
            Snake[0].x = Snake[0].x + 1

        # Moves the snake head
        if secondSnakeDirection == 1:
            self.g.move(secondSnake[0].id, 0, -cellSize)
            secondSnake[0].oldx = secondSnake[0].x
            secondSnake[0].oldy = secondSnake[0].y
            secondSnake[0].y = secondSnake[0].y - 1
        elif secondSnakeDirection == 2:
            self.g.move(secondSnake[0].id, 0, cellSize)
            secondSnake[0].oldx = secondSnake[0].x
            secondSnake[0].oldy = secondSnake[0].y
            secondSnake[0].y = secondSnake[0].y + 1
        elif secondSnakeDirection == 3:
            self.g.move(secondSnake[0].id, -cellSize, 0)
            secondSnake[0].oldx = secondSnake[0].x
            secondSnake[0].oldy = secondSnake[0].y
            secondSnake[0].x = secondSnake[0].x - 1
        elif secondSnakeDirection == 4:
            self.g.move(secondSnake[0].id, cellSize, 0)
            secondSnake[0].oldx = secondSnake[0].x
            secondSnake[0].oldy = secondSnake[0].y
            secondSnake[0].x = secondSnake[0].x + 1

        if len(Snake) > 0: # Fixes an error where the first iteration does not have any objects. No idea why it is happening as the same oject is beig modified earlier, but it works so im not going to try to fix it
            #print(Snake[0].x, ",", Snake[0].y) # For debugging 

            if Snake[0].x == 0 or Snake[0].x == cellCount+1 or Snake[0].y == 0 or Snake[0].y == cellCount+1 or secondSnake[0].x == 0 or secondSnake[0].y == 0 or secondSnake[0].x == cellCount+1 or secondSnake[0].y == cellCount+1: # When a wall is hit...
                running = False
                return

            for i in range(1, len(Snake)-1): # For each body part, not head
                if Snake[0].x == Snake[i].x and Snake[0].y == Snake[i].y: # If head hits any body part...
                    running = False
                    return

            # Moves entire snake
            # Set each part old coords to current
            # Set new coords to Snake[n-1] coords (shift by one)
            # Move snake by tuple(old coords) - tuple(new coords)
            for i in range(1, len(Snake)): # Iterate through indicies
                if i == len(Snake) - 1: # This if prevents the second sejailgment (Snake[1]) from drawing over the head. 
                    Snake[len(Snake)-i].oldx = Snake[len(Snake)-i].x
                    Snake[len(Snake)-i].oldy = Snake[len(Snake)-i].y
                    Snake[len(Snake)-i].x = Snake[(len(Snake)-i)-1].oldx
                    Snake[len(Snake)-i].y = Snake[(len(Snake)-i)-1].oldy
                else:
                    Snake[len(Snake)-i].oldx = Snake[len(Snake)-i].x
                    Snake[len(Snake)-i].oldy = Snake[len(Snake)-i].y
                    Snake[len(Snake)-i].x = Snake[(len(Snake)-i)-1].x
                    Snake[len(Snake)-i].y = Snake[(len(Snake)-i)-1].y

                deltaX = Snake[len(Snake)-i].x - Snake[len(Snake)-i].oldx
                deltaY = Snake[len(Snake)-i].y - Snake[len(Snake)-i].oldy
                self.g.move(Snake[len(Snake)-i].id, deltaX*cellSize, deltaY*cellSize)
            
            
            
            if Snake[0].x == FoodObjectList[0].x and Snake[0].y == FoodObjectList[0].y: # When food is hit...
                # Creates a new part and sets it to the previous position of the last part
                newSnakePart = snakePart()
                newSnakePart.x = Snake[(len(Snake)-1)].oldx
                newSnakePart.y = Snake[(len(Snake)-1)].oldy
                self.drawSnakePart(newSnakePart)
                Snake.append(newSnakePart)

                # Creates new food object
                self.spawnNewFood()

                # Increaces score
                U1Score += 1
                self.scoreLabel.config(text="Score: " + str(U1Score) +" vs " + str(U2Score) + "          Total: " + str(U1Score+U2Score))
           

        if len(secondSnake) > 0:
            for i in range(1, len(secondSnake)):
                if i == len(secondSnake) - 1:
                    secondSnake[len(secondSnake)-i].oldx = secondSnake[len(secondSnake)-i].x
                    secondSnake[len(secondSnake)-i].oldy = secondSnake[len(secondSnake)-i].y
                    secondSnake[len(secondSnake)-i].x = secondSnake[(len(secondSnake)-i)-1].oldx
                    secondSnake[len(secondSnake)-i].y = secondSnake[(len(secondSnake)-i)-1].oldy
                else:
                    secondSnake[len(secondSnake)-i].oldx = secondSnake[len(secondSnake)-i].x
                    secondSnake[len(secondSnake)-i].oldy = secondSnake[len(secondSnake)-i].y
                    secondSnake[len(secondSnake)-i].x = secondSnake[(len(secondSnake)-i)-1].x
                    secondSnake[len(secondSnake)-i].y = secondSnake[(len(secondSnake)-i)-1].y

                deltaX = secondSnake[len(secondSnake)-i].x - secondSnake[len(secondSnake)-i].oldx
                deltaY = secondSnake[len(secondSnake)-i].y - secondSnake[len(secondSnake)-i].oldy
                self.g.move(secondSnake[len(secondSnake)-i].id, deltaX*cellSize, deltaY*cellSize)

            if secondSnake[0].x == FoodObjectList[0].x and secondSnake[0].y == FoodObjectList[0].y:
                newSnakePart = snakePart()
                newSnakePart.x = secondSnake[(len(secondSnake)-1)].oldx
                newSnakePart.y = secondSnake[(len(secondSnake)-1)].oldy
                self.drawSnakePart(newSnakePart)
                secondSnake.append(newSnakePart)

                self.spawnNewFood()

                U2Score += 1
                self.scoreLabel.config(text="Score: " + str(U1Score) +" vs " + str(U2Score) + "          Total: " + str(U1Score+U2Score))

                for i in range(1, len(secondSnake)-1):
                    if secondSnake[0].x == secondSnake[i].x and secondSnake[0].y == secondSnake[i].y:
                        running = False
                        return

        for i in range(len(secondSnake)):
            if Snake[0].x == secondSnake[i].x and Snake[0].y == secondSnake[i].y:
                running = False
                return

        for i in range(len(Snake)):
            if secondSnake[0].x == Snake[i].x and secondSnake[0].y == Snake[i].y:
                running = False
                return

        time.sleep(1/tps) # Sleeps for 1 tick
          
    
# Class for each body part object
class snakePart():
    def __init__(self):
        # x and y are the cell coords, not the pixel coords
        self.x = 0
        self.y = 0
        self.oldx = 0
        self.oldy = 0
        self.id = int
        self.fillColor = "green" # Default for body - head would be changed to black
    

# Class for each food object
class food():
    def __init__(self):
        self.x = rand.randrange(1, cellCount+1) # Rangrange is not inclusive of the upper bound
        self.y = rand.randrange(1, cellCount+1) # Thats why we use cellCount+1
        self.id = app.g.create_rectangle(((self.x-1)*cellSize), ((self.y-1)*cellSize), (self.x*cellSize), (self.y*cellSize), fill="red") # Weird math to draw the parts correctly
    
    
# Main tick loop 
def runGame():
    global running
    global U1Score
    global U2Score
    global highScore
    running = True

    # Tick loop
    while running == True:
        app.tick()
    
    scoreMessage = "You have lost. Score: " + str(U1Score) + " vs " + str(U2Score) + "     Total: " + str(U1Score + U2Score)

    messagebox.showinfo("Game Over", scoreMessage)

    #if score > highScore:
       # highScore = score
        #app.highScoreLabel.config(text="High Score: " + str(highScore))

    # Resets the game
    app.reset()


# Initializes class object of App to app
app = App()
# Calls function to run game an start the two loops
runGame()
