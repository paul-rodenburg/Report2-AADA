import os
from point import ClusterPoint

class Dataset:
    """
    Contains input parameters n, d, epsilon, and min_pts
    as well as a list of ClusterPoints that is modified by DBScan
    """
    def __init__(self, n, d, epsilon, min_pts, points):
        self.n = n
        self.d = d
        self.epsilon = epsilon
        self.min_pts = min_pts
        self.cluster_points = points

    def print_output(self, c, assignment_nr):
        print("{}\n".format(assignment_nr))
        print("{} {} {}".format(self.n, self.d, c))
        for point in self.cluster_points:
            print(point)

    def write_output(self, c, path_out, assignment_nr):
        # create directory if not exists
        os.makedirs(os.path.dirname(path_out), exist_ok=True)

        with open(path_out, "w+") as f:
            f.write("{}\n".format(assignment_nr))
            f.write("{} {} {}\n".format(self.n, self.d, c))

            for point in self.cluster_points:
                f.write("{}\n".format(point))


    @staticmethod
    def read_input(file):
        """
        Parses the input file into a Dataset object

        :param file:    opened file object (or stdio)\\
        :return         a Dataset object for the input set
        """
        # read first line and split into list
        words = file.readline().split()

        # check whether first line contains correct nr. of parameters
        assert len(words) == 4

        n, d, epsilon, min_pts = int(words[0]), int(words[1]), float(words[2]), int(words[3])
        points = []

        # Read n points
        for _ in range(n):
            words = file.readline().split()

            # check whether input line contains exactly d coordinates
            assert len(words) == d

            # Read d coords
            coords = [float(word) for word in words]

            # Add point to array
            points.append(ClusterPoint(d, coords))

        return Dataset(n, d, epsilon, min_pts, points)