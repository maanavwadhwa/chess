from cmu_graphics import *
from bishop_class import Bishop
from king_class import King
from knight_class import Knight
from pawn_class import Pawn
from queen_class import Queen
from rook_class import Rook

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
    app.kingInCheck = False 
    app.label = 'Chess'
    app.colorTurn = 'white' #starts off game
    app.whiteTurn = True 

def isKingInCheck(app, currPiece):
    rows, cols = len(app.board),len(app.board[0])
    # initialLegalMoves = copy.copy(currPiece.legalMoves(app.board))
    for row in range(rows):
        for col in range(cols):
            cell = app.board[row][col]
            if isinstance(cell, King) and cell.color != currPiece.color:
                if (row,col) in currPiece.legalMoves(app.board):
                    # app.kingInCheck = True
                    # app.label = 'Check'
                    return True
    return False

def redrawAll(app):
    drawLabel(app.label, 200, 30, size=16)#16
    drawBoard(app)
    drawPieces(app)
    if app.showMoves == True:
        drawPossibleMoves(app)
    # if app.kingInCheck == True:
    #     drawLabel(app.label, 200, 30, size = 16)
    
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

def getCellFromClick(app, mouseX, mouseY):
    cellWidth, cellHeight = getCellSize(app)
    for row in range(len(app.board)):
        for col in range(len(app.board[0])):
            cellLeft, cellTop = getCellLeftTop(app, row, col)
            if ((cellLeft<=mouseX<=cellLeft+cellWidth) and 
            (cellTop<=mouseY<=cellTop+cellHeight)):
                return (row, col)
    return None

def onMousePress(app, mouseX, mouseY):
    cellLocation = getCellFromClick(app, mouseX, mouseY)
    # color = app.colorTurn if app.whiteTurn else 'black'

    #if i click outside of board
    if cellLocation == None:
        app.selectedCell = None

    # if app.whiteTurn == True:
    #if i click on a cell that is already highlighted I want to make it not highlighted
    if app.selectedCell == cellLocation:
        app.selectedCell = None
        app.showMoves = False

    #if I click on piece on the board
    elif cellLocation != None and app.board[cellLocation[0]][cellLocation[1]]!=None:
        #if my currently selected cell is none (I am not on a piece)
        if app.selectedCell == None:
            app.selectedCell = cellLocation
        
        #if my currently selected cell is a piece and I click on a another piece of my color show it
        elif app.selectedCell!=None and app.board[app.selectedCell[0]][app.selectedCell[1]].color == app.board[cellLocation[0]][cellLocation[1]].color:
             app.selectedCell = cellLocation
        app.showMoves = True

    #if my selectedCell is a piece and the location I click on is None or has piece, move the piece
    if app.selectedCell!=None:
        currPiece = app.board[app.selectedCell[0]][app.selectedCell[1]]
        # doNotIncludeKingInLegalMoves(app, currPiece, app.board)
        if (cellLocation) in currPiece.legalMoves(app.board):
            currPiece.move(cellLocation[0], cellLocation[1])
            app.board[app.selectedCell[0]][app.selectedCell[1]] = None
            app.board[cellLocation[0]][cellLocation[1]] = currPiece
            app.selectedCell = None
            app.showMoves = False
            
def onKeyPress(app, key):
    if key == 'r':
        resetBoard(app)

def main():
    runApp()

main()