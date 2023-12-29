from typing import Dict, List, Optional, Set, Tuple
from mdp import MarkovDecisionProcess
from environment import Environment
from mathutils import Point, Direction
from helpers.mt19937 import RandomGenerator
from helpers.utils import NotImplemented
import json
from dataclasses import dataclass

"""
Environment Description:
    The snake is a 2D grid world where the snake can move in 4 directions.
    The snake always starts at the center of the level (floor(W/2), floor(H/2)) having a length of 1 and moving LEFT.
    The snake can wrap around the grid.
    The snake can eat apples which will grow the snake by 1.
    The snake can not eat itself.
    You win if the snake body covers all of the level (there is no cell that is not occupied by the snake).
    You lose if the snake bites itself (the snake head enters a cell occupied by its body).
    The action can not move the snake in the opposite direction of its current direction.
    The action can not move the snake in the same direction 
        i.e. (if moving right don't give an action saying move right).
    Eating an apple increases the reward by 1.
    Winning the game increases the reward by 100.
    Losing the game decreases the reward by 100.
"""


# IMPORTANT: This class will be used to store an observation of the snake environment
@dataclass(frozen=True)
class SnakeObservation:
    snake: Tuple[Point]  # The points occupied by the snake body
    # where the head is the first point and the tail is the last
    direction: Direction  # The direction that the snake is moving towards
    apple: Optional[
        Point
    ]  # The location of the apple. If the game was already won, apple will be None


