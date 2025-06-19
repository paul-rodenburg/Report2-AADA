def find_clustering(points, epsilon, min_pts, query_object):
    """
    For every point in our dataset we find the set of it's neighbors N
    A neighbor is a point with distance smaller than or equal to epsilon
    If | N | < minPts it is not a core point and we move to the next point

    :param points       array of all points
    :param epsilon      epsilon as specified in lecture notes
    :param min_pts      minPts as specified in lecture notes
    :param query_object RangeQuery object used to find neighbours
    :return             number of clusters found
    """

    # Step 1: find all core points
    core_points = []
    for point in points:
        nr_neighbors = query_object.count_range(point, epsilon)
        if nr_neighbors < min_pts:
            point.cluster_label = 0
        else:
            core_points.append(point)

    # Step 2: remove all noise points from the quad tree
    for point in points:
        if point.is_labeled():
            query_object.delete_point(point)
    
    # Step 3: create clusters
    cluster_counter = 1
    for point in core_points:

        # Skip points that are already labeled
        if point.is_labeled():
            continue

        # New cluster:
        stack = [point]
        query_object.delete_point(point)

        while stack:
            cluster_point = stack.pop()
            cluster_point.cluster_label = cluster_counter            

            # Add neighbors to stack
            neighbors = query_object.report_range(cluster_point, epsilon)
            stack += neighbors
            for neighbor in neighbors:
                query_object.delete_point(neighbor)

        cluster_counter += 1
    
    return cluster_counter - 1 # disregard the noise points, which carry label 0