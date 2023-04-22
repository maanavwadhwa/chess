from bishop_class import Bishop
from king_class import King
from knight_class import Knight
from pawn_class import Pawn
from queen_class import Queen
from rook_class import Rook
import copy

class Board:
    def __init__(self):
        self.rows = 8
        self.cols = 8
        board = [([None] * self.cols) for row in range(self.rows)]

        board[0][0] = Rook(0,0,'black')
        board[0][1] = Knight(0,1,'black')
        board[0][2] = Bishop(0,2,'black')
        board[0][3] = Queen(0,3,'black')
        board[0][4] = King(0,4,'black')
        board[0][5] = Bishop(0,5,'black')
        board[0][6] = Knight(0,6,'black')
        board[0][7] = Rook(0,7,'black')

        board[7][0] = Rook(7,0,'white')
        board[7][1] = Knight(7,1,'white')
        board[7][2] = Bishop(7,2,'white')
        board[7][3] = Queen(7,3,'white')
        board[7][4] = King(7,4,'white')
        board[7][5] = Bishop(7,5,'white')
        board[7][6] = Knight(7,6,'white')
        board[7][7] = Rook(7,7,'white')

        for i in range(self.cols):
            board[1][i] = Pawn(1,i,'black')
            board[6][i] = Pawn(6,i,'white')

        self.blackPieces = [(board[0][0]),(board[0][1]),(board[0][2]), 
                            (board[0][3]), (board[0][4]),(board[0][5]),(board[0][6]),
                            (board[0][7]), (board[1][0]),(board[1][1]),(board[1][2]), 
                            (board[1][3]), (board[1][4]),(board[1][5]),
                            (board[1][6]), (board[1][7])]
        
        self.whitePieces = [(board[7][0]),(board[7][1]),(board[7][2]), 
                            (board[7][3]), (board[7][4]), (board[7][5]),(board[7][6]),
                            (board[7][7]), (board[6][0]),(board[6][1]),(board[6][2]), 
                            (board[6][3]), (board[6][4]),(board[6][5]),
                            (board[6][6]), (board[6][7])]

        self.board = board
        self.playerTurn = 'white' #white starts off
        self.blackKing = board[0][4] #updates properties of object every time it moves
        self.whiteKing = board[7][4]
        self.kingInCheck = False
        self.promotablePiece = None
        self.message = 'Chess'
        self.gameOver = False
        self.fontSize = 35
        self.removedPiece = False
        self.gameLog = []

    def move(self, piece, desiredCellLocation):#takes piece and place I want it to move and updates board
        #if king is moving two spaces castle, otherwise perform move regularly
        self.message = 'Chess'
        self.fontSize = 35
        row, col = desiredCellLocation

        if isinstance(piece,King) and abs(col-piece.file) == 2:
            self.castling((desiredCellLocation))
        else:
            self.board[piece.rank][piece.file] = None
            pieceAtDesiredCell = self.board[row][col]
            self.removeCapturedPiece(pieceAtDesiredCell)
            piece.move(row, col) #updates pieces rank and file but doesn't update board until next line
            self.board[row][col] = piece #updates board

        self.gameLog.append((row,col))
        #promotion
        if isinstance(piece, Pawn) and (piece.rank == 7 or piece.rank == 0):
            self.promotablePiece = piece
            self.message = "Which piece would you like?"
            self.fontSize = 30

        else:
            #updating playerTurn before seeing if king in check
            self.playerTurn = 'black' if self.playerTurn == 'white' else 'white'

            self.seeIfKingInCheck() 
            
            if self.isCheckmate():
                self.gameOver = True
                self.message ='Checkmate!! Press r to play again'
                self.fontSize = 25
            elif self.isStalemate():
                self.gameOver = True
                self.message ='Stalemate!! Press r to play again'
                self.fontSize = 25

    def seeIfKingInCheck(self): 
        #is king in check after I simulate move and 
        #is king in check after every move in general
        self.kingInCheck = False #false until proven true
        if self.playerTurn == 'black':
            for cell in self.whitePieces:
                if (self.blackKing.rank, self.blackKing.file) in cell.legalMoves(self.board):
                    self.message = 'Check!'
                    self.kingInCheck = True  

        elif self.playerTurn == 'white':
            for cell in self.blackPieces:
                if (self.whiteKing.rank, self.whiteKing.file) in cell.legalMoves(self.board):
                    self.message = 'Check!'
                    self.kingInCheck = True
                    
    def isCheckmate(self):
        return self.kingInCheck and self.noMovesToMake()

    def isStalemate(self):
        return self.kingInCheck == False and self.noMovesToMake()
        
    def noMovesToMake(self):
        if self.playerTurn == 'white':
            pieces = self.whitePieces 
        else:
            pieces = self.blackPieces
        for piece in pieces:
            if self.updatedLegalMoves(piece) != []:
                return False
        return True
    
    def updatedLegalMoves(self, piece): #piece is the piece I am moving
        res = []
        #copy board so that I am not directly mutating the original board
        replicaBoard = copy.deepcopy(self) 
        #original piece does not update for replicaBoard since replicaBoard is a deepcopy, 
        #must get replicaBoardPiece
        replicaBoardPiece = replicaBoard.board[piece.rank][piece.file]
        initialLegalMoves = replicaBoardPiece.legalMoves(replicaBoard.board)

        #if my piece is a King, its initial moves should include its set of standard one space 
        #moves along with castling moves
        if isinstance(replicaBoardPiece, King) and not replicaBoard.kingInCheck: 
            initialLegalMoves = initialLegalMoves + replicaBoard.getCastlingMoves(replicaBoardPiece) 

        #simulate each move and if it still leaves king in check exclude it from 
        #updated legal moves
        for (row,col) in initialLegalMoves:
            originalRank = replicaBoardPiece.rank
            originalFile = replicaBoardPiece.file
            pieceAtNewSquare = replicaBoard.board[row][col] 

            #simulate move
            replicaBoardPiece.simulateMove(row,col)
            replicaBoard.board[originalRank][originalFile] = None
            #check if newSquare has another piece, if so remove that piece from its 
            #list of colored pieces
            replicaBoard.removeCapturedPiece(pieceAtNewSquare)
            replicaBoard.board[row][col] = replicaBoardPiece  

            replicaBoard.seeIfKingInCheck()
            if not replicaBoard.kingInCheck: 
                res.append((row,col))

            #undo simulated move
            replicaBoardPiece.simulateMove(originalRank, originalFile)
            replicaBoard.board[originalRank][originalFile] = replicaBoardPiece
            replicaBoard.board[row][col] = None 
            replicaBoard.addPiece(pieceAtNewSquare)

        #if i can move king two cells over but in moving it one cell over it would 
        #be in check remove ability to move two cells over 
        if isinstance(piece, King):
            if (piece.rank,piece.file-2) in res and (piece.rank, piece.file -1) not in res:
                res.remove((piece.rank,piece.file-2))
            if (piece.rank, piece.file+2) in res and (piece.rank, piece.file+1) not in res:
                res.remove((piece.rank, piece.file+2))
        return res

    def removeCapturedPiece(self, pieceCaptured): 
        self.removedPiece = False
        if pieceCaptured!=None:
            if pieceCaptured.color == 'white':
                self.whitePieces.remove(pieceCaptured)
                self.removedPiece = True
            else:
                self.blackPieces.remove(pieceCaptured)
                self.removedPiece= True
            self.board[pieceCaptured.rank][pieceCaptured.file] = None

    def addPiece(self, piece):#for promotion and updating replicaBoard
        if piece!=None:
            if piece.color == 'white':
                self.whitePieces.append(piece)
            else:
                self.blackPieces.append(piece)
            self.board[piece.rank][piece.file] = piece

    def promotion(self, pieceDesired):
        self.message = 'Chess'
        #CITATION: used 'eval' for next line: https://stackoverflow.com/questions/1176136/convert-string-to-python-class-object
        pieceClass = eval(pieceDesired)
        newPiece = pieceClass(self.promotablePiece.rank, self.promotablePiece.file, self.promotablePiece.color)
        self.removeCapturedPiece(self.promotablePiece)
        self.addPiece(newPiece)
        self.playerTurn = 'black' if self.playerTurn == 'white' else 'white'
        self.seeIfKingInCheck()
        if self.isCheckmate():
            self.message = 'Checkmate!! Press r to play again'
        elif self.isStalemate():
            self.message = 'Stalemate!! Press r to play again'
        self.promotablePiece = None

    def castling(self, desiredCell):
        #castles for white in queen direction
        if desiredCell == (7,2):
            rook = self.board[7][0]
            king = self.board[7][4]
            rook.move(7,3)
            king.move(7,2)
            self.board[7][3] = rook
            self.board[7][0] = None
            self.board[7][2] = king
            self.board[7][4] = None

        #castles for white in king direction
        elif desiredCell == (7,6):
            rook = self.board[7][7]
            king = self.board[7][4]
            rook.move(7,5)
            king.move(7,6)
            self.board[7][5] = rook
            self.board[7][7] = None
            self.board[7][6] = king
            self.board[7][4] = None

        #castles for black in queen direction
        elif desiredCell == (0,2):
            rook = self.board[0][0]
            king = self.board[0][4]
            rook.move(0,3)
            king.move(0,2)
            self.board[0][0] = None
            self.board[0][3] = rook
            self.board[0][2] = king
            self.board[0][4] = None

        #castles for black in king direction
        elif desiredCell == (0,6):
            rook = self.board[0][7]
            king = self.board[0][4]
            rook.move(0,5)
            king.move(0,6)
            self.board[0][7] = None
            self.board[0][5] = rook
            self.board[0][6] = king
            self.board[0][4] = None

    def getCastlingMoves(self, kingPiece):
        castlingRes = []
        if kingPiece.movedFromInitialCell == False: #able to castle
            #check white king
            betweenRookAndKingLeftSide = (None, None, None)
            betweenRookAndKingRightSide = (None, None)
            if kingPiece.color == 'white':
                #check if rook is at its normal position and see if it has moved
                #castling left side
                if (self.board[7][1], self.board[7][2], self.board[7][3]) == betweenRookAndKingLeftSide:
                    if (isinstance(self.board[7][0],Rook) and
                        self.board[7][0].movedFromInitialCell ==False):
                        castlingRes.append((kingPiece.rank,kingPiece.file-2))
                #castling right side
                if (self.board[7][5], self.board[7][6]) == betweenRookAndKingRightSide:
                    if (isinstance(self.board[7][7],Rook) and
                        self.board[7][7].movedFromInitialCell ==False):
                        castlingRes.append((kingPiece.rank,kingPiece.file+2))

            elif kingPiece.color == 'black':
                #castling left side
                if (self.board[0][1], self.board[0][2], self.board[0][3]) == betweenRookAndKingLeftSide:
                    if (isinstance(self.board[0][0],Rook) and
                        self.board[0][0].movedFromInitialCell ==False):
                        castlingRes.append((kingPiece.rank,kingPiece.file-2))
                #castling right side
                if (self.board[0][5], self.board[0][6]) == betweenRookAndKingRightSide:
                    if (isinstance(self.board[0][7],Rook) and
                        self.board[0][7].movedFromInitialCell ==False):
                        castlingRes.append((kingPiece.rank,kingPiece.file+2)) 
        return castlingRes 
    
    def allMovesAvailableBlack(self):
        resultBlack = dict()
        for piece in self.blackPieces:
            resultBlack[piece] = self.updatedLegalMoves(piece)
        return resultBlack
    
    def allMovesAvailableWhite(self):
        resultWhite = dict()
        for piece in self.whitePieces:
            resultWhite[piece] = self.updatedLegalMoves(piece)
        return resultWhite
    
    def __repr__(self):
        return f'{self.board}'
    
