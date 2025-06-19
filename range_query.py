from abc import ABC, abstractmethod


class RangeQuery(ABC):
    """
    Abstract class representing the range query functionality
    Both methods need to be implemented when inheriting
    """
    @abstractmethod
    def report_range(self, p, epsilon):
        pass

    @abstractmethod
    def count_range(self, p, epsilon):
        pass
    
    @abstractmethod
    def delete_point(self, point):
        pass


class LinearQuery(RangeQuery):
    """
    Range query with time complexity O(n) where n is the number of points
    To find the neighbors of a point it compares the distances of all other points
    and adds those with distance smaller than or equal to epsilon to a list.
    """
    def __init__(self, points):
        self.points = points

    def report_range(self, p, epsilon):
        return [point for point in self.points if p.sq_distance_to(point) < epsilon ** point.dimension]

    def count_range(self, p, epsilon):
        return len(self.report_range(p, epsilon))        

    def delete_point(self, point):
        self.points.remove(point)
