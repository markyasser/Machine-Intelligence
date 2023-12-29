from typing import Tuple
from game import HeuristicFunction, Game, S, A
from helpers.utils import NotImplemented

#TODO: Import any modules you want to use

# All search functions take a problem, a state, a heuristic function and the maximum search depth.
# If the maximum search depth is -1, then there should be no depth cutoff (The expansion should not stop before reaching a terminal state) 

# All the search functions should return the expected tree value and the best action to take based on the search results

# This is a simple search function that looks 1-step ahead and returns the action that lead to highest heuristic value.
# This algorithm is bad if the heuristic function is weak. That is why we use minimax search to look ahead for many steps.
def greedy(game: Game[S, A], state: S, heuristic: HeuristicFunction, max_depth: int = -1) -> Tuple[float, A]:
    agent = game.get_turn(state)
    
    terminal, values = game.is_terminal(state)
    if terminal: return values[agent], None

    actions_states = [(action, game.get_successor(state, action)) for action in game.get_actions(state)]
    value, _, action = max((heuristic(game, state, agent), -index, action) for index, (action , state) in enumerate(actions_states))
    return value, action

# Apply Minimax search and return the game tree value and the best action
# Hint: There may be more than one player, and in all the testcases, it is guaranteed that 
# game.get_turn(state) will return 0 (which means it is the turn of the player). All the other players
# (turn > 0) will be enemies. So for any state "s", if the game.get_turn(s) == 0, it should a max node,
# and if it is > 0, it should be a min node. Also remember that game.is_terminal(s), returns the values
# for all the agents. So to get the value for the player (which acts at the max nodes), you need to
# get values[0].
def minimax(game: Game[S, A], state: S, heuristic: HeuristicFunction, max_depth: int = -1) -> Tuple[float, A]:
    def minimax_decision(state: S, depth: int) -> Tuple[float, A]:
        # Check if the current state is a terminal state
        terminal, values = game.is_terminal(state)
        if terminal:
            return values[0], None

        # Check if the maximum depth has been reached
        if depth == 0:
            return heuristic(game, state, 0), None

        # Get the agent (player) who is making the move
        agent = game.get_turn(state)

        # If it's the player's turn, call max_value function
        if agent == 0:
            return max_value(state, depth)

        # If it's the enemy's turn, call min_value function
        return min_value(state, depth)
    
    def max_value(state: S, depth: int) -> Tuple[float, A]:
        # Get all possible actions and their resulting states
        actions_states = [(action, game.get_successor(state, action)) for action in game.get_actions(state)]

        # Initialize the maximum value and best action
        max_value = float('-inf')
        best_action = None

        # Iterate over each action and state pair
        for action, state in actions_states:
            # Recursively call minimax_decision to get the value of the next state
            value = minimax_decision(state, depth - 1)[0]

            # Update the maximum value and best action if a better value is found
            if value > max_value:
                max_value = value
                best_action = action

        # Return the maximum value and best action
        return max_value, best_action

    def min_value(state: S, depth: int) -> Tuple[float, A]:
        # Get all possible actions and their resulting states
        actions_states = [(action, game.get_successor(state, action)) for action in game.get_actions(state)]

        # Initialize the minimum value and best action
        min_value = float('inf')
        best_action = None

        # Iterate over each action and state pair
        for action, state in actions_states:
            # Recursively call minimax_decision to get the value of the next state
            value = minimax_decision(state, depth - 1)[0]

            # Update the minimum value and best action if a smaller value is found
            if value < min_value:
                min_value = value
                best_action = action

        # Return the minimum value and best action
        return min_value, best_action
    
    return minimax_decision(state, max_depth)
    

# Apply Alpha Beta pruning and return the tree value and the best action
# Hint: Read the hint for minimax.
def alphabeta(game: Game[S, A], state: S, heuristic: HeuristicFunction, max_depth: int = -1) -> Tuple[float, A]:
    def alphabeta_decision(state: S, depth: int, alpha, beta) -> Tuple[float, A]:
        # Check if the current state is a terminal state
        terminal, values = game.is_terminal(state)
        if terminal:
            return values[0], None

        # Check if the maximum depth has been reached
        if depth == 0:
            return heuristic(game, state, 0), None

        # Get the agent (player) who is making the move
        agent = game.get_turn(state)

        # If it's the player's turn, call max_value function
        if agent == 0:
            return max_value(state, depth, alpha, beta)

        # If it's the enemy's turn, call min_value function
        return min_value(state, depth, alpha, beta)
    
    def max_value(state: S, depth: int, alpha, beta) -> Tuple[float, A]:
        # Get all possible actions and their resulting states
        actions_states = [(action, game.get_successor(state, action)) for action in game.get_actions(state)]

        # Initialize the maximum value and best action
        max_value = float('-inf')
        best_action = None

        # Iterate over each action and state pair
        for action, state in actions_states:
            # Recursively call alphabeta_decision to get the value of the next state
            value = alphabeta_decision(state, depth - 1, alpha, beta)[0]

            # Update the maximum value and best action if a better value is found
            if value > max_value:
                max_value = value
                best_action = action

            # Update the alpha value
            alpha = max(alpha, max_value)

            # Check if pruning is possible
            if alpha >= beta:
                break

        # Return the maximum value and best action
        return max_value, best_action
    
    def min_value(state: S, depth: int, alpha, beta) -> Tuple[float, A]:
        # Get all possible actions and their resulting states
        actions_states = [(action, game.get_successor(state, action)) for action in game.get_actions(state)]

        # Initialize the minimum value and best action
        min_value = float('inf')
        best_action = None

        # Iterate over each action and state pair
        for action, state in actions_states:
            # Recursively call alphabeta_decision to get the value of the next state
            value = alphabeta_decision(state, depth - 1, alpha, beta)[0]

            # Update the minimum value and best action if a smaller value is found
            if value < min_value:
                min_value = value
                best_action = action

            # Update the beta value
            beta = min(beta, min_value)

            # Check if pruning is possible
            if alpha >= beta:
                break

        # Return the minimum value and best action
        return min_value, best_action
    
    return alphabeta_decision(state, max_depth, float('-inf'), float('inf'))
    
    

