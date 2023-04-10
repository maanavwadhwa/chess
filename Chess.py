from cmu_graphics import *
class Rook:
    def __init__(self, rank, file, color): #rank --> row, file---> col
        self.rank = rank
        self.file = file
        self.color = color
        self.image = f'Images/rook_{self.color}.png'
        self.name = 'Rook'
        self.movedFromInitialCell = False

    def move(self, newRank, newFile):
        self.rank = newRank
        self.file = newFile 
        self.movedFromInitialCell = True
  
    def legalMoves(self, currStateBoard):

        possibleMoves = (getRightMoves(self, currStateBoard)+
                         getUpwardMoves(self, currStateBoard)+
                         getDownwardMoves(self, currStateBoard)+
                         getLeftMoves(self, currStateBoard))
        
        return possibleMoves

    def __repr__(self):
        return f'{self.name}: ({self.rank},{self.file}, {self.color})'

class Knight:
    def __init__(self, rank, file, color): #rank --> row, file---> col
        self.rank = rank
        self.file = file
        self.color = color
        self.image = f'Images/knight_{self.color}.png'
        self.name = 'Rook'
        self.movedFromInitialCell = False

    def move(self, newRank, newFile):
        self.rank = newRank
        self.file = newFile 
        self.movedFromInitialCell = True
  
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

    def __repr__(self):
        return f'{self.name}: ({self.rank},{self.file}, {self.color})'
    
class Bishop:
    def __init__(self, rank, file, color): #rank --> row, file---> col
        self.rank = rank
        self.file = file
        self.color = color 
        self.image = f'Images/bishop_{self.color}.png'
        self.name = 'Bishop'

    def move(self, newRank, newFile):
        self.rank = newRank
        self.file = newFile 
        
    def legalMoves(self, currStateBoard):
        #returns all legal moves for the bishop

        possibleMoves = (getUpwardRightMoves(self, currStateBoard)+
                         getUpwardLeftMoves(self, currStateBoard)+
                         getDownwardRightMoves(self, currStateBoard)+
                         getDownwardLeftMoves(self, currStateBoard))
        return possibleMoves

    def __repr__(self):
        return f'{self.name}: ({self.rank},{self.file}, {self.color})'

class Queen:
    def __init__(self,rank, file, color): #rank --> row, file---> col
        self.rank = rank
        self.file = file
        self.color = color
        self.image = f'Images/queen_{self.color}.png'
        self.name = 'Queen'

    def move(self, newRank, newFile):
        self.rank = newRank
        self.file = newFile 
        
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

    def __repr__(self):
        return f'{self.name}: ({self.rank},{self.file},{self.color})' 

class Pawn:
    def __init__(self,rank, file, color): #rank --> row, file---> col
        self.rank = rank
        self.file = file
        self.color = color
        self.image = f'Images/pawn_{self.color}.png'
        self.name = 'Pawn'
        self.movedFromInitialCell = False
        

    def move(self, newRank, newFile):
        self.rank = newRank
        self.file = newFile 
        self.movedFromInitialCell = True
        
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
                if upLeft!=None:
                    possibleMoves.append((self.rank-1,self.file-1))

            #check upright
            if self.file != 7 and self.rank!=0:
                upRight = currStateBoard[self.rank-1][self.file+1]
                if upRight!=None:
                    possibleMoves.append((self.rank-1,self.file+1))

        elif self.color == 'black':
            #check if it has moved from initial state
            oneCellUp = currStateBoard[self.rank+1][self.file]
            if oneCellUp==None:
                possibleMoves.append((self.rank+1,self.file))

            #check if it has moved from initial cell
            if self.movedFromInitialCell == False:
                twoCellsUp = currStateBoard[self.rank+2][self.file]
                if twoCellsUp==None and oneCellUp ==None:
                    possibleMoves.append((self.rank+2,self.file))

            #check downleft
            if self.file!=0 or self.rank != 7:
                upLeft = currStateBoard[self.rank+1][self.file-1]
                if upLeft!=None:
                    possibleMoves.append((self.rank+1,self.file-1))

            #check downright
            if self.file!=7 and self.rank != 7:
                upLeft = currStateBoard[self.rank+1][self.file+1]
                if upLeft!=None:
                    possibleMoves.append((self.rank+1,self.file+1))
        
        return possibleMoves

    def __repr__(self):
        return f'{self.name}: ({self.rank},{self.file}, {self.color})'
    
class King:
    def __init__(self,rank, file, color): #rank --> row, file---> col
        # super().__init__(rank,file,color)
        # self.image = 
        # self.name = 
        self.rank = rank
        self.file = file
        self.color = color
        self.image = f'Images/king_{self.color}.png'
        self.name = 'King'
        self.movedFromInitialCell = False

    def move(self, newRank, newFile):
        self.rank = newRank
        self.file = newFile 
        self.movedFromInitialCell = True
        
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

    def __repr__(self):
        return f'{self.name}: ({self.rank},{self.file}, {self.color})'

