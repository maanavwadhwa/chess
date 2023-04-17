from piece_class import Piece
from directions_helper_functions import getDownwardMoves, getLeftMoves, getRightMoves, getUpwardMoves

class Rook(Piece):
    def __init__(self, rank, file, color): #rank --> row, file---> col
        super().__init__(rank,file,color)
        self.image = f'Images/rook_{self.color}.png'
        self.name = 'Rook'
        self.pointsWorth = 5

    def legalMoves(self, currStateBoard):
        possibleMoves = (getRightMoves(self, currStateBoard)+
                         getUpwardMoves(self, currStateBoard)+
                         getDownwardMoves(self, currStateBoard)+
                         getLeftMoves(self, currStateBoard))
        return possibleMoves