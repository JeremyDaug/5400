"""
The main file of our puzzle solver.
"""

from Puzzle4 import Warehouse
from Puzzle4.Warehouse import UP, DOWN, LEFT, RIGHT
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

    # A flag to yell if we've solved our problem.
    solved = False
    dirs = [UP, DOWN, LEFT, RIGHT]

    while not solved:
        # find the best option from the frontier.
        Puzzle.Active = Puzzle.get_best()
        # if the steps are higher then our hard_max, then move on.
        # print(Puzzle.Active.steps)
        # check if our current state is the goal
        if Puzzle.check_soln():
            # if it is, mark it and break out of this popsicle stand.
            solved = True
            break
        else:
            Puzzle.show_grid()
        # if it's not, then put it in the explored set
        Puzzle.explored.append(Puzzle.Active)
        # run through all the directions it
        # could go and add them to the frontier.
        for i in dirs:
            # get the next state
            temp_state = Puzzle.move(i)
            # If the move succeded (returned not None) do more.
            if temp_state is not None:
                # If it's not an explored state, add it to the frontier.
                if temp_state not in Puzzle.explored:
                    Puzzle.frontier.append(temp_state)
                    # if it's in the explored do nothing and keep going on.

    end = time()
    if solved:
        Puzzle.output(file_name, start, end)

if __name__ == '__main__':
    main(sys.argv)
