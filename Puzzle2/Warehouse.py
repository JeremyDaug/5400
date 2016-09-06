"""
Jeremy Daugherty - Puzzle 2 Iterative-Deepening - Depth-First Tree Search
Sokoban Solver V2
"""

# a few necessary constants
UP = 'U'
DOWN = 'D'
LEFT = 'L'
RIGHT = 'R'
WALL = 'w'
SPACE = '.'
CRATE = 'c'
TARGET = 't'


class Warehouse:
    def __init__(self, file_name):
        with open(file_name) as file:
            file_lines = file.read().split('\n')
            size = file_lines[0].split(' ')
            # grid size
            width = int(size[0])
            height = int(size[1])
            start = file_lines[1].split(' ')
            # starting point
            start = (int(start[0]), int(start[1]))
            # our grid
            grid = [[j for j in i] for i in file_lines[2:]]
            # Tree setup
            self.Head = StateNode(None,
                                  0,
                                  height,
                                  width,
                                  start,
                                  grid,
                                  [])
            self.Active = self.Head
            # the endpoints for our crates, for ease of access
            self.targets = []
            for i in range(width):
                for j in range(height):
                    if grid[i][j] == TARGET:
                        self.targets.append((i, j))

        return

    def back_to_head(self):
        """
        Helper function for our tree, returns the active node to the head
        """
        self.Active = self.Head
        return

    def check_soln(self, grid=None):
        """
        A Solution Checker
        :param grid: The grid we are checking.
        :return: True if solved, False otherwise.
        """
        if grid is None:
            grid = self.Active.grid
        for t in self.targets:
            if not grid[t[0]][t[1]] == CRATE:
                return False
        return True

    def move(self, dir):
        """
        A delegate function to make using a move easier.
        :param dir: the direction we want to go.
        :return: the new node that has been added to our tree. If the move
        failed it returns None.
        """
        return self.Active.move(dir, self.targets)


class StateNode:
    def __init__(self, parent, step_count, height, width, actor, grid, steps):
        self.height = height
        self.width = width
        self.actor = actor
        self.grid = [[j for j in i] for i in grid]
        self.steps = steps
        self.parent = parent
        self.kids = dict()
        self.step_count = step_count
        return

    def add(self, key, height, width, actor, grid, steps):
        """
        Adds a new kid to the node
        :param key: the key to the child
        :param height: height of the grid
        :param width: width of the grid
        :param actor: the current location of the actor
        :param grid: the state of the grid
        :param steps: the steps taken to get to the grid
        """
        self.kids[key] = StateNode(self, self.step_count + 1,
                                   height, width, actor, grid, steps)
        return

    def delete(self, key):
        """
        Deletes a child
        :param key: The key to the child we want to delete.
        """
        self.kids.pop(key)
        return

    def get_target(self, dir, actor=None):
        """
        Relative direction getter for our position
        :param dir: the direction we want to go
        :param actor:
        :return:
        """
        if actor is None:
            actor = self.actor
        target = None
        if dir == UP:
            target = (actor[0] - 1, actor[1])
        elif dir == DOWN:
            target = (actor[0] + 1, actor[1])
        elif dir == LEFT:
            target = (actor[0], actor[1] - 1)
        elif dir == RIGHT:
            target = (actor[0], actor[1] + 1)
        return target

    def in_grid(self, target):
        """
        Checker for the space we want to move to.
        :param target: The space we want to move to
        :return: True if the target is in the Grid, else False
        """
        if not 0 <= target[0] < self.width:
            return False
        if not 0 <= target[1] < self.height:
            return False
        return True

    def check_move(self, dir):
        """
        Checks if our move is valid or not.
        :param dir: the direction we want to move
        :return: We return True if the space we want to move
         to is empty (valid), we return CRATE if there's a crate to push and we
         can push the crate, otherwise we return False.
        """
        target = self.get_target(dir)
        # check if in the grid
        if not self.in_grid(target):
            return False
        # check for wall
        if self.grid[target[0]][target[1]] == WALL:
            return False
        # check for box and valid box move
        if self.grid[target[0]][target[1]] == CRATE:
            # TODO check for another box in the way
            # if box in the way, check if we can move the box properly
            box = self.get_target(dir, target)
            # if box move in grid
            if not self.in_grid(box):
                return False
            # if wall in way
            if self.grid[box[0]][box[1]] == WALL:
                return False
            return CRATE
        # if no crate, no wall, and in grid, we're good.
        else:
            return True

    def move(self, dir, end_points):
        """
        A move function to do all the work of moving. Will move the actor,
        the crate (if valid as well), and create a new StateNode, and add it
        to our kids. If it is not a valid move it will put None in the kid that
        would've been made, marking that direction as invalid.
        :param dir: The direction we are trying to move.
        :param end_points: The target squares, so that if we move a crate off
        a target we reapply it to the grid.
        """
        # check if it's valid
        valid = self.check_move(dir)
        if not valid:
            self.kids[dir] = None
            return self.kids[dir]
        # since it is, do it.
        target = self.get_target(dir)
        newGrid = [[j for j in i] for i in self.grid]
        # if theres' a box, move it.
        if valid == CRATE:
            box = self.get_target(dir, target)
            newGrid[target[0]][target[1]] = SPACE
            newGrid[box[0]][box[1]] = CRATE
            # if it is moved off an endpoint, then put the target back.
            if target in end_points:
                newGrid[target[0]][target[1]] = TARGET
        # add our dir as our newest step.
        next_step = self.steps[:]
        next_step.append(dir)
        self.add(dir, self.height, self.width, target, newGrid, next_step)
        return self.kids[dir]


if __name__ == "__main__":
    test = Warehouse("Puzzle1.txt")
