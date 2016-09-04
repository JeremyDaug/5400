"""
Jeremy Daugherty - Puzzle 1 Breadth-First Tree Search
Sokoban Solver V1
"""


class Warehouse:
    def __init__(self, file_name):
        with open(file_name) as file:
            file_lines = file.read().split('\n')
            size = file_lines[0].split(' ')
            self.width = int(size[0])
            self.height = int(size[1])
            start = file_lines[1].split(' ')
            self.start = (int(start[0]), int(start[1]))
            self.grid = [[j for j in i] for i in file_lines[2:]]
            self.targets = []
            for i in range(self.width):
                for j in range(self.height):
                    if self.grid[i][j] == 't':
                        self.targets.append((i, j))
        return

    def check_soln(self, grid):
        for t in self.targets:
            if not grid[t[0]][t[1]] == 'c':
                return False
        return True


class State:
    def __init__(self, height, width, actor, grid, steps):
        self.height = height
        self.width = width
        self.grid = [[j for j in i] for i in grid]
        self.actor = actor
        self.steps = steps
        return

    def print(self):
        for i in self.grid:
            print(i)
        print('\n')

    def path_length(self):
        return len(self.steps)

    def get_target(self, dir, actor=None):
        if actor is None:
            actor = self.actor
        target = None
        if dir == 'U':
            target = (actor[0] - 1, actor[1])
        elif dir == 'D':
            target = (actor[0] + 1, actor[1])
        elif dir == 'L':
            target = (actor[0], actor[1] - 1)
        elif dir == 'R':
            target = (actor[0], actor[1] + 1)
        return target

    def in_grid(self, target):
        if not 0 <= target[0] < self.width:
            return False
        if not 0 <= target[1] < self.height:
            return False
        return True

    def check_move(self, dir):
        target = self.get_target(dir)
        # check if in the grid
        if not self.in_grid(target):
            return False
        # check for wall
        if self.grid[target[0]][target[1]] == 'w':
            return False
        # check for box and valid box move
        elif self.grid[target[0]][target[1]] == 'c':
            box = self.get_target(dir, target)
            # if box move in grid
            if not self.in_grid(box):
                return False
            # if wall in way
            if self.grid[box[0]][box[1]] == 'w':
                return False
            return 'B'
        # if no crate, no wall, and in grid, we're good.
        else:
            return True

    def move(self, dir, end_points):
        # check if it's valid
        Valid = self.check_move(dir)
        if not Valid:
            return None
        # since it is, do it.
        target = self.get_target(dir)
        newGrid = [[j for j in i] for i in self.grid]
        # if theres' a box, move it.
        if Valid == 'B':
            box = self.get_target(dir, target)
            newGrid[target[0]][target[1]] = '.'
            newGrid[box[0]][box[1]] = 'c'
            # if it is moved off an endpoint, then put it back.
            if target in end_points:
                newGrid[target[0]][target[1]] = 't'
        next_step = self.steps[:]
        next_step.append(dir)
        ret = State(self.height, self.width, target, newGrid, next_step)
        return ret


if __name__ == "__main__":
    test = Warehouse("Puzzle1.txt")