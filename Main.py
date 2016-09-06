"""
The main file of our puzzle solver.
"""

from Puzzle1 import Warehouse
import Tree
import datetime
import timeit
import sys
start = datetime.datetime.now()


def main(argv):
    file_name = str(argv[1])

    # prerun setup.
    start_point = Warehouse.Warehouse(file_name)
    states = Tree.Tree()
    states.Head.data = Warehouse.State(start_point.height,
                                       start_point.width,
                                       start_point.start,
                                       start_point.grid,
                                       [])
    # helper vars since these will probably be used alot.
    up_dir = 'U'
    down_dir = 'D'
    left_dir = 'L'
    right_dir = 'R'

    # a frontier that we'll explore. FIFO.
    frontier = [states.Head]

    solved = False
    step = 0
    while not solved:
        states.Active = frontier.pop(0)
        # up
        Up = states.Active.data.move(up_dir, start_point.targets)
        if Up is not None:
            states.add(up_dir, Up)
            if start_point.check_soln(Up.grid):
                states.Active = states.Active.kids[up_dir]
                solved = up_dir
            else:
                frontier.append(states.Active.kids[up_dir])
        # down
        Down = states.Active.data.move(down_dir, start_point.targets)
        if Down is not None:
            states.add(down_dir, Down)
            if start_point.check_soln(Down.grid):
                states.Active = states.Active.kids[down_dir]
                solved = down_dir
            else:
                frontier.append(states.Active.kids[down_dir])
        # left
        Left = states.Active.data.move(left_dir, start_point.targets)
        if Left is not None:
            states.add(left_dir, Left)
            if start_point.check_soln(Left.grid):
                states.Active = states.Active.kids[left_dir]
                solved = left_dir
            else:
                frontier.append(states.Active.kids[left_dir])
        # right
        Right = states.Active.data.move(right_dir, start_point.targets)
        if Right is not None:
            step += 1
            states.add(right_dir, Right)
            if start_point.check_soln(Right.grid):
                states.Active = states.Active.kids[right_dir]
                solved = right_dir
            else:
                frontier.append(states.Active.kids[right_dir])

    end = datetime.datetime.now()
    if solved:
        output = str((end-start).microseconds) + '\n'
        output += str(states.Active.data.path_length()) + '\n'
        for i in states.Active.data.steps:
            output += i
        output += '\n'
        output += str(states.Active.data.width) + ' ' + \
            str(states.Active.data.height) + '\n'
        output += str(states.Active.data.actor[0]) + ' ' + \
            str(states.Active.data.actor[1]) + '\n'
        for i in states.Active.data.grid:
            for j in i:
                output += j
            output += '\n'

        with open("soln_"+file_name, 'w') as out:
            out.write(output)

    print('WE DID IT I THINK!')

if __name__ == '__main__':
    main(sys.argv)
