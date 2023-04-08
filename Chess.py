from cmu_graphics import *
class Rook:
    def __init__(self,rank, file, color): #rank --> row, file---> col
        self.rank = rank
        self.file = file
        self.color = color
        self.image = f'Images/rook_{self.color}.png'
        self.name = 'Rook'

    def move(self, newRank, newFile):
        self.rank = newRank
        self.file = newFile 
        
    def legalMoves(self, currStateBoard):
        #returns all legal moves for the rook
        return

    def __repr__(self):
        return f'{self.name}: ({self.rank},{self.file}, {self.color})'



def onAppStart(app):
    app.rows = 8
    app.cols = 8
    app.boardLeft = 37.5
    app.boardTop = 50
    app.boardWidth = 325
    app.boardHeight = 325
    app.cellBorderWidth = 1
    app.board = initialBoard(app.rows, app.cols)
    print(app.board)
    app.selectedCell = None

def initialBoard(rows, cols):
    board = [([None] * cols) for row in range(rows)]
    for row in range(rows):
        for col in range(cols):
            if (row,col) in [(0,0),(0,7)]:
                board[row][col] = Rook(row,col,'black')
            elif (row,col) in [(7,0),(7,7)]:
                board[row][col] = Rook(row,col,'white')
    return board 


    
def redrawAll(app):
    drawLabel('Chess', 200, 30, size=16)
    drawBoard(app)
    # drawBoardBorder(app)
    drawPieces(app)
    
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
            print(piece)
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
    for row in range(len(app.board)):
        for col in range(len(app.board[0])):
            cellLeft, cellTop = getCellLeftTop(app, row, col)
            if ((cellLeft<=mouseX<=cellLeft+getCellSize(app)[0]) and 
            (cellTop<=mouseY<=cellTop+getCellSize(app)[1])):
                # if row == 0 or row == 7 or col == 0 or col == 7:
                #     app.cellBorderWidth =
                return (row, col)
    return None

def onMousePress(app, mouseX, mouseY):
    cellLocation = getCellFromPoint(app, mouseX, mouseY)
    if (cellLocation == None) or (cellLocation == app.selectedCell):
        app.selectedCell = None
    else:
        app.selectedCell = cellLocation #gives me (row, col)

def main():
    runApp()

main()