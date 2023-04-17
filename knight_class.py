from piece_class import Piece
from directions_helper_functions import isInbounds

class Knight(Piece):
    def __init__(self, rank, file, color): #rank --> row, file---> col
        super().__init__(rank,file,color)
        self.image = f'Images/knight_{self.color}.png'
        self.name = 'Knight'
        self.pointsWorth = 3

    def legalMoves(self, currStateBoard):
        possibleMoves = []
        directions = [(2,1),(2,-1),(-2,1),(-2,-1),(1,2),(1,-2),(-1,2),(-1,-2)]
        rows,cols = len(currStateBoard), len(currStateBoard[0])
        for (drow,dcol) in directions:
            if isInbounds(self.rank+drow,self.file+dcol,rows,cols):
                newMove = currStateBoard[self.rank+drow][self.file+dcol]
                if (newMove==None) or (newMove!=None and newMove.color!=self.color):
                    possibleMoves.append((self.rank+drow,self.file+dcol))
        return possibleMoves