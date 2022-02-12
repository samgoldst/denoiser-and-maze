from algorithms import trail
from node import Node
from collections import defaultdict

WHITE = (255, 255, 255)

def BFS(node, goal):
    marked = defaultdict(int)
    q = [node]
    while len(q) != 0:
        curr = q.pop(0)
        marked[curr] = 1
        curr.color = (0, 0, 0)
        for mapped in curr:
            if goal == mapped:
                return True
            if marked[mapped] == 0 and mapped is not None:
                q.append(mapped)
    return False

def DFS(node, goal):
    marked = defaultdict(int)
    q = [node]
    while len(q) != 0:
        curr = q.pop()
        marked[curr] = 1
        curr.color = (0, 0, 0)
        for mapped in curr:
            if goal == mapped:
                return True
            if marked[mapped] == 0 and mapped is not None:
                q.append(mapped)
    return False

def dijkstra(node, goal):
    d_dict = {node: 0} #distance
    p_dict = {node: None} #previous
    seen = [node]
    while len(seen) != 0:
        min_seen = seen[0]
        for child in seen:
            if d_dict[child] < d_dict[min_seen]:
                min_seen = child
        seen.remove(min_seen)
        min_seen.color = (0,0,0)
        if min_seen == goal:
            trail(p_dict, goal, node)
            return True
        for mapped in min_seen:
            if mapped is not None and mapped.color != (0,0,0):
                if not mapped in seen:
                    d_dict[mapped] = d_dict[min_seen] + mapped.weight
                    p_dict[mapped] = min_seen
                    seen.append(mapped)
                if d_dict[min_seen] + mapped.weight < d_dict[mapped]:
                    d_dict[mapped] = d_dict[min_seen] + mapped.weight
                    p_dict[mapped] = min_seen

def dijkstra_setup(node, goal):
    d_dict = {node: 0} #distance
    p_dict = {node: None} #previous
    seen = [node]
    return seen, p_dict, d_dict

def dijkstra_step(goal, node, seen, p_dict, d_dict):
    min_seen = seen[0]
    for child in seen:
        if d_dict[child] < d_dict[min_seen]:
            min_seen = child
    seen.remove(min_seen)
    min_seen.color = (0,0,0)
    if min_seen == goal:
        trail(p_dict, goal, node)
        return True
    for mapped in min_seen:
        if mapped is not None and mapped.color != (0,0,0):
            if not mapped in seen:
                d_dict[mapped] = d_dict[min_seen] + mapped.weight
                p_dict[mapped] = min_seen
                seen.append(mapped)
            if d_dict[min_seen] + mapped.weight < d_dict[mapped]:
                d_dict[mapped] = d_dict[min_seen] + mapped.weight
                p_dict[mapped] = min_seen

def astar(node, goal):
    d_dict = {node: 0} #actualdistance
    f_dict = {node: 0} #actual distance + guess
    p_dict = {node: None} #previous
    seen = [node]
    while len(seen) != 0:
        min_seen = seen[0]
        for child in seen:
            if f_dict[child] < f_dict[min_seen]:
                min_seen = child
        seen.remove(min_seen)
        min_seen.color = (0,0,0)
        if min_seen == goal:
            trail(p_dict, goal, node)
            return True
        for mapped in min_seen:
            if mapped is not None and mapped.color != (0,0,0):
                if not mapped in seen:
                    d_dict[mapped] = d_dict[min_seen] + mapped.weight                   
                    f_dict[mapped] = d_dict[mapped] + astar_h(mapped, goal)
                    p_dict[mapped] = min_seen
                    seen.append(mapped)
                if d_dict[min_seen] + mapped.weight < d_dict[mapped]:
                    d_dict[mapped] = d_dict[min_seen] + mapped.weight            
                    f_dict[mapped] = d_dict[mapped] + astar_h(mapped, goal)
                    p_dict[mapped] = min_seen

def astar_setup(node, goal):
    d_dict = {node: 0} #actualdistance
    f_dict = {node: 0} #actual distance + guess
    p_dict = {node: None} #previous
    seen = [node]
    return seen, p_dict, d_dict, f_dict

