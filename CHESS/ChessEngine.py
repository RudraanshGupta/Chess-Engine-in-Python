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
