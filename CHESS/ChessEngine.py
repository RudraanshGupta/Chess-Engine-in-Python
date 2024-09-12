class gamestate():
    def __init__(self):
        self.board = [
            ["bR", "bN", "bB", "bQ", "bK", "bB", "bN", "bR"],
            ["bp", "bp", "bp", "bp", "bp", "bp", "bp", "bp"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["wp", "wp", "wp", "wp", "wp", "wp", "wp", "wp"],
            ["wR", "wN", "wB", "wQ", "wK", "wB", "wN", "wR"]
        ]
        
        self.moveFunctions = {'p': self.getPawnMoves, 'R': self.getRookMoves, 'N': self.getKnightMoves,
                              'B': self.getBishopMoves, 'Q': self.getQueenMoves, 'K': self.getKingMoves}
        self.whitetomove = True
        self.movelog = []

    def makeMoves(self, move):
        if len(self.movelog)!=0:    
            self.board[move.endRow][move.endCol] = move.pieceMoved
            self.board[move.startRow][move.startCol] = "--"
            self.movelog.append(move) 
            self.whitetomove = not self.whitetomove  # Toggle turn
            if move.pieceMoved == 'wK':
                self.whiteKingLocation = (move.endRow, move.endCol)
            elif move.pieceMoved == 'bK':
                self.blackKingLocation = (move.endRow, move.endCol)
                
            if move.isPawnPromotion:
                 self.board[move.endRow][move.endCol] = move.pieceMoved[0] + 'Q' 
            if move.isEnpassantMOve:
                self.board[move.startRow][move.endCol] = '--'
                
            if move.pieceMoved[1] == 'p' and abs(move.startRow - move.endRow) == 2:
                self.enpassantPossible =((move.startRow + move.endRow)//2, move.startCol)
            else:
                self.enpassantPossible =()    

    def undoMove(self):
        if len(self.movelog) != 0:
            move = self.movelog.pop()
            self.board[move.startRow][move.startCol] = move.pieceMoved
            self.board[move.endRow][move.endCol] = move.pieceCaptured
            self.whitetomove = not self.whitetomove  # Toggle turn back
            if move.pieceMoved == 'wK':
                self.whiteKingLocation = (move.startRow, move.startCol)
            elif move.pieceMoved == 'bK':
                self.blackKingLocation = (move.startRow, move.startCol)
            if move.isEnpassantMove:
                self.board[move.endRow][move.endCol] = '--'
                self.board[move.startRow][move.startCol] = move.pieceCaptured
                self.enpassantPossible = (move.endRow, move.endCol)
            if move.pieceMoved[1]== 'p' and abs(move.startRow- move.endRow) == 2:
                self.enpassantPossible =()  

    def getValidMoves(self):
        for log in self.castleRightsLogs:
            print(log.wks, log.wqs, log.bks, log.bqs, end =",")
        print()    
        tempEnpassantPossible = self.enpassantPossible
        tempCastleRights = CastleRights(self.currentCastelingrights.wks, self.currentCastelingrights.bks,
                                        self.currentCastelingrights.wqs, self.currentCastelingrights.bqs)
        moves=self.getAllPossibleMoves()
        if self.whitetomove:
            self.getCastleMoves(self.whiteKingLocation[0],self.whiteKingLocation[1],moves)
        else:
            self.getCastleMoves(self.blackKingLocation[0],self.blackKingLocation[1],moves)   
        for i in range(len(moves)-1,-1,-1):
            self.makeMoves(moves[i])
            self.whitetomove = not self.whitetomove
            if self.inCheck():
                moves.remove(moves[i])
            self.whitetomove = not self.whitetomove
            self.undoMove()
        if len(moves) == 0:
            if self.inCheck():
                self.checkMate = True
            else:
                self.staleMate = True
        else:
            self.checkMate = False
            self.staleMate = False                  
        self.enpassantPossible= tempEnpassantPossible
        self.currentCastelingrights = tempCastleRights
        return moves

    def getAllPossibleMoves(self):
        moves = []
        for r in range(len(self.board)):
            for c in range(len(self.board[r])):
                turn = self.board[r][c][0] 
                if (turn == 'w' and self.whitetomove) or (turn == 'b' and not self.whitetomove): 
                    piece = self.board[r][c][1]
                    self.moveFunctions[piece](r, c, moves)
        return moves  

    def getPawnMoves(self, r, c, moves):
        if self.whitetomove:
            if self.board[r-1][c] == "--":
                moves.append(Move((r, c), (r-1, c), self.board))
                if r == 6 and self.board[r-2][c] == "--":
                    moves.append(Move((r, c), (r-2, c), self.board))
            if c-1 >= 0:
                if self.board[r-1][c-1][0] == 'b':
                    moves.append(Move((r, c), (r-1, c-1), self.board))
                #elif (r-1,c-1) == self.enpassantPossible:
                    #moves.append(Move((r,c), (r-1, c-1), self.board, enpassantPossible= True))    
            if c+1 <= 7: 
                if self.board[r-1][c+1][0] == 'b':
                    moves.append(Move((r, c), (r-1, c+1), self.board))    
                #elif (r-1,c+1) == self.enpassantPossible:
                    #moves.append(Move((r,c), (r-1, c+1), self.board, enpassantPossible= True))
        else:
            if self.board[r+1][c] == "--":
                    moves.append(Move((r, c), (r+1, c), self.board))
                    if r == 1 and self.board[r+2][c] == "--":
                        moves.append(Move((r, c), (r+2, c), self.board))
            if c-1 >= 0:
                    if self.board[r+1][c-1][0] == 'w':
                        moves.append(Move((r, c), (r+1, c-1), self.board))
                    #elif (r+1,c-1) == self.enpassantPossible:
                        #moves.append(Move((r,c), (r+1, c-1), self.board, enpassantPossible= False))              
            if c+1 <= 7:
                    if self.board[r+1][c+1][0] == 'w':
                        moves.append(Move((r, c), (r+1, c+1), self.board))           
                    #elif (r+1,c+1) == self.enpassantPossible:
                        #moves.append(Move((r,c), (r+1, c+1), self.board, enpassantPossible= False))     
    
    
    def getRookMoves(self, r, c, moves): 
        directions = ((-1, 0), (0, -1), (1, 0), (0, 1))
        enemyColor = "b" if self.whitetomove else "w"   
        for d in directions:
            for i in range(1, 8):
                endRow = r + d[0] * i
                endCol = c + d[1] * i
                if 0 <= endRow < 8 and 0 <= endCol < 8:
                        endPiece = self.board[endRow][endCol]
                        if endPiece == "--":
                            moves.append(Move((r, c), (endRow, endCol), self.board))
                        elif endPiece[0] == enemyColor:
                            moves.append(Move((r, c), (endRow, endCol), self.board))
                            break
                        else:
                            break
                else:
                    break

    def getKnightMoves(self, r, c, moves):
        knightMoves = ((-2, -1), (-2, 1),(-1, -2), (-1, 2), (1,-2), (1, 2), (2,-1), (2, 1))
        allyColor = "w" if self.whitetomove else "b"
        for m in knightMoves:
            endRow = r + m[0]
            endCol = c + m[1]
            if 0 <= endRow < 8 and 0 <= endCol < 8:
                endPiece = self.board[endRow][endCol]
                if endPiece[0] != allyColor:
                    moves.append(Move((r, c), (endRow, endCol), self.board))

    def getBishopMoves(self, r, c, moves):
        directions = ((-1, -1), (-1, 1), (1, -1), (1, 1))
        enemyColor = "b" if self.whitetomove else "w"
        for d in directions:
            for i in range(1, 8):
                endRow = r + d[0] * i
                endCol = c + d[1] * i
                if 0 <= endRow < 8 and 0 <= endCol < 8:
                    endPiece = self.board[endRow][endCol]
                    if endPiece == "--":
                        moves.append(Move((r, c), (endRow, endCol), self.board))
                    elif endPiece[0] == enemyColor:
                        moves.append(Move((r, c), (endRow, endCol), self.board))
                        break
                    else:
                            break
                else:
                    break
