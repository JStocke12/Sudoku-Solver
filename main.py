class Sudoku:
    def __init__(self):
        self.board = [[None]*9]*9

    def __setitem__(self, pos, item):
        self.board[pos[0]][pos[1]] = item

    def populate(self, dict):
        for pos, item in dict:
            self.board[pos] = item

    def __str__(self):
        strOut = ""
        for i in self.board:
            for j in i:
                if (j in range(10) if type(j) is int else False):
                    strOut += j
                elif j is None:
                    strOut += " "
                else:
                    strOut += "#"

            strOut += "\n"

def main():
    test_sudoku = Sudoku()

if __name__ == "__main__":
    main()