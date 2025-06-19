from point import Point

class Square:
    """
    This object represents an square that is aligned with the x-axis and y-axis.
    """

    def __init__(self, top, bottom, left, right):
        self.top = top
        self.bottom = bottom
        self.left = left
        self.right = right

    @staticmethod
    def get_bounding_square(points: "list of points") -> "Square":
        """
        Creates a square bounding the set of points with 1 wiggle room.
        """
        return Square(
            max(points, key=lambda x: x.coords[1]).coords[1] + 1, #top
            min(points, key=lambda x: x.coords[1]).coords[1] - 1, #bottom
            min(points, key=lambda x: x.coords[0]).coords[0] - 1, #left
            max(points, key=lambda x: x.coords[0]).coords[0] + 1  #right
        )

    def splice_square(self) -> "list of squares":
        """
        Returns a list of its four smaller equally sized subsquares
        """
        horizontal = (self.top + self.bottom) / 2
        vertical = (self.left + self.right) / 2
        return [
            Square(self.top, horizontal, self.left, vertical), # Top left
            Square(self.top, horizontal, vertical, self.right), # Top right
            Square(horizontal, self.bottom, self.left, vertical), # Bottom left
            Square(horizontal, self.bottom, vertical, self.right) # Bottom right
        ]

    def contains_point(self, point: Point) -> bool:
        """
        Returns whether `point` lies within the bounds of this square\\
        Note: the bottom and left border of the square are included, whereas the top and right border are excluded.
        """
        return self.left <= point.coords[0] and \
                point.coords[0] < self.right and \
                self.bottom <= point.coords[1] and \
                point.coords[1] < self.top

    def is_contained_in_circle(self, center: Point, radius: float) -> bool:
        """
        Returns whether this square is completely inside the circle with given center and radius.
        """
        result = True
        for b in self.vertex_circle_overlap(center, radius):
            result &= b
        return result

    def vertex_circle_overlap(self, center: Point, radius: float) -> "list of bool":
        """
        Returns a list of booleans stating with which vertices of this square the circle coincides.\\
        Starting with the top left corner and progressing in clockwise fashion.
        """
        radsqr = radius**2
        return [
            center.sq_distance_to(Point(2, [self.left, self.top])) <= radsqr,
            center.sq_distance_to(Point(2, [self.right, self.top])) <= radsqr,
            center.sq_distance_to(Point(2, [self.right, self.bottom])) <= radsqr,         
            center.sq_distance_to(Point(2, [self.left, self.bottom])) <= radsqr
        ]

    def circle_overlaps_vertex(self, center: Point, radius: float) -> bool:
        """
        Returns whether the circle originating in center overlaps with
        at least one vertex of this square.
        """
        result = False
        for b in self.vertex_circle_overlap(center, radius):
            result |= b
        return result

    def overlaps_with_circle(self, center: Point, radius: float) -> bool:
        """
        Returns whether circle overlaps with square.
        """
        # Circle too far away
        if center.coords[1] + radius < self.bottom:
            return False
        elif self.top + radius <= center.coords[1]:
            return False
        elif center.coords[0] + radius < self.left:
            return False
        elif self.right + radius <= center.coords[0]:
            return False

        # So, point is now potentially within range
        if self.bottom <= center.coords[1] and center.coords[1] < self.top:
            return True
        elif self.left <= center.coords[0] and center.coords[0] < self.right:
            return True
        
        # Last corner case:
        return self.circle_overlaps_vertex(center, radius)
