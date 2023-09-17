from Map import Map_Obj
from math import sqrt
import numpy as np
np.set_printoptions(threshold=np.inf, linewidth=300)
import pandas as pd
import time
from PIL import Image

class Node:
    def __init__(self, x, y, parent=None):
        self.x = x
        self.y = y
        self.parent = parent
        self.g = 0
        self.h = 0
        self.explored = False
        
    def f(self):
        return self.get_g() + self.get_h()
    def get_g(self):
        return self.g
    def get_h(self):
        return self.h
    def set_h(self, h):
        self.h = h
    def set_g(self, g):
        self.g = g 

def search(maze, start_pos, goal_pos):
    opened_nodes = []
    closed_nodes = []   
    opened_nodes.append(Node(start_pos[0], start_pos[1]))
    no_rows, no_columns = np.shape(maze)
    
    for i in range(1000):
        current_node = opened_nodes[0]
        current_index = 0
        for index, item in enumerate(opened_nodes):
            if item.f() < current_node.f():
                current_node = item
                current_index = index
        opened_nodes.pop(current_index)
        closed_nodes.append(current_node)
        if current_node.x == goal_pos[0] and current_node.y == goal_pos[1]:
            print("Path found")
            print("moves: " + str(i))
            break
        neighbour_nodes = []
        for i in range(-1, 2):
            for j in range(-1, 2):
                if i == 0 and j == 0:
                    continue
                neighbor_x = current_node.x + i
                neighbor_y = current_node.y + j
                if (neighbor_x > (no_rows - 1) or neighbor_x < 0 or neighbor_y > (no_columns -1) or neighbor_y < 0):
                    continue
                if maze[neighbor_x][neighbor_y] == -1:
                    continue
                neighbor = Node(neighbor_x, neighbor_y, current_node)
                neighbour_nodes.append(neighbor)
        for node in neighbour_nodes:
            visited = False
            for opened_node in opened_nodes:
                if node.x == opened_node.x and node.y == opened_node.y:
                    visited = True
            for closed_node in closed_nodes:
                if node.x == closed_node.x and node.y == closed_node.y:
                    visited = True
            if visited:
                continue              
            node.set_g(current_node.get_g() + maze[node.x][node.y])
            node.set_h(abs(neighbor.x - goal_pos[0]) + abs(node.y - goal_pos[1]))
            if len([i for i in opened_nodes if node == i and node.get_g() > i.get_g()]) > 0:
                continue
            opened_nodes.append(node)
    samf, path = return_path(current_node, maze)
    return opened_nodes, closed_nodes, samf, path

def show_path(map, opened_nodes, closed_nodes, path):
        width = map.shape[1]
        height = map.shape[0]
        scale = 20
        # Create an all-yellow image
        image = Image.new('RGB', (width * scale, height * scale), (255, 102, 255))
        pixels = image.load()

        # Define what colors to give to different values of the string map (undefined values will remain yellow, this is
        colors = {-1: (255, 0, 0), 1: (215, 215, 215), 2: (166, 166, 166), 3: (96, 96, 96), 4: (36, 36, 36),
         8: (255, 102, 255) }
                 

        """{' # ': (255, 0, 0), ' . ': (215, 215, 215), ' , ': (166, 166, 166), ' : ': (96, 96, 96),
                  ' ; ': (36, 36, 36), ' S ': (255, 0, 255), ' G ': (0, 128, 255)}"""
        # Go through image and set pixel color for every position
        for y in range(height):
            for x in range(width):
                if map[y][x] not in colors: continue
                for i in range(scale):
                    for j in range(scale):
                        pixels[x * scale + i, y * scale + j] = colors[map[y][x]]
        
        for node in closed_nodes:
            if (node.x, node.y) in path: continue
            for i in range(scale):
                    for j in range(scale):
                        pixels[node.y * scale + i, node.x * scale + j] = (0, 204, 0)

        for node in opened_nodes:
            if (node.x, node.y) in path: continue
            color = (255, 102, 0)
            for i in range(scale):
                for j in range(scale):
                    pixels[node.y * scale + i, node.x * scale + j] = color

        # Show image
        image.show()

def return_path(current_node, map_int_np):
    path = []
    result = map_int_np
    current = current_node
    while current is not None:
        path.append((current.x, current.y))
        current = current.parent

    path = path[::-1]
   
    for i in range(len(path)):
        result[path[i][0]][path[i][1]] = 8
    return result, path

def main():
    map_obj = Map_Obj(task=4) #Choose task 1, 2, 3 or 4.
    map_int_np, map_str_np = map_obj.get_maps()
    start = map_obj.get_start_pos()
    goal = map_obj.get_goal_pos()
    opened_nodes, closed_nodes, maze, path = search(map_int_np, start, goal)
    show_path(maze, opened_nodes, closed_nodes, path)
main()