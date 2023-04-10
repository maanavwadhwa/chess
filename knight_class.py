from piece_class import Piece
from directions_helper_functions import isInbounds


class Knight(Piece):
    def __init__(self, rank, file, color): #rank --> row, file---> col
        super().__init__(rank,file,color)
        self.image = f'Images/knight_{self.color}.png'
        self.name = 'Knight'

  
    def legalMoves(self, currStateBoard):
        possibleMoves = []
        directions = [(2,1),(2,-1),(-2,1),(-2,-1),(1,2),(1,-2),(-1,2),(-1,-2)]
        for (drow,dcol) in directions:
            rows,cols = len(currStateBoard), len(currStateBoard[0])
            if isInbounds(self.rank+drow,self.file+dcol,rows,cols):
                x = currStateBoard[self.rank+drow][self.file+dcol]
                if (x==None) or (x!=None and x.color!=self.color):
                    possibleMoves.append((self.rank+drow,self.file+dcol))

        return possibleMoves