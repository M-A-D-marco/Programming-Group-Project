# Memory
import random
import pygame
import sys
from pygame.locals import *

FPS = 30
WINDOWWIDTH = 800
WINDOWHEIGHT = 600
REVEALSPEED = 8
BOXSIZE = 40
GAPSIZE = 10
BOARDWIDTH = 5
BOARDHEIGHT = 4

assert (BOARDWIDTH * BOARDHEIGHT) % 2 == 0, 'Board must have an even number of boxes for pairs of matches.'

XMARGIN = int((WINDOWWIDTH - (BOARDWIDTH * (BOXSIZE + GAPSIZE))) / 2)
YMARGIN = int((WINDOWHEIGHT - (BOARDHEIGHT * (BOXSIZE + GAPSIZE))) / 2)

# Colors
GRAY = (100, 100, 100)
NAVYBLUE = (60, 60, 100)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 102, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
BLACK = (0, 0, 0)
BGCOLOR = BLACK
LIGHTBGCOLOR = GRAY
BOXCOLOR = WHITE
HIGHLIGHTCOLOR = BLUE

# Themes
themes = {
    'default': {'colors': (RED, GREEN, BLUE, YELLOW), 'letters': 'AEFGHILP', 'bonusWord': 'APPLE'},
    'animals': {'colors': (RED, GREEN, BLUE, YELLOW), 'letters': 'CATTIGDOG', 'bonusWord': 'CAT'},
    'space': {'colors': (RED, GREEN, BLUE, YELLOW), 'letters': 'STARMOON', 'bonusWord': 'DOG'}
}

def selectTheme(theme):
    global ALLCOLORS, ALLLETTERS, bonusWord
    ALLCOLORS = themes[theme]['colors']
    ALLLETTERS = themes[theme]['letters']
    bonusWord = themes[theme]['bonusWord']

# Initialize the theme
currentTheme = 'default'
selectTheme(currentTheme)
assert len(ALLCOLORS) * len(ALLLETTERS) * 2 >= BOARDWIDTH * BOARDHEIGHT, "Board is too big for the number of shapes/colors defined."

# Time settings
gameTimeLimit = 180000  # 3 minutes in milliseconds
bonusTime = 40000  # 40 seconds bonus time

def drawBoard(board, revealed):
    for boxx in range(BOARDWIDTH):
        for boxy in range(BOARDHEIGHT):
            left, top = leftTopCoordsOfBox(boxx, boxy)
            if not revealed[boxx][boxy]:
                pygame.draw.rect(DISPLAYSURF, BOXCOLOR, (left, top, BOXSIZE, BOXSIZE))
            else:
                letter, color = getLetterAndColor(board, boxx, boxy)
                drawIcon(letter, color, boxx, boxy)

def getRandomizedBoard():
    icons = [(letter, color) for color in ALLCOLORS for letter in ALLLETTERS]
    random.shuffle(icons)
    numIconsUsed = int(BOARDWIDTH * BOARDHEIGHT / 2)
    icons = icons[:numIconsUsed] * 2
    random.shuffle(icons)

    board = []
    for x in range(BOARDWIDTH):
        column = []
        for y in range(BOARDHEIGHT):
            column.append(icons.pop(0))
        board.append(column)
    return board

def getLetterAndColor(board, boxx, boxy):
    return board[boxx][boxy]

def drawIcon(letter, color, boxx, boxy):
    half = BOXSIZE // 2
    left, top = leftTopCoordsOfBox(boxx, boxy)
    font = pygame.font.Font('times new roman', 20)
    text = font.render(letter, True, color, BGCOLOR)
    textRect = text.get_rect()
    textRect.center = (left + half, top + half)
    DISPLAYSURF.blit(text, textRect)

def checkWord(board, revealed, word):
    foundWord = ''.join(board[x][y][0] for x in range(BOARDWIDTH) for y in range(BOARDHEIGHT) if revealed[x][y])
    return word in foundWord

