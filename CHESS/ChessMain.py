import pygame as p
import ChessEngine

WIDTH = HEIGHT = 512
DIMENTIONS = 8
SQ_SIZE = HEIGHT // DIMENTIONS
MAX_FPS = 15
IMAGES = {}

def loadimages():
    pieces = ['bB', 'bK', 'bN', 'bp', 'bQ', 'bR', 'wB', 'wK', 'wN', 'wp', 'wQ', 'wR']
    for piece in pieces:
        IMAGES[piece] = p.image.load("my_chess/images/" + piece + ".png")

def main():
    """
    Main driver for the chess game. Handles user input and game state updates.
    """
    p.init()
    screen = p.display.set_mode((WIDTH, HEIGHT))
    clock = p.time.Clock()
    screen.fill(p.Color("white"))
    gs = ChessEngine.gamestate()  # Updated to match ChessEngine naming convention
    validMoves = gs.getValidMoves()
    moveMade = False  # Flag for when a move is made
    loadImages()  # Load images once at the beginning
    running = True
    sqSelected = ()  # No square selected initially
    playerClicks = []  # Keep track of player clicks (two tuples for two clicks)

    while running:
        for e in p.event.get():
            if e.type == p.QUIT:
                running = False

            # Mouse handling
            elif e.type == p.MOUSEBUTTONDOWN:
                location = p.mouse.get_pos()  # Get mouse click location
                col = location[0] // SQ_SIZE
                row = location[1] // SQ_SIZE

                if sqSelected == (row, col):  # Deselect if clicked same square
                    sqSelected = ()
                    playerClicks = []
                else:
                    sqSelected = (row, col)
                    playerClicks.append(sqSelected)  # Add the square to the clicks list
                if len(playerClicks) == 2:  # After two clicks
                        move = ChessEngine.Move(playerClicks[0], playerClicks[1], gs.board)
                        print(f"Attempting move: {move.getChessnotation()}")
                        for i in range(len(validMoves)):
                            if move == validMoves[i]:
                                gs.makeMoves(validMoves[i])
                                moveMade = True
                                animate = True
                                sqSelected = ()  # Reset user clicks
                                playerClicks = []
                            if not moveMade:
                                playerClicks = [sqSelected]  # Re-select if invalid move
            # Key handling
            elif e.type == p.KEYDOWN:
                if e.key == p.K_z:  # Undo move on 'z' key press
                    gs.undoMove()
                    moveMade = True
                    animate = False
                if e.key == p.K_r: # Undo board on 'r' key press
                    gs  = ChessEngine.Gamestate()
                    validMoves = gs.validMoves()
                    sqSelected = ()
                    playerClicks = []
                    moveMade = False
                    animate = False     
     
        
        
