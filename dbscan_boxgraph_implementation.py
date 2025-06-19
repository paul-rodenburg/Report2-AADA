import sys
import os
import time
from point import ClusterPoint as CP
from boxgraph import BoxGraph
from box import Box
from collections import deque

def find_core_points(bg):
    """
    Step 2: find the core points
    """

#// BEGIN_TODO [FIND-CORE-POINTS]

    # Map each point to its containing box
    point_box = {}
    for box in bg.boxes:
        for p in box.points:
            point_box[p] = box

    # First mark cores
    for p in bg.points:
        # gather candidate neighbor boxes: own + neighbors
        b = point_box[p]
        candidate_boxes = [b] + b.neighbours
        # count neighbors within eps (including self)
        cnt = 0
        sqr_eps = bg.eps_sqr
        for nb in candidate_boxes:
            for q in nb.points:
                if p.sq_distance_to(q) <= sqr_eps:
                    cnt += 1
                    if cnt >= bg.min_pts:
                        break
            if cnt >= bg.min_pts:
                break
        if cnt >= bg.min_pts:
            p.func = CP.Func.CORE
    # Then mark borders
    for p in bg.points:
        if p.func != CP.Func.CORE:
            b = point_box[p]
            candidate_boxes = [b] + b.neighbours
            found = False
            sqr_eps = bg.eps_sqr
            for nb in candidate_boxes:
                for q in nb.points:
                    if q.func == CP.Func.CORE and p.sq_distance_to(q) <= sqr_eps:
                        found = True
                        break
                if found:
                    break
            if found:
                p.func = CP.Func.BORDER


def compute_cluster_cores(bg):
    """
    Step 3: compute the cluster cores
    """

    # Map each core-containing box and perform BFS to label core clusters
    # initialize
    nr_clusters = 0
    for box in bg.boxes:
        # check if box has any core points
        core_pts = [p for p in box.points if p.func == CP.Func.CORE]
        if not core_pts or box.is_labeled():
            continue
        # start new cluster
        nr_clusters += 1
        cluster_id = nr_clusters
        # BFS on boxes
        queue = deque([box])
        box.label = cluster_id
        while queue:
            b = queue.popleft()
            # label all core points in this box
            for p in b.points:
                if p.func == CP.Func.CORE:
                    p.cluster_label = cluster_id
            # explore neighbors
            for nb in b.neighbours:
                if nb.is_labeled():
                    continue
                # part of same core cluster if at least one core-core neighbor within eps
                if b.is_core_neighbour(nb, bg.eps):
                    nb.label = cluster_id
                    queue.append(nb)
    return nr_clusters


def assign_border_points(bg):
    """
    Step 4: assign border points to clusters
    """

    # For each border point, assign to nearest core neighbor label
    # Pre-map box of points
    point_box = {}
    for box in bg.boxes:
        for p in box.points:
            point_box[p] = box

    sqr_eps = bg.eps_sqr
    for p in bg.points:
        if p.func == CP.Func.BORDER:
            b = point_box[p]
            candidate_boxes = [b] + b.neighbours
            best = None
            best_dist = None
            for nb in candidate_boxes:
                for q in nb.points:
                    if q.func == CP.Func.CORE:
                        d = p.sq_distance_to(q)
                        if d <= sqr_eps and (best is None or d < best_dist):
                            best = q
                            best_dist = d
            if best is not None:
                p.cluster_label = best.cluster_label