def getUpwardMoves(piece, currStateBoard):
    possibleMoves = []
    for i in range(piece.rank-1,-1,-1):
        if currStateBoard[i][piece.file]!=None:
            if currStateBoard[i][piece.file].color != piece.color:
                possibleMoves.append((i,piece.file))
            break
        else:
            possibleMoves.append((i,piece.file))
    return possibleMoves

def getDownwardMoves(piece, currStateBoard):
    possibleMoves = []
    rows = len(currStateBoard)
    for i in range(piece.rank+1,rows):
        if currStateBoard[i][piece.file]!=None:
            if currStateBoard[i][piece.file].color != piece.color:
                possibleMoves.append((i,piece.file))
            break
        else:
            possibleMoves.append((i,piece.file))
    return possibleMoves

def getLeftMoves(piece, currStateBoard):
    possibleMoves = []
    for i in range(piece.file-1, -1, -1):
        if currStateBoard[piece.rank][i]!=None:
            if currStateBoard[piece.rank][i].color != piece.color:
                possibleMoves.append((piece.rank, i))
            break
        else:
            possibleMoves.append((piece.rank, i))
    return possibleMoves

def getRightMoves(piece, currStateBoard):
    possibleMoves = []
    cols = len(currStateBoard[0])
    for i in range(piece.file+1,cols):
        if currStateBoard[piece.rank][i]!=None:
            if currStateBoard[piece.rank][i].color != piece.color:
                possibleMoves.append((piece.rank, i))
            break
        else:
            possibleMoves.append((piece.rank, i))
    return possibleMoves

def getUpwardRightMoves(piece, currStateBoard):
    possibleMoves = []
    cols = len(currStateBoard[0])
    j = 1 #represents a way to increment the row relative to its starting row
    for i in range(piece.file+1, cols):
        #prevents piece from being able to position itself to a row above the board 
        if piece.rank-j<0: 
            break
        elif currStateBoard[piece.rank-j][i]!=None:
            if currStateBoard[piece.rank-j][i].color != piece.color:
                possibleMoves.append((piece.rank-j, i))
            break
        else:
            possibleMoves.append((piece.rank-j, i))
        j+=1
    return possibleMoves

def getUpwardLeftMoves(piece, currStateBoard):
    possibleMoves = []
    j =1
    for i in range(piece.file-1, -1, -1):
        #prevents piece from being able to position itself to a row above the board 
        if piece.rank - j < 0: 
            break
        elif currStateBoard[piece.rank-j][i]!=None:
            if currStateBoard[piece.rank-j][i].color != piece.color:
                possibleMoves.append((piece.rank-j, i))
            break
        else:
            possibleMoves.append((piece.rank-j, i))
        j+=1
    return possibleMoves

def getDownwardRightMoves(piece, currStateBoard):
    possibleMoves = []
    rows, cols = len(currStateBoard), len(currStateBoard[0])
    j = 1
    for i in range(piece.file+1, cols): 
        #prevents piece from being able to position itself to a row below the board 
        if piece.rank+j>=rows: 
            break
        elif currStateBoard[piece.rank+j][i]!=None: #7,3
            if currStateBoard[piece.rank+j][i].color != piece.color:
                possibleMoves.append((piece.rank+j,i))
            break
        else:
            possibleMoves.append((piece.rank+j, i))
        j+=1
    return possibleMoves

def getDownwardLeftMoves(piece, currStateBoard):
    possibleMoves = []
    rows = len(currStateBoard)
    j = 1
    for i in range(piece.file-1, -1, -1):
        #prevents piece from being able to position itself to a row below the board 
        if piece.rank +j>=rows: 
            break
        elif currStateBoard[piece.rank+j][i]!=None:
            if currStateBoard[piece.rank+j][i].color != piece.color:
                possibleMoves.append((piece.rank+j,i))
            break
        else:
            possibleMoves.append((piece.rank+j, i))
        j+=1
    return possibleMoves

def initialBoard(rows, cols):
    board = [([None] * cols) for row in range(rows)]
    for row in range(rows):
        for col in range(cols):
            if (row,col) in [(0,0),(0,7)]:
                board[row][col] = Rook(row,col,'black')
            elif (row,col) in [(7,0),(7,7)]:
                board[row][col] = Rook(row,col,'white')
            elif (row, col) in [(0,2),(0,5)]:
                board[row][col] = Bishop(row,col,'black')
            elif (row,col) in [(7,2),(7,5)]:
                board[row][col] = Bishop(row,col,'white')
            elif (row,col) == (0,3):
                board[row][col] = Queen(row,col,'black')
            elif (row,col) == (7,3):
                board[row][col] = Queen(row,col,'white')
            elif row == 1:
                board[row][col] = Pawn(row,col, 'black')
            elif row == 6:
                board[row][col] = Pawn(row, col, 'white')
            elif (row,col) == (0,4):
                board[row][col] = King(row,col, 'black')
            elif (row,col) == (7,4):
                board[row][col] = King(row,col, 'white')
            elif (row,col) in [(0,1),(0,6)]:
                board[row][col] = Knight(row,col, 'black')
            elif (row,col) in [(7,1),(7,6)]:
                board[row][col] = Knight(row,col,'white')
    return board 


