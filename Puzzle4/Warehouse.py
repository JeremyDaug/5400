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
            self.width = int(size[0])
            self.height = int(size[1])
            start = file_lines[1].split(' ')
            # starting point
            self.start = (int(start[1]), int(start[0]))
            # print(start)
            # our grid
            self.grid = [[j for j in i] for i in file_lines[2:]]
        self.crates = []
        # get crates and replace the crate on the board with space.
        for i in range(self.height):
            for j in range(self.width):
                if self.grid[i][j] == CRATE:
                    self.crates.append((i, j))
                    self.grid[i][j] = SPACE
        # State Space Setup
        self.Head = State(self.start, self.crates, [])
        self.Active = self.Head
        # the endpoints for our crates, for ease of access
        self.frontier = [self.Head]
        self.explored = []
        self.targets = []
        for i in range(self.height):
            for j in range(self.width):
                if self.grid[i][j] == TARGET:
                    self.targets.append((i, j))
        self.Active.weight = self.cost()
        # A dead space checker to assist with finding fail states.
        self.dead_space = self.get_dead_space()
        return

    def get_dead_space(self):
        """
        A function that finds the spaces where it's impossible to get a crate
        to a target. This will be a bit complicated, but it'll only need to
        run once per target. The method We use here to find dead nodes is that
        we find corners which cannot automatically fail us. Then we trace lines
        between corners in the same row or column and if they share a line of
        walls between them then the entire line is a dead zone. If the target
        is there however we don't consider it a dead zone. We do this for each
        target and check each if it's a fail state.
        :return: A dict with an index for each target which has a list of dead
        spaces.
        """
        ret = {}
        # find the corners of the space.
        corners = []
        for i in range(self.height):
            for j in range(self.width):
                # if it's a wall we skip it.
                if self.grid[i][j] == WALL:
                    continue
                # if it's a space and has 2 non-opposing walls, it's a corner.
                if self.is_corner((i, j)):
                    corners.append((i, j))
        # loop over all the targets.
        for i in self.targets:
            ret[i] = self.singular_dead_space(i)
        return ret

    def singular_dead_space(self, target, corners):
        """
        Function to find deadspace for a single target.
        :param target: The target in question
        :param corners: The corners of the grid (precalculated)
        :return: a list of the dead squares.
        """
        ret = []
        for active in corners:
            for other in corners:
                # if either corner is a target skip it.
                if active == target or other == target:
                    continue
                # if active and the other is the same corner skip it.
                if active == other:
                    continue
                # if they are not in the same row or column skip it.
                if active[0] != other[0] and active[1] != other[0]:
                    continue
                # if there's a wall between them skip it.
                spaces = [i for i in self.get_spaces(active, other)]
                tiles = [self.grid[i[0]][i[1]] for i in spaces]
                if WALL in tiles:
                    continue
                # if the target between them, skip it.
                if target in spaces:
                    continue
                # check if there is a wall along the entire path.
                has_wall = False
                direction = ''
                if active[0] == other[0]:
                    direction = 'row'
                elif active[1] == [other[1]]:
                    direction = 'col'
                for space in spaces:
                    if direction == 'row':
                        adj = [(1, 0), (-1, 0)]
                    elif direction == 'col':
                        adj = [(0, 1), (0, -1)]
                    for curr in adj:
                        wall_check = [add_tuples(i, curr) for i in spaces]
                        # if the target isn't in the grid, then we certainly
                        # have a wall
                        if not self.in_grid(wall_check[0]):
                            has_wall = True
                            break
                        # run along and see if it has a wall.
                        for check in wall_check:
                            if check != WALL:
                                # if it doesn't set has_wall to false and
                                # break out of both loops.
                                break
                # if it has a wall then add it to the dead space.
                if has_wall:
                    for i in spaces:
                        if i not in ret:
                            ret.append(i)
        return ret

    def get_spaces(self, first, second):
        """
        A retrieval function to get the spaces in between 2 spaces (inclusive)
        if they are not in the same row it returns a smaller section of them.
        :param first:
        :param second:
        :return:
        """
        if first[0] < second[0]:
            row1, row2 = first[0], second[0]
        else:
            row1, row2 = second[0], first[0]
        if first[1] < second[1]:
            col1, col2 = first[1], second[1]
        else:
            col1, col2 = second[1], first[1]
        for i in range(row1, row2):
            for j in range(col1, col2):
                yield (i, j)
        return

    def is_corner(self, space):
        """
        An assistant fuction that states whether the given space is a corner or
        not.
        :param space: The space we are checking
        :return: True if it is a corner, false otherwise.
        """
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
            adj = self.get_target(direction, space)
            # if its in the grid, keep working.
            if self.in_grid(adj):
                # if a wall, it's false
                if self.grid[adj[0]][adj[1]] == WALL:
                    results[key] = False
            # if adj_point is outside of the grid, it's false.
            else:
                results[key] = False
        return not results['vertical'] or results['horizontal']

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

    def cost(self, state=None):
        """
        Gets the value cost of this state, the lower the closer it
        is to solved.
        :param state: The state we are getting the cost of.
        Defaults to self.Active
        :return: the value of the state, the lower the better. If it's a fail
        state it returns None, this state should be caught and thrown into the
        Explored set immediately.
        """
        if state is None:
            state = self.Active
        # get the distance from the crates to the nearest targets
        total = 0
        for i in state.crates:
            shortest = -1
            for j in self.targets:
                current = get_distance(i, j)
                if current < shortest or shortest < 0:
                    shortest = current
            # check that the current box is in a non-fail state
            # it's not frozen in a corner or stuck.
            if not self.crate_movable(i):
                # if it failed, multiply by an arbitrarily large number.
                # If it's on a target, then it won't matter as shortest will
                # be 0.
                print('Immovable Crate', i)
                shortest *= 10000
                if shortest == 0:
                    # if the crate is immovable, and on a target, then decrease
                    # it's value a bit more, to reward it. Such spaces are
                    # more valuable as it' gets the box out of the way of other
                    # boxes.
                    shortest = -2
            # weight the distance on the crates to targets more then actor to
            # crate to encourage moving boxes over moving itself.
            total += 3*shortest
        # add the distance between the actor and the nearest box, being
        # adjacent to the box is considered to be 0.
        total += (self.closest_box(state.crates, state)-1)
        # multiply it to add weight to the state and allow movement to a box or
        # movement of a box to be valued more.
        total *= 2
        # Get the distance traveled.
        total += state.step_count()
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
        # Add the current crate to the prev list, for later. TODO FIX ME
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
                elif adj in self.crates:
                    adj_crate = self.crate_movable(adj, prev)
                    results[key] = adj_crate
            # if adj_point is outside of the grid, it's false.
            else:
                results[key] = False
        # return both results if both are false then the box can't be moved.
        return results['vertical'] or results['horizontal']

    def output(self, file_name, start, end, state=None):
        if state is None:
            state = self.Active
        output = str(int((end - start) * 10 ** 6)) + '\n'
        output += str(state.step_count()) + '\n'
        for i in state.steps:
            output += i
        output += '\n'
        output += str(self.width) + ' '
        output += str(self.height) + '\n'
        output += str(state.actor[0]) + ' '
        output += str(state.actor[1]) + '\n'
        for i in range(self.height):
            for j in range(self.width):
                if (i, j) in state.crates:
                    output += CRATE
                else:
                    output += self.grid[i][j]
            output += '\n'

        with open("soln_" + file_name, 'w') as out:
            out.write(output)
        print(output)

    def show_grid(self):
        """
        A helper output function for debugging and optimization purposes.
        :return:
        """
        out = ""
        for i in range(self.height):
            for j in range(self.width):
                if (i, j) in self.Active.crates:
                    out += CRATE
                else:
                    out += self.grid[i][j]
            out += "\n"
        print(out)
        return out

    def check_soln(self, state=None):
        """
        A Solution Checker
        :param targets: The grid we are checking.
        :return: True if solved, False otherwise.
        """
        if state is None:
            state = self.Active
        for t in self.targets:
            if t not in state.crates:
                return False
        return True

    def get_target(self, direction, actor=None, state=None):
        """
        Relative direction getter for our position
        :param direction: the direction we want to go
        :param actor: the place we are starting our move from. if no location
        is given we use the actor of the state.
        :return: the target square.
        """
        if state is None:
            state = self.Active
        if actor is None:
            actor = state.actor
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

    def check_move(self, direction, start=None, state=None):
        """
        Checks if our move is valid or not.
        :param direction: the direction we want to move
        :param start: the point we are starting at.
        :return: We return True if the space we want to move
         to is empty (valid), we return CRATE if there's a crate to push and we
         can push the crate, otherwise we return False.
        """
        if state is None:
            state = self.Active
        if start is None:
            start = state.actor
        target = self.get_target(direction, start)
        # check if in the grid
        if not self.in_grid(target):
            return False
        # check for wall
        if self.grid[target[0]][target[1]] == WALL:
            return False
        # check for box and valid box move
        if target in state.crates:
            # if box in the way, check if we can move the box properly
            box_move = self.get_target(direction, target)
            # if box move in grid
            if not self.in_grid(box_move):
                return False
            # if wall or crate in the way.
            is_wall = self.grid[box_move[0]][box_move[1]] == WALL
            is_crate = box_move in state.crates
            if is_wall or is_crate:
                return False
            # return crate to mark it as a push.
            return CRATE
        # if no crate, no wall, and in grid, we're good.
        else:
            return True

    def move(self, direction, state=None):
        """
        A move function to do all the work of moving. Will move the actor,
        the crate (if valid as well), and create a new StateNode, and add it
        to our kids. If it is not a valid move it will put None in the kid that
        would've been made, marking that direction as invalid.
        :param direction: The direction we are trying to move.
        :param state: The state we are starting with.
        :return : Returns the state that the move would produce, if it's not a
        valid move then it returns None.
        """
        if state is None:
            state = self.Active
        # check if it's valid
        valid = self.check_move(direction, state=state)
        if not valid:
            return None
        # since it is, do it.
        # get stuff we'll need for the next state anyways.
        crates = state.crates[:]
        target = self.get_target(direction)
        # if theres' a box, move it.
        if valid == CRATE:
            box = self.get_target(direction, target)
            crates.remove(target)
            crates.append(box)
        # add our direction as our newest step.
        next_step = state.steps[:]
        next_step.append(direction)
        ret = State(target, crates, next_step)
        ret.weight = self.cost(ret)
        return ret

    def closest_box(self, crates, states=None):
        """
        Gets the distance between the actor and the nearest chest.
        :return: the distance between actor and nearest chest.
        """
        if states is None:
            states = self.Active
        actor = states.actor
        best = -1
        for i in crates:
            current = get_distance(actor, i)
            if best < 0 or best > current:
                best = current
        return best


class State:
    """
    State holds our neccissary data for a state.
    Actor is the player that can move.
    Crates are the positions of the crates in the grid.
    steps is the steps taken to get to the state.
    weight is the states cost via h(n)
    """
    def __init__(self, actor, crates, steps, weight=None):
        self.actor = actor
        self.crates = [crate for crate in crates]
        self.steps = steps
        self.weight = weight
        return

    def __eq__(self, other):
        if self.actor != other.actor:
            return False
        for i, j in zip(self.crates, other.crates):
            if i != j:
                return False
        # we skip steps, as the steps to get to a state doesn't
        # make that state meaningfully different. It also implies
        # we got to the state faster already. We also skip weight, as
        # getting to the same state via different methods will already be
        # caught.
        return True

    def step_count(self):
        return len(self.steps)


if __name__ == "__main__":
    test = Warehouse("Puzzle1.txt")
