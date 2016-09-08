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

    def move(self, direction):
        """
        A delegate function to make using a move easier.
        :param dir: the direction we want to go.
        :return: the new node that has been added to our tree. If the move
        failed it returns None.
        """
        return self.Active.move(direction, self.targets)


class StateNode:
    def __init__(self, parent, step_count, height, width, actor, grid, key):
        """
        Init function
        :param parent: Who our parent is (should be a node)
        :param step_count: The number of steps to get here from head
        :param height: The height of the grid
        :param width: The width of the grid
        :param actor: the current position of the actor
        :param grid: the grid itself
        :param key: they key to get here from our parent
        """
        self.height = height
        self.width = width
        self.actor = actor
        self.grid = [[j for j in i] for i in grid]
        self.key = key
        self.parent = parent
        self.kids = dict()
        self.step_count = step_count
        return

    def get_steps(self):
        """
        A recursive function to get the path to this node via the entire
        tree. While this is not as fast as simply storing the list, we only
        need to call this at the end so it's far easier and requires less
        work overall (and less memory).
        :return: A list of all steps taken.
        """
        # if the head, then return an empty list
        if self.parent is None:
            return []
        # if not the head, get the parent, then append our step.
        else:
            return self.parent.get_steps().append(self.key)

    def output(self, file_name, start, end):
        """
        An output function that outputs this node (presumably a goal) to
         a file.
        :param file_name: The name of the file our output is based off of.
        :param start: the start time for the program.
        :param end: the end time for our program.
        """
        # runtime
        output = str((end - start).microseconds) + '\n'
        # total number of steps
        output += str(self.step_count) + '\n'
        # the steps taken
        for i in self.get_steps():
            output += i
        output += '\n'
        # grid size
        output += str(self.width) + ' ' + \
                  str(self.height) + '\n'
        # actor endpoint
        output += str(self.actor[0]) + ' ' + \
                  str(self.actor[1]) + '\n'
        # the grid
        for i in self.grid:
            for j in i:
                output += j
            output += '\n'

        with open("soln_" + file_name, 'w') as out:
            out.write(output)
        return

    def check_soln(self, targets):
        """
        A Solution Checker
        :param targets: The end points where are crates should be.
        :return: True if solved, False otherwise.
        """
        for t in targets:
            if not self.grid[t[0]][t[1]] == CRATE:
                return False
        return True

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
        Deletes a child and all of it's children, on down
        :param key: The key to the child we want to delete.
        """
        self.kids[key].deep_delete()
        self.kids.pop(key)
        return

    def deep_delete(self):
        """
        A recursive delete function to be used to delete all of it's children
        on down.
        """
        for key in self.kids:
            self.kids[key].deep_delete()
        self.kids.clear()
        return

    def get_target(self, direction, actor=None):
        """
        Relative direction getter for our position
        :param direction: the direction we want to go
        :param actor: The position we are starting from. If not given it
        defaults to self.actor
        :return: the position (x,y) of the target sqare.
        """
        if actor is None:
            actor = self.actor
        poss_dirs = {UP:   (-1, 0),
                     DOWN: (1, 0),
                     LEFT: (0, -1),
                     RIGHT: (0, 1)}
        target = (actor[0]+poss_dirs[direction][0],
                  actor[1]+poss_dirs[direction][1])
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

    def check_move(self, direction):
        """
        Checks if our move is valid or not.
        :param direction: the direction we want to move
        :return: We return True if the space we want to move
         to is empty (valid), we return CRATE if there's a crate to push and we
         can push the crate, otherwise we return False.
        """
        target = self.get_target(direction)
        # check if in the grid
        if not self.in_grid(target):
            return False
        # check for wall
        if self.grid[target[0]][target[1]] == WALL:
            return False
        # check for box and valid box move
        if self.grid[target[0]][target[1]] == CRATE:
            # if box in the way, check if we can move the box properly
            box = self.get_target(dir, target)
            # if box move in grid
            if not self.in_grid(box):
                return False
            # check if a wall or box is at the box's target
            is_wall = self.grid[box[0]][box[1]] == WALL
            is_crate = self.grid[box[0]][box[1]] == CRATE
            if is_wall or is_crate:
                return False
            return CRATE
        # if no crate, no wall, and in grid, we're good.
        return True

    def move(self, direction, end_points):
        """
        A move function to do all the work of moving. Will move the actor,
        the crate (if valid as well), and create a new StateNode, and add it
        to our kids. If it is not a valid move it will put None in the kid that
        would've been made, marking that direction as invalid.
        :param direction: The direction we are trying to move.
        :param end_points: The target squares, so that if we move a crate off
        a target we reapply it to the grid.
        """
        # check if it's valid
        valid = self.check_move(direction)
        if not valid:
            self.kids[direction] = None
            return self.kids[direction]
        # since it is, do it.
        target = self.get_target(direction)
        newGrid = [[j for j in i] for i in self.grid]
        # if theres' a box, move it.
        if valid == CRATE:
            box = self.get_target(direction, target)
            newGrid[target[0]][target[1]] = SPACE
            newGrid[box[0]][box[1]] = CRATE
            # if it is moved off an endpoint, then put the target back.
            if target in end_points:
                newGrid[target[0]][target[1]] = TARGET
        # add our dir as our newest step.
        self.add(direction, self.height, self.width, target, newGrid, direction)
        return self.kids[direction]


if __name__ == "__main__":
    test = Warehouse("Puzzle1.txt")
