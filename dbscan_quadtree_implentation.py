import time
import sys
from point import Point, ClusterPoint
from square import Square
from node import Node
from db_scan import *
from dataset import *
from range_query import RangeQuery


def _subtree_count(node):
    if not node.children:
        return 1 if node.point is not None else 0
    count = 0
    for child in node.children:
        count += _subtree_count(child)
    return count



class QuadTree(RangeQuery):
    """
    Implementation of RangeQuery using a QuadTree
    """

    def __init__(self, points):
        self.points = points


        # compute bounding square
        boundary = Square.get_bounding_square(points)
        # create root node
        root_node = Node(parent=None, size=0, square=boundary, children=[])
        # recursive insert
        def insert(node, p):
            if not node.square.contains_point(p):
                return False
            if not node.children:
                if node.point is None:
                    node.set_point(p)
                    return True
                # leaf with point: subdivide
                subsq = node.square.splice_square()
                for sq in subsq:
                    node.add_child(Node(parent=node, size=0, square=sq, children=[]))
                old = node.point
                node.set_point(None)
                insert(node, old)
                return insert(node, p)
            # internal node
            for child in node.children:
                if child.square.contains_point(p):
                    return insert(child, p)
            return False
        # insert all provided points
        for pt in points:
            insert(root_node, pt)

        self.root_node = root_node

    def report_range(self, p, epsilon):
        """
        Returns the points that lie within range epsilon from p
        """

        neighbors = []

        eps2 = epsilon ** 2
        def recurse(node):
            # prune if square too far
            if not node.square.overlaps_with_circle(p, epsilon):
                return
            if not node.children:
                if node.point is not None and p.sq_distance_to(node.point) <= eps2:
                    neighbors.append(node.point)
            else:
                for c in node.children:
                    recurse(c)
        recurse(self.root_node)

        return neighbors

    def count_range(self, p, epsilon):
        """
        Returns the number of points that lie within range epsilon from p
        """

        count = 0

        eps2 = epsilon ** 2
        def recurse_count(node):
            # fully inside circle
            if node.square.is_contained_in_circle(p, epsilon):
                return _subtree_count(node)
            # no overlap
            if not node.square.overlaps_with_circle(p, epsilon):
                return 0
            # leaf
            if not node.children:
                return 1 if (node.point is not None and p.sq_distance_to(node.point) <= eps2) else 0
            # internal
            total = 0
            for c in node.children:
                total += recurse_count(c)
            return total
        count = recurse_count(self.root_node)

        return count

    def delete_point(self, point):
        """
        Deletes point from this quad tree
        """

        def recurse_del(node):
            if not node.square.contains_point(point):
                return False
            if not node.children:
                if node.point is not None and node.point == point:
                    node.set_point(None)
                    return True
                return False
            for c in node.children:
                if recurse_del(c):
                    return True
            return False
        recurse_del(self.root_node)
