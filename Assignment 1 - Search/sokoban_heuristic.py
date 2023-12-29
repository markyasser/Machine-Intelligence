from sokoban import SokobanProblem, SokobanState
from mathutils import Direction, Point, manhattan_distance,euclidean_distance
from helpers.utils import NotImplemented
# This heuristic returns the distance between the player and the nearest crate as an estimate for the path cost
# While it is consistent, it does a bad job at estimating the actual cost thus the search will explore a lot of nodes before finding a goal
def weak_heuristic(problem: SokobanProblem, state: SokobanState):
    return min(manhattan_distance(state.player, crate) for crate in state.crates) - 1

#TODO: Import any modules and write any functions you want to use


def strong_heuristic(problem: SokobanProblem, state: SokobanState) -> float:
    #IMPORTANT: DO NOT USE "problem.get_actions" HERE.
    # Calling it here will mess up the tracking of the expanded nodes count
    # which is the number of get_actions calls during the search
    #NOTE: you can use problem.cache() to get a dictionary in which you can store information that will persist between calls of this function
    # This could be useful if you want to store the results heavy computations that can be cached and used across multiple calls of this function
    # Check if the cache already contains the heuristic value for the given state


    # Check if the state is deadlock return infinity (this node will never reach the goal)
    if is_deadlock(state):
        return float('inf')

    # calculate the sum of the distances of all the crates to their closest goals
    result = 0
    for crate in state.crates:
        result += min(manhattan_distance(crate, goal) for goal in state.layout.goals)
    
    # get the distance between the player and the nearest crates
    result += min(manhattan_distance(state.player, crate) for crate in state.crates) - 1
	
    
	# Store the heuristic value in the cache
    return result



def is_deadlock(state):
    for crate in state.crates:
        if crate in state.layout.goals:
            continue
        # check if a crate is in corner
        if is_corner(crate, state):
            return True
        # check if crate is adjacent to a wall and goal is not on the same line
        if is_adjacent_to_wall_and_not_to_goal(crate, state):
            return True
        # check arround the crate if there is 4 crates or 3 crates and a wall or 2 crates and 2 walls
        if is_blocked_by_crates_or_wall(crate, state):
            return True
    return False

	

def is_corner(crate, state):
    # check if a box is in corner
    corners = [Point(1, 1), Point(-1, 1), Point(1, -1), Point(-1, -1)]
    
    if all(crate + corner not in state.layout.walkable for corner in corners):
        return True
    
    return False



def is_adjacent_to_wall_and_not_to_goal(crate, state):
    # check if a box is adjacent to a wall
    # get the nearest goal point using manhattan distance
    nearest_distance = float('inf')
    for goal in state.layout.goals:
        m_distance = manhattan_distance(crate, goal)
        if m_distance < nearest_distance :
            nearest_distance = m_distance
            nearest_goal = goal
            
    if (crate + Point(1,0)) not in state.layout.walkable : # crate has wall on the right
        if crate.x > nearest_goal.x: # goal is on the crate's left
            return True
    if (crate + Point(-1,0)) not in state.layout.walkable: # crate has wall on the left   
        if crate.x < nearest_goal.x: # goal is on the crate's right
            return True
    if (crate + Point(0,1)) not in state.layout.walkable: # crate has wall on the bottom
        if crate.y > nearest_goal.y: # goal is on the crate's top
            return True
    if (crate + Point(0,-1)) not in state.layout.walkable: # crate has wall on the top
        if crate.y < nearest_goal.y: # goal is on the crate's bottom
            return True
    return False



def is_blocked_by_crates_or_wall(crate, state):
    x, y = crate.x, crate.y
    
    # initialize the 4 square to check in
    s1 = [Point(x,y), Point(x+1,y), Point(x,y+1), Point(x+1,y+1)] # top left square
    s2 = [Point(x-1,y), Point(x,y), Point(x-1,y+1), Point(x,y+1)] # top right square
    s3 = [Point(x,y-1), Point(x+1,y-1), Point(x,y), Point(x+1,y)] # bottom left square
    s4 = [Point(x-1,y-1), Point(x,y-1), Point(x-1,y), Point(x,y)] # bottom right square
    squares = [s1, s2, s3, s4]

    for s in squares:
        count_crates = 0
        count_walls = 0
        for point in s:
            if point in state.crates: # if the point is crate 
                count_crates += 1
            elif point not in state.layout.walkable: # if the point is wall
                count_walls += 1
        if count_crates + count_walls == 4:
            return True
    return False
    

