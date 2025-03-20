import random

pieceScore = {"K": 0, "Q": 10, "R": 5, "B": 3, "N": 3, "P": 1, "k": 0, "q": 10, "r": 5, "b": 3, "n": 3, "p": 1}
knightsScore = [[1,1,1,1,1,1,1,1],
                [1,2,2,2,2,2,2,1],
                [1,2,3,3,3,3,2,1],
                [1,2,3,4,4,3,2,1],
                [1,2,3,4,4,3,2,1],
                [1,2,3,3,3,3,2,1],
                [1,2,2,2,2,2,2,1],
                [1,1,1,1,1,1,1,1]]

bishopScore =  [[4,3,2,1,1,2,3,4],
                [3,4,3,2,2,3,4,3],
                [2,3,4,3,3,4,3,2],
                [1,2,3,4,4,3,2,1],
                [1,2,3,4,4,3,2,1],
                [2,3,4,3,3,4,3,2],
                [3,4,3,2,2,3,4,3],
                [4,3,2,1,1,2,3,4]]

queenScore =   [[1,1,1,3,1,1,1,1],
                [1,2,3,3,3,1,1,1],
                [1,4,3,3,3,4,2,1],
                [1,2,3,3,3,2,2,1],
                [1,2,4,4,4,3,2,1],
                [1,4,3,3,3,4,2,1],
                [1,2,3,3,3,1,1,1],
                [1,1,1,3,1,1,1,1]]

rookScore =    [[4,3,4,4,4,4,3,4],
                [4,4,4,4,4,4,4,4],
                [1,4,3,3,3,4,2,1],
                [1,2,3,3,3,2,2,1],
                [1,2,3,4,4,3,2,1],
                [1,4,3,3,3,4,2,1],
                [4,4,4,4,4,4,4,4],
                [4,3,4,4,4,4,3,4]]

whitePawnsScore = [[8,8,8,8,8,8,8,8],
                   [8,8,8,8,8,8,8,8],
                   [5,6,6,7,7,6,6,5],
                   [2,3,3,5,5,3,3,2],
                   [2,3,3,5,5,3,3,2],
                   [1,1,2,3,3,2,1,1],
                   [1,1,1,0,0,1,1,1],
                   [0,0,0,0,0,0,0,0]]

blackPawnsScore = [[0,0,0,0,0,0,0,0],
                   [1,1,1,0,0,1,1,1],
                   [1,1,2,3,3,2,1,1],
                   [2,3,3,5,5,3,3,2],
                   [2,3,3,5,5,3,3,2],
                   [5,6,6,7,7,6,6,5],
                   [8,8,8,8,8,8,8,8],
                   [8,8,8,8,8,8,8,8]]

piecePositionScores = {"N": knightsScore, "B": bishopScore, "Q": queenScore, "R": rookScore, "bp":blackPawnsScore, "wp": whitePawnsScore}
CHECKMATE = 10000
STALEMATE = 0
DEPTH = 5

def findRandomMove(validmoves):
    return validmoves [random.randint(0, len(validmoves)-1)]
def findBestMoveMinMaxNoRecursion(gs, validmoves):
    """ Returns the best move by evaluating the material score for all valid moves """
    turnMultiplier = 1 if gs.whitetomove else -1
    opponentMinMaxScore = CHECKMATE  # Initially set to a very low value
    bestPlayerMove = None
    random.shuffle(validmoves)
    for playerMove in validmoves:
        gs.makeMoves(playerMove)
        opponentsMove = gs.getValidMoves()
        if gs.staleMate:
            opponentMaxScore = STALEMATE
        elif gs.checkMate:
            opponentMaxScore = -CHECKMATE
        else:
            opponentMaxScore = -CHECKMATE
            for opponentsMove in opponentsMove:
                gs.makeMove(opponentsMove)
                gs.getvalidMoves()
            # If we find a better move, update maxScore and bestMove
                if gs.checkMate:
                    score = CHECKMATE
                elif gs.staleMate:
                    score = STALEMATE
                else:
                    score = -turnMultiplier * scoreMaterial(gs.board) 
                if score> opponentMaxScore:
                    opponentMaxScore = score           
            gs.undoMove()
        if opponentMaxScore < opponentMinMaxScore:
            opponentMinMaxScore = opponentMaxScore 
            bestPlayerMove = playerMove
        gs.undoMove()  # Undo the move and evaluate the next one
    return bestPlayerMove

