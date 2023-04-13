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
        #clean up code for constructing initial board
        for row in range(self.rows):
            for col in range(self.cols):
                if (row,col) in [(0,0),(0,7)]:
                    board[row][col] = Rook(row,col,'black')
                elif (row,col) in [(7,0),(7,7)]:
                    board[row][col] = Rook(row,col,'white')
                elif (row, col) in [(0,2),(0,5)]:
                    board[row][col] = Bishop(row,col,'black')
                elif (row,col) in [(7,2),(7,5)]:
                    board[row][col] = Bishop(row,col,'white')
                elif (row,col) == (0,3):
                    board[row][col] = Queen(row,col,'black')
                elif (row,col) == (7,3):
                    board[row][col] = Queen(row,col,'white')
                elif row == 1:
                    board[row][col] = Pawn(row,col, 'black')
                elif row == 6:
                    board[row][col] = Pawn(row, col, 'white')
                elif (row,col) == (0,4):
                    board[row][col] = King(row,col, 'black')
                elif (row,col) == (7,4):
                    board[row][col] = King(row,col, 'white')
                elif (row,col) in [(0,1),(0,6)]:
                    board[row][col] = Knight(row,col, 'black')
                elif (row,col) in [(7,1),(7,6)]:
                    board[row][col] = Knight(row,col,'white')
        self.board = board
        self.playerTurn = 'white' #white starts off
        self.blackKing = board[0][4] #updates properties of object every time it moves
        self.whiteKing = board[7][4]
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
        
        self.kingInCheck = False
        self.promotablePiece = None
        self.message = 'Chess'

    def move(self, piece, desiredCellLocation):#takes piece and place I want it to move and updates board
        #if king is moving two spaces castle, otherwise perform move regularly
        row, col = desiredCellLocation
        if isinstance(piece,King) and abs(col-piece.file) == 2:
            self.castling((desiredCellLocation))
        else:
            self.board[piece.rank][piece.file] = None
            pieceAtDesiredCell = self.board[row][col]
            self.removeCapturedPiece(pieceAtDesiredCell)
            piece.move(row, col)
            self.board[row][col] = piece

        #promotion
        if isinstance(piece, Pawn) and (piece.rank == 7 or piece.rank == 0):
            self.promotablePiece = piece
            self.message = "Which piece would you like?"

        if self.playerTurn == 'white': #updating playerTurn before seeing if king in check
            self.playerTurn = 'black'
        else:
            self.playerTurn = 'white'

        self.seeIfKingInCheck() #whoevers current turn it is are they in check
        self.seeIfCheckmate()
        self.seeIfStalemate()
        
    def seeIfStalemate(self):
        if self.kingInCheck == False and self.noMovesToMake():
            self.message = 'Stalemate!'
        #     return True
        # return False
    
    def seeIfCheckmate(self):
        if self.kingInCheck == True and self.noMovesToMake():
            self.message = 'Checkmate!! Press r to play again'
        #     return True
        # return False
        
    def noMovesToMake(self): #have to take into account the check
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
        #original piece does not update for replicaBoard since replicaBoard is a deepcopy, must get replicaBoardPiece
        replicaBoardPiece = replicaBoard.board[piece.rank][piece.file]
        initialLegalMoves = replicaBoardPiece.legalMoves(replicaBoard.board)

        #if my piece is a King, its initial moves should include its set of standard one space moves along with castling moves
        if isinstance(replicaBoardPiece, King) and not replicaBoard.kingInCheck: 
            initialLegalMoves = initialLegalMoves + replicaBoard.getCastlingMoves(replicaBoardPiece) 

        #simulate each move and if it still leaves king in check exclude it from updated legal moves
        for (row,col) in initialLegalMoves:
            originalRank = replicaBoardPiece.rank
            originalFile = replicaBoardPiece.file
            pieceAtNewSquare = replicaBoard.board[row][col] 

            replicaBoardPiece.simulateMove(row,col)
            replicaBoard.board[originalRank][originalFile] = None
            #check if newSquare has another piece, if so remove that piece from its list of colored pieces
            replicaBoard.removeCapturedPiece(pieceAtNewSquare)
            replicaBoard.board[row][col] = replicaBoardPiece  
            replicaBoard.seeIfKingInCheck()
            if not replicaBoard.kingInCheck: 
                res.append((row,col))

            #undo move
            replicaBoardPiece.simulateMove(originalRank,originalFile)
            replicaBoard.board[originalRank][originalFile] = replicaBoardPiece
            replicaBoard.addPiece(pieceAtNewSquare)

        #if i can move king two cells over but in moving it one cell over it would be in check remove ability to move two cells over 
        if isinstance(piece, King):
            if (piece.rank,piece.file-2) in res and (piece.rank, piece.file -1) not in res:
                res.remove((piece.rank,piece.file-2))
            if (piece.rank, piece.file+2) in res and (piece.rank, piece.file+1) not in res:
                res.remove((piece.rank, piece.file+2))
        return res
    
    def seeIfKingInCheck(self): #is king in check after I simulate move and is king in check after every move in general
        self.kingInCheck = False #false until proven true
        self.message = 'Chess'
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

    def removeCapturedPiece(self, pieceCaptured): 
        if pieceCaptured!=None:
            if pieceCaptured.color == 'white':
                self.whitePieces.remove(pieceCaptured)
            else:
                self.blackPieces.remove(pieceCaptured)
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
        pieceClass = eval(pieceDesired)
        newPiece = pieceClass(self.promotablePiece.rank, self.promotablePiece.file, self.promotablePiece.color)
        self.addPiece(newPiece)
        self.seeIfKingInCheck()
        self.seeIfCheckmate()
        self.seeIfStalemate()
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
                #check if rook has moved from initial cell
                #how do i do that? check if rook is at its normal position and see if it has moved
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
     
    def __repr__(self):
        return f'{self.board}'


