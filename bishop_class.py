from piece_class import Piece
from directions_helper_functions import getDownwardLeftMoves, getDownwardRightMoves, getUpwardLeftMoves, getUpwardRightMoves


class Bishop(Piece):
    def __init__(self, rank, file, color): #rank --> row, file---> col
        super().__init__(rank,file,color)
        self.image = f'Images/bishop_{self.color}.png'
        self.name = 'Bishop'
        
    def legalMoves(self, currStateBoard):
        #returns all legal moves for the bishop

        possibleMoves = (getUpwardRightMoves(self, currStateBoard)+
                         getUpwardLeftMoves(self, currStateBoard)+
                         getDownwardRightMoves(self, currStateBoard)+
                         getDownwardLeftMoves(self, currStateBoard))
        return possibleMoves