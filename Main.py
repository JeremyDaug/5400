"""
The main file of our puzzle solver.
"""

from Puzzle3 import Warehouse
from Puzzle3.Warehouse import UP, DOWN, LEFT, RIGHT
from time import time
import sys
start = time()


def main(argv):
    """
    The Algorithm for Greedy Best-First Graph Search
    :param argv:
    :return:
    """
    if len(argv) < 2:
        print("You need to input a single file.")
        return
    file_name = str(argv[1])

    # prerun setup.
    Puzzle = Warehouse.Warehouse(file_name)

    # a frontier that we'll explore. FILO.
    frontier = [Puzzle.Head]
    solved = False
    dirs = [UP, DOWN, LEFT, RIGHT]
    # Set our max steps to start at 2 and increment for every major loop
    # we can start at 2 rather than 0 or 1. If a box is 1 move from completion
    # it will take at least 2 (wasted) moves to find a less efficient path.
    max_step = 2
    while not solved:
        Puzzle.Active = frontier.pop()
        # if our current step is at the max distance, then get the next
        # frontier node as we already have
        if Puzzle.Active.step_count() <= max_step:
            # run through the directions
            for i in dirs:
                # get the next state
                temp_state = Puzzle.move(i)
                # If the move succeded (returned not None) do more.
                if temp_state is not None:
                    # check if it's a solution
                    if temp_state.check_soln(Puzzle.targets):
                        # if its a solution wrap up and break out
                        solved = True
                        Puzzle.Active = temp_state
                        break
                    else:
                        # if it isn't add it to the frontier and move on
                        frontier.append(temp_state)
        elif frontier:
            # if we are over the max_step line, but we have more nodes, simply
            # restart the loop
            continue
        elif max_step <= Puzzle.Head.height*Puzzle.Head.width*2:
            # since we have no frontier and our max_step has yet to hit
            # our hard limit, restart and increase max_steps
            # We set our hard limit at 2*the grid size as beyond that point
            # it's questionable if there is an answer.

            # Bump up our max step
            max_step += 1
            # reset the frontier
            frontier.append(Puzzle.Head)
        else:
            # finally if our max step is larger then our hard limit,
            # then stop running and output our failure.
            print("Uh Oh, we couldn't find an answer.")

    end = time()
    if solved:
        Puzzle.Active.output(file_name, start, end)

if __name__ == '__main__':
    main(sys.argv)