# Apply Alpha Beta pruning with move ordering and return the tree value and the best action
# Hint: Read the hint for minimax.
# Apply Alpha Beta pruning with move ordering and return the tree value and the best action
# Hint: Read the hint for minimax.

def alphabeta_with_move_ordering(game: Game[S, A], state: S, heuristic: HeuristicFunction, max_depth: int = -1) -> Tuple[float, A]:
    def alphabeta_decision(state: S, depth: int, alpha, beta) -> Tuple[float, A]:
        # Check if the current state is a terminal state
        terminal, values = game.is_terminal(state)
        if terminal:
            return values[0], None

        # Check if the maximum depth has been reached
        if depth == 0:
            return heuristic(game, state, 0), None

        # Get the agent (player) who is making the move
        agent = game.get_turn(state)

        # If it's the player's turn, call max_value function
        if agent == 0:
            return max_value(state, depth, alpha, beta)

        # If it's the enemy's turn, call min_value function
        return min_value(state, depth, alpha, beta)
    
    def max_value(state: S, depth: int, alpha, beta) -> Tuple[float, A]:
        # Get all possible actions and their resulting states
        actions_states = [(action, game.get_successor(state, action)) for action in game.get_actions(state)]

        # Sort the actions based on the heuristic value of the resulting states
        actions_states.sort(key=lambda x: heuristic(game, x[1], 0), reverse=True)

        # Initialize the maximum value and best action
        max_value = float('-inf')
        best_action = None

        # Iterate over each action and state pair
        for action, state in actions_states:
            # Recursively call alphabeta_decision to get the value of the next state
            value = alphabeta_decision(state, depth - 1, alpha, beta)[0]

            # Update the maximum value and best action if a better value is found
            if value > max_value:
                max_value = value
                best_action = action

            # Update the alpha value
            alpha = max(alpha, max_value)

            # Check if pruning is possible
            if alpha >= beta:
                break

        # Return the maximum value and best action
        return max_value, best_action
    
    def min_value(state: S, depth: int, alpha, beta) -> Tuple[float, A]:
        # Get all possible actions and their resulting states
        actions_states = [(action, game.get_successor(state, action)) for action in game.get_actions(state)]

        # Sort the actions based on the heuristic value of the resulting states
        actions_states.sort(key=lambda x: heuristic(game, x[1], 0))

        # Initialize the minimum value and best action
        min_value = float('inf')
        best_action = None

        # Iterate over each action and state pair
        for action, state in actions_states:
            # Recursively call alphabeta_decision to get the value of the next state
            value = alphabeta_decision(state, depth - 1, alpha, beta)[0]

            # Update the minimum value and best action if a smaller value is found
            if value < min_value:
                min_value = value
                best_action = action

            # Update the beta value
            beta = min(beta, min_value)

            # Check if pruning is possible
            if alpha >= beta:
                break
        
        # Return the minimum value and best action
        return min_value, best_action
    
    return alphabeta_decision(state, max_depth, float('-inf'), float('inf'))

# Apply Expectimax search and return the tree value and the best action
# Hint: Read the hint for minimax, but note that the monsters (turn > 0) do not act as min nodes anymore,
# they now act as chance nodes (they act randomly).
def expectimax(game: Game[S, A], state: S, heuristic: HeuristicFunction, max_depth: int = -1) -> Tuple[float, A]:
    def expectimax_decision(state: S, depth: int) -> Tuple[float, A]:
        # Check if the current state is a terminal state
        terminal, values = game.is_terminal(state)
        if terminal:
            return values[0], None

        # Check if the maximum depth has been reached
        if depth == 0:
            return heuristic(game, state, 0), None

        # Get the agent (player) who is making the move
        agent = game.get_turn(state)

        # If it's the player's turn, call max_value function
        if agent == 0:
            return max_value(state, depth)

        # If it's the enemy's turn, call chance_value function
        return chance_value(state, depth)
    
    def max_value(state: S, depth: int) -> Tuple[float, A]:
        # Get all possible actions and their resulting states
        actions_states = [(action, game.get_successor(state, action)) for action in game.get_actions(state)]

        # Initialize the maximum value and best action
        max_value = float('-inf')
        best_action = None

        # Iterate over each action and state pair
        for action, state in actions_states:
            # Recursively call expectimax_decision to get the value of the next state
            value = expectimax_decision(state, depth - 1)[0]

            # Update the maximum value and best action if a better value is found
            if value > max_value:
                max_value = value
                best_action = action

        # Return the maximum value and best action
        return max_value, best_action

    def chance_value(state: S, depth: int) -> Tuple[float, A]:
        # Get all possible actions and their resulting states
        actions_states = [(action, game.get_successor(state, action)) for action in game.get_actions(state)]

        # Initialize the chance value and best action
        chance_value = 0
        best_action = None

        # Iterate over each action and state pair
        for action, state in actions_states:
            # Recursively call expectimax_decision to get the value of the next state
            value = expectimax_decision(state, depth - 1)[0]

            # Add the value to the chance value
            chance_value += value

        # Calculate the average chance value
        chance_value /= len(actions_states)

        # Return the chance value and best action
        return chance_value, best_action
    
    return expectimax_decision(state, max_depth)