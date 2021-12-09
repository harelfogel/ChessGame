import pygame as p
import ChessEngine

WIDTH = HEIGHT = 512
DIMENTION = 8 #chess board 8*8
SQ_SIZE = HEIGHT // DIMENTION
MAX_FPS = 15 #for animation later on
IMAGES = {}

'''
Initializr a global dictionary of images. This will be called excactly once in the main
'''
def loadImages():
    pieces = ['wp', 'wR', 'wN', 'wB', 'wK', 'wQ', 'bp', 'bR', 'bN', 'bB', 'bK', 'bQ']
    for piece in pieces:
        IMAGES[piece] = p.transform.scale(p.image.load("images/" + piece + ".png"), (SQ_SIZE,SQ_SIZE))
    #Now we can use IMAGES['wp']

def main():
    p.init()
    screen = p.display.set_mode((WIDTH,HEIGHT))
    clock = p.time.Clock
    screen.fill(p.Color("white"))
    gs = ChessEngine.GameState()
    validMoves = gs.getValidMoves()
    moveMade = False #flag variable for when a move is made
    loadImages()
    running = True
    sqSelected = () #no square selected, keep track of the last click of the user (tuple: (rew,col))
    playerClicks = [] #Keep track the player clicks (two tuples: [(6,4),(4,4)]
    while running:
        for e in p.event.get():
            if e.type == p.QUIT:
                running = False
            #mouse handler
            elif e.type == p.MOUSEBUTTONDOWN:
                location = p.mouse.get_pos() #(x,y) location of the mouse
                col = location[0]//SQ_SIZE
                row = location[1]//SQ_SIZE
                if sqSelected == (row,col): #the user clicked the same square
                    sqSelected = () #deselect
                    playerClicks = [] #clear player clicks
                else:
                    sqSelected = (row,col)
                    playerClicks.append(sqSelected) #append for both 1st and 2nd clicks
                if len(playerClicks) == 2: #after 2nd click
                    move = ChessEngine.Move(playerClicks[0], playerClicks[1], gs.board)
                    print(move.getChessNotation())
                    if move in validMoves:
                        gs.makeMove(move)
                        moveMade = True
                    sqSelected = () #reset user clicks
                    playerClicks = []

            #key handler
            elif e.type == p.KEYDOWN:
                if e.key == p.K_z: #undo when 'z' is pressed
                    print("undo")
                    gs.undoMove()
                    moveMade = True

        if moveMade:
            validMoves = gs.getValidMoves()
            moveMade = False

        # clock.tick(MAX_FPS)
        p.display.flip()
        drawGameState(screen, gs)

'''
#Responsible for all the graphics within a current game state
'''
def drawGameState(screen,gs):
    drawBoard(screen)
    drawPieces(screen,gs.board)

'''
Draws the squares on the board
'''
def drawBoard(screen):
    colors = [p.Color("white"),p.Color("gray")]
    for r in range(DIMENTION):
        for c in range(DIMENTION):
            color = colors[((r+c) % 2)]
            p.draw.rect(screen, color, p.Rect(c*SQ_SIZE, r*SQ_SIZE, SQ_SIZE, SQ_SIZE))

'''
Draw the pieces on the board using the current GameState.boars
'''
def drawPieces(screen,board):
    for r in range(DIMENTION):
        for c in range(DIMENTION):
            piece = board[r][c]
            if piece != "--":
                screen.blit(IMAGES[piece], p.Rect(c*SQ_SIZE, r*SQ_SIZE, SQ_SIZE, SQ_SIZE))




main()