class SnakeEnv(Environment[SnakeObservation, Direction]):
    rng: RandomGenerator  # A random generator which will be used to sample apple locations

    snake: List[Point]
    direction: Direction
    apple: Optional[Point]

    def __init__(self, width: int, height: int) -> None:
        super().__init__()
        assert width > 1 or height > 1, "The world must be larger than 1x1"
        self.rng = RandomGenerator()
        self.width = width
        self.height = height
        self.snake = []
        self.direction = Direction.LEFT
        self.apple = None

    def generate_random_apple(self) -> Point:
        """
        Generates and returns a random apple position which is not on a cell occupied
        by the snake's body.
        """
        snake_positions = set(self.snake)
        possible_points = [
            Point(x, y)
            for x in range(self.width)
            for y in range(self.height)
            if Point(x, y) not in snake_positions
        ]
        print("possible_points", possible_points)
        print("snake_positions", snake_positions)
        return self.rng.choice(possible_points)

    def reset(self, seed: Optional[int] = None) -> Point:
        """
        Resets the Snake environment to its initial state and returns the starting state.
        Args:
            seed (Optional[int]): An optional integer seed for the random
            number generator used to generate the game's initial state.

        Returns:
            The starting state of the game, represented as a Point object.
        """
        if seed is not None:
            self.rng.seed(seed)  # Initialize the random generator using the seed
        # Define the snake before calling generate_random_apple
        center_x = self.width // 2
        center_y = self.height // 2
        self.snake = [Point(center_x, center_y)]
        self.direction = Direction.LEFT
        self.apple = self.generate_random_apple()

        return SnakeObservation(tuple(self.snake), self.direction, self.apple)

    def actions(self) -> List[Direction]:
        """
        Returns a list of the possible actions that can be taken from the current state of the Snake game.
        Returns:
            A list of Directions, representing the possible actions that can be taken from the current state.

        """
        # can't move in the opposite direction
        if self.direction in [Direction.UP, Direction.DOWN]:
            return [Direction.NONE, Direction.LEFT, Direction.RIGHT]
        else:
            return [Direction.NONE, Direction.UP, Direction.DOWN]

    def step(self, action: Direction) -> Tuple[SnakeObservation, float, bool, Dict]:
        """
        Updates the state of the Snake game by applying the given action.

        Args:
            action (Direction): The action to apply to the current state.

        Returns:
            A tuple containing four elements:
            - next_state (SnakeObservation): The state of the game after taking the given action.
            - reward (float): The reward obtained by taking the given action.
            - done (bool): A boolean indicating whether the episode is over.
            - info (Dict): A dictionary containing any extra information. You can keep it empty.
        """
        # Update the direction of the snake

        curr_head = self.snake[0]
        # Calculate the new head position of the snake based on the given action
        new_head = None
        if action == Direction.RIGHT:
            new_head = Point((curr_head.x + 1) % self.width, curr_head.y)
        elif action == Direction.UP:
            new_head = Point(curr_head.x, (curr_head.y - 1) % self.height)
        elif action == Direction.LEFT:
            new_head = Point((curr_head.x - 1) % self.width, curr_head.y)
        elif action == Direction.DOWN:
            new_head = Point(curr_head.x, (curr_head.y + 1) % self.height)
        # if the action is NONE, then the snake keeps moving in the same direction
        else:
            if self.direction == Direction.RIGHT:
                new_head = Point((curr_head.x + 1) % self.width, curr_head.y)
            elif self.direction == Direction.UP:
                new_head = Point(curr_head.x, (curr_head.y - 1) % self.height)
            elif self.direction == Direction.LEFT or self.direction == Direction.NONE:
                new_head = Point((curr_head.x - 1) % self.width, curr_head.y)
            elif self.direction == Direction.DOWN:
                new_head = Point(curr_head.x, (curr_head.y + 1) % self.height)
        # Update the direction of the snake
        if action != Direction.NONE:
            self.direction = action
        # Check if the new head position overlaps with the snake's body
        if new_head in self.snake[1:]:
            # Snake bites itself, game over
            game_over = True
            reward = -100
            observation = SnakeObservation(
                tuple(self.snake), self.direction, self.apple
            )
            return observation, reward, game_over, {}

        # Update the snake's body
        self.snake.insert(0, new_head)
        reward = 0
        # Check if the snake has covered the entire level
        if len(self.snake) == self.width * self.height:
            # Snake has won the game
            game_over = True
            reward += 100
        else:
            game_over = False
            # Check if the new head position overlaps with the apple
        if new_head == self.apple:
            # Snake eats the apple, increase reward and generate a new apple
            reward += 1
            if not game_over:
                self.apple = self.generate_random_apple()
            # print("Snake eats apple")
        else:
            # Snake did not eat the apple, remove the tail
            # print("Snake did not eat apple")
            self.snake.pop()

        observation = SnakeObservation(tuple(self.snake), self.direction, self.apple)
        return observation, reward, game_over, {}

    ###########################
    #### Utility Functions ####
    ###########################

    def render(self) -> None:
        # render the snake as * (where the head is an arrow < ^ > v) and the apple as $ and empty space as .
        for y in range(self.height):
            for x in range(self.width):
                p = Point(x, y)
                if p == self.snake[0]:
                    char = ">^<v"[self.direction]
                    print(char, end="")
                elif p in self.snake:
                    print("*", end="")
                elif p == self.apple:
                    print("$", end="")
                else:
                    print(".", end="")
            print()
        print()

    # Converts a string to an observation
    def parse_state(self, string: str) -> SnakeObservation:
        snake, direction, apple = eval(str)
        return SnakeObservation(
            tuple(Point(x, y) for x, y in snake),
            self.parse_action(direction),
            Point(*apple),
        )

    # Converts an observation to a string
    def format_state(self, state: SnakeObservation) -> str:
        snake = tuple(tuple(p) for p in state.snake)
        direction = self.format_action(state.direction)
        apple = tuple(state.apple)
        return str((snake, direction, apple))

    # Converts a string to an action
    def parse_action(self, string: str) -> Direction:
        return {
            "R": Direction.RIGHT,
            "U": Direction.UP,
            "L": Direction.LEFT,
            "D": Direction.DOWN,
            ".": Direction.NONE,
        }[string.upper()]

    # Converts an action to a string
    def format_action(self, action: Direction) -> str:
        return {
            Direction.RIGHT: "R",
            Direction.UP: "U",
            Direction.LEFT: "L",
            Direction.DOWN: "D",
            Direction.NONE: ".",
        }[action]
