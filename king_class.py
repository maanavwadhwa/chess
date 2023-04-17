from piece_class import Piece
from directions_helper_functions import isInbounds

class King(Piece):
    def __init__(self,rank, file, color): #rank --> row, file---> col
        super().__init__(rank,file,color)
        self.image = f'Images/king_{self.color}.png'
        self.name = 'King'
        self.pointsWorth = 0
        
    def legalMoves(self, currStateBoard):
        possibleMoves = []
        rows,cols = len(currStateBoard), len(currStateBoard[0])
        #check all possible directions
        directions = [(1,0),(-1,0),(0,1),(0,-1),(1,1),(1,-1),(-1,1),(-1,-1)]
        for (drow,dcol) in directions:
            if isInbounds(self.rank+drow,self.file+dcol,rows,cols):
                newMove = currStateBoard[self.rank+drow][self.file+dcol]
                if (newMove==None) or (newMove!=None and newMove.color!=self.color):
                    possibleMoves.append((self.rank+drow,self.file+dcol))
        return possibleMoves
    
