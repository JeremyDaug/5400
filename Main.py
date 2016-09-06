"""
The main file of our puzzle solver.
"""

from Puzzle2 import Warehouse
from Puzzle2.Warehouse import UP, DOWN, LEFT, RIGHT
import datetime
import sys
start = datetime.datetime.now()


def main(argv):
    file_name = str(argv[1])

    # prerun setup.
    Puzzle = Warehouse.Warehouse(file_name)

    # a frontier that we'll explore. FIFO.
    frontier = [Puzzle.Head]

    solved = False
    step = 0
    while not solved:
        Puzzle.Active = frontier.pop(0)
        dirs = [UP, DOWN, LEFT, RIGHT]
        end_dirs = {UP: None, DOWN: None, LEFT: None, RIGHT: None}
        # run through the directions
        for i in dirs:
            # do the move (if possible)
            end_dirs[i] = Puzzle.move(i)
            # If the move succeded (returned not None) do more.
            if end_dirs[i] is not None:
                # check if it's a solution
                if Puzzle.check_soln(end_dirs[i].grid):
                    # if it wrap up and break out
                    solved = i
                    Puzzle.Active = end_dirs[i]
                    break
                else:
                    # if it isn't add it to the frontier and move on
                    frontier.append(end_dirs[i])

    end = datetime.datetime.now()
    if solved:
        output = str((end-start).microseconds) + '\n'
        output += str(Puzzle.Active.step_count) + '\n'
        for i in Puzzle.Active.steps:
            output += i
        output += '\n'
        output += str(Puzzle.Active.width) + ' ' + \
            str(Puzzle.Active.height) + '\n'
        output += str(Puzzle.Active.actor[0]) + ' ' + \
            str(Puzzle.Active.actor[1]) + '\n'
        for i in Puzzle.Active.grid:
            for j in i:
                output += j
            output += '\n'

        with open("soln_"+file_name, 'w') as out:
            out.write(output)

    print('WE DID IT I THINK!')

if __name__ == '__main__':
    main(sys.argv)
