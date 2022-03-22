class Sudoku:
    def __init__(self):
        self.board = [[None]*9 for i in range(9)]

    def __getitem__(self, pos):
        return self.board[pos[0]][pos[1]]

    def __setitem__(self, pos, item):
        self.board[pos[0]][pos[1]] = item

    def populate(self, dict):
        for pos, item in dict.items():
            self[pos] = item

    def parse(self, boardstr):
        for i,l in enumerate(boardstr.split("\n")):
            for j,e in enumerate(list(l)):
                if e.isdigit():
                    self[(i,j)] = int(e)
                else:
                    self[(i,j)] = None

    def __str__(self):
        strOut = ""
        for i in self.board:
            for j in i:
                if (int(j) in range(10) if str(j).isdigit() else False):
                    strOut += str(j)
                elif j is None:
                    strOut += "."
                else:
                    strOut += "#"
            strOut += "\n"
        
        return strOut

def main():
    test_sudoku = Sudoku()
    test_sudoku.parse(".........\n.5.......\n.........\n.........\n.........\n...6.....\n.........\n.........\n.........")
    print(str(test_sudoku))
    print(test_sudoku[(1,1)])

if __name__ == "__main__":
    main()