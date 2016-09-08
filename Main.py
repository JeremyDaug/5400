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

    # a frontier that we'll explore. FILO.
    frontier = [Puzzle.Head]

    solved = False
    # Set our max steps to start at 0 and increment for every major loop
    max_step = 0
    while not solved:
        Puzzle.Active = frontier.pop(len(frontier)-1)
        dirs = [UP, DOWN, LEFT, RIGHT]
        end_dirs = {UP: None, DOWN: None, LEFT: None, RIGHT: None}
        # if our current step is at the max distance, then get the next
        # frontier node as we already have
        if Puzzle.Active.step_count <= max_step:
            # run through the directions
            for i in dirs:
                # if it already exists in the tree, don't move again,
                #  save space
                if i in Puzzle.Active.kids.keys():
                    end_dirs[i] = Puzzle.Active.kids[i]
                else:
                    # if it doesn't exist do the move.
                    end_dirs[i] = Puzzle.move(i)
                    # If the move succeded (returned not None) do more.
                if end_dirs[i] is not None:
                    # check if it's a solution
                    if end_dirs[i].check_soln(Puzzle.targets):
                        # if it wrap up and break out
                        solved = i
                        Puzzle.Active = end_dirs[i]
                        break
                    else:
                        # if it isn't add it to the frontier and move on
                        frontier.append(end_dirs[i])
        height = Puzzle.Head.height
        width = Puzzle.Head.width
        # if the frontier has emptied and we are below the max steps
        # we put an absolute maximum on it equivalent to stepping across the
        # entire grid twice for the worst case scenario where it can't find an
        # end
        if frontier:
            pass  # if we have a frontier, simply move on.
        elif not frontier and height*width*2 > max_step:
            # reset our Active pointer
            Puzzle.back_to_head()
            # Bump up our max step
            max_step += 1
            print(max_step)
            # reset the frontier
            frontier.append(Puzzle.Head)
        # if empty and at the end.
        elif not frontier and height*width*2 == max_step:
            print("Uh Oh, we couldn't find an answer.")

    end = datetime.datetime.now()
    if solved:
        Puzzle.Active.sutput(file_name, start, end)
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

if __name__ == '__main__':
    main(sys.argv)
