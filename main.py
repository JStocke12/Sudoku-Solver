class Sudoku:
    def __init__(self):
        self.board = [[None]*9 for i in range(9)]

    def __getitem__(self, pos):
        if type(pos) is slice:
            if type(pos.start) is tuple and type(pos.stop) is tuple and type(pos.stop is tuple):
                return self[(slice(pos.start[0], pos.stop[0], pos.step[0]), slice(pos.start[1], pos.stop[1], pos.step[1]))]
            else:
                raise NotImplementedError("sudoku slicer of non-tuples not implemented")
        elif type(pos) is tuple:
            if type(pos[0]) is not type(pos[1]):
                raise NotImplementedError("sudoku indices have mismatched type: {} and {}".format(type(pos[0]).__name__,type(pos[1]),__name__))
            elif type(pos[0]) is int:
                if pos[0] > 8 or pos[0] < 0:
                    raise IndexError("sudoku first index out of range")
                elif pos[1] > 8 or pos[1] < 0:
                    raise IndexError("sudoku second index out of range")
                else:
                    return self.board[pos[0]][pos[1]]
            elif type(pos[0]) is slice:
                return [i[pos[1]] for i in self.board[pos[0]]]
            else:
                raise TypeError("sudoku tuple indices must be integers or slices, not {}".format(type(pos[0]).__name__))
        else:
            raise TypeError("sudoku indices must be tuples or slices, not {}".format(type(pos).__name__))

    def __setitem__(self, pos, item):
        if type(pos) is tuple:
            if type(pos[0]) is int and type(pos[1]) is int:
                if pos[0] > 8 or pos[0] < 0:
                    raise IndexError("sudoku first index out of range")
                elif pos[1] > 8 or pos[1] < 0:
                    raise IndexError("sudoku second index out of range")
                else:
                    self.board[pos[0]][pos[1]] = item
            else:
                raise TypeError("sudoku setitem indices must be tuples of integers, not {} and {}".format(type(pos[0]).__name__,type(pos[1]),__name__))
        else:
            raise TypeError("sudoku setitem indices must be tuples, not {}".format(type(pos).__name__))

    def populate(self, dict):
        for pos, item in dict.items():
            self[pos] = item

    def __iter__(self):
        for l in self.board:
            for e in l:
                yield e

    def array_enumerate(self):
        for i,l in enumerate(self.board):
            for j,e in enumerate(list(l)):
                yield (i,j), e

    def simplify(self):
        for t,e in self.array_enumerate():
            if e is None:
                self[t] = set(range(1,10))
        for t,e in self.array_enumerate():
            if type(e) is int:
                for i,s in enumerate(self[(slice(t[0],t[0]+1),slice(0,9))][0]):
                    if type(s) is set:
                        temp_s = s
                        temp_s.discard(e)
                        self[(t[0],i)] = temp_s
                for i,s in enumerate(self[(slice(0,9),slice(t[1],t[1]+1))]):
                    if type(s) is set:
                        temp_s = s[0]
                        temp_s.discard(e)
                        self[(i,t[1])] = temp_s
                box = find_box(t)
                for i,l in enumerate(self[box]):
                    for j,s in enumerate(l):
                        if type(s) is set:
                            temp_s = s
                            temp_s.discard(e)
                            self[(box[0].start+i,box[1].start+j)] = temp_s
        for t,e in self.array_enumerate():
            if type(e) is set:
                if len(e) == 1:
                    self[t] = list(e)[0]

    def solve(self):
        temp_sudoku = Sudoku()
        while temp_sudoku.board != self.board: # simplify until it doesn't get any better
            for t,e in self.array_enumerate():
                temp_sudoku[t] = e
            self.simplify()
        smallestSet = set(range(1,10))
        setIndex = (-1,-1)
        for t,e in self.array_enumerate(): # identify the smallest remaining array
            if type(e) is set:
                if len(e) < len(smallestSet):
                    smallestSet = e
                    setIndex = t
        if setIndex == (-1,-1):
            return
        print(self)
        new_sudoku = Sudoku()
        for i in smallestSet: # solve recursively
            for t,e in self.array_enumerate():
                    new_sudoku[t] = e
            new_sudoku[setIndex] = i
            new_sudoku.solve()
            if new_sudoku is not None:
                for t,e in new_sudoku.array_enumerate():
                    self[t] = e
                return
        self = None

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

def find_box(coords):
    return (slice((coords[0]//3)*3,(coords[0]//3)*3+3),slice((coords[1]//3)*3,(coords[1]//3)*3+3))

def main():
    test_sudoku = Sudoku()
    test_sudoku.parse(".35.2....\n9....8.57\n7.849.6..\n6.4.7..3.\n8.2.637..\n35.84..9.\n47.28..6.\n...15..7.\n...63.42.")
    print(str(test_sudoku))
    test_sudoku.solve()
    print(test_sudoku)


if __name__ == "__main__":
    main()