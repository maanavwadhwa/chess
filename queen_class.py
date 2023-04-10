from piece_class import Piece
from directions_helper_functions import getDownwardLeftMoves, getDownwardMoves, getDownwardRightMoves, getLeftMoves, getRightMoves, getUpwardLeftMoves, getUpwardMoves, getUpwardRightMoves


class Queen(Piece):
    def __init__(self,rank, file, color): #rank --> row, file---> col
        super().__init__(rank,file,color)
        self.image = f'Images/queen_{self.color}.png'
        self.name = 'Queen'
        
    def legalMoves(self, currStateBoard):
        #returns all legal moves for the rook
        possibleMoves = (getRightMoves(self, currStateBoard)+
                         getUpwardMoves(self, currStateBoard)+
                         getDownwardMoves(self, currStateBoard)+
                         getLeftMoves(self, currStateBoard)+
                         getUpwardRightMoves(self, currStateBoard)+
                         getUpwardLeftMoves(self, currStateBoard)+
                         getDownwardRightMoves(self, currStateBoard)+
                         getDownwardLeftMoves(self, currStateBoard))
        return possibleMoves   