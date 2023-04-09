from cmu_graphics import *
class Rook:
    def __init__(self, rank, file, color): #rank --> row, file---> col
        self.rank = rank
        self.file = file
        self.color = color
        self.image = f'Images/rook_{self.color}.png'
        self.name = 'Rook'

    def move(self, newRank, newFile):
        self.rank = newRank
        self.file = newFile 
  
    def legalMoves(self, currStateBoard):

        possibleMoves = (getRightMoves(self, currStateBoard)+
                         getUpwardMoves(self, currStateBoard)+
                         getDownwardMoves(self, currStateBoard)+
                         getLeftMoves(self, currStateBoard))
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

# def pieceInWay(app, board):
#     currPieceHighlighted = board[app.selectedCell[0]][app.selectedCell[1]]
#     movesAvailable = board[app.selectedCell[0]][app.selectedCell[1]].legalMoves(board)
#     for i in range(len(movesAvailable)):
#         #if there is a piece located in one of the possible moves 
#         if board[movesAvailable[i][0]][movesAvailable[i][1]]!=None:
#             if currPieceHighlighted.color == (board[movesAvailable[i][0]][movesAvailable[i][1]]).color:
#                 return True
#     return False

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

def onAppStart(app):
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
    return board 

def redrawAll(app):
    drawLabel('Chess', 200, 30, size=16)
    drawBoard(app)
    # drawBoardBorder(app)
    drawPieces(app)
    if app.showMoves == True:
        drawPossibleMoves(app)
    
def drawPossibleMoves(app):
    currPiece = app.board[app.selectedCell[0]][app.selectedCell[1]]
    rows, cols = len(app.board), len(app.board[0])
    possibleMoves = currPiece.legalMoves(app.board)
    for row in range(rows):
        for col in range(cols):
            if ((row,col) in possibleMoves and (row,col)!=(app.selectedCell[0], app.selectedCell[1])):
                    cellWidth, cellHeight = getCellSize(app)
                    xcoordinate = 38+col*cellWidth+cellWidth/2
                    ycoordinate = 50+row*cellHeight+cellHeight/2
                    drawCircle(xcoordinate,ycoordinate, 5, fill = 'midnightBlue')

def drawBoard(app):
    rows, cols = len(app.board), len(app.board[0])
    for row in range(rows):
        for col in range(cols):
            if row%2 ==0 and col%2 ==0:
                drawCell(app, row, col, 'saddleBrown')
            elif row%2 ==1 and col%2 ==1:
                drawCell(app,row,col,'saddleBrown')
            else:
                drawCell(app,row,col,'burlywood')

def drawPieces(app):
    rows, cols = len(app.board), len(app.board[0])
    for row in range(rows):
        for col in range(cols):
            piece = app.board[row][col]
            if piece != None:
                cellWidth, cellHeight = getCellSize(app)
                xcoordinate = 38+piece.file*cellWidth+cellWidth/2
                ycoordinate = 50+piece.rank*cellHeight+cellHeight/2
                drawImage(piece.image, xcoordinate, 
                       ycoordinate,align = 'center',
                        width=cellWidth-8, height=cellHeight-8)

# def drawBoardBorder(app):
#   # draw the board outline (with double-thickness):
#   drawRect(app.boardLeft, app.boardTop, app.boardWidth, app.boardHeight,
#            fill=None, border='black',
#            borderWidth=2*app.cellBorderWidth)

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
                # if row == 0 or row == 7 or col == 0 or col == 7:
                #     app.cellBorderWidth =
                return (row, col)
    return None

def onMousePress(app, mouseX, mouseY):
    cellLocation = getCellFromPoint(app, mouseX, mouseY)

    if cellLocation == None:
        app.selectedCell = None

    # if I am not highlighting a cell and i click on a piece
    elif app.selectedCell == None and app.board[cellLocation[0]][cellLocation[1]]!=None:
        currPiece = app.board[cellLocation[0]][cellLocation[1]]
        app.showMoves = True
        app.selectedCell = cellLocation

    #if I click on cell that is already selected/highlighted, I want to make it no longer selected
    elif cellLocation == app.selectedCell:
        app.selectedCell = None 
        app.showMoves = False

    #if my selectedCell is a piece and the location I click on is None, move the piece
    elif app.selectedCell!=None and app.board[cellLocation[0]][cellLocation[1]] == None:
        currPiece = app.board[app.selectedCell[0]][app.selectedCell[1]]
        if (cellLocation) in currPiece.legalMoves(app.board):
            currPiece.move(cellLocation[0], cellLocation[1])
            app.board[app.selectedCell[0]][app.selectedCell[1]] = None
            app.board[cellLocation[0]][cellLocation[1]] = currPiece
            app.selectedCell = None
            app.showMoves = False

    #if I click somewhere on the board and that space contains a piece
    elif cellLocation!=None and app.board[cellLocation[0]][cellLocation[1]]!=None:
        if app.selectedCell!=None:
            currPiece = app.board[app.selectedCell[0]][app.selectedCell[1]]
            if (cellLocation) in currPiece.legalMoves(app.board):
                currPiece.move(cellLocation[0], cellLocation[1])
                app.board[app.selectedCell[0]][app.selectedCell[1]] = None
                app.board[cellLocation[0]][cellLocation[1]] = currPiece
                app.selectedCell = None
        app.selectedCell = cellLocation 

def main():
    runApp()

main()