def drawTimer(timeRemaining):
    mins, secs = divmod(timeRemaining // 1000, 60)
    timeText = f'Time remaining: {mins:02}:{secs:02}'
    font = pygame.font.Font(None, 36)
    text = font.render(timeText, True, WHITE)
    textRect = text.get_rect()
    textRect.topleft = (10, 10)
    DISPLAYSURF.blit(text, textRect)

def gameOverAnimation():
    font = pygame.font.Font(None, 48)
    text = font.render("Time's up!", True, RED)
    textRect = text.get_rect()
    textRect.center = (WINDOWWIDTH // 2, WINDOWHEIGHT // 2)
    DISPLAYSURF.blit(text, textRect)
    pygame.DISPLAYSURF.update()
    DISPLAYSURF.fill(BGCOLOR)  # Clear the screen

def generateRevealedBoxesData(val):
    return [[val] * BOARDHEIGHT for _ in range(BOARDWIDTH)]

def startGameAnimation(board):
    coveredBoxes = generateRevealedBoxesData(False)
    boxes = [(x, y) for x in range(BOARDWIDTH) for y in range(BOARDHEIGHT)]
    random.shuffle(boxes)
    boxGroups = splitIntoGroupsOf(8, boxes)
    drawBoard(board, coveredBoxes)
    for boxGroup in boxGroups:
        revealBoxesAnimation(board, boxGroup)
        coverBoxesAnimation(board, boxGroup)

def gameWonAnimation(board):
    coveredBoxes = generateRevealedBoxesData(True)
    color1 = LIGHTBGCOLOR
    color2 = BGCOLOR
    for _ in range(13):
        color1, color2 = color2, color1
        DISPLAYSURF.fill(color1)
        drawBoard(board, coveredBoxes)
        pygame.display.update()
        pygame.time.wait(300)

def hasWon(revealedBoxes):
    return all(all(row) for row in revealedBoxes)

def celebrationAnimation():
    colors = [RED, GREEN, BLUE, YELLOW]
    for _ in range(60):
        DISPLAYSURF.fill(BGCOLOR)
        for _ in range(20):
            pygame.draw.circle(DISPLAYSURF, random.choice(colors), (random.randint(0, WINDOWWIDTH), random.randint(0, WINDOWHEIGHT)), random.randint(10, 40))
        pygame.display.update()
        pygame.time.wait(50)

def splitIntoGroupsOf(groupSize, theList):
    return [theList[i:i + groupSize] for i in range(0, len(theList), groupSize)]

def drawHighlightBox(boxx, boxy):
    left, top = leftTopCoordsOfBox(boxx, boxy)
    pygame.draw.rect(DISPLAYSURF, HIGHLIGHTCOLOR, (left - 5, top - 5, BOXSIZE + 10, BOXSIZE + 10), 4)

def leftTopCoordsOfBox(boxx, boxy):
    left = boxx * (BOXSIZE + GAPSIZE) + XMARGIN
    top = boxy * (BOXSIZE + GAPSIZE) + YMARGIN
    return (left, top)

def revealBoxesAnimation(board, boxesToReveal):
    for coverage in range(BOXSIZE, -REVEALSPEED - 1, -REVEALSPEED):
        drawBoxCovers(board, boxesToReveal, coverage)

def drawBoxCovers(board, boxes, coverage):
    for box in boxes:
        left, top = leftTopCoordsOfBox(box[0], box[1])
        pygame.draw.rect(DISPLAYSURF, BGCOLOR, (left, top, BOXSIZE, BOXSIZE))
        letter, color = getLetterAndColor(board, box[0], box[1])
        drawIcon(letter, color, box[0], box[1])
        if coverage > 0:
            pygame.draw.rect(DISPLAYSURF, BOXCOLOR, (left, top, coverage, BOXSIZE))
    pygame.display.update()
    FPSCLOCK.tick(FPS)

def coverBoxesAnimation(board, boxesToCover):
    for coverage in range(0, BOXSIZE + REVEALSPEED, REVEALSPEED):
        drawBoxCovers(board, boxesToCover, coverage)

def getBoxAtPixel(x, y):
    for boxx in range(BOARDWIDTH):
        for boxy in range(BOARDHEIGHT):
            left, top = leftTopCoordsOfBox(boxx, boxy)
            boxRect = pygame.Rect(left, top, BOXSIZE, BOXSIZE)
            if boxRect.collidepoint(x, y):
                return (boxx, boxy)
    return (None, None)

def increaseBoardSize():
    global BOARDWIDTH, BOARDHEIGHT, XMARGIN, YMARGIN, gameTimeLimit
    if BOARDWIDTH < 10 and BOARDHEIGHT < 10:  # Max size limit
        BOARDWIDTH += 1
        BOARDHEIGHT += 1
        XMARGIN = int((WINDOWWIDTH - (BOARDWIDTH * (BOXSIZE + GAPSIZE))) / 2)
        YMARGIN = int((WINDOWHEIGHT - (BOARDHEIGHT * (BOXSIZE + GAPSIZE))) / 2)
        gameTimeLimit += 60000  # Add 1 minute for each level

def main():
    global FPSCLOCK, DISPLAYSURF, startTime, timeRemaining
    pygame.init()
    FPSCLOCK = pygame.time.Clock()
    DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))

    mousex = 0
    mousey = 0
    pygame.display.set_caption('Memory Game')

    # Allow the player to select a theme at the beginning of the game
    selectThemeMenu()

    mainBoard = getRandomizedBoard()
    revealedBoxes = generateRevealedBoxesData(False)

    firstSelection = None
    DISPLAYSURF.fill(BGCOLOR)
    startGameAnimation(mainBoard)

    startTime = pygame.time.get_ticks()
    timeRemaining = gameTimeLimit

    while True:
        gameTimeElapsed = pygame.time.get_ticks() - startTime
        timeRemaining = gameTimeLimit - gameTimeElapsed if gameTimeElapsed < gameTimeLimit else 0

        if timeRemaining <= 0:
            gameOverAnimation()

        mouseClicked = False
        DISPLAYSURF.fill(BGCOLOR)
        drawBoard(mainBoard, revealedBoxes)
        drawTimer(timeRemaining)

        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYUP and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
            elif event.type == MOUSEMOTION:
                mousex, mousey = event.pos
            elif event.type == MOUSEBUTTONUP:
                mousex, mousey = event.pos
                mouseClicked = True

        boxx, boxy = getBoxAtPixel(mousex, mousey)
        if boxx is not None and boxy is not None:
            if not revealedBoxes[boxx][boxy]:
                drawHighlightBox(boxx, boxy)
            if not revealedBoxes[boxx][boxy] and mouseClicked:
                revealBoxesAnimation(mainBoard, [(boxx, boxy)])
                revealedBoxes[boxx][boxy] = True
                if firstSelection is None:
                    firstSelection = (boxx, boxy)
                else:
                    icon1letter, icon1color = getLetterAndColor(mainBoard, firstSelection[0], firstSelection[1])
                    icon2letter, icon2color = getLetterAndColor(mainBoard, boxx, boxy)

                    if icon1letter != icon2letter or icon1color != icon2color:
                        pygame.time.wait(1000)
                        coverBoxesAnimation(mainBoard, [(firstSelection[0], firstSelection[1]), (boxx, boxy)])
                        revealedBoxes[firstSelection[0]][firstSelection[1]] = False
                        revealedBoxes[boxx][boxy] = False
                    else:
                        if checkWord(mainBoard, revealedBoxes, bonusWord):
                            startTime += bonusTime

                        if hasWon(revealedBoxes):
                            celebrationAnimation()
                            pygame.time.wait(2000)
                            increaseBoardSize()
                            startTime = pygame.time.get_ticks()
                            mainBoard = getRandomizedBoard()
                            revealedBoxes = generateRevealedBoxesData(False)
                            startGameAnimation(mainBoard)

                    firstSelection = None

        pygame.display.update()
        FPSCLOCK.tick(FPS)

def selectThemeMenu():
    global currentTheme
    while True:
        DISPLAYSURF.fill(BGCOLOR)
        font = pygame.font.Font(None, 36)
        text = font.render('Select Theme:', True, WHITE)
        textRect = text.get_rect()
        textRect.center = (WINDOWWIDTH // 2, WINDOWHEIGHT // 4)
        DISPLAYSURF.blit(text, textRect)

        themeOptions = list(themes.keys())
        for i, theme in enumerate(themeOptions):
            themeText = font.render(theme.capitalize(), True, WHITE)
            themeRect = themeText.get_rect()
            themeRect.center = (WINDOWWIDTH // 2, WINDOWHEIGHT // 2 + i * 40)
            DISPLAYSURF.blit(themeText, themeRect)

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYUP and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
            elif event.type == MOUSEBUTTONUP:
                mousex, mousey = event.pos
                for i, theme in enumerate(themeOptions):
                    themeRect = pygame.Rect(WINDOWWIDTH // 2 - 50, WINDOWHEIGHT // 2 + i * 40 - 20, 100, 40)
                    if themeRect.collidepoint(mousex, mousey):
                        currentTheme = theme
                        selectTheme(theme)
                        return

# Define run_game_memory
def run_game_memory():
    print("Starting Memory Game...")
    main()  # Start the Game

if __name__ == '__main__':
    run_game_memory()
