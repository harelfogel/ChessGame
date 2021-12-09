"""
This is the main driver file. It will be responsible for handling user input and displaying the current gameState
"""


class GameState():
    def __init__(self):
        self.board = [
            ["bR", "bN", "bB", "bQ", "bK", "bB", "bN", "bR"],
            ["bp", "bp", "bp", "bp", "bp", "bp", "bp", "bp"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["wp", "wp", "wp", "wp", "wp", "wp", "wp", "wp"],
            ["wR", "wN", "wB", "wQ", "wK", "wB", "wN", "wR"]]
        self.moveFunctions = {'p': self.getPawnMoves, 'R': self.getRookMoves, 'N': self.getKnightMoves,
                              'B': self.getBishopMoves, 'Q': self.getQueenMoves, 'K': self.getKingMoves}

        self.whiteToMove = True
        self.moveLog = []
        self.whiteKingLocation=(7,4)
        self.blackKingLocation = (0,4)
        # self.inCheck=False
        # self.pins=[]
        # self.pins=[]
        # self.checks=[]
        self.checkMate=False
        self.staleMate=False
        self.lolo= False




    def makeMove(self, move):
        self.board[move.startRow][move.startCol] = "--"
        self.board[move.endRow][move.endCol] = move.pieceMoved
        self.moveLog.append(move)
        self.whiteToMove = not self.whiteToMove  # swap players (switch turns)
        #update king location
        if move.pieceMoved=='wK':
            self.whiteKingLocation=(move.endRow,move.endCol)
            if move.pieceMoved == 'bK':
                self.blackKingLocation = (move.endRow, move.endCol)

    '''
    Undo the last move
    '''

    def undoMove(self):
        if len(self.moveLog) != 0:
            move = self.moveLog.pop()
            self.board[move.startRow][move.startCol] = move.pieceMoved
            self.board[move.endRow][move.endCol] = move.pieceCaptures
            self.whiteToMove = not self.whiteToMove  # swap players (switch turns)
            #update king position:
            if move.pieceMoved == 'wK':
                self.whiteKingLocation = (move.startRow, move.startCol)
                if move.pieceMoved == 'bK':
                    self.blackKingLocation = (move.startRow, move.startCol)


    '''
    All moves considering checks
    '''

    def getValidMoves(self):
        #1. generate all possible moves
        moves= self.getAllPosibleMoves()
        #2. make the move for each move make it
        for i in range(len(moves)-1,-1,-1):  #when removing from a list go backwards through that list
            self.makeMove(moves[i])
            #3 generate all oppents moves
            #4. for each of your oppents moves see if they attack the king
            self.whiteToMove=not self.whiteToMove
            if self.inCheck():
                moves.remove(moves[i])  #5 . if they a do attack thr king , not a valid move
            self.whiteToMove = not self.whiteToMove
            self.undoMove()
        if len(moves)==0:  #either checkmate or stalemate
            if self.inCheck():
                self.checkMate=True
            else:
                self.staleMate=True
        else:
            self.checkMate=False
            self.staleMate=False

        return moves  # for now we will not worry about checks.

    """
    Determine if the current player is under attack
    """

    def inCheck(self):
        if self.whiteToMove:
            return self.squareUnderAttack(self.whiteKingLocation[0],self.whiteKingLocation[1])
        else:
            return self.squareUnderAttack(self.blackKingLocation[0],self.blackKingLocation[1])


    """
        Determine if enemy can attack the squares r,c
    """

    def squareUnderAttack(self,r,c):
        self.whiteToMove=not self.whiteToMove  #switch to oppenents turn
        oppMoves=self.getAllPosibleMoves()
        self.whiteToMove=not self.whiteToMove #switch the turn back
        for move in oppMoves:
            if move.endRow==r and move.endCol==c:  #square under attack
                return True
        return False






    '''
    All moves without considering checks
    '''

    def getAllPosibleMoves(self):
        moves = []
        for r in range(len(self.board)):  # number of rows
            for c in range(len(self.board[r])):  # number of col in given row
                turn = self.board[r][c][0]  # return the color of a piece at a specific square
                if (turn == 'w' and self.whiteToMove) or (turn == 'b' and not self.whiteToMove):
                    piece = self.board[r][c][1]  # return the type of the piece
                    print("turn:", turn, "piece:", piece)
                    self.moveFunctions[piece](r, c, moves)  # calls the apporopriate move function based on piece type
        return moves

    '''
    Get all the pawn moves for the pawn located at row, col and add these moves to the list
    '''

    def getPawnMoves(self, r, c, moves):
        if self.whiteToMove:  # white pawn moves
            if self.board[r - 1][c] == "--":  # 1 square pawn advance
                moves.append(Move((r, c), (r - 1, c), self.board))
                if r == 6 and self.board[r - 2][c] == "--":  # 2 square pawn advance
                    currMove = Move((r, c), (r - 2, c),self.board)
                    currMove.__str__()
                    moves.append(Move((r, c), (r - 2, c), self.board))
            if c - 1 >= 0:  # captures to the left
                if self.board[r - 1][c - 1][0] == 'b':  # enemy piece to capture
                    moves.append(Move((r, c), (r - 1, c - 1), self.board))
            if c + 1 <= 7:  # able to cpature to the right until last column
                if self.board[r - 1][c + 1][0] == 'b':  # enemy piece to capture
                    moves.append(Move((r, c), (r - 1, c + 1), self.board))

        else:  # black pawn moves:
            if self.board[r + 1][c] == "--":  # 1 square pawn advance
                moves.append(Move((r, c), (r + 1, c), self.board))
                if r == 1 and self.board[r + 2][c] == "--":  # 2 square pawn advance
                    moves.append(Move((r, c), (r + 2, c), self.board))
            if c - 1 >= 0:  # captures to the right
                if self.board[r + 1][c - 1][0] == 'w':  # enemy piece to capture
                    moves.append(Move((r, c), (r + 1, c - 1), self.board))
            if c + 1 <= 7:  # able to cpature to the left until last column
                if self.board[r + 1][c + 1][0] == 'w':  # enemy piece to capture
                    moves.append(Move((r, c), (r + 1, c + 1), self.board))

    '''
    Get all the  knight for the pawn located at row, col and add these moves to the list
    '''

    def getKnightMoves(self, r, c, moves):
        knightMoves = ((-2, -1), (-2, 1), (-1, -2), (-1, 2), (1, -2), (1, 2), (2, -1), (2, 1))
        allyColor = 'w' if self.whiteToMove else 'b'
        for m in knightMoves:
            endRow = r + m[0]
            endCol = c + m[1]
            if 0 <= endRow < 8 and 0 <= endCol < 8:
                endPiece = self.board[endRow][endCol]
                if endPiece[0] != allyColor:  # not an ally piece ( empty or enemy piece)
                    moves.append(Move((r, c), (endRow, endCol), self.board))

        # print("Knight moves:", moves)

    '''
    Get all the rook  for the pawn located at row, col and add these moves to the list
    '''

    def getRookMoves(self, r, c, moves):
        directions = ((-1, 0), (0, -1), (1, 0), (0, 1))  # up, left, down, right
        enemyColor = "b" if self.whiteToMove else "w"
        for d in directions:
            for i in range(1, 8):
                endRow = r + d[0] * i
                endCol = c + d[1] * i

                if 0 <= endRow < 8 and 0 <= endCol < 8:

                    endPiece = self.board[endRow][endCol]
                    print(i, d, endCol, endRow, endPiece)
                    if endPiece == "--":  # empty space valid
                        currMove = Move((r, c), (endRow, endCol), self.board)
                        currMove.__str__()
                        moves.append(Move((r, c), (endRow, endCol), self.board))
                    elif endPiece[0] == enemyColor:  # enemy piece valid
                        moves.append(Move((r, c), (endRow, endCol), self.board))
                        break
                    else:  # friendly piece invalid
                        break
                else:  # off board
                    break

        # print("Rook moves:" , moves)

    '''
       Get all the bishop moves for the pawn located at row, col and add these moves to the list
    '''

    def getBishopMoves(self, r, c, moves):
        directions = ((-1, -1), (-1, 1), (1, -1), (1, 1))
        enemyColor = "b" if self.whiteToMove else "w"
        for d in directions:
            for i in range(1, 8):
                endRow = r + d[0] * i
                endCol = c + d[1] * i
                #   print(enemyColor, ",", endRow, ",", endCol)
                if 0 <= endRow < 8 and 0 <= endCol < 8:
                    endPiece = self.board[endRow][endCol]
                    if endPiece == "--":  # empty space valid
                        moves.append(Move((r, c), (endRow, endCol), self.board))
                    elif endPiece[0] == enemyColor:  # enemy piece valid
                        moves.append(Move((r, c), (endRow, endCol), self.board))
                        break
                    else:  # friendly piece invalid
                        break
                else:  # off board
                    break

    '''
           Get all the queen moves for the pawn located at row, col and add these moves to the list
    '''

    def getQueenMoves(self, r, c, moves):
        self.getBishopMoves( r, c, moves)
        self.getRookMoves( r, c, moves)

    '''
               Get all the king moves for the pawn located at row, col and add these moves to the list
    '''

    def getKingMoves(self, r, c, moves):
        kingMoves = ((-1,-1),(-1,0),(-1,1),(0,-1),(0,1),(1,-1),(1,0),(1,1))
        allyColor = "w" if self.whiteToMove else "b"
        for i in range(8):
            endRow = r + kingMoves[i][0]
            endCol = c + kingMoves[i][1]
            if 0 <= endRow < 8 and 0 <= endCol < 8:
                endPiece = self.board[endRow][endCol]
                if endPiece[0] != allyColor: # not an ally piece, empty or enemy piece
                    moves.append(Move((r,c),(endRow,endCol),self.board))


class Move():
    ranksToRows = {"1": 7, "2": 6, "3": 5, "4": 4,
                   "5": 3, "6": 2, "7": 1, "8": 0}
    RowsToRanks = {v: k for k, v in ranksToRows.items()}
    filesToCols = {"a": 0, "b": 1, "c": 2, "d": 3,
                   "e": 4, "f": 5, "g": 6, "h": 7}
    colsToFiles = {v: k for k, v in filesToCols.items()}

    def __init__(self, startSq, endSq, board):
        self.startRow = startSq[0]
        self.startCol = startSq[1]
        self.endRow = endSq[0]
        self.endCol = endSq[1]
        self.pieceMoved = board[self.startRow][self.startCol]
        self.pieceCaptures = board[self.endRow][self.endCol]
        self.moveID = self.startRow * 1000 + self.startCol * 100 + self.endRow * 10 + self.endCol

    #  print(self.moveID)

    '''
    Overriding the equals method
    '''

    def __eq__(self, other):
        if isinstance(other, Move):
            return self.moveID == other.moveID
        return False

    def __str__(self):
        print(self.endRow, self.endCol)

    def getChessNotation(self):
        return self.getRankFile(self.startRow, self.startCol) + self.getRankFile(self.endRow, self.endCol)

    def getRankFile(self, r, c):
        return self.colsToFiles[c] + self.RowsToRanks[r]