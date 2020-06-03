import numpy as np
from pathfinding.core.grid import Grid
from pathfinding.core.node import Node
from pathfinding.finder.a_star import AStarFinder
import math

class PathFinder():
    def __init__(self, map = None):
        self.finder = AStarFinder()
        self.map = map * 10
        self.grid = Grid(matrix = map)
        self.grid.set_passable_up_down_border()
        self.path = []
        
    def set_map(self, map):
        self.map = map
        self.grid = Grid(matrix = map)
        self.grid.set_passable_up_down_border()
        
    def set_end(self, end):
        self.end = self.grid.node(end[1], end[0])
        
    def set_start(self, start):
        self.start = self.grid.node(start[1], start[0])
        
    def get_path_distance(self):
        if len(self.path) == 0:
            return 0
        else:
            distance = 0
            for node in self.path:
                distance += self.map[node[1], node[0]]
            distance = math.ceil(distance / 10)
            return distance
            
    def get_direction(self, node_start, node_end):
        if node_end[0] - node_start[0] == 1:
            return 'south'
        if node_end[0] - node_start[0] == -1:
            return 'north'
        if node_end[1] - node_start[1] == 1 or node_end[1] - node_start[1] == - len(self.map) + 1:
            return 'east'
        if node_end[1] - node_start[1] == -1 or node_end[1] - node_start[1] == len(self.map) - 1:
            return 'west'
        else:
            return 'no direction'
            
    def print_path(self):
        if len(self.path) > 0:
            previous_node = self.path[0]
        for node in self.path:
            print('x: ', node[1], 'y: ', node[0], 'distance: ', self.map[node[1], node[0]], 'direction: ', self.get_direction(previous_node, node))
            previous_node = node
            
    def get_manhattan_distance(self):
        return abs(self.start.x - self.end.x) + abs(self.start.y - self.end.y)
        
    def find_path(self, start_list = None, end_list = None):
        if start_list is not None:
            self.set_start(start_list)
        start = self.start
        if end_list is not None:
            self.set_end(end_list)
        end = self.end
        self.path, runs = self.finder.find_path(start, end, self.grid)
        print('operations:', runs, 'path length:', len(self.path))
        print('path: {}'.format(self.path))
        distance = self.get_path_distance()
        print('distance: ', distance)
        
    def map_values(self, original_value, new_value):
        self.map[self.map == original_value] = new_value
        self.grid = Grid(matrix = self.map)
        self.grid.set_passable_up_down_border()