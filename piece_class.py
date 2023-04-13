class Piece:
    def __init__(self, rank, file, color): #rank --> row, file---> col
        self.rank = rank
        self.file = file
        self.color = color
        self.movedFromInitialCell = False

    def move(self, newRank, newFile):
        self.rank = newRank
        self.file = newFile 
        self.movedFromInitialCell = True

    def simulateMove(self, newRank, newFile):
        self.rank = newRank
        self.file = newFile 


    def __repr__(self):
        return f'{self.name}: ({self.rank},{self.file}, {self.color})'