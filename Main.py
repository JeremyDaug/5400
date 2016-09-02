"""
The main file of our puzzle solver.
"""

from Puzzle1 import Warehouse
import Tree


file_name = "Puzzle1.txt"

# prerun setup.
start_point = Warehouse.Warehouse(file_name)
states = Tree.Tree()
states.Head.data = Warehouse.State(start_point.height,
                                   start_point.width,
                                   start_point.start,
                                   start_point.grid,
                                   [])
# helper vars since these will probably be used alot.
U = 'U'
D = 'D'
L = 'L'
R = 'R'

# a frontier that we'll explore. FIFO.
Frontier = [states.Head]

if __name__ == '__main__':
    solved = False
    while not solved:
        states.Active = Frontier.pop(0)
        # up
        Up = states.Active.data.move(U, start_point.targets)
        if Up is not None:
            states.add(U, Up)
            if start_point.check_soln(Up.grid):
                states.Active = states.Active.kids[U]
                solved = 'U'
            else:
                Frontier.append(states.Active.kids[U])
        # down
        Down = states.Active.data.move(D, start_point.targets)
        if Down is not None:
            states.add(D, Down)
            if start_point.check_soln(Down.grid):
                states.Active = states.Active.kids[D]
                solved = 'D'
            else:
                Frontier.append(states.Active.kids[D])
        # left
        Left = states.Active.data.move(L, start_point.targets)
        if Left is not None:
            states.add(L, Left)
            if start_point.check_soln(Left.grid):
                states.Active = states.Active.kids[L]
                solved = 'L'
            else:
                Frontier.append(states.Active.kids[L])
        # right
        Right = states.Active.data.move(R, start_point.targets)
        if Right is not None:
            states.add(R, Right)
            if start_point.check_soln(Right.grid):
                states.Active = states.Active.kids[R]
                solved = 'R'
            else:
                Frontier.append(states.Active.kids[R])

    print('WE DID IT I THINK!')
