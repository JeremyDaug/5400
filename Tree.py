"""
A class for our tree.
"""


class Node:
    def __init__(self, data=None, parent=None):
        self.data = data
        self.parent = parent
        self.children = dict()
        return

    def find(self, steps=list()):
        """
        Find function that looks for the data at the end of the list
        :param steps: a list of the steps it wasnts us to take. If it's
         empty then the list is at its end and we're done
        :return: If our steps are empty we return the node's data, if not the
         children's data. If the child doesn't exist we return None.
        """
        # if the list is empty, return our current data we are at the
        # end of our list
        if not steps:
            return self.data
        # if it is a child pop down into it and keep looking
        if steps[0] in self.children:
            return self.children[steps[0]].find(steps[1:])
        # if that child doesn't exist, return None
        return None

    def find_node(self, steps=list()):
        """
        finds and returns a node
        :param steps: The steps to reach the node.
        :return: The node we are looking for or None if we can't find it.
        """
        # if the list is empty, return ourself as we are what they are looking
        # for.
        if not steps:
            return self
        # if it is a child pop down into it and keep looking
        if steps[0] in self.children:
            return self.children[steps[0]].find(steps[1:])
        # if that child doesn't exist, return None
        return None

    def create_child(self, name=None, data=None):
        """
        Create a child for the node.
        :param name: The name we are putting it under.
        :param data: The data in the child.
        """
        if name is None:
            raise Exception('The child needs a NAME!')
        self.children[name] = Node(data, self)
        return

    def find_yourself(self):
        """
        A function to find how to find yourself from your parent.
        :return: The key to get from our parent to ourself.
        """
        for key in self.parent.children:
            if self.parent.children[key] is self:
                return key
        raise Exception('Something went wrong, our parent doesn\'t point to us'
                        '.')

    def get_steps(self):
        """
        Reverse pather for our nodes.
        :return: Returns a list of all the steps we took to get to this node.
        If there is a no parent return an empty list.
        """
        ret = []
        # if we have a parent and they are a node
        if self.parent is not None and isinstance(self.parent, Node):
            # have them get the steps to themselves and put that in our steps
            ret.extend(self.parent.get_steps())
            # then get the step to ourself.
            ret.append(self.find_yourself())
        elif not isinstance(self.parent, Node) and self.parent is not None:
            raise Exception('We have a problem, our parent isn\'t a node.')
        return ret


class Tree:
    def __init__(self):
        # the head of the tree, it should never change.
        self.Head = Node('')
        # the node we are looking at right now. Always change this.
        self.Active = self.Head
        return

    def find(self, steps=list()):
        """
        Finds the data of a node.
        :param steps: the steps we want to take in list form.
        :return: the data in the node. If the node doesn't exist it
        returns None.
        """
        if not steps:
            raise Exception('Need steps to find something.')
        return self.Head.find(steps)

    def change_node(self, steps=list()):
        if not steps:
            raise Exception('Need steps to find something.')
        self.Active = self.Head
        return


# tester main for this. Just to be sure this works.
if __name__ == '__main__':
    testNode = Node('head')
    testNode.create_child('kid')
    testKid = testNode.children['kid']
    print(testNode.find_yourself())
    print(testKid.find_)
    testTree = Tree()
