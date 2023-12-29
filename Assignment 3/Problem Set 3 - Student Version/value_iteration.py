from typing import Dict, Optional
from agents import Agent
from environment import Environment
from mdp import MarkovDecisionProcess, S, A
import json
from helpers.utils import NotImplemented

# This is a class for a generic Value Iteration agent
class ValueIterationAgent(Agent[S, A]):
    mdp: MarkovDecisionProcess[S, A] # The MDP used by this agent for training 
    utilities: Dict[S, float] # The computed utilities
                                # The key is the string representation of the state and the value is the utility
    discount_factor: float # The discount factor (gamma)

    def __init__(self, mdp: MarkovDecisionProcess[S, A], discount_factor: float = 0.99) -> None:
        super().__init__()
        self.mdp = mdp
        self.utilities = {state:0 for state in self.mdp.get_states()} # We initialize all the utilities to be 0
        self.discount_factor = discount_factor

    # Given a state, compute its utility using the bellman equation
    # if the state is terminal, return 0
    def compute_bellman(self, state: S) -> float:
        if self.mdp.is_terminal(state):
            return 0
        max_utility = float('-inf')
        for action in self.mdp.get_actions(state):
            utility = 0
            for next_state, probability in self.mdp.get_successor(state, action).items():
                utility += probability* ( self.mdp.get_reward(state, action, next_state) + self.discount_factor * self.utilities[next_state])
            max_utility = max(utility, max_utility)
        return max_utility

  
    # Applies a single utility update
    # then returns True if the utilities has converged (the maximum utility change is less or equal the tolerance)
    # and False otherwise
    def update(self, tolerance: float = 0) -> bool:
        # Compute new utilities for each state using the Bellman equation
        new_utilities = {state: self.compute_bellman(state) for state in self.mdp.get_states()}

        # Calculate the maximum change in utilities across all states
        # Initialize max_change to handle the case when there are no states
        max_change = 0

        # Iterate over states and update max_change if needed
        for state in self.mdp.get_states():
            current_change = abs(new_utilities[state] - self.utilities[state])
            max_change = max(max_change, current_change)

        # Update the utilities with the newly computed values
        self.utilities = new_utilities

        # Check if the maximum change is below the specified tolerance
        return max_change <= tolerance
    

    # This function applies value iteration starting from the current utilities stored in the agent and stores the new utilities in the agent
    # NOTE: this function does incremental update and does not clear the utilities to 0 before running
    # In other words, calling train(M) followed by train(N) is equivalent to just calling train(N+M)
    def train(self, iterations: Optional[int] = None, tolerance: float = 0) -> int:
        # If iterations is not provided, set it to 100
        if iterations is None:
            iterations = 100
        
        num_iterations = 0  # Initialize the number of iterations to 0
        converged = False  # Initialize the convergence flag to False
        while num_iterations < iterations and not converged:  # Loop until the number of iterations reaches the specified limit or convergence is achieved
            # Update the values and check for convergence
            converged = self.update(tolerance)  # Call the update method to update the values and check for convergence
            num_iterations += 1  # Increment the number of iterations
        
        return num_iterations  # Return the number of iterations performed

    
    # Given an environment and a state, return the best action as guided by the learned utilities and the MDP
    # If the state is terminal, return None
    def act(self, env: Environment[S, A], state: S) -> A:
        if self.mdp.is_terminal(state):  # Check if the state is terminal
            return None

        best_action = None  # Initialize the best action to None
        max_utility = float('-inf')  # Initialize the maximum utility to negative infinity

        for action in self.mdp.get_actions(state):  # Iterate over all possible actions for the given state
            action_utility = 0  # Initialize the action utility to 0

            for next_state, probability in self.mdp.get_successor(state, action).items():  # Iterate over the successor states and their probabilities
                next_state_utility = self.utilities[next_state]  # Get the utility of the next state
                reward = self.mdp.get_reward(state, action, next_state)  # Get the reward for taking the action and transitioning to the next state
                action_utility += probability * (reward + self.discount_factor * next_state_utility)  # Calculate the action utility using the Bellman equation

            if action_utility > max_utility:  # Check if the current action utility is greater than the maximum utility
                max_utility = action_utility  # Update the maximum utility
                best_action = action  # Update the best action

        return best_action  # Return the best action for the given state
    
    # Save the utilities to a json file
    def save(self, env: Environment[S, A], file_path: str):
        with open(file_path, 'w') as f:
            utilities = {self.mdp.format_state(state): value for state, value in self.utilities.items()}
            json.dump(utilities, f, indent=2, sort_keys=True)
    
    # loads the utilities from a json file
    def load(self, env: Environment[S, A], file_path: str):
        with open(file_path, 'r') as f:
            utilities = json.load(f)
            self.utilities = {self.mdp.parse_state(state): value for state, value in utilities.items()}
