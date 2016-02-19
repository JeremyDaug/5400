import math

class Grid:
    """
    A class that will simulate our grid, automatically fills itself out with data
    Includes a grid that we travel across, The size of that grid, the number of colors.
    """
    def __init__(self, our_size, num_colors, space):
        """
        Init Function
        :param space: The grid we are iterating over. MUST Be 2D square Array
        :return: Returns complete class.
        """
        # size of a side (grid must be square).
        self.size = our_size
        # number of colors.
        self.colors = num_colors
        # Copy our grid down quickly.
        self.space = [row[:] for row in space]
        # get our starting points
        self.starts = {}
        for rex in range(self.size):
            for Xal in range(self.size):
                # if not empty
                if not self.space[rex][Xal] == 'e':
                    # if first time
                    if self.space[rex][Xal] not in self.starts:
                        self.starts[self.space[rex][Xal]] = []
                    # add to starts.
                    self.starts[self.space[rex][Xal]].append((rex, Xal))

        # simulated graph made. GTFO

    def move_valid(self, startpoint, endpoint, currentColor, taken_data=None):
        """
        Move function for our graph, ensures proper movement.
        :param startpoint: The point(tuple) we are starting at,
        :param endpoint: The point(Tuple) we are attempting to move to.
        :param taken_data: Any nodes previously taken to ensure no backtracking or overlapping.
                           If No previous moves it will be an empty array. Should be list of Tuples.
        :return: If valid it returns the value of the space, If invalid it returns False.
        """
        if taken_data is None:
            taken_data = []

        # check for adjacency
        if not -1 <= ((startpoint[0]-endpoint[0])**2 + (startpoint[1]-endpoint[1])**2)**0.5 <= 1:
            return False
        # check for range
        elif not (-1 < startpoint[0] < self.size and -1 < startpoint[1] < self.size):
            return False
        elif not (-1 < endpoint[0] < self.size and -1 < endpoint[1] < self.size):
            return False
        # check if not already taken.

        end_color = self.space[endpoint[0]][endpoint[1]]

        if endpoint in taken_data:
            return False
        # if empty or same color
        elif end_color == 'e' or currentColor == end_color:
            return end_color
        # Color does not match, space not valid.
        else:
            return False

    @staticmethod
    def distance(p0, p1):
        """
        Helper function for measuring distance between 2 points, uses manhattan distance to keep numbers
        nicer.
        :param p0: First Point
        :param p1: Second Point
        :return: The distance between p0 and p1
        """
        return math.fabs(p0[0]-p1[0])+math.fabs(p0[1]-p1[1])

    def addpath(self, color, path_taken):
        """
        Updates the grid with a discovered path
        :param color: The color of the path
        :param path_taken: a list of spaces to change.
        :return: None
        """
        for X in path_taken:
            self.space[X[0]][X[1]] = color


class Node:
    """
    A quick tree to keep our paths straight, only includes the current space, current distance to end,
    the color, and it's parent. If it is the head then 'parent' DNE in value.

    'parent' in value should always either point to a node or None, if it doesn't exist problems may arise.
    """
    def __init__(self, value, children=None):
        if children is None:
            children = []

        self.value = value
        self.children = children
        if 'parent' not in self.value:
            self.value['parent'] = None
