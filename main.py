import pygame, time, sys, random, _thread, tempfile, os
from pygame.locals import *
from tkinter.filedialog import askopenfilename
from tkinter import Tk
from imp import load_source
from operator import add

root = Tk()
root.withdraw()
root.wm_attributes('-topmost', 1)

pygame.init()

screen = pygame.display.set_mode((600, 600), RESIZABLE)

pygame.display.set_caption("CodeSnake")

scale = 1
name1 = "Select Snake"
name2 = "Select Snake"

title = "CodeSnake"

snake1 = None
snake2 = None

snake1Pos = []
snake2Pos = []
pelletPos = [0, 0]

snake1Length = 1
snake2Length = 1

moveFunction1 = None
moveFunction2 = None

resetFunction1 = None
resetFunction2 = None

gameInProgress = False

def setupLabels():
    global titleFont, titleLabel, buttonFont, button1Label, button2Label, startButtonFont, startButtonLabel
    titleFont = pygame.font.Font("assets/fonts/FORCED SQUARE.ttf", int(50*scale))
    titleLabel = titleFont.render(title, 0, (0, 0, 0))

    buttonFont = pygame.font.Font("assets/fonts/FORCED SQUARE.ttf", int(20*scale))
    button1Label = buttonFont.render(name1, 0, (255, 255, 255))
    button2Label = buttonFont.render(name2, 0, (255, 255, 255))

    startButtonFont = pygame.font.Font("assets/fonts/FORCED SQUARE.ttf", int(30*scale))
    startButtonLabel = startButtonFont.render("Start Game", 0, (255, 255, 255))

setupLabels()

gridSize = 400

cellsPerRow = 30

selectButtonSize = [185, 50]
startButtonSize = [300, 100]

file1 = None
file2 = None

def moveSnakes():
    global snake1Pos, snake2Pos, pelletPos, moveFunction1, moveFunction2, snake1Length, snake2Length, gameInProgress, title
    mapOutput = {"left": [-1, 0],
                 "right": [1, 0],
                 "up": [0, -1],
                 "down": [0, 1]}
    snake1Output = moveFunction1(snake1Pos[-1], snake2Pos[-1], pelletPos)
    snake2Output = moveFunction2(snake2Pos[-1], snake1Pos[-1], pelletPos)
    snake1Pos.append([x % cellsPerRow for x in list(map(add, snake1Pos[-1], mapOutput[snake1Output]))])
    snake2Pos.append([x % cellsPerRow for x in list(map(add, snake2Pos[-1], mapOutput[snake2Output]))])

    if snake1Pos[-1] == pelletPos:
        snake1Length += 1
        pelletPos = [random.randint(0, cellsPerRow-1), random.randint(0, cellsPerRow-1)]
        while pelletPos in snake1Pos[-snake2Length:] or pelletPos in snake2Pos[-snake2Length:]:
            pelletPos = [random.randint(0, cellsPerRow-1), random.randint(0, cellsPerRow-1)]

    if snake2Pos[-1] == pelletPos:
        snake2Length += 1
        pelletPos = [random.randint(0, cellsPerRow-1), random.randint(0, cellsPerRow-1)]
        while pelletPos in snake1Pos[-snake2Length:] or pelletPos in snake2Pos[-snake2Length:]:
            pelletPos = [random.randint(0, cellsPerRow-1), random.randint(0, cellsPerRow-1)]

    if snake1Pos[-1] == snake2Pos[-1]:
        gameInProgress = False
        title = "Draw!"
    if snake1Pos[-1] in snake2Pos[-snake2Length:-1] or snake1Pos[-1] in snake1Pos[-snake1Length:-1]:
        gameInProgress = False
        title = "Player 2 Wins!"
    if snake2Pos[-1] in snake1Pos[-snake1Length:-1] or snake2Pos[-1] in snake2Pos[-snake2Length:-1]:
        gameInProgress = False
        title = "Player 1 Wins!"

    if not gameInProgress:
        setupLabels()
        resetFunction1()
        resetFunction2()
        
def runGame():
    while gameInProgress:
        time.sleep(0.05)
        moveSnakes()

