def isInbounds(rank, file, rows, cols):
    return 0<=rank<rows and 0<=file<cols

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

