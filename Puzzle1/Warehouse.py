"""
Jeremy Daugherty - Puzzle 1 Breadth-First Tree Search
Sokoban Solver V1
"""


class Warehouse:
    def __init__(self, filename=None):
        """
        Init function, creates
        :param filename:
        """
        if filename is None:
            raise Exception("File not valid, please try again.")
        # Open the file
        with open(filename, 'r') as file:
            # First is the size
            fileStr = file.read()
            fileLines = fileStr.split('\n')
            # size of our grids
            self.width, self.height = fileLines[0].split(' ')
            self.width = int(self.width)
            self.height = int(self.height)
            # Starting point of our actor and actor var for later
            start_column, start_row = fileLines[1].split(' ')
            self.start = (int(start_column), int(start_row))
            self.actor = None
            tempGrid = fileLines[2:]
            # the starting point the grid is working with
            self.InitGrid = [[i for i in j] for j in tempGrid]
            # a working grid that we can alter as needed, we set to none when
            # it's not being used.
            self.WGrid = None
        return

    def getTarget(self, direction, start=None):
        """
        A helper to get a target in our grid.
        :param direction: The direction we want to go
        :param start:
        :return:
        """
        # check if we have a start
        if start is None:
            # if no start is given use self.actor, or self.start if no actor
            if self.actor is None:
                start = self.actor
            else:
                start = self.start

        target = [-1, -1]
        if direction == 'U':
            target = [start[1], start[1] - 1]
        elif direction == 'D':
            target = [start[1], start[1] + 1]
        elif direction == 'L':
            target = [start[1] - 1, start[1]]
        elif direction == 'R':
            target = [start[1] + 1, start[1]]
        return target

    def checkMove(self, direction, start=None):
        """
        Checker to ensure a move is valid.
        :param direction: The direction we are wanting to mowe
        :param start: The location we are starting from, if no start is given
        then we use self.actor. If self.actor doesn't exist, then we use
        self.start.
        :return: true or false.
        """
        # get our starting point properly.
        if start is None:
            if self.actor is None:
                start = self.start
            else:
                start = self.actor
        # check whether we have a working grid
        if self.WGRid is None:
            working_grid = False
        else:
            working_grid = True
        target = [-1,-1]

        # check that its in the grid.
        if 0 > target[0] or target[0] > self.width:
            return False
        if 0 > target[1] or target[1] > self.height:
            return False
        # check that there are no walls.
        if working_grid:
            if self.WGrid[target[0]][target[1]]:
                pass

    def move(self, direction=None):
        if self.WGrid is None:
            self.ResetWGrid()
        if direction == 'U':
            pass
        # if direction == 'D':
        # if direction == 'L':
        # if direction == 'R':
        return

    def ResetWGrid(self):
        self.WGrid = [[j for j in i] for i in self.InitGrid]
        self.printGrids()
        return

    def ResetActor(self):
        self.actor = [self.start[0], self.start[1]]
        return

    def printGrids(self):
        for i in self.InitGrid:
            print(i)
        if self.WGrid is None:
            return
        for j in self.WGrid:
            print(j)
        return

if __name__ == "__main__":
    test = Warehouse("Puzzle1.txt")
    # test.move('U')
    # test.move('D')
    # test.move('R')
    # test.move('L')
    test.printGrids()
    for i in range(4):
        print(test.InitGrid[i][i])
