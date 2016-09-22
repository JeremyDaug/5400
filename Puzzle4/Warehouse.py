"""
Jeremy Daugherty - Puzzle 3 Greedy Best-First Graph Search
Sokoban Solver V3
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


def get_distance(start, end):
    """
    A helper to get the step distance between to points. Simple Manhattan
    distance.
    :param start: The starting point.
    :param end: the Ending point. 
    :return: The distance between them.
    """
    total = abs(start[0]-end[0])
    total += abs(start[1]-end[1])
    return total


def add_tuples(x, y):
    """
    a helper to add tuples together more nicely.
    :param x: first tuple
    :param y: 2nd tuple
    :return: the resultant tuple
    """
    return tuple((x[0]+y[0], x[1]+y[1]))


class Warehouse:
    def __init__(self, file_name):
        with open(file_name) as the_file:
            file_lines = the_file.read().split('\n')
            size = file_lines[0].split(' ')
            # grid size
            width = int(size[0])
            height = int(size[1])
            start = file_lines[1].split(' ')
            # starting point
            start = (int(start[1]), int(start[0]))
            # print(start)
            # our grid
            grid = [[j for j in i] for i in file_lines[2:]]
        # State Space Setup
        self.Head = State(height,
                          width,
                          start,
                          grid,
                          [])
        self.Active = self.Head
        # the endpoints for our crates, for ease of access
        self.frontier = [self.Head]
        self.explored = []
        self.targets = []
        for i in range(height):
            for j in range(width):
                if grid[i][j] == TARGET:
                    self.targets.append((i, j))
        self.Active.weight = self.cost()
        return

    def check_soln(self):
        """
        A delegate function that calls the check solution function on the current active state.
        :return: The result of the check.
        """
        return self.Active.check_soln(self.targets)

    def get_best(self):
        """
        A wrapper to get the min out of our frontier, and remove it from the
        frontier.
        :return: The best state in the frontier. If states share the value, it
        will take the first option in the list.
        """
        # get the smallest based on it's weight.
        smallest = min(self.frontier, key=lambda s: s.weight)
        self.frontier.remove(smallest)
        print(smallest.weight, smallest.step_count())
        # for i in smallest.grid:
        #     print(i)
        return smallest

    def back_to_head(self):
        """
        Helper function for our tree, returns the active node to the head
        """
        self.Active = self.Head
        return

    def move(self, direction):
        """
        A delegate function to make using a move easier.
        :param direction: the direction we want to go.
        :return: the new node that has been added to our tree. If the move
        failed it returns None.
        """
        temp = self.Active.move(direction, self.targets)
        if temp:
            temp.weight = temp.cost(self.targets)
        return temp

    def cost(self):
        return self.Active.cost(self.targets)


class State:
    def __init__(self, height, width, actor, grid, steps):
        self.height = height
        self.width = width
        self.actor = actor
        self.grid = [[j for j in i] for i in grid]
        self.steps = steps
        self.weight = None
        return

    def __eq__(self, other):
        if self.height != other.height:
            return False
        if self.width != other.width:
            return False
        if self.actor != other.actor:
            return False
        for s, o in zip(self.grid, other.grid):
            for sf, of in zip(s, o):
                if sf != of:
                    return False
        # we skip steps, as the steps to get to a state doesn't
        # make that state meaningfully different. It also implies we got to the state faster already.
        return True

    def cost(self, targets):
        """
        Gets the value cost of this state, the lower the closer it is to solved.
        :param targets: The target squares, imported from Warehouse.
        :return: the value of the state, the lower the better.
        """
        # get the crate locations for use.
        crates = self.crates()
        # get the distance from the crates to the nearest targets
        total = 0
        for i in crates:
            shortest = -1
            for j in targets:
                current = get_distance(i, j)
                if current < shortest or shortest < 0:
                    shortest = current
            # check that the current box is in a non-fail state
            # it's not frozen in a corner or stuck.
            if not self.crate_movable(i):
                # if it failed, multiply by an arbitrarily large number.
                # If it's on a target, then it won't matter as shortest will
                # be 0.
                shortest *= 1000
                if shortest == 0:
                    # if the crate is immovable, and on a target, then decrease
                    # it's value a bit more, to reward it.
                    shortest = -2
            total += 3*shortest
        # add the distance between the actor and the nearest box
        total += (self.closest_box(crates)-1)
        total *= 2
        # Get the distance traveled.
        total += self.step_count()
        # print('actor: ', self.actor)
        # print('cost: ', total)
        # for i in self.grid:
        #     print(i)
        return total

    def crate_movable(self, crate, prev=None):
        """
        A checker to see if a crate can be moved, can recurse into itself to
        see if crates are actually blocking each other, or just are there.
        :param crate: The crate in question
        :param prev: the previous crates touched.
        :return: True if the crate is movable, false otherwise.
        """
        # Add the current crate to the prev list, for later.
        if not prev:
            prev = []
        prev.append(crate)
        directions = [UP, DOWN, LEFT, RIGHT]
        results = {'vertical': True, 'horizontal': True}
        for direction in directions:
            # get our axis
            key = ''
            if direction == UP or direction == DOWN:
                key = 'vertical'
                # if the axis is already false, then skip this direction, we
                # already have our answer
                if not results[key]:
                    continue
            if direction == LEFT or direction == RIGHT:
                key = 'horizontal'
                if not results[key]:
                    continue
            # get adjacent
            adj = self.get_target(direction, crate)
            # if its in the grid, keep working.
            if self.in_grid(adj):
                # if a wall, it's false
                if self.grid[adj[0]][adj[1]] == WALL:
                    results[key] = False
                # if it's a previously touched crate, assume it's stuck.
                elif adj in prev:
                    results[key] = False
                # if not previous, and a crate, run it on that crate and get
                # the result
                elif self.grid[adj[0]][adj[1]] == CRATE:
                    adj_crate = self.crate_movable(adj, prev)
                    results[key] = adj_crate
            # if adj_point is outside of the grid, it's false.
            else:
                results[key] = False
        # if both vertical and horizontal are false, then this box is broken.
        return results['vertical'] or results['horizontal']

    def closest_box(self, crates):
        """
        Gets the distance between the actor and the nearest chest.
        :return: the distance between actor and nearest chest.
        """
        best = -1
        for i in crates:
            current = get_distance(self.actor, i)
            if best < 0 or best > current:
                best = current
        return best

    def crates(self):
        """
        A function that finds all the crates in the grid and returns their locations in a list.
        :return: The list of locations that have crates.
        """
        ret = []
        for i in range(self.height):
            for j in range(self.width):
                if self.grid[i][j] == CRATE:
                    ret.append((i, j))
        return ret

    def step_count(self):
        return len(self.steps)

    def output(self, file_name, start, end):
        output = str(int((end - start) * 10 ** 6)) + '\n'
        output += str(self.step_count()) + '\n'
        for i in self.steps:
            output += i
        output += '\n'
        output += str(self.width) + ' '
        output += str(self.height) + '\n'
        output += str(self.actor[0]) + ' '
        output += str(self.actor[1]) + '\n'
        for i in self.grid:
            for j in i:
                output += j
            output += '\n'

        with open("soln_" + file_name, 'w') as out:
            out.write(output)
        print(output)

    def check_soln(self, targets):
        """
        A Solution Checker
        :param targets: The grid we are checking.
        :return: True if solved, False otherwise.
        """
        for t in targets:
            if not self.grid[t[0]][t[1]] == CRATE:
                return False
        return True

    def get_target(self, direction, actor=None):
        """
        Relative direction getter for our position
        :param direction: the direction we want to go
        :param actor: the place we are starting our move from. if no location
        is given we use the actor of the state.
        :return: the target square.
        """
        if actor is None:
            actor = self.actor
        dir_moves = {UP: (-1, 0),
                     DOWN: (1, 0),
                     LEFT: (0, -1),
                     RIGHT: (0, 1)}
        return add_tuples(actor, dir_moves[direction])

    def in_grid(self, target):
        """
        Checker for the space we want to move to.
        :param target: The space we want to move to
        :return: True if the target is in the Grid, else False
        """
        if not 0 <= target[0] < self.height:
            return False
        if not 0 <= target[1] < self.width:
            return False
        return True

    def check_move(self, direction, start=None):
        """
        Checks if our move is valid or not.
        :param direction: the direction we want to move
        :param start: the point we are starting at.
        :return: We return True if the space we want to move
         to is empty (valid), we return CRATE if there's a crate to push and we
         can push the crate, otherwise we return False.
        """
        target = self.get_target(direction, start)
        # check if in the grid
        if not self.in_grid(target):
            return False
        # check for wall
        if self.grid[target[0]][target[1]] == WALL:
            return False
        # check for box and valid box move
        if self.grid[target[0]][target[1]] == CRATE:
            # if box in the way, check if we can move the box properly
            box_move = self.get_target(direction, target)
            # if box move in grid
            if not self.in_grid(box_move):
                return False
            # if wall or crate in the way.
            is_wall = self.grid[box_move[0]][box_move[1]] == WALL
            is_crate = self.grid[box_move[0]][box_move[1]] == CRATE
            if is_wall or is_crate:
                return False
            return CRATE
        # if no crate, no wall, and in grid, we're good.
        else:
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
        :return : Returns the state that the move would produce, if it's not a
        valid move then it returns None.
        """
        # check if it's valid
        valid = self.check_move(direction)
        if not valid:
            return None
        # since it is, do it.
        target = self.get_target(direction)
        new_grid = [[j for j in i] for i in self.grid]
        # if theres' a box, move it.
        if valid == CRATE:
            box = self.get_target(direction, target)
            new_grid[target[0]][target[1]] = SPACE
            new_grid[box[0]][box[1]] = CRATE
            # if it is moved off an endpoint, then put the target back.
            if target in end_points:
                new_grid[target[0]][target[1]] = TARGET
        # add our direction as our newest step.
        next_step = self.steps[:]
        next_step.append(direction)
        return State(self.height, self.width, target, new_grid, next_step)


if __name__ == "__main__":
    test = Warehouse("Puzzle1.txt")
