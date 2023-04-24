from board_class import Board, miniMaxAlgo
from cmu_graphics import *

def onAppStart(app):
    app.width = 600
    app.height = 600
    app.mode = None
    resetBoard(app)

def resetBoard(app):
    app.boardLeft = 37.5
    app.boardTop = 50
    app.boardWidth = 525 
    app.boardHeight = 525 
    app.cellBorderWidth = 1
    app.board = Board()
    app.selectedCell = None
    app.showMoves = False 
    app.promotionBoard = [['Queen'],['Rook'],['Knight'],['Bishop']]
    app.promotionBoardLeft = 169 
    app.promotionBoardTop = 181 
    app.promotionBoardWidth = 262 
    app.promotionBoardHeight = 263 

#CITATION: To create a main screen, I relied on the framework taught in lecture on 4/18
def main_redrawAll(app):
    drawRect(0,0,600,600, fill = 'peachPuff', border = 'darkSlateGray', borderWidth = 15)
    drawLabel('Welcome to Chessmate!', app.width/2,app.height/4, size = 40, font = 'sacramento')
    drawLabel('Which mode would you like to play?', app.width/2,app.height/2.5, size = 25, font = 'cinzel')
    drawMultiplayerButton(app)
    drawEasyAIButton(app)
    drawMediumAIButton(app)
    drawHardAIButton(app)
    drawImage('Images/queen_white.png', 100, 
            400,align = 'center',
            width=100, height=100, rotateAngle = -30)
    drawImage('Images/queen_black.png', 500, 
            400,align = 'center',
            width=100, height=100, rotateAngle = 30)

def main_onMousePress(app, mouseX, mouseY):
    if isMultiplayerClicked(app, mouseX, mouseY):
        app.mode = 'multiplayer'
        setActiveScreen('game')
    elif isEasyAIClicked(app, mouseX, mouseY):
        app.mode = 'easyAI'
        app.depth = 1 
        setActiveScreen('game')
    elif isMediumAIClicked(app, mouseX, mouseY):
        app.mode = 'mediumAI'
        app.depth = 2 
        setActiveScreen('game') 
    elif isHardAIClicked(app,mouseX,mouseY):
        app.mode = 'hardAI'
        app.depth = 3
        setActiveScreen('game')

def game_redrawAll(app):
    drawRect(0,0, 600, 600, fill = 'darkSlateGray')
    drawLabel(app.board.message, 300, 25, size=app.board.fontSize, fill = 'gainsboro', font = 'monospace', bold = True)
    drawBoard(app)
    drawPieces(app)
    if app.showMoves == True:
        drawPossibleMoves(app)

    if app.board.promotablePiece!=None:
        drawPromotionBoard(app)
    drawLabel("Press space bar to return to menu", app.width/2, 585, size = 14, fill = 'white')
 
def drawPossibleMoves(app):
    currPiece = app.board.board[app.selectedCell[0]][app.selectedCell[1]]
    if currPiece.color == app.board.playerTurn and app.board.promotablePiece==None:
        possibleMoves = app.board.updatedLegalMoves(currPiece)
        for row, col in possibleMoves:
            cellWidth, cellHeight = getCellSize(app)
            xcoordinate = app.boardLeft+col*cellWidth+cellWidth/2
            ycoordinate = app.boardTop+row*cellHeight+cellHeight/2
            drawCircle(xcoordinate,ycoordinate, 7, fill = None, border = 'yellow', borderWidth = 4)

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
                #CITATION: I got the chess pieces' images from https://commons.wikimedia.org/wiki/Category:SVG_chess_pieces
                drawImage(piece.image, xcoordinate, 
                       ycoordinate,align = 'center',
                        width=cellWidth, height=cellHeight)

def drawCell(app, row, col, color):
    cellLeft, cellTop = getCellLeftTop(app, row, col)
    cellWidth, cellHeight = getCellSize(app)
    if app.selectedCell==(row, col) and app.board.promotablePiece==None and not app.board.gameOver:
        drawRect(cellLeft, cellTop,
            cellWidth, cellHeight,
            fill=color, border='gold', borderWidth=3*app.cellBorderWidth)
    else:
        drawRect(cellLeft, cellTop, cellWidth, cellHeight,
             fill=color)

#CITATION: I used the getCellLeftTop and getCellSize functions we used when making Tetris 
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

def game_onMousePress(app, mouseX, mouseY):
    if not app.board.gameOver:  
        cellLocation = getCellFromClick(app, mouseX, mouseY)

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
                    app.board.message = 'Chess'
                    app.showMoves = True
                else:
                    app.board.message = 'Not your turn yet!'     

            #if my selectedCell is a piece and the location I click on is None or has piece, move the piece
            if app.selectedCell!=None:
                currPiece = app.board.board[app.selectedCell[0]][app.selectedCell[1]]
                if currPiece.color == app.board.playerTurn:
                    if (cellLocation) in app.board.updatedLegalMoves(currPiece):
                        app.board.move(currPiece, cellLocation)
                        app.selectedCell = None
                        app.showMoves = False

        if app.board.promotablePiece!=None:
            if getPromotionCellFromClick(app, mouseX, mouseY) != None:
                rowClicked, colClicked = getPromotionCellFromClick(app, mouseX, mouseY)
                pieceDesired = app.promotionBoard[rowClicked][colClicked]
                app.board.promotion(pieceDesired)

def game_onMouseRelease(app,mouseX,mouseY):
    if app.board.playerTurn == 'black' and 'AI' in app.mode and not app.board.gameOver:
        piece, newMove = miniMaxAlgo(app.board, app.depth, True)[1]
        pieceOnOriginalBoard = app.board.board[piece.rank][piece.file]
        app.board.move(pieceOnOriginalBoard,newMove)
        if app.board.promotablePiece!=None:
            pieceDesired = 'Queen'
            app.board.promotion(pieceDesired)
        
def game_onKeyPress(app, key):
    if key == 'r' and app.board.gameOver: 
        resetBoard(app)

    if key == 'space':
        setActiveScreen('main')
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
    drawLabel(f'{app.promotionBoard[row][col]}', (cellLeft+(cellWidth)/2), (cellTop+(cellHeight)/2), size = 20, bold = True, align = 'center')

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

def drawMultiplayerButton(app):
    drawRect(app.width/2,app.height/1.9,app.width/3.5, 50, align = 'center', fill = 'cadetBlue', border = 'black')
    drawLabel('Multiplayer', app.width/2, app.height/1.9, size = 24, font = 'monospace' , bold = True, align = 'center')

def isMultiplayerClicked(app, mouseX, mouseY):
    cellLeft, cellTop = 214,291
    cellWidth, cellHeight = app.width/3.5, 50
    if ((cellLeft<=mouseX<=cellLeft+cellWidth) and 
            (cellTop<=mouseY<=cellTop+cellHeight)):
        return True
    return False

def drawEasyAIButton(app):
    drawRect(app.width/2,app.height/1.9+59,app.width/3.5, 50, align = 'center', fill = 'cadetBlue', border = 'black')
    drawLabel('Easy AI', app.width/2, app.height/1.6, size = 24, font = 'monospace' , bold = True, align = 'center')

def isEasyAIClicked(app, mouseX, mouseY):
    cellLeft, cellTop = 214,350
    cellWidth, cellHeight = app.width/3.5, 50
    if ((cellLeft<=mouseX<=cellLeft+cellWidth) and 
            (cellTop<=mouseY<=cellTop+cellHeight)):
        return True
    return False

def drawMediumAIButton(app):
    drawRect(app.width/2,app.height/1.9+(59*2),app.width/3.5, 50, align = 'center', fill = 'cadetBlue', border = 'black')
    drawLabel('Medium AI', app.width/2, app.height/1.9+(59*2), size = 24, font = 'monospace' , bold = True, align = 'center')

def isMediumAIClicked(app, mouseX, mouseY):
    cellLeft, cellTop = 214, 409
    cellWidth, cellHeight = app.width/3.5, 50
    if ((cellLeft<=mouseX<=cellLeft+cellWidth) and 
            (cellTop<=mouseY<=cellTop+cellHeight)):
        return True
    return False

def drawHardAIButton(app):
    drawRect(app.width/2,app.height/1.9+(59*3),app.width/3.5, 50, align = 'center', fill = 'cadetBlue', border = 'black')
    drawLabel('Hard AI', app.width/2, app.height/1.9+(59*3), size = 24, font = 'monospace' , bold = True, align = 'center')

def isHardAIClicked(app, mouseX, mouseY):
    cellLeft, cellTop = 214,468
    cellWidth, cellHeight = app.width/3.5, 50
    if ((cellLeft<=mouseX<=cellLeft+cellWidth) and 
            (cellTop<=mouseY<=cellTop+cellHeight)):
        return True
    return False

def main():
    runAppWithScreens(initialScreen = 'main')

main()