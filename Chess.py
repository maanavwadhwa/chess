from cmu_graphics import *

def onAppStart(app):
    app.rows = 8
    app.cols = 8
    app.boardLeft = 37.5
    app.boardTop = 50
    app.boardWidth = 325
    app.boardHeight = 325
    app.cellBorderWidth = 2
    app.board = [([None] * app.cols) for row in range(app.rows)]
    # app.url = 'cmu://1533/159473/pawn.png'
    app.selectedCell = None
    
# drawImage
#     Image(app.url, 50, 100)


def redrawAll(app):
    drawLabel('Chess', 200, 30, size=16)
    drawBoard(app)
    drawBoardBorder(app)
    
    # imageWidth, imageHeight = getImageSize(app.url)



    # drawImage(app.url, 59, 315, align = 'center',
    #           width=imageWidth//25, height=imageHeight//25)

def drawBoard(app):
    color = 'black'
    for row in range(app.rows):
        for col in range(app.cols):
            if row%2 ==0 and col%2 ==0:
                drawCell(app, row, col, 'saddleBrown')
            elif row%2 ==1 and col%2 ==1:
                drawCell(app,row,col,'saddleBrown')
            else:
                drawCell(app,row,col,'burlywood')

def drawBoardBorder(app):
  # draw the board outline (with double-thickness):
  drawRect(app.boardLeft, app.boardTop, app.boardWidth, app.boardHeight,
           fill=None, border='black',
           borderWidth=2*app.cellBorderWidth)

def drawCell(app, row, col, color):
    cellLeft, cellTop = getCellLeftTop(app, row, col)
    cellWidth, cellHeight = getCellSize(app)


    drawRect(cellLeft, cellTop, cellWidth, cellHeight,
             fill=color, border='black',
             borderWidth=app.cellBorderWidth)
             
    cellColor = 'gold' if ((row, col) == app.selectedCell) else 'black'
             
    # if row == 0 or row == 7 or col == 0 or col == 7:
    #     borderWidth = 2*app.cellBorderWidth
    # cellColor = 'gold' if ((row, col) == app.selectedCell) else 'black'
    drawRect(cellLeft, cellTop,
            getCellSize(app)[0], getCellSize(app)[1],
            fill=None, border=cellColor, borderWidth=app.cellBorderWidth)

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
    for row in range(app.rows):
        for col in range(app.cols):
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
    # elif app.selectedCell == None:
    #     app.selectedCell = cellLocation
    else:
        app.selectedCell = cellLocation
        



def main():
    runApp()

main()