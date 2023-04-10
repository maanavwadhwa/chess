from piece_class import Piece
from directions_helper_functions import isInbounds
from rook_class import Rook


class King(Piece):
    def __init__(self,rank, file, color): #rank --> row, file---> col
        super().__init__(rank,file,color)
        self.image = f'Images/king_{self.color}.png'
        self.name = 'King'
        
    def legalMoves(self, currStateBoard):
        #returns all legal moves for the king
        possibleMoves = []

         #check all possible directions
        rows,cols = len(currStateBoard), len(currStateBoard[0])
        directions = [(1,0),(-1,0),(0,1),(0,-1),(1,1),(1,-1),(-1,1),(-1,-1)]
        for (drow,dcol) in directions:
            if isInbounds(self.rank+drow,self.file+dcol,rows,cols):
                x = currStateBoard[self.rank+drow][self.file+dcol]
                if (x==None) or (x!=None and x.color!=self.color):
                    possibleMoves.append((self.rank+drow,self.file+dcol))

        if self.movedFromInitialCell == False: #able to castle
            #check white king
            betweenRookAndKingLeftSide = (None, None, None)
            betweenRookAndKingRightSide = (None, None)
            if self.color == 'white':
                #check if rook has moved from initial cell
                #how do i do that? check if rook is at its normal position and see if it has moved

                #castling left side
                if (currStateBoard[7][1], currStateBoard[7][2], currStateBoard[7][3]) == betweenRookAndKingLeftSide:
                    if (isinstance(currStateBoard[7][0],Rook) and
                        currStateBoard[7][0].movedFromInitialCell ==False):
                        possibleMoves.append((self.rank,self.file-2))

                #castling right side
                if (currStateBoard[7][5], currStateBoard[7][6]) == betweenRookAndKingRightSide:
                    if (isinstance(currStateBoard[7][7],Rook) and
                        currStateBoard[7][7].movedFromInitialCell ==False):
                        possibleMoves.append((self.rank,self.file+2))

            elif self.color == 'black':

                #castling left side
                if (currStateBoard[0][1], currStateBoard[0][2], currStateBoard[0][3]) == betweenRookAndKingLeftSide:
                    if (isinstance(currStateBoard[0][0],Rook) and
                        currStateBoard[0][0].movedFromInitialCell ==False):
                        possibleMoves.append((self.rank,self.file-2))

                #castling right side
                if (currStateBoard[0][5], currStateBoard[0][6]) == betweenRookAndKingRightSide:
                    if (isinstance(currStateBoard[0][7],Rook) and
                        currStateBoard[0][7].movedFromInitialCell ==False):
                        possibleMoves.append((self.rank,self.file+2))       

        return possibleMoves