def isInbounds(rank, file, rows, cols):
    return 0<=rank<rows and 0<=file<cols


def onAppStart(app):
    resetBoard(app)

def resetBoard(app):
    app.rows = 8
    app.cols = 8
    app.boardLeft = 37.5
    app.boardTop = 50
    app.boardWidth = 325
    app.boardHeight = 325
    app.cellBorderWidth = 1
    app.board = initialBoard(app.rows, app.cols)
    app.selectedCell = None
    app.showMoves = False 


def redrawAll(app):
    drawLabel("Chess", 200, 30, size=16)#16
    drawBoard(app)
    drawPieces(app)
    if app.showMoves == True:
        drawPossibleMoves(app)
    
def drawPossibleMoves(app):
    currPiece = app.board[app.selectedCell[0]][app.selectedCell[1]]
    possibleMoves = currPiece.legalMoves(app.board)
    for row, col in possibleMoves:
        cellWidth, cellHeight = getCellSize(app)
        xcoordinate = app.boardLeft+col*cellWidth+cellWidth/2
        ycoordinate = app.boardTop+row*cellHeight+cellHeight/2
        drawCircle(xcoordinate,ycoordinate, 5, fill = 'yellow')

def drawBoard(app):
    rows, cols = len(app.board), len(app.board[0])
    for row in range(rows):
        for col in range(cols):
            if row%2 ==0 and col%2 ==0:
                drawCell(app, row, col, 'burlywood')
            elif row%2 ==1 and col%2 ==1:
                drawCell(app,row,col,'burlywood')
            else:
                drawCell(app,row,col,'saddleBrown')

def drawPieces(app):
    rows, cols = len(app.board), len(app.board[0])
    for row in range(rows):
        for col in range(cols):
            piece = app.board[row][col]
            if piece != None:
                cellWidth, cellHeight = getCellSize(app)
                xcoordinate = app.boardLeft+piece.file*cellWidth+cellWidth/2
                ycoordinate = app.boardTop+piece.rank*cellHeight+cellHeight/2
                drawImage(piece.image, xcoordinate, 
                       ycoordinate,align = 'center',
                        width=cellWidth-8, height=cellHeight-8)

def drawCell(app, row, col, color):
    cellLeft, cellTop = getCellLeftTop(app, row, col)
    cellWidth, cellHeight = getCellSize(app)
    if app.selectedCell==(row, col):
        drawRect(cellLeft, cellTop,
            cellWidth, cellHeight,
            fill=color, border='gold', borderWidth=3*app.cellBorderWidth)
    else:
        drawRect(cellLeft, cellTop, cellWidth, cellHeight,
             fill=color)

def getCellLeftTop(app, row, col):
    cellWidth, cellHeight = getCellSize(app)
    cellLeft = app.boardLeft + col * cellWidth
    cellTop = app.boardTop + row * cellHeight
    return (cellLeft, cellTop)

def getCellSize(app):
    cellWidth = app.boardWidth / app.cols
    cellHeight = app.boardHeight / app.rows
    return (cellWidth, cellHeight)

def getCellFromPoint(app, mouseX, mouseY):
    cellWidth, cellHeight = getCellSize(app)
    for row in range(len(app.board)):
        for col in range(len(app.board[0])):
            cellLeft, cellTop = getCellLeftTop(app, row, col)
            if ((cellLeft<=mouseX<=cellLeft+cellWidth) and 
            (cellTop<=mouseY<=cellTop+cellHeight)):
                return (row, col)
    return None

def onMousePress(app, mouseX, mouseY):
    cellLocation = getCellFromPoint(app, mouseX, mouseY)

    if cellLocation == None:
        app.selectedCell = None

    #if I click on cell that is already selected/highlighted, I want to make it no longer selected
    elif app.selectedCell==cellLocation:
        app.selectedCell = None 
        app.showMoves = False

    #if my selectedCell is a piece and the location I click on is None, move the piece
    elif app.selectedCell!=None:
        currPiece = app.board[app.selectedCell[0]][app.selectedCell[1]]
        if (cellLocation) in currPiece.legalMoves(app.board):
            currPiece.move(cellLocation[0], cellLocation[1])
            app.board[app.selectedCell[0]][app.selectedCell[1]] = None
            app.board[cellLocation[0]][cellLocation[1]] = currPiece
            app.selectedCell = None
            app.showMoves = False

    # if I am not highlighting a cell and i click on a piece highlight it
    if app.board[cellLocation[0]][cellLocation[1]]!=None:
        app.showMoves = True
        app.selectedCell = cellLocation
            

def onKeyPress(app, key):
    if key == 'r':
        resetBoard(app)

def main():
    runApp()

main()