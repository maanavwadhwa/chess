from board_class import Board
from cmu_graphics import *

def onAppStart(app):
    resetBoard(app)

def resetBoard(app):
    app.boardLeft = 37.5
    app.boardTop = 50
    app.boardWidth = 325
    app.boardHeight = 325
    app.cellBorderWidth = 1
    app.board = Board()
    app.selectedCell = None
    app.showMoves = False 
    app.promotionBoard = [['Queen'],['Rook'],['Knight'],['Bishop']]
    app.promotionBoardLeft = 78
    app.promotionBoardTop = 130
    app.promotionBoardWidth = 244
    app.promotionBoardHeight = 162.5

def redrawAll(app):
    drawLabel(app.board.message, 200, 30, size=16)
    drawBoard(app)
    drawPieces(app)
    if app.showMoves == True:
        drawPossibleMoves(app)
    # if app.kingInCheck == True:
    #     drawLabel(app.label, 200, 30, size = 16)
    if app.board.promotablePiece!=None:
        drawPromotionBoard(app)
    
def drawPossibleMoves(app):
    currPiece = app.board.board[app.selectedCell[0]][app.selectedCell[1]]
    if currPiece.color == app.board.playerTurn and app.board.promotablePiece==None:
        possibleMoves = app.board.updatedLegalMoves(currPiece)
        for row, col in possibleMoves:
            cellWidth, cellHeight = getCellSize(app)
            xcoordinate = app.boardLeft+col*cellWidth+cellWidth/2
            ycoordinate = app.boardTop+row*cellHeight+cellHeight/2
            drawCircle(xcoordinate,ycoordinate, 6, fill = 'yellow', opacity = 80)

def drawBoard(app):
    rows, cols = app.board.rows, app.board.cols
    for row in range(rows):
        for col in range(cols):
            if row%2 ==0 and col%2 ==0:
                drawCell(app, row, col, 'burlywood')
            elif row%2 ==1 and col%2 ==1:
                drawCell(app,row,col,'burlywood')
            else:
                drawCell(app,row,col,'saddleBrown')

def drawPieces(app):
    rows, cols = app.board.rows,app.board.cols
    for row in range(rows):
        for col in range(cols):
            piece = app.board.board[row][col]
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
    if app.selectedCell==(row, col) and app.board.promotablePiece==None and app.board.message!='Checkmate!! Press r to play again':
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
    cellWidth = app.boardWidth / app.board.cols
    cellHeight = app.boardHeight / app.board.rows
    return (cellWidth, cellHeight)

def getCellFromClick(app, mouseX, mouseY):
    cellWidth, cellHeight = getCellSize(app)
    for row in range(app.board.rows):
        for col in range(app.board.cols):
            cellLeft, cellTop = getCellLeftTop(app, row, col)
            if ((cellLeft<=mouseX<=cellLeft+cellWidth) and 
            (cellTop<=mouseY<=cellTop+cellHeight)):
                return (row, col)
    return None

def onMousePress(app, mouseX, mouseY):
    #revisit and fix up 
    cellLocation = getCellFromClick(app, mouseX, mouseY)

    if app.board.promotablePiece!=None:
        if getPromotionCellFromClick(app, mouseX, mouseY) != None:
            rowClicked, colClicked = getPromotionCellFromClick(app, mouseX, mouseY)
            pieceDesired = app.promotionBoard[rowClicked][colClicked]
            app.board.promotion(pieceDesired)
            


    if app.board.promotablePiece == None:
    #if i click outside of board
        if cellLocation == None:
            app.selectedCell = None

        #if i click on a cell that is already highlighted I want to make it not highlighted
        if app.selectedCell == cellLocation:
            app.selectedCell = None
            app.showMoves = False

        #if I click on piece on the board
        elif cellLocation != None and app.board.board[cellLocation[0]][cellLocation[1]]!=None:
            currPiece = app.board.board[cellLocation[0]][cellLocation[1]]
            if currPiece.color == app.board.playerTurn:
                #if my currently selected cell is none (I am not on a piece)
                if app.selectedCell == None:
                    app.selectedCell = cellLocation
        
                #if my currently selected cell is a piece and I click on a another piece of my color show it
                elif app.selectedCell!=None and app.board.board[app.selectedCell[0]][app.selectedCell[1]].color == app.board.board[cellLocation[0]][cellLocation[1]].color:
                    app.selectedCell = cellLocation
                app.showMoves = True


        #if my selectedCell is a piece and the location I click on is None or has piece, move the piece
        if app.selectedCell!=None:
            currPiece = app.board.board[app.selectedCell[0]][app.selectedCell[1]]
            if currPiece.color == app.board.playerTurn:
                if (cellLocation) in app.board.updatedLegalMoves(currPiece):
                    app.board.move(currPiece, cellLocation)

                        
                    # if app.message != 'Chess':
                    #     app.message = 'Chess'
                    # if app.board.isStalemate():
                    #     app.message = 'Stalemate!'
                    
                    # elif app.board.isCheckmate():
                    #     app.message = 'Checkmate!'
                
                    # elif app.board.kingInCheck:
                    #     app.message = 'Check!!'

                    # else:
                    #     app.message = 'Chess'

                    app.selectedCell = None
                    app.showMoves = False

def onKeyPress(app, key):
    if key == 'r': 
        resetBoard(app)

def drawPromotionBoard(app):
    rows, cols = len(app.promotionBoard), len(app.promotionBoard[0])
    for row in range(rows):
        for col in range(cols):
            drawPromotionCell(app, row, col, 'mistyRose')

def drawPromotionCell(app, row, col, color):
    cellLeft, cellTop = getPromotionCellLeftTop(app, row, col)
    cellWidth, cellHeight = getPromotionCellSize(app)
    drawRect(cellLeft, cellTop,
            cellWidth, cellHeight,
            fill=color, border='black', borderWidth=3*app.cellBorderWidth)
    drawLabel(f'{app.promotionBoard[row][col]}', (cellLeft+(cellWidth)/2), (cellTop+(cellHeight)/2), align = 'center')

def getPromotionCellLeftTop(app, row, col):
    cellWidth, cellHeight = getPromotionCellSize(app)
    cellLeft = app.promotionBoardLeft + col * cellWidth
    cellTop = app.promotionBoardTop + row * cellHeight
    return (cellLeft, cellTop)

def getPromotionCellSize(app):
    rows, cols = len(app.promotionBoard), len(app.promotionBoard[0])
    cellWidth = app.promotionBoardWidth / cols
    cellHeight = app.promotionBoardHeight / rows
    return (cellWidth, cellHeight)

def getPromotionCellFromClick(app, mouseX, mouseY):
    rows, cols = len(app.promotionBoard), len(app.promotionBoard[0])
    cellWidth, cellHeight = getPromotionCellSize(app)
    for row in range(rows):
        for col in range(cols):
            cellLeft, cellTop = getPromotionCellLeftTop(app, row, col)
            if ((cellLeft<=mouseX<=cellLeft+cellWidth) and 
            (cellTop<=mouseY<=cellTop+cellHeight)):
                return (row, col)
    return None
            

def main():
    runApp(width = 400, height = 400)

main()