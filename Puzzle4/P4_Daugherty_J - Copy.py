# Color Connect Puzzle 3
# Jeremy Daughrety
# Greedy Best-first Graph Search

# Get our imports
import Grid
import sys
import datetime
start_time = datetime.datetime.now()  # start our time for runtime

# Get our data for the AI.
if len(sys.argv) < 1:  # if an argument has been given.
    filename = sys.argv[-1]  # get the .txt which has the puzzle.
    F = open(filename)  # open it as a read only.
else:  # if no file argument given go to the puzzle.txt
    F = open('puzzle.txt')  # for non-commandline file input.

# Read the data from the file
raw = F.read()
raw1 = []
raw1.extend(raw.split(' '))  # strip whitespace
raw2 = []
for i in raw1:
    raw2.extend(i.split('\n'))  # strip endlines


# store our data
size = int(raw2.pop(0))  # get size
colors = int(raw2.pop(0))  # get number of colors
grid = []  # initialize our grid
for i in range(size):
    grid.append([])
    for j in range(size):
        grid[i].append(raw2.pop(0))

Space = Grid.Grid(size, colors, grid)


# begin running through our program.
if __name__ == '__main__':
    # finished nodes that we have no need for anymore.
    finished = []
    # Final Track of our current paths.
    FinalTrack = {}
    # the Frontier of nodes we are working with.
    frontier = []
    # Holds the list of finished Colors.
    ColorsFinished = []
    # Head to start with, will change with to the color we are working on at the time.
    Head = Grid.Node({'parent': None,
                      'curr': None,
                      'color': '',
                      'dist': 0
                      })

    # Start looping through the colors, closest colors first.
    done = False
    while not done:
        # look for the first color
        closest = (10000000, '')  # tuple is effectively a placeholder
        for i in Space.starts:
            curr = Space.distance(Space.starts[i][0], Space.starts[i][1])
            if curr < closest[0] and i not in ColorsFinished:

                closest = (curr, i)

        # get a copy of our current color for later and move on.
        currentcolor = closest[1]

        # if there is no closest get out cause we're done.
        if closest[1] == '':
            break

        # We have the color with the shortest distance, let's put it in as the head, add to frontier,
        #  and get 'xplorin'.
        Head.value['dist'] = closest[0]
        Head.value['curr'] = Space.starts[currentcolor][0]
        Head.value['color'] = currentcolor
        frontier.append(Head)

        movestaken = []

        Path = False
        while not Path:
            # Get the current closest point in frontier.
            closest2 = (1000000000, 0)
            for i in range(len(frontier)):
                if frontier[i].value['dist'] < closest2[0]:
                    closest2 = (frontier[i].value['dist'], i)
                # print('Frontier', frontier[i].value['curr'], frontier[i].value['dist'])

            # we now have our current space.
            curr = frontier.pop(closest2[1])

            # add our current space to the list of moves taken preemptively.
            movestaken.append(curr.value['curr'])

            # get the location of our start spot for later use.
            start = curr.value['curr']

            # Up
            end = (curr.value['curr'][0]-1, curr.value['curr'][1])
            action = Space.move_valid(start, end, currentcolor, movestaken)

            # if action is valid, and no path has been found, # movevalid checks if the space is not been touched yet.
            if (action == currentcolor or action == 'e') and not Path:

                curr.children.append(Grid.Node(value={'dist': Space.distance(end, Space.starts[currentcolor][1]),
                                                      'curr': end,
                                                      'color': currentcolor,
                                                      'parent': curr
                                                      }))
                frontier.append(curr.children[-1])
                movestaken.append(end)

                # if current color is an appropriate end point
                if Space.starts[currentcolor][1] == end:
                    # add our color to completed colors section preemptively since we found a path.
                    ColorsFinished.append(currentcolor)
                    # The Node we want is put into path to make it read true.
                    Path = frontier[-1]

            # right
            end = (curr.value['curr'][0], curr.value['curr'][1]+1)
            action = Space.move_valid(start, end, currentcolor, movestaken)

            # if action is valid, and no path has been found, # movevalid checks if the space is not been touched yet.
            if (action == currentcolor or action == 'e') and not Path:

                curr.children.append(Grid.Node(value={'dist': Space.distance(end, Space.starts[currentcolor][1]),
                                                      'curr': end,
                                                      'color': currentcolor,
                                                      'parent': curr
                                                      }))
                frontier.append(curr.children[-1])
                movestaken.append(end)

                # if current color is an appropriate end point
                if Space.starts[currentcolor][1] == end:
                    # add our color to completed colors section preemptively since we found a path.
                    ColorsFinished.append(currentcolor)
                    # The Node we want is put into path to make it read true.
                    Path = frontier[-1]

            # down
            end = (curr.value['curr'][0]+1, curr.value['curr'][1])
            action = Space.move_valid(start, end, currentcolor, movestaken)

            # if action is valid, and no path has been found, # movevalid checks if the space is not been touched yet.
            if (action == currentcolor or action == 'e') and not Path:

                curr.children.append(Grid.Node(value={'dist': Space.distance(end, Space.starts[currentcolor][1]),
                                                      'curr': end,
                                                      'color': currentcolor,
                                                      'parent': curr
                                                      }))
                frontier.append(curr.children[-1])
                movestaken.append(end)

                # if current color is an appropriate end point
                if Space.starts[currentcolor][1] == end:
                    # add our color to completed colors section preemptively since we found a path.
                    ColorsFinished.append(currentcolor)
                    # The Node we want is put into path to make it read true.
                    Path = frontier[-1]

            # left
            end = (curr.value['curr'][0], curr.value['curr'][1]-1)
            action = Space.move_valid(start, end, currentcolor, movestaken)

            # if action is valid, and no path has been found, move_valid checks if the space is not been touched yet.
            if (action == currentcolor or action == 'e') and not Path:

                curr.children.append(Grid.Node(value={'dist': Space.distance(end, Space.starts[currentcolor][1]),
                                                      'curr': end,
                                                      'color': currentcolor,
                                                      'parent': curr
                                                      }))
                frontier.append(curr.children[-1])
                movestaken.append(end)

                # if current color is an appropriate end point
                if Space.starts[currentcolor][1] == end:
                    # add our color to completed colors section preemptively since we found a path.
                    ColorsFinished.append(currentcolor)
                    # The Node we want is put into path to make it read true.
                    Path = frontier[-1]

            # if there is nothing in the frontier and path hasn't been found, break and get ready to clear
            # this color.
            if not frontier:
                Path = None

            # if we found a path, we'll break from the loop to work with that path.

        # Path found, lets add it to the current grid. Finishing the While loop will get us a new color.
        if Path:
            backtrack = []
            Back = Path
            while Back.value['parent'] is not None:
                backtrack.append(Back.value['curr'])
                Back = Back.value['parent']
            backtrack.append(Back.value['curr'])
            Space.addpath(currentcolor, backtrack)
            Path = False
            frontier = []
            FinalTrack[currentcolor] = backtrack
        elif Path is None:
            ColorsFinished.append(currentcolor)

        # we have finished our path check if there are any more.
        done = True
        for i in Space.starts:
            if i not in ColorsFinished:
                done = False

    # print our data to the console
    end_time = datetime.datetime.now()
    run_time = end_time - start_time
    print("%d " % run_time.microseconds)

    Temp = 0
    for i in FinalTrack:
        Temp += len(FinalTrack[i])

    print('%d' % Temp)
    for i in FinalTrack:
        for j in FinalTrack[i]:
            print(i, j[1], j[0], ',', end=' ')
    print(' ')
    for i in Space.space:
        for j in i:
            print(j, end=' ')
        print('')

    with open('solution.txt', 'w') as F:

        end_time = datetime.datetime.now()
        run_time = end_time - start_time
        F.write("%d \n" % run_time.microseconds)

        Temp = 0
        for i in FinalTrack:
            Temp += len(FinalTrack[i])

        F.write('%d\n' % Temp)
        for i in FinalTrack:
            for j in FinalTrack[i]:
                F.write('%s %d %d,' % (i, j[1], j[0]))
        F.write('\n')
        for i in Space.space:
            for j in i:
                F.write('%s ' % j)
            F.write('\n')