#CITATION: I referred to the minimax pseudocode in the TP Guide on Game AI pdf provided
#https://www.cs.cmu.edu/~112/notes/student-tp-guides/GameAI.pdf
def miniMaxAlgo(boardInstance, depth, maximizing):
    if depth == 0 or boardInstance.gameOver:
        return (value(boardInstance), )
    duplicateBoard = copy.deepcopy(boardInstance)
    if maximizing:
        bestScore = -10000000
        bestMove = None
        blackPieceMoves = duplicateBoard.allMovesAvailableBlack()
        moves = blackPieceMoves
        promotionPawnRank = 7
    else:
        bestScore = 10000000
        bestMove = None
        whitePieceMoves = duplicateBoard.allMovesAvailableWhite()
        moves = whitePieceMoves
        promotionPawnRank = 0

    for piece in moves:
        originalRank = piece.rank
        originalFile = piece.file
        for row,col in moves[piece]:
            pieceAtNewSquare = duplicateBoard.board[row][col] 
            piece.simulateMove(row, col)
            duplicateBoard.board[originalRank][originalFile] = None
            duplicateBoard.removeCapturedPiece(pieceAtNewSquare)
            if type(piece) == Pawn and piece.rank == promotionPawnRank:
                duplicateBoard.removeCapturedPiece(piece)
                duplicateBoard.addPiece(Queen(piece.rank, piece.file, piece.color))
            else:    
                #check if newSquare has another piece, if so remove that piece 
                #from its list of colored pieces
                duplicateBoard.board[row][col] = piece 
            duplicateBoard.playerTurn = 'white' if duplicateBoard.playerTurn == 'black' else 'black'
            #use updated board as boardstate and obtain score from boardstate
            score = miniMaxAlgo(duplicateBoard, depth-1, False)
            x = score[0]>bestScore if maximizing else score[0]<bestScore
            if x:
                bestScore = score[0]
                bestMove = (piece, (row,col))
            #undo move
            if type(piece) == Pawn and piece.rank == promotionPawnRank:
                duplicateBoard.removeCapturedPiece(duplicateBoard.board[piece.rank][piece.file])
                duplicateBoard.addPiece(piece)
            piece.simulateMove(originalRank,originalFile)
            duplicateBoard.board[originalRank][originalFile] = piece
            duplicateBoard.board[row][col] = None 
            duplicateBoard.addPiece(pieceAtNewSquare)
            duplicateBoard.playerTurn = 'black' if duplicateBoard.playerTurn == 'white' else 'white'
    return (bestScore, bestMove)

#valueHelper function and value function below for minimax algo
def valueHelper(boardObject, piece):
    score = 0
    if piece.rank in (3,4) and piece.file in (3,4) and len(boardObject.blackPieces)>=13:
        score+=1
    if ((type(piece)!= King or type(piece)!=Pawn or type(piece) != Rook) and 
        len(boardObject.gameLog)<12 and piece.movedFromInitialCell):
        score += 2
    if type(piece) == Knight and len(piece.legalMoves(boardObject.board))>=4:
        score+=1
    elif ((type(piece) == Bishop or type(piece) == Rook) and 
            len(piece.legalMoves(boardObject.board))>=5 and len(boardObject.gameLog)<=8):
        score+=1
    elif type(piece) == Queen and len(piece.legalMoves(boardObject.board))>15:
        score+=1
    return score

def value(boardObject):
    score = 0
    #totalpointsWorth when starting game = 9+5(2)+3(4)+8(1)=39
    sumBlack = 0
    sumWhite = 0
    for piece in boardObject.blackPieces:
        sumBlack+=piece.pointsWorth
        score += valueHelper(boardObject, piece)
    for piece in boardObject.whitePieces:
        sumWhite+=piece.pointsWorth
        score -= valueHelper(boardObject, piece)

    if boardObject.playerTurn == 'black':
        sign = -1
        kingRank = 0
    else:
        sign = 1
        kingRank = 7
        
    if boardObject.kingInCheck:
        score += (sign*6)
    if boardObject.isCheckmate():
        score += (sign*400)
    if type(boardObject.board[kingRank][4])!=King:
        score += (sign*6)
    score+=(sumBlack-sumWhite)
    return score

