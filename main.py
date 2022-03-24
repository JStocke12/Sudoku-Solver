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

    def populate(self, dict): # given a dictionary of items and coordinates, populate the sudoku board with said coordinates
        for pos, item in dict.items():
            self[pos] = item

    def __iter__(self): # iteration over a sudoku board will yield both the element and the coordinates
        for i,l in enumerate(self.board):
            for j,e in enumerate(list(l)):
                yield (i,j), e

    def fill_empty(self): # fills all of the empty cells with the full set of possibilites 1-9, this will be reduced later
        for t,e in self:
            if e is None:
                self[t] = set(range(1,10)) # fills the empty space on the board with all possibilities 1-9

    def discard(self, t, e): # discards an element from a set at a given position
        if type(self[t]) is set:
            temp_s = self[t]
            temp_s.discard(e)
            self[t] = temp_s

    def box_simplify(self, b, t): # simplifies a cell by a defined box neighborhood
        x_range = range(9)[b[0]]
        y_range = range(9)[b[1]]
        if type(self[t]) is set: # this simplifies a set by the values surrounding it
            for (i,j),e in self:
                if i in x_range and j in y_range and type(e) is int:
                    self.discard(t,e)
        elif type(self[t]) is int: # this simplifies the sets around a value
            for (i,j),e in self:
                if i in x_range and j in y_range and type(e) is set:
                    self.discard((i,j),self[t])

    def full_simplify(self, t): # simplifies a single cell using the integers in its neighborhood.
        self.box_simplify(find_box(t),t)
        self.box_simplify((slice(t[0],t[0]+1),slice(0,9)),t)
        self.box_simplify((slice(0,9),slice(t[1],t[1]+1)),t)

    def is_correct(self): # TODO implement is_correct
        for i in range(9):
            if not {i for l in self[(slice(i,i+1),slice(0,9))] for i in l}.issubset(set(range(9))):
                return False
        for i in range(9):
            if not {i for l in self[(slice(0,9),slice(i,i+1))] for i in l}.issubset(set(range(9))):
                return False
        for i in range(3):
            for j in range(3):
                if not {i for l in self[(slice(i*3,i*3+3),slice(j*3,j*3+3))] for i in l}.issubset(set(range(9))):
                    return False
        
        return True

    def simplify(self):
        self.fill_empty() # fills the empty space on the board with all possibilities 1-9
        for t,e in self:
            if type(e) is int: # remove known impossibilities
                self.full_simplify(t)
        for t,e in self: # crystallizes determined sets (sets with only one element)
            if type(e) is set:
                if len(e) == 1:
                    self[t] = list(e)[0]

    def solve(self):
        print(self, 1)
        temp_sudoku = Sudoku()
        while temp_sudoku.board != self.board: # simplify until it doesn't get any better
            for t,e in self:
                temp_sudoku[t] = e
            self.simplify()
        smallestSet = set(range(1,10))
        setIndex = (-1,-1)
        for t,e in self: # identify the smallest remaining array
            if type(e) is set:
                if len(e) < len(smallestSet):
                    smallestSet = e
                    setIndex = t
        if setIndex == (-1,-1):
            return
        print(self, 2)
        new_sudoku = Sudoku()
        for i in smallestSet: # solve recursively
            for t,e in self:
                    new_sudoku[t] = e
            new_sudoku[setIndex] = i
            new_sudoku.solve()
            if new_sudoku is not None and new_sudoku.is_correct():
                for t,e in new_sudoku:
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
    test_sudoku.parse("827.15.43\n3.1249.76\n...8...25\n6.....2..\n.1839....\n....61.3.\n.62..43..\n1.5...48.\n...9...1.")
    print(str(test_sudoku))
    test_sudoku.solve()
    print(test_sudoku)


if __name__ == "__main__":
    main()