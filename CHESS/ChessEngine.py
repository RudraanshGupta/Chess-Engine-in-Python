import copy

class Gamestate():
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
        self.whiteKingLocation= (7,4)
        self.blackKingLocation= (0,4)
        self.checkMate= False
        self.staleMate = False
        self.enpassantPossible =()
        self.enpassantPossibleLog = [self.enpassantPossible]
        self.currentCastelingrights = CastleRights(True, True, True,True)
        self.castleRightsLogs = [CastleRights(self.currentCastelingrights.wks, self.currentCastelingrights.bks,
                                              self.currentCastelingrights.wqs, self.currentCastelingrights.bqs)]
        
            
    def makeMoves(self, move):
            self.board[move.startRow][move.startCol] = "--"    
            self.board[move.endRow][move.endCol] = move.pieceMoved
            self.movelog.append(move) 
            self.whitetomove = not self.whitetomove  # Toggle turn
            if move.pieceMoved == 'wK':
                self.whiteKingLocation = (move.endRow, move.endCol)
            elif move.pieceMoved == 'bK':
                self.blackKingLocation = (move.endRow, move.endCol)
            if move.isPawnPromotion:
                 self.board[move.endRow][move.endCol] = move.pieceMoved[0] + 'Q' 
            if move.isEnpassantMove:
                self.board[move.startRow][move.endCol] = '--'
                
            if move.pieceMoved[1] == 'p' and abs(move.startRow - move.endRow) == 2:
                self.enpassantPossible =((move.startRow + move.endRow)//2, move.startCol)
            else:
                self.enpassantPossible =()
            
            if move.isCastleMove:
                if move.endCol - move.startCol ==2:
                    self.board[move.endRow][move.endCol-1] = self.board[move.endRow][move.endCol+1]
                    self.board[move.endRow][move.endCol+1] = '--'
                else:
                    self.board[move.endRow][move.endCol+1] = self.board[move.endRow][move.endCol+-2]
                    self.board[move.endRow][move.endCol-2] = '--'   
            self.enpassantPossibleLog.append(self.enpassantPossible)
            
            self.updateCastelRights(move)                                 
            self.castleRightsLogs.append(CastleRights(self.currentCastelingrights.wks, self.currentCastelingrights.bks,
                                                  self.currentCastelingrights.wqs, self.currentCastelingrights.bqs))
    
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
            self.enpassantPossibleLog.pop()
            self.enpassantPossible = self.enpassantPossibleLog[-1]
            self.castleRightsLogs.pop()
            newRights = self.castleRightsLogs[-1]
            self.currentCastelingrights = CastleRights(newRights.wks, newRights.bks, newRights.wqs, newRights.bqs)
            if move.isCastleMove:
                if move.endCol- move.startCol == 2:
                    self.board[move.endRow][move.endCol+1] = self.board[move.startRow][move.startCol-1]
                    self.board[move.endRow][move.endCol-1] = '--'
                else:
                    self.board[move.endRow][move.endCol-2] = self.board[move.startRow][move.startCol+1]
                    self.board[move.endRow][move.endCol+1] = '--'
            self.checkMate = False
            self.staleMate = False           
            
    def updateCastelRights(self, move):
        if move.pieceMoved == 'wK':
            self.currentCastelingrights.wks = False
            self.currentCastelingrights.wqs = False
        elif move.pieceMoved == 'bK':
            self.currentCastelingrights.bks = False
            self.currentCastelingrights.bqs = False
        elif move.pieceMoved == 'wR':
            if move.startRow == 7:
                if move.startCol == 0:
                    self.currentCastelingrights.wqs = False
                elif move.startCol == 7:
                    self.currentCastelingrights.wks = False
        elif move.pieceMoved == 'bR':
            if move.startRow == 0:
                if move.startCol == 0:
                    self.currentCastelingrights.bqs = False
                elif move.startCol == 7:
                    self.currentCastelingrights.bks = False  
        if move.pieceCaptured =='wR':
            if move.startRow == 7:
                if move.endCol == 0:
                    self.currentCastelingrights.wqs = False                          
                elif move.endCol ==7:
                    self.currentCastelingrights.wks = False
        elif move.pieceCaptured == 'bR':
            if move.endRow == 0:
                if move.endCol == 0:
                    self.currentCastelingrights.bqs = False                
                elif move.endCol ==7:
                    self.currentCastelingrights.bks = False     
                                   
            
    def getValidMoves(self):  
        tempEnpassantPossible = self.enpassantPossible
        tempCastleRights = CastleRights(self.currentCastelingrights.wks, self.currentCastelingrights.bks,
                                        self.currentCastelingrights.wqs, self.currentCastelingrights.bqs)
        moves=self.getAllPossibleMoves() 
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
        
        if self.whitetomove:
            self.getCastleMoves(self.whiteKingLocation[0],self.whiteKingLocation[1],moves)
        else:
            self.getCastleMoves(self.blackKingLocation[0],self.blackKingLocation[1],moves)                    
        self.enpassantPossible= tempEnpassantPossible
        self.currentCastelingrights = tempCastleRights
        return moves
    
    def inCheck(self):
        if self.whitetomove:
            return self.squareUnderAttack(self.whiteKingLocation[0],self.whiteKingLocation[1])
        else:
            return self.squareUnderAttack(self.blackKingLocation[0],self.blackKingLocation[1])
        
    def squareUnderAttack(self,r,c):
        self.whitetomove = not self.whitetomove    
        oppMoves=self.getAllPossibleMoves()
        self.whitetomove = not self.whitetomove
        for move in oppMoves:
            if move.endRow == r and move.endCol == c:
                return True
        return False                                                      
 
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
            kingRow, kingCol = self.whiteKingLocation
        else:
            kingRow, kingCol = self.blackKingLocation    
        if self.whitetomove:
            if self.board[r-1][c] == "--":
                moves.append(Move((r, c), (r-1, c), self.board))
                if r == 6 and self.board[r-2][c] == "--":
                    moves.append(Move((r, c), (r-2, c), self.board))
            if c-1 >= 0:
                if self.board[r-1][c-1][0] == 'b':
                    moves.append(Move((r, c), (r-1, c-1), self.board))
                #elif (r-1,c-1) == self.enpassantPossible:
                    attackingPiece = blockingPiece = False
                    if kingRow == r:
                        if kingCol < c:
                            insiderange = range(kingCol+1, c-1)
                            outsiderange = range(c+2, 8)
                        else:
                            insiderange = range(kingCol-1, c+1, -1)
                            outsiderange = range(c-1, -1,-1)  
                        for i in insiderange: 
                            if self.board[r][i] != "--":
                                blockingPiece = True
                        for i in outsiderange:
                            square = self.board[r][i]
                            if square[0] == (square[1] == "R" or square[1] == "Q"):
                                attackingPiece = True
                            elif square != '--':
                                blockingPiece = True         
                    #if not attackingPiece or blockingPiece:
                    #     moves.append(Move((r,c), (r-1, c-1), self.board, enpassantPossible= True))    
            if c+1 <= 7: 
                if self.board[r-1][c+1][0] == 'b':
                    moves.append(Move((r, c), (r-1, c+1), self.board))    
                # elif (r-1,c+1) == self.enpassantPossible:
                #     moves.append(Move((r,c), (r-1, c+1), self.board, enpassantPossible= True))
        else:
            if self.board[r+1][c] == "--":
                    moves.append(Move((r, c), (r+1, c), self.board))
                    if r == 1 and self.board[r+2][c] == "--":
                        moves.append(Move((r, c), (r+2, c), self.board))
            if c-1 >= 0:
                    if self.board[r+1][c-1][0] == 'w':
                        moves.append(Move((r, c), (r+1, c-1), self.board))
                    # elif (r+1,c-1) == self.enpassantPossible:
                    #     moves.append(Move((r,c), (r+1, c-1), self.board, enpassantPossible= True))              
            if c+1 <= 7:
                    if self.board[r+1][c+1][0] == 'w':
                        moves.append(Move((r, c), (r+1, c+1), self.board))           
                    # elif (r+1,c+1) == self.enpassantPossible:
                    #     moves.append(Move((r,c), (r+1, c+1), self.board, enpassantPossible= True))     
    
    
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
    
    def getQueenMoves(self, r, c, moves):
        self.getRookMoves(r, c, moves)
        self.getBishopMoves(r, c, moves)
    
    def getKingMoves(self, r, c, moves):
        kingMoves = ((-1,-1),(-1,0),(-1,1),(0,-1),(0,1),(1,-1),(1,0),(1,1))
        allyColor = "w" if self.whitetomove else "b"
        for i in range(8):
            endRow = r + kingMoves[i][0]
            endCol = c + kingMoves[i][1]
            if 0 <= endRow < 8 and 0 <= endCol < 8:
                endPiece = self.board[endRow][endCol]
                if endPiece[0] != allyColor:
                    moves.append(Move((r, c), (endRow, endCol), self.board))
        
    def getCastleMoves(self,r,c,moves):
        if self.squareUnderAttack(r,c):
            return  
        if (self.whitetomove and self.currentCastelingrights.wks) or (not self.whitetomove and self.currentCastelingrights.bks):
            self.getkingsideCastleMoves(r,c,moves)
        if (self.whitetomove and self.currentCastelingrights.wqs) or (not self.whitetomove and self.currentCastelingrights.bqs):
            self.getQueensideCastleMoves(r,c,moves)
    
    def getkingsideCastleMoves(self,r,c,moves):
        if self.board[r][c+1] == '--' and self.board[r][c+2] == '--':
            if not self.squareUnderAttack(r, c+1) and not self.squareUnderAttack(r,c+2):
                moves.append(Move((r,c),(r,c+2),self.board))#,isCastleMoves=True))  
    
    def getQueensideCastleMoves(self,r,c,moves):
        if self.board[r][c-1] == '--' and self.board[r][c-3] == '--' and self.board[r][c-3]=='--':
            if not self.squareUnderAttack(r, c-1) and not self.squareUnderAttack(r,c-2):
                moves.append(Move((r,c),(r,c-2),self.board))#isCastleMoves=True))
                                                        
class CastleRights():
    def __init__(self, wks, bks,wqs, bqs):
        self.wks = wks
        self.bks = bks
        self.wqs = wqs
        self.bqs = bqs

class Move():
    # maps keys to values
    # keys: value
    ranksToRows = {"1":7,"2":6,"3":5,"4":4,
                   "5":3,"6":2,"7":1,"8":0}
    rowsToRanks=  {v:k for k, v in ranksToRows.items()}
    filesToCols=  {"a":0,"b":1,"c":2,"d":3,
                   "e":4,"f":5,"g":6,"h":7}
    colstoFiles=  {v:k for k, v in filesToCols.items()}