while True:
    mousePos = pygame.mouse.get_pos()
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            gameInProgress = False
            sys.exit()
        if event.type == VIDEORESIZE:
            scale = min(event.size)/600
            screen = pygame.display.set_mode(event.size, RESIZABLE)
            setupLabels()
        if event.type == MOUSEBUTTONDOWN:
            if not gameInProgress:
                if (screen.get_width()-30*scale)/2-selectButtonSize[0]*scale <= mousePos[0] <= (screen.get_width()-30*scale)/2:
                    if screen.get_height()-30*scale-selectButtonSize[1]*scale <= mousePos[1] <= screen.get_height()-30*scale-selectButtonSize[1]*scale+selectButtonSize[1]*scale:
                        file1 = askopenfilename(filetypes=[("Python files", "*.py")])
                        if file1:
                            snake1 = load_source(".".join(file1.split(".")[:-1]).split("/")[-1], file1)
                            moveFunction1 = getattr(snake1, "move")
                            name1 = getattr(snake1, "name")
                            resetFunction1 = getattr(snake1, "reset")
                            setupLabels()
                if (screen.get_width()+30*scale)/2 <= mousePos[0] <= (screen.get_width()-30*scale)/2+selectButtonSize[0]*scale:
                    if screen.get_height()-30*scale-selectButtonSize[1]*scale <= mousePos[1] <= screen.get_height()-30*scale-selectButtonSize[1]*scale+selectButtonSize[1]*scale:
                        file2 = askopenfilename(filetypes=[("Python files", "*.py")])
                        if file2:
                            if file2 == file1:
                                file, file2 = tempfile.mkstemp()
                                os.close(file)
                                with open(file1) as read:
                                    data = read.read()
                                with open(file2, "w") as write:
                                    write.write(data)
                            snake2 = load_source(".".join(file2.split(".")[:-1]).split("/")[-1], file2)
                            moveFunction2 = getattr(snake2, "move")
                            name2 = getattr(snake2, "name")
                            resetFunction2 = getattr(snake2, "reset")
                            setupLabels()
            if not gameInProgress and snake1 and snake2:
                if (screen.get_width()-startButtonSize[0]*scale)/2 <= mousePos[0] <= (screen.get_width()+startButtonSize[0]*scale)/2:
                    if (screen.get_height()-startButtonSize[1]*scale)/2 <= mousePos[1] <= (screen.get_height()+startButtonSize[1]*scale)/2:
                        gameInProgress = True
                        title = "CodeSnake"
                        setupLabels()
                        snake1Length = 1
                        snake2Length = 1
                        snake1Pos = [[random.randint(0, cellsPerRow-1), random.randint(0, cellsPerRow-1)]]
                        snake2Pos = [[random.randint(0, cellsPerRow-1), random.randint(0, cellsPerRow-1)]]
                        while snake2Pos == snake1Pos:
                            snake2Pos = [[random.randint(0, cellsPerRow-1), random.randint(0, cellsPerRow-1)]]
                        pelletPos = [random.randint(0, cellsPerRow-1), random.randint(0, cellsPerRow-1)]
                        while pelletPos == snake1Pos[0] or pelletPos == snake2Pos[0]:
                            pelletPos = [random.randint(0, cellsPerRow-1), random.randint(0, cellsPerRow-1)]
                        _thread.start_new_thread(runGame, ())
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                gameInProgress = False

    screen.fill((255, 255, 255))

    screen.blit(titleLabel, ((screen.get_width()-titleLabel.get_width())/2, 30*scale))

    pygame.draw.rect(screen, (200, 200, 200), ((screen.get_width()-gridSize*scale)/2, titleLabel.get_height()+60*scale, gridSize*scale, gridSize*scale))
    for row in range(cellsPerRow):
        for col in range(cellsPerRow):
            rect = ((screen.get_width()-gridSize*scale)/2+row*gridSize*scale/cellsPerRow, titleLabel.get_height()+60*scale+col*gridSize*scale/cellsPerRow, gridSize*scale/cellsPerRow, gridSize*scale/cellsPerRow)
            pygame.draw.rect(screen, (150, 150, 150), rect, 3)
            if gameInProgress:
                if [row,col] in snake1Pos[-snake1Length:]:
                    pygame.draw.rect(screen, (255, 0, 0), rect)
                if [row,col] in snake2Pos[-snake2Length:]:
                    pygame.draw.rect(screen, (0, 255, 0), rect)
                if [row,col] == pelletPos:
                    pygame.draw.rect(screen, (255, 255, 255), rect)
    pygame.draw.rect(screen, (0, 0, 0), ((screen.get_width()-gridSize*scale)/2, titleLabel.get_height()+60*scale, gridSize*scale, gridSize*scale), 3)

    button1Colour = (150, 90, 90)
    if (screen.get_width()-30*scale)/2-selectButtonSize[0]*scale <= mousePos[0] <= (screen.get_width()-30*scale)/2:
        if screen.get_height()-30*scale-selectButtonSize[1]*scale <= mousePos[1] <= screen.get_height()-30*scale-selectButtonSize[1]*scale+selectButtonSize[1]*scale:
            button1Colour = (100, 50, 50)

    button2Colour = (90, 150, 90)
    if (screen.get_width()+30*scale)/2 <= mousePos[0] <= (screen.get_width()-30*scale)/2+selectButtonSize[0]*scale:
        if screen.get_height()-30*scale-selectButtonSize[1]*scale <= mousePos[1] <= screen.get_height()-30*scale-selectButtonSize[1]*scale+selectButtonSize[1]*scale:
            button2Colour = (50, 100, 50)
            
    pygame.draw.rect(screen, button1Colour, ((screen.get_width()-30*scale)/2-selectButtonSize[0]*scale, screen.get_height()-30*scale-selectButtonSize[1]*scale, selectButtonSize[0]*scale, selectButtonSize[1]*scale))
    pygame.draw.rect(screen, (0, 0, 0), ((screen.get_width()-30*scale)/2-selectButtonSize[0]*scale, screen.get_height()-30*scale-selectButtonSize[1]*scale, selectButtonSize[0]*scale, selectButtonSize[1]*scale), 3)
    screen.blit(button1Label, ((screen.get_width()-30*scale-selectButtonSize[0]*scale-button1Label.get_width())/2, screen.get_height()-30*scale-(selectButtonSize[1]*scale+button1Label.get_height())/2))

    pygame.draw.rect(screen, button2Colour, ((screen.get_width()+30*scale)/2, screen.get_height()-30*scale-selectButtonSize[1]*scale, selectButtonSize[0]*scale, selectButtonSize[1]*scale))
    pygame.draw.rect(screen, (0, 0, 0), ((screen.get_width()+30*scale)/2, screen.get_height()-30*scale-selectButtonSize[1]*scale, selectButtonSize[0]*scale, selectButtonSize[1]*scale), 3)
    screen.blit(button2Label, ((screen.get_width()+30*scale+selectButtonSize[0]*scale-button2Label.get_width())/2, screen.get_height()-30*scale-(selectButtonSize[1]*scale+button2Label.get_height())/2))

    if not gameInProgress and snake1 and snake2:
        startButtonColour = (90, 90, 150)
        if (screen.get_width()-startButtonSize[0]*scale)/2 <= mousePos[0] <= (screen.get_width()+startButtonSize[0]*scale)/2:
            if (screen.get_height()-startButtonSize[1]*scale)/2 <= mousePos[1] <= (screen.get_height()+startButtonSize[1]*scale)/2:
                startButtonColour = (50, 50, 100)
        pygame.draw.rect(screen, startButtonColour, ((screen.get_width()-startButtonSize[0]*scale)/2, (screen.get_height()-startButtonSize[1]*scale)/2, startButtonSize[0]*scale, startButtonSize[1]*scale))
        pygame.draw.rect(screen, (0, 0, 0), ((screen.get_width()-startButtonSize[0]*scale)/2, (screen.get_height()-startButtonSize[1]*scale)/2, startButtonSize[0]*scale, startButtonSize[1]*scale), 3)
        screen.blit(startButtonLabel, ((screen.get_width()-startButtonLabel.get_width())/2, (screen.get_height()-startButtonLabel.get_height())/2))

    keys = pygame.key.get_pressed()

    pygame.display.update()
    time.sleep(0.01)
