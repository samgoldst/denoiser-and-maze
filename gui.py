from typing import Dict, List, Union
import pygame
from node import Node
from collections import defaultdict
from algs import *
from algorithms import bfs_step, bfs_step_setup, trail
import random
from scipy.io import loadmat, savemat
import numpy as np


BLACK = (0,0,0)
WHITE = (255,255,255)
RED = (255,0,0)
GREEN = (0,255,0)
BLUE = (0,0,255)

# Screen height and width

board = loadmat("output.mat")["x"]

S_HEIGHT = 800
S_WIDTH = 800

nodes: List[List[Node]] = []

if input("use provided map (y/n)") == "y":
    dim = (S_HEIGHT // np.shape(board)[1], S_WIDTH // np.shape(board)[0])
    for i in range(np.shape(board)[1]):
        lst = []
        for k in range(np.shape(board)[0]):
            lst.append(Node(dim, int(1000*board[k][i] + 1), (int(255*board[k][i]), 0, 255 - int(255*board[k][i]))))
            lst[-1].pos = (k, i)
        nodes.append(lst)

else:
    NODES = int(input("Nodes / Side"))

    dim = (S_WIDTH // NODES, S_HEIGHT // NODES)

    for i in range(NODES):
        lst = []
        for k in range(NODES):
            lst.append(Node(dim, 1, BLUE))
            lst[-1].pos = (k, i)
        nodes.append(lst)

for r_i, row in enumerate(nodes):
    for c_i, node in enumerate(row):
        if c_i > 0:
            # node.left = (row[c_i - 1], 1)
            node.left = row[c_i - 1]
        if c_i < len(row) - 1:
            # node.right = (row[c_i + 1], 1)
            node.right = row[c_i + 1]
        if r_i > 0:
            # node.up = (nodes[r_i - 1][c_i], 1)
            node.up = nodes[r_i - 1][c_i]
        if r_i < len(nodes) - 1:
            # node.down = (nodes[r_i + 1][c_i], 1)
            node.down = nodes[r_i + 1][c_i]

root = nodes[0][0]

pygame.init() #start pygame

screen = pygame.display.set_mode((S_WIDTH, S_HEIGHT))

pygame.display.set_caption('Pygame')

clock = pygame.time.Clock()

done = False

start: Union[Node, None] = None
goal: Union[Node, None] = None

s_down = False
g_down = False
num_down = (False, None)
keys = [pygame.K_1, pygame.K_2, pygame.K_3, pygame.K_4, pygame.K_5, pygame.K_6, pygame.K_7, pygame.K_8, pygame.K_9]
stepping_dijkstra = False
stepping_astar = False
stepping_astar_swarm = False
seen = None

while not done:
    for event in pygame.event.get(): #check the events list
        if event.type == pygame.QUIT: #if the user clicks the X
            done = True #now we're done displaying
        elif event.type == pygame.MOUSEMOTION:
            if event.buttons[0]:
                for row in nodes:
                    for node in row:
                        if node.inside(event.pos):
                            if num_down[0]:
                                node.color = (255 * (num_down[1] - 48)/9, 255 * (num_down[1] - 48)/9, 255 * (num_down[1] - 48)/9)
                                node.weight = num_down[1] - 48
                            else:
                                node.color = RED
                                node.weight = 1000
                            if node == goal:
                                goal = None
                            elif node == start:
                                start = None
            elif event.buttons[2]:
                for row in nodes:
                    for node in row:
                        if node.inside(event.pos):
                            node.color = BLUE
                            node.weight = 1
                            if node == goal:
                                goal = None
                            elif node == start:
                                start = None
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                for row in nodes:
                    for node in row:
                        if node.inside(event.pos):
                            if s_down:
                                if start:
                                    start.color = BLUE
                                start = node
                                node.color = GREEN
                            elif g_down:
                                if goal:
                                    goal.color = BLUE
                                goal = node
                                goal.color = WHITE
                            elif num_down[0]:
                                if node == goal:
                                    goal = None
                                elif node == start:
                                    start = None
                                node.color = (255 * (num_down[1] - 48)/9, 255 * (num_down[1] - 48)/9, 255 * (num_down[1] - 48)/9)
                                node.weight = num_down[1] - 48
                            else:
                                node.color = RED
                                node.weight = 1000
                                if node == goal:
                                    goal = None
                                elif node == start:
                                    start = None
            elif event.button == 3:
                for row in nodes:
                    for node in row:
                        if node.inside(event.pos):
                            if s_down:
                                if start:
                                    start.color = BLUE
                                start = node
                                node.color = GREEN
                            elif g_down:
                                if goal:
                                    goal.color = BLUE
                                goal = node
                                goal.color = WHITE
                            else:
                                node.color = BLUE
                                node.weight = 1
                                if node == goal:
                                    goal = None
                                elif node == start:
                                    start = None

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_s:
                s_down = True
            elif event.key == pygame.K_g:
                g_down = True

            elif event.key == pygame.K_q:
                if start and goal:
                    stepping_astar = True

            elif event.key == pygame.K_w:
                if start and goal:
                    stepping_dijkstra = True

            elif event.key == pygame.K_e:
                if start and goal:
                    stepping_astar_swarm = True

            elif event.key == pygame.K_r:
                for row in nodes:
                    for node in row:
                        node.color = BLUE
                        start = None
                        goal = None
                        node.weight = 1

            elif event.key == pygame.K_SPACE:
                if start and goal:
                    # INSERT FUNCTION HERE
                    dijkstra(start, goal)

            elif event.key == pygame.K_z:
                if start and goal:
                    # INSERT FUNCTION HERE
                    astar(start, goal)

            elif event.key == pygame.K_x:
                if start and goal:
                    # INSERT FUNCTION HERE
                    astar_swarm(start, goal)

            elif event.key == pygame.K_p:
                for row in nodes:
                    for node in row:
                        if random.random() < .33 and node.color == BLUE:
                            node.color = RED
                            node.weight = 1000

            else:
                for key in keys:
                    if event.key == key:
                        print(event.key)
                        num_down = (True, key)
            
            

        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_s:
                s_down = False
            elif event.key == pygame.K_g:
                g_down = False
            else:
                if event.key == num_down[1]:
                    num_down = (False, None)

    screen.fill(BLACK)

    if stepping_astar:
        if seen is None:
            seen, p_dict, d_dict, f_dict = astar_setup(start, goal)
        
        if astar_step(goal, stepping_astar_swarm, seen, p_dict, d_dict, f_dict):
            seen, p_dict, d_dict, f_dict = None, None, None, None
            stepping_astar = False

    if stepping_dijkstra:
        if seen is None:
            seen, p_dict, d_dict = dijkstra_setup(start, goal)
        
        if dijkstra_step(goal, start, seen, p_dict, d_dict):
            seen, p_dict, d_dict = None, None, None
            stepping_dijkstra = False

    if stepping_astar_swarm:
        if seen is None:
            astar_swarm_output = astar_swarm_setup(start, goal)
            seen = True

        if astar_swarm_step(goal, start, *astar_swarm_output):
            astar_swarm_output = None
            stepping_astar_swarm = False
            seen = None    

    x = 0
    y = 0

    for row in nodes:
        for node in row:
            node.draw(screen, (x, y))
            y += dim[1]
        x += dim[0]
        y = 0

    

    pygame.display.update()

    clock.tick(180)