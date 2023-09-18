from PIL import Image
import pygame
import time
import pandas as pd
from Map import Map_Obj
from math import sqrt
import numpy as np
np.set_printoptions(threshold=np.inf, linewidth=300)

YELLOW = (20, 204, 20)
RED = (255, 0, 0)
WHITE = (255, 255, 255)
GRAY = (166, 166, 166)
GREEN = (0, 204, 0)
ORANGE = (255, 102, 0)
BLUE = (0, 128, 255)
colors = {-1: (255, 0, 0), 1: (215, 215, 215),
          2: (166, 166, 166), 3: (96, 96, 96), 4: (36, 36, 36)}


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
                if (neighbor_x > (no_rows - 1) or neighbor_x < 0 or neighbor_y > (no_columns - 1) or neighbor_y < 0):
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
            node.set_h(
                abs(neighbor.x - goal_pos[0]) + abs(node.y - goal_pos[1]))
            if len([i for i in opened_nodes if node == i and node.get_g() > i.get_g()]) > 0:
                continue
            opened_nodes.append(node)
    samf, path = return_path(current_node, maze)
    return opened_nodes, closed_nodes, samf, path


def show_path(maze, path, start, goal):
    # Pygame initialization
    pygame.init()
    scale = 20
    width = maze.shape[1] * scale
    height = maze.shape[0] * scale
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption("Pathfinding Visualization")

    running = True
    clock = pygame.time.Clock()
    # Milliseconds delay between each frame (adjust as needed)
    draw_delay = 100
    draw_counter = 0

    # Create a list to store the frames of the path
    path_frames = []

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Clear the screen
        screen.fill((215, 215, 215))

        # Draw the maze
        for y in range(maze.shape[0]):
            for x in range(maze.shape[1]):
                if maze[y][x] in colors:
                    pygame.draw.rect(screen, colors[maze[y][x]], (x * scale,
                                     y * scale, scale, scale))
        pygame.draw.rect(screen, YELLOW, (start[1] * scale,
                         start[0] * scale, scale, scale))
        pygame.draw.rect(screen, YELLOW, (goal[1] * scale,
                         goal[0] * scale, scale, scale))

        # Draw the path in blue
        if draw_counter < len(path):
            node_x, node_y = path[draw_counter]
            pygame.draw.rect(screen, BLUE, (node_y * scale,
                             node_x * scale, scale, scale))
            draw_counter += 1

        pygame.display.flip()

        # Create a snapshot of the current frame and add it to the path_frames list
        path_frames.append(pygame.surfarray.array3d(screen))

        clock.tick(60)
        pygame.time.delay(draw_delay)

        # If the path is fully drawn, replay the frames
        if draw_counter >= len(path) and len(path_frames) > 0:
            for frame in path_frames:
                screen.blit(pygame.surfarray.make_surface(frame), (0, 0))
                pygame.display.flip()
                pygame.time.delay(draw_delay)

    pygame.quit()


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
    map_obj = Map_Obj(task=4)  # Choose task 1, 2, 3 or 4.
    map_int_np, map_str_np = map_obj.get_maps()
    start = map_obj.get_start_pos()
    goal = map_obj.get_goal_pos()
    opened_nodes, closed_nodes, maze, path = search(map_int_np, start, goal)
    show_path(maze, path, start, goal)


main()
