from directions_helper_functions import isInbounds
from piece_class import Piece

class Pawn(Piece):
    def __init__(self,rank, file, color): #rank --> row, file---> col
        super().__init__(rank,file,color)
        self.image = f'Images/pawn_{self.color}.png'
        self.name = 'Pawn'
        self.pointsWorth = 1
        
    def legalMoves(self, currStateBoard):
        possibleMoves = []
        rows, cols = len(currStateBoard), len(currStateBoard[0])
        if self.color == 'white':
            directions = [(-2,0),(-1,0),(-1,1),(-1,-1)]
            sign = -1
        else:
            directions = [(2,0),(1,0),(1,1),(1,-1)]
            sign = 1

        for (drow, dcol) in directions:
            if isInbounds(self.rank+drow,self.file+dcol,rows,cols):
                newMove = currStateBoard[self.rank+drow][self.file+dcol]
                if self.movedFromInitialCell == False and (abs(drow),dcol) == (2,0): #check for 2 spaces up
                    if newMove == None and currStateBoard[self.rank+(sign*1)][self.file] == None: #only valid if one square up is none and two squares up is none
                        possibleMoves.append((self.rank+drow, self.file+dcol))
                elif newMove == None and (abs(drow),dcol) == (1,0): #if one square up is none 
                    possibleMoves.append((self.rank+drow,self.file+dcol))
                elif newMove!=None and newMove.color != self.color and ((drow,dcol)) in [(sign*1,1),(sign*1,-1)]: #check upright, upleft
                    possibleMoves.append((self.rank+drow, self.file+dcol))

        return possibleMoves