def astar_step(goal, node, seen, p_dict, d_dict, f_dict):
    min_seen = seen[0]
    for child in seen:
        if f_dict[child] < f_dict[min_seen]:
            min_seen = child
    seen.remove(min_seen)
    min_seen.color = (0,0,0)
    if min_seen == goal:
        trail(p_dict, goal, node)
        return True
    for mapped in min_seen:
        if mapped is not None and mapped.color != (0,0,0):
            if not mapped in seen:
                d_dict[mapped] = d_dict[min_seen] + mapped.weight                   
                f_dict[mapped] = d_dict[mapped] + astar_h(mapped, goal)
                p_dict[mapped] = min_seen
                seen.append(mapped)
            if d_dict[min_seen] + mapped.weight < d_dict[mapped]:
                d_dict[mapped] = d_dict[min_seen] + mapped.weight            
                f_dict[mapped] = d_dict[mapped] + astar_h(mapped, goal)
                p_dict[mapped] = min_seen

def astar_h(curr, target):
    s1 = curr.pos[0] - target.pos[0]
    s2 = curr.pos[1] - target.pos[1]
    return (s1**2 + s2**2)**.5

def astar_swarm(start, goal):
    start_d_dict = {start: 0} #actualdistance
    start_f_dict = {start: 0} #actual distance + guess
    start_p_dict = {start: None} #previous
    start_seen = [start]
    goal_d_dict = {goal: 0} #actualdistance
    goal_f_dict = {goal: 0} #actual distance + guess
    goal_p_dict = {goal: None} #previous
    goal_seen = [goal]
    while len(start_seen) != 0 and len(goal_seen) != 0:
        result = astar_swarm_helper(goal, start, start_seen, start_p_dict, start_d_dict, start_f_dict, goal_seen)
        if result:
            result.color = WHITE
            trail(goal_p_dict, result, goal)
            break
        result = astar_swarm_helper(start, goal, goal_seen, goal_p_dict, goal_d_dict, goal_f_dict, start_seen)
        if result:
            result.color = WHITE
            trail(start_p_dict, result, start)
            break

def astar_swarm_helper(goal, node, seen, p_dict, d_dict, f_dict, goal_seen):
    min_seen = seen[0]
    for child in seen:
        if f_dict[child] < f_dict[min_seen]:
            min_seen = child
    seen.remove(min_seen)
    min_seen.color = (0,0,0)
    if min_seen in goal_seen:
        trail(p_dict, min_seen, node)
        return min_seen
    for mapped in min_seen:
        if mapped is not None and mapped.color != (0,0,0):
            if not mapped in seen:
                d_dict[mapped] = d_dict[min_seen] + mapped.weight                   
                f_dict[mapped] = d_dict[mapped] + astar_h(mapped, goal)
                p_dict[mapped] = min_seen
                seen.append(mapped)
            if d_dict[min_seen] + mapped.weight < d_dict[mapped]:
                d_dict[mapped] = d_dict[min_seen] + mapped.weight            
                f_dict[mapped] = d_dict[mapped] + astar_h(mapped, goal)
                p_dict[mapped] = min_seen
    return None

def astar_swarm_setup(start, goal):
    start_d_dict = {start: 0} #actualdistance
    start_f_dict = {start: 0} #actual distance + guess
    start_p_dict = {start: None} #previous
    start_seen = [start]
    goal_d_dict = {goal: 0} #actualdistance
    goal_f_dict = {goal: 0} #actual distance + guess
    goal_p_dict = {goal: None} #previous
    goal_seen = [goal]
    return start_seen, start_p_dict, start_d_dict, start_f_dict, goal_seen, goal_p_dict, goal_d_dict, goal_f_dict

def astar_swarm_step(start, goal, start_seen, start_p_dict, start_d_dict, start_f_dict, goal_seen, goal_p_dict, goal_d_dict, goal_f_dict):
    result = astar_swarm_helper(goal, start, start_seen, start_p_dict, start_d_dict,start_f_dict, goal_seen)
    if result:
        result.color = WHITE
        trail(goal_p_dict, result, goal)
        return True
    result = astar_swarm_helper(start, goal, goal_seen, goal_p_dict, goal_d_dict,goal_f_dict, start_seen)
    if result:
        result.color = WHITE
        trail(start_p_dict, result, start)
        return True
    return False