def findBestMove(gs, validMoves, returnQueue=None):
    global nextMove, counter
    nextMove = None
    counter = 0   # Reset counter
    findMoveNegaMaxAlphaBeta(gs, validMoves, DEPTH, -CHECKMATE, CHECKMATE, 1 if gs.whitetomove else -1)
    if returnQueue is not None:
        returnQueue.put(nextMove)
    return nextMove

def findMoveMinMax(gs, validMoves, depth, whitetomove):
    global nextMove
    if depth == 0:
        return scoreMaterial(gs.board)
    if whitetomove:
        maxScore = -CHECKMATE
        for move in validMoves:
            gs.makeMoves(move)
            nextMove = gs.getValidMoves()
            score = findMoveMinMax(gs, nextMove, depth-1, False) 
            if score > maxScore:
                maxScore = score
                if depth == DEPTH:
                    nextMove = move
            gs.undoMove()
        return maxScore            
                
    else:
        minScore = CHECKMATE 
        for move in validMoves:
            gs.makeMoves(move)
            nextMove = gs.getValidMoves()
            score = findMoveMinMax(gs, nextMove, depth-1, True) 
            if score < minScore:
                minScore = score
                if depth == DEPTH:
                    nextMove = move
            gs.undoMove()
        return minScore     
    
def findMoveNegaMax(gs, validMoves, depth, turnMultiplier): 
    global nextMove, counter
    counter += 1
    if depth == 0:
        return turnMultiplier * scoreBoard(gs)
    maxScore = -CHECKMATE 
    for move in validMoves:
        gs.makeMoves(move)
        nextMoves = gs.getValidMoves()
        score = -findMoveNegaMax(gs, nextMoves, depth-1, -turnMultiplier)
        if score > maxScore:
            maxScore = score
            if depth == DEPTH:
                nextMoves = move 
        gs.undoMove()
    return maxScore               

def findMoveNegaMaxAlphaBeta(gs, validMoves, depth, alpha, beta,turnMultiplier): 
    global nextMove, counter
    counter += 1
    if depth == 0:
        return turnMultiplier * scoreBoard(gs)
    
    maxScore = -CHECKMATE 
    for move in validMoves:
        gs.makeMoves(move)
        nextMoves = gs.getValidMoves()
        score = -findMoveNegaMaxAlphaBeta(gs, nextMoves, depth-1,-alpha, -beta, -turnMultiplier)
        if score > maxScore:
            maxScore = score
            if depth == DEPTH:
                nextMoves = move 
                print(move,score)
        gs.undoMove()
        if maxScore > alpha:
            alpha = maxScore
        if alpha >= beta:
            break   
    return maxScore            
                                               
def scoreBoard(gs):
    if gs.checkMate:
        if gs.whitetomove:
            return -CHECKMATE
        else:
            return CHECKMATE
    elif gs.staleMate:
        return STALEMATE    
    
    score = 0
    for row in range(len(gs.board)):
        for col in range (len(gs.board[row])):
            square = gs.board[row][col]
            if square != "--":  # Only evaluate non-empty squares
                piecePositionScore =0
                if square[1] != "K":
                    if square[1] == "p":
                        piecePositionScore = piecePositionScores[square][row][col]
                    else:
                        piecePositionScore = piecePositionScores[square[1]][row][col]
                if square[0] == 'w':
                    score += pieceScore[square[1].upper()] + piecePositionScore* .1 # Add white piece's value
                else:
                    score -= pieceScore[square[1].lower()] + piecePositionScore * .1 # Subtract black piece's value
    return score                         

def scoreMaterial(board):
    """ Evaluates the board based on material value """
    score = 0
    for row in board:
        for square in row:
            if square[0] == 'w':
                score += pieceScore.get(square[1], 0)  # Default to 0 if not found
            elif square[0] == 'b':
                score -= pieceScore.get(square[1], 0)  # Default to 0 if not found
    return score            
    

