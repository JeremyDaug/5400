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
    master_head = Grid.Node({'parent': None,
                             'curr': None,
                             'color': '',
                             'dist': 0
                             })

    # Start looping through the colors, closest colors first.
    done = False
    while not done:
        # Put our starting points in our
        movestaken = []
        for i in Space.starts:
            # put our starting points in the frontier.
            master_head.children.append(Grid.Node({'parent': None,
                                                   'curr': Space.starts[i][0],
                                                   'color': i,
                                                   'dist': Space.distance(Space.starts[i][0],Space.starts[i][1])}))
            frontier.append(master_head.children[-1])
            movestaken.append(Space.starts[i])

        Path = None
        while Path is None:
            # Get the current closest point in frontier.
            closest2 = (1000000000, 0)
            for i in range(len(frontier)):
                print('steps taken', frontier[i].node_depth())
                if (frontier[i].value['dist']+frontier[i].node_depth()) < closest2[0] and \
                        frontier[i].value['color'] not in ColorsFinished:
                    closest2 = (frontier[i].value['dist'], i)
                # print('Frontier', frontier[i].value['curr'], frontier[i].value['dist'])
                print('closest', closest2[0], frontier[closest2[1]].value['curr'])

            # we now have our current space.
            curr = frontier.pop(closest2[1])
            currentcolor = curr.value['color']

            # add our current space to the list of moves taken preemptively.
            movestaken.append(curr.value['curr'])

            # get the location of our start spot for later use.
            start = curr.value['curr']

            # Up
            end = (curr.value['curr'][0]-1, curr.value['curr'][1])
            # print("start and end", start, end)
            if Path is None:
                print('up')
                Path = Space.complete_action( curr, end, currentcolor, movestaken, frontier)

            # right
            end = (curr.value['curr'][0], curr.value['curr'][1]+1)
            # print("start and end", start, end)
            if Path is None:
                print('right')
                Path = Space.complete_action( curr, end, currentcolor, movestaken, frontier)

            # down
            end = (curr.value['curr'][0]+1, curr.value['curr'][1])
            # print("start and end", start, end)
            if Path is None:
                print('down')
                Path = Space.complete_action( curr, end, currentcolor, movestaken, frontier)

            # left
            end = (curr.value['curr'][0], curr.value['curr'][1]-1)
            # print("start and end", start, end)
            if Path is None:
                print('left')
                Path = Space.complete_action( curr, end, currentcolor, movestaken, frontier)

            # if there is nothing in the frontier and path hasn't been found, break and get ready to clear
            # this color.
            if not frontier:
                Path = None

            for i in Space.space:
                for j in i:
                    print(j, end=' ')
                print('')

            # if we found a path, we'll break from the loop to work with that path.

        # Path found, lets add it to the current grid. Finishing the While loop will get us a new color.
        if Path:
            ColorsFinished.append(currentcolor)
            backtrack = []
            Back = Path
            while Back.value['parent'] is not None:
                backtrack.append(Back.value['curr'])
                Back = Back.value['parent']
            backtrack.append(Back.value['curr'])
            Space.add_path(currentcolor, backtrack)
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
