class Node():
    """
    Object that represents a node in a QuadTree
    """

    def __init__(self, parent, size, square, children):
        self.parent = parent
        self.size = size
        self.square = square
        self.children = children    
        self.point = None        

    def add_child(self, child):
        self.children.append(child)

    def set_point(self, point):
        self.point = point