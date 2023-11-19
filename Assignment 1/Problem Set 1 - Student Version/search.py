from problem import HeuristicFunction, Problem, S, A, Solution
from collections import deque
from helpers.utils import NotImplemented

#TODO: Import any modules you want to use
import heapq
import itertools

# All search functions take a problem and a state
# If it is an informed search function, it will also receive a heuristic function
# S and A are used for generic typing where S represents the state type and A represents the action type

# All the search functions should return one of two possible type:
# 1. A list of actions which represent the path from the initial state to the final state
# 2. None if there is no solution

def BreadthFirstSearch(problem: Problem[S, A], initial_state: S) -> Solution:
    # If the initial state is already a goal state, return an empty path
    if problem.is_goal(initial_state):
        return []
    # Initialize a queue with the initial state and an empty action list
    frontier = deque([(initial_state, [])])
    # Initialize a hash set to keep track of explored states
    explored = {initial_state}
    
    while frontier:
        # Pop the node at the front of the queue
        state, actions = frontier.popleft()
        
        # For each successor of the node, add it to the queue if it has not been explored yet
        for action in problem.get_actions(state):
            child = problem.get_successor(state, action)
            if child not in explored:
                new_actions = actions + [action]
                if problem.is_goal(child):
                    return new_actions
                frontier.append((child, new_actions))
                explored.add(child)
    # If no solution is found, return None
    return None


    
def DepthFirstSearch(problem: Problem[S, A], initial_state: S) -> Solution:
    # If the initial state is already a goal state, return an empty path
    if problem.is_goal(initial_state):
        return []
    # Initialize a stack with the initial state and an empty action list
    frontier = [(initial_state, [])]
    # Initialize a set to keep track of explored states
    explored = set()
    
    while frontier:
        # Pop the node on top of the stack
        state, actions = frontier.pop()
        # Add the node to the explored set
        explored.add(state)
        # If the node is a goal state, return the path to it
        if problem.is_goal(state):
            return actions
        
        # For each successor of the node, add it to the stack if it has not been explored yet
        for action in problem.get_actions(state):
            child = problem.get_successor(state, action)
            if child not in explored and child not in [x[0] for x in frontier]:
                new_actions = actions + [action]
                frontier.append((child, new_actions))
    # If no solution is found, return None
    return None

    
def UniformCostSearch(problem: Problem[S, A], initial_state: S) -> Solution:
    # Initialize the frontier with the initial state and an empty path
    frontier = []
    # Initialize the explored set to be empty
    explored = set()
    # Initialize a counter to break ties in the priority queue
    count = itertools.count()
    # Add the initial state to the frontier with a cost of 0, counter, initial_State and an empty path
    # (cost, counter, state, actions)
    heapq.heappush(frontier, (0, next(count), initial_state,[]))

    while frontier:
        # Pop the node with the lowest cost from the frontier
        cost, _, state, actions = heapq.heappop(frontier)
        # If the node is a goal state, return the path to it
        if problem.is_goal(state):
            return actions

        # If the node has not been explored yet, add it to the explored set
        if state not in explored:
            explored.add(state)
            # For each successor of the node, calculate its cost and add it to the frontier
            for action in problem.get_actions(state):
                child = problem.get_successor(state, action)
                new_cost = cost + problem.get_cost(state, action)
                new_actions = actions + [action]
                heapq.heappush(frontier, (new_cost, next(count), child, new_actions))
    # If no solution is found, return None
    return None

def AStarSearch(problem: Problem[S, A], initial_state: S, heuristic: HeuristicFunction) -> Solution:
    # If the initial state is already a goal state, return an empty path
    if problem.is_goal(initial_state):
        return []
    # Initialize a priority queue with the initial state and an empty action list
    frontier = []
    # Initialize the explored set to be empty
    explored = set()
    # Initialize a counter to break ties in the priority queue
    count = itertools.count()
    # Add the initial state to the frontier with a heuristic, counter, initial_State and an empty path
    # (heuristic, counter, cost, state, actions)
    heapq.heappush(frontier, (heuristic(problem, initial_state), next(count), 0, initial_state, []))

    while frontier:
        # Pop the node with the lowest f(n) value from the priority queue
        _, _, cost, state, actions = heapq.heappop(frontier)
        # If the node is a goal state, return the path to it
        if problem.is_goal(state):
            return actions

        # If the node has not been explored yet, add it to the explored set
        if state not in explored:
            explored.add(state)
            # For each successor of the node, add it to the priority queue if it has not been explored yet
            for action in problem.get_actions(state):
                child = problem.get_successor(state, action)
                new_cost = cost + problem.get_cost(state, action)
                if child not in explored:
                    new_actions = actions + [action]
                    f_value = new_cost + heuristic(problem,child)
                    heapq.heappush(frontier, (f_value, next(count),new_cost, child, new_actions))
    # If no solution is found, return None
    return None


def BestFirstSearch(problem: Problem[S, A], initial_state: S, heuristic: HeuristicFunction) -> Solution:
    # If the initial state is already a goal state, return an empty path
    if problem.is_goal(initial_state):
        return []
    # Initialize a priority queue with the initial state and an empty action list
    frontier = []
    # Initialize the explored set to be empty
    explored = set()
    # Initialize a counter to break ties in the priority queue
    count = itertools.count()
    # Add the initial state to the frontier with a heuristic, counter, initial_State and an empty path
    # (heuristic, counter, state, actions)
    heapq.heappush(frontier, (heuristic(problem, initial_state), next(count), initial_state, []))

    while frontier:
        # Pop the node with the lowest f(n) value from the priority queue
        _, _, state, actions = heapq.heappop(frontier)
        # If the node is a goal state, return the path to it
        if problem.is_goal(state):
            return actions

        # If the node has not been explored yet, add it to the explored set
        if state not in explored:
            explored.add(state)
            # For each successor of the node, add it to the priority queue if it has not been explored yet
            for action in problem.get_actions(state):
                child = problem.get_successor(state, action)
                if child not in explored:
                    new_actions = actions + [action]
                    heapq.heappush(frontier, (heuristic(problem, child), next(count), child, new_actions))
    # If no solution is found, return None
    return None


