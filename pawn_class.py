from piece_class import Piece


class Pawn(Piece):
    def __init__(self,rank, file, color): #rank --> row, file---> col
        super().__init__(rank,file,color)
        self.image = f'Images/pawn_{self.color}.png'
        self.name = 'Pawn'
        
    def legalMoves(self, currStateBoard):
        #returns all legal moves for the pawn
        possibleMoves = []
        #make sure can't capture pieces of own color
        # directions = [(1,0),(1,1),(1,-1),(-1,0),(-1,1),(-1,-1),(2,0),(-2,0)]
        # rows, cols = len(currStateBoard), len(currStateBoard[0])
        # for (drow, dcol) in directions:
        #     if isInbounds(self.rank+drow,self.file+dcol,rows,cols):
        #         x = currStateBoard[self.rank+drow][self.file+dcol]
        #         if self.movedFromInitialCell == False and (drow,dcol) in [(2,0),(-2,0)]:
        #             if x==None:
        #                 possibleMoves.append((self.rank+drow, self.file+dcol))
        #         if (x==None) and (drow,dcol) in [(1,0),(-1,0)]:
        #             possibleMoves.append((self.rank+drow,self.file+dcol))
        #         if (x!=None) and (x.color!=self.color) and ((drow,dcol) in [(1,1),(1,-1),(-1,1),(-1,-1)]):
        #             possibleMoves.append((self.rank+drow,self.file+dcol))

        #white pieces:
        if self.color == 'white':
            #check if it has moved from initial state
            if self.rank!=0:
                oneCellUp = currStateBoard[self.rank-1][self.file]
                if oneCellUp==None:
                    possibleMoves.append((self.rank-1,self.file))
            
            #check if it has moved from initial cell
            if self.movedFromInitialCell == False:
                twoCellsUp = currStateBoard[self.rank-2][self.file]
                if twoCellsUp==None and oneCellUp ==None:
                    possibleMoves.append((self.rank-2,self.file))

            #check upleft
            if self.file!=0 and self.rank != 0:
                upLeft = currStateBoard[self.rank-1][self.file-1]
                if upLeft!=None and upLeft.color != self.color:
                    possibleMoves.append((self.rank-1,self.file-1))

            #check upright
            if self.file != 7 and self.rank!=0:
                upRight = currStateBoard[self.rank-1][self.file+1]
                if upRight!=None and upRight.color != self.color:
                    possibleMoves.append((self.rank-1,self.file+1))

        elif self.color == 'black':
            #check if it has moved from initial state
            if self.rank!=7:
                oneCellUp = currStateBoard[self.rank+1][self.file]
                if oneCellUp==None:
                    possibleMoves.append((self.rank+1,self.file))

            #check if it has moved from initial cell
            if self.movedFromInitialCell == False:
                twoCellsUp = currStateBoard[self.rank+2][self.file]
                if twoCellsUp==None and oneCellUp ==None:
                    possibleMoves.append((self.rank+2,self.file))

            #check downleft
            if self.file!=0 and self.rank != 7:
                downLeft = currStateBoard[self.rank+1][self.file-1]
                if downLeft!=None and downLeft.color != self.color:
                    possibleMoves.append((self.rank+1,self.file-1))

            #check downright
            if self.file!=7 and self.rank != 7:
                downRight = currStateBoard[self.rank+1][self.file+1]
                if downRight!=None and downRight.color!=self.color:
                    possibleMoves.append((self.rank+1,self.file+1))
        
        return possibleMoves