import pygame as p
import ChessEngine, chessAI

BOARD_WIDTH = BOARD_HEIGHT = 512
MOVE_LOG_PANEL_WIDTH = 250
MOVE_LOG_PANEL_HEIGHT = BOARD_HEIGHT
DIMENTIONS = 8  # 8x8 board
SQ_SIZE = BOARD_HEIGHT // DIMENTIONS
MAX_FPS = 15
IMAGES = {}

def loadImages():
    """
    Initializes a dictionary of images for each piece and scales them to fit the board squares.
    """
    pieces = ['bB', 'bK', 'bN', 'bp', 'bQ', 'bR', 'wB', 'wK', 'wN', 'wp', 'wQ', 'wR']
    for piece in pieces:
        IMAGES[piece] = p.transform.scale(p.image.load(f"my_chess/images/{piece}.png"), (SQ_SIZE, SQ_SIZE))

def main():
    """
    Main driver for the chess game. Handles user input and game state updates.
    """
    p.init()
    screen = p.display.set_mode((BOARD_WIDTH + MOVE_LOG_PANEL_WIDTH , BOARD_HEIGHT))
    clock = p.time.Clock()
    screen.fill(p.Color("white"))
    moveLogFont = p.font.SysFont("Arial",14,False,False)
    gs = ChessEngine.Gamestate()  # Updated to match ChessEngine naming convention
    validMoves = gs.getValidMoves()
    moveMade = False  # Flag for when a move is made
    animate = False
    loadImages()  # Load images once at the beginning
    running = True
    sqSelected = ()  # No square selected initially
    playerClicks = []  # Keep track of player clicks (two tuples for two clicks)
    gameOver = False
    playerOne = True
    playerTwo = False
    AIThinking= False
    moveFinderProcess =None
    moveUndone = False
    
    while running:
        humanTurn = (gs.whitetomove and playerOne) or (not gs.whitetomove and playerTwo)
        for e in p.event.get():
            if e.type == p.QUIT:
                running = False

            # Mouse handling
            elif e.type == p.MOUSEBUTTONDOWN:
                if not gameOver:
                    location = p.mouse.get_pos()  # Get mouse click location
                    col = location[0] // SQ_SIZE
                    row = location[1] // SQ_SIZE

                    if sqSelected == (row, col) or col >= 8:  # Deselect if clicked same square
                        sqSelected = ()
                        playerClicks = []
                    else:
                        sqSelected = (row, col)
                        playerClicks.append(sqSelected)  # Add the square to the clicks list

                    if len(playerClicks) == 2 and humanTurn:  # After two clicks
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
                    sqSelected = ()
                    playerClicks = []
                    moveMade = True
                    animate = False
                    gameOver = False
                    if AIThinking:
                        moveFinderProcess.terminate()
                        AIThinking = False
                    moveUndone = True   
                if e.key == p.K_r: # Undo board on 'r' key press
                    gs  = ChessEngine.Gamestate()
                    validMoves = gs.validMoves()
                    sqSelected = ()
                    playerClicks = []
                    moveMade = False
                    animate = False
                    gameOver = False  
                    if AIThinking:
                        moveFinderProcess.terminate()
                        AIThinking = False   
                    moveUndone = True   

        if not gameOver and not humanTurn and not moveUndone:
            if not AIThinking:
                AIThinking= True
                print("thinking....")
                returnQueue = Queue()
                moveFinderProcess = Process(target = chessAI.findBestMove, args= (gs, validMoves, returnQueue))
                moveFinderProcess.start()
            
            if not moveFinderProcess.is_alive():
                print("Done thinking") 
                AIMove = returnQueue.get()   
                AIMove = chessAI.findBestMove(gs, validMoves,returnQueue)
                if AIMove is None:
                    AIMove = chessAI.findRandomMove(validMoves)
                gs.makeMoves(AIMove)
                moveMade = True
                animate = True
                AIThinking = False
            
        # After a move is made
        if moveMade:
            if animate:
                animateMove(gs.movelog[-1], screen,gs.board, clock)
            validMoves = gs.getValidMoves()  # Recalculate valid moves
            moveMade = False
            animate = False
            moveUndone = False


        drawGameState(screen, gs,validMoves,sqSelected,moveLogFont)  # Redraw the game state on the screen
        if gs.checkMate or gs.staleMate:
            gameOver = True
            drawEndGameText(screen,'Stalemate' if gs.staleMate else 'Black wins by Checkmate' if gs.whitetomove else 'Black wins by Checkmate')
                     
        clock.tick(MAX_FPS)
        p.display.flip()
        
def drawGameState(screen, gs,validMoves,sqSelected,moveLogFont):
    """
    Responsible for all the graphics within the current game state.
    """
    drawBoard(screen)  # Draw the squares on the board
    highlightSquares(screen, gs,validMoves,sqSelected )
    drawPieces(screen, gs.board)  # Draw the pieces on top of the squares
    drawMoveLog(screen, gs, moveLogFont)

def drawBoard(screen):
    """
    Draws the board with alternating colors (white and gray).
    """
    global colors
    colors = [p.Color("white"), p.Color("gray")]
    for r in range(DIMENTIONS):
        for c in range(DIMENTIONS):
            color = colors[((r + c) % 2)]  # Alternate colors
            p.draw.rect(screen, color, p.Rect(c * SQ_SIZE, r * SQ_SIZE, SQ_SIZE, SQ_SIZE))

def highlightSquares(screen,gs,validMoves,sqSelecred):
      if sqSelecred !=():
        r,c = sqSelecred
        if gs.board[r][c][0] == ('w' if gs.whitetomove else 'b'):
            s= p.Surface((SQ_SIZE,SQ_SIZE))
            s.set_alpha(100)
            s.fill(p.Color('blue'))
            screen.blit(s,(c*SQ_SIZE, r*SQ_SIZE))
            s.fill(p.Color('yellow'))
            for move in validMoves:
                if move.startRow == r and move.startCol == c:
                    screen.blit(s,(move.endCol*SQ_SIZE, move.endRow*SQ_SIZE))  

def drawPieces(screen, board):
    """
    Draws the pieces on the board using the current game state's board array.
    """
    for r in range(DIMENTIONS):
        for c in range(DIMENTIONS):
            piece = board[r][c]
            if piece != "--":  # If not an empty square
                screen.blit(IMAGES[piece], p.Rect(c * SQ_SIZE, r * SQ_SIZE, SQ_SIZE, SQ_SIZE))

def drawMoveLog(screen, gs,font):
    moveLogRect = p.Rect(BOARD_WIDTH,0 , MOVE_LOG_PANEL_WIDTH, MOVE_LOG_PANEL_HEIGHT)
    p.draw.rect(screen, p.Color("black"), moveLogRect)
    moveLog = gs.movelog
    moveTexts = []
    for i in range(0, len(moveLog),2):
        moveString = str(i//2 + 1) + ". " + str(moveLog[i])+ " "
        if i+1 < len(moveLog):
            moveString += str(moveLog[i+1]) + " "
        moveTexts.append(moveString)  
    movesPerRow = 3      
    padding  = 5
    lineSpacing = 2
    textY = padding
    for i in range(0,len(moveTexts), movesPerRow):
        text = ""
        for j in range(movesPerRow):
            if i+j < len(moveTexts):
                text += moveTexts[i+j]
        textObject = font.render(text,True,p.Color('white')) 
        textLocation = moveLogRect.move(padding,textY)
        screen.blit(textObject,textLocation)   
        textY += textObject.get_height() + lineSpacing

    
def animateMove(move,screen,board,clock):
    global colors
    dR = move.endRow - move.startRow
    dC = move.endCol - move.startCol
    framesPerSquare = 10
    frameCount = (abs(dR) + abs(dC)) * framesPerSquare
    for frame in range(frameCount + 1):
        r = move.startRow + dR * frame / frameCount
        c = move.startCol + dC * frame / frameCount
        drawBoard(screen)
        drawPieces(screen, board)

        color = colors[(move.endRow + move.endCol) % 2]
        endSquare = p.Rect(move.endCol * SQ_SIZE, move.endRow * SQ_SIZE, SQ_SIZE, SQ_SIZE)
        p.draw.rect(screen, color, endSquare)

        # Only try to draw the captured piece if it's not '--'
        if move.pieceCaptured != '--':
            screen.blit(IMAGES[move.pieceCaptured], endSquare)
            
        
        screen.blit(IMAGES[move.pieceMoved], p.Rect(c * SQ_SIZE, r * SQ_SIZE, SQ_SIZE, SQ_SIZE))
        p.display.flip()
        clock.tick(60)
        
def drawEndGameText(screen, text):
    font = p.font.SysFont("Helvetica",32,True,False)
    textObject = font.render(text,0,p.Color('Gray')) 
    textLocation = p.Rect(0,0,  BOARD_WIDTH, BOARD_HEIGHT).move(BOARD_WIDTH/2 - textObject.get_width()/2, BOARD_HEIGHT/2 - textObject.get_height()/2)   
    screen.blit(textObject,textLocation)   
    textObject = font.render(text,0,p.Color("Black"))
    screen.blit(textObject, textLocation.move(2,2))    

if __name__ == "__main__":
    main()
