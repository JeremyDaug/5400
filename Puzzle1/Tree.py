"""
A class for our tree.
"""


class Node:
    def __init__(self, data=None, parent=None):
        self.data = data
        self.parent = parent
        self.children = dict()


class Tree:
    def __init__(self):
        self.tree = Node('')
