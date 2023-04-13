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
        return possibleMoves
    
