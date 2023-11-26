from typing import Any, Dict, Set, Tuple, List
from problem import Problem
from mathutils import Direction, Point
from helpers.utils import NotImplemented

#TODO: (Optional) Instead of Any, you can define a type for the parking state
ParkingState = Tuple[Point]

# An action of the parking problem is a tuple containing an index 'i' and a direction 'd' where car 'i' should move in the direction 'd'.
ParkingAction = Tuple[int, Direction]

# This is the implementation of the parking problem
class ParkingProblem(Problem[ParkingState, ParkingAction]):
    passages: Set[Point]    # A set of points which indicate where a car can be (in other words, every position except walls).
    cars: Tuple[Point]      # A tuple of points where state[i] is the position of car 'i'. 
    ranks: Tuple[Point]      
    slots: Dict[Point, int] # A dictionary which indicate the index of the parking slot (if it is 'i' then it is the lot of car 'i') for every position.
                            # if a position does not contain a parking slot, it will not be in this dictionary.
    width: int              # The width of the parking lot.
    height: int             # The height of the parking lot.

    # This function should return the initial state
    def get_initial_state(self) -> ParkingState:
        return self.cars
    
    # This function should return True if the given state is a goal. Otherwise, it should return False.
    def is_goal(self, state: ParkingState) -> bool:
        # Iterate over each car in the state
        for i, car in enumerate(state):
            # Check if the car is in its own parking slot
            if car not in self.slots or self.slots[car] != i:
                # If the car is not in its own parking slot, then the current state is not a goal state
                return False
        # If all cars are in their own parking slots, then the current state is a goal state
        return True
    
    # This function returns a list of all the possible actions that can be applied to the given state
    def get_actions(self, state: ParkingState) -> List[ParkingAction]:
        actions = []
        # Iterate over each car in the state
        for i, car in enumerate(state):
            # Iterate over each direction
            for direction in Direction:
                # Check if the car can move in the current direction
                if self.can_move(car, direction):
                    # If the car can move in the current direction, add the action to the list of actions
                    actions.append((i, direction))
        # Return the list of actions
        return actions  
    
    # This function returns a new state which is the result of applying the given action to the given state
    def get_successor(self, state: ParkingState, action: ParkingAction) -> ParkingState:
        # Extract the index and direction from the action
        i, direction = action
        # Get the current position of the car
        car = state[i]
        # Calculate the new position of the car 
        new_car = self.move(car, direction)
        # Create a new list to store the updated state
        new_state = list(state)
        # Update the position of the car in the new state
        new_state[i] = new_car
    
        # Update our state
        self.cars = new_state
        # Return the new state as a tuple
        return tuple(new_state)
    
    # This function returns the cost of applying the given action to the given state
    def get_cost(self, state: ParkingState, action: ParkingAction) -> float:
        i, direction = action
        car = state[i]
        new_car = self.move(car, direction)
        cost = self.ranks[i]
        if new_car in self.slots and self.slots[new_car] != i:
            cost += 100
        return cost

    def can_move(self, car: Point, direction: Direction) -> bool:
        # Calculate the new position of the car 
        new_car = self.move(car, direction)
        # Check if the new position is a valid passage (i.e. not a wall)
        
        if new_car not in self.passages:
            return False
        # Check if the new position overlaps with any other car but not itself
        for other_car in self.cars:
            if other_car != car and new_car == other_car:
                return False
        # If the new position is a valid passage and does not overlap with any other car, then the car can move in the given direction
        
        return True
        
    def move(self, car: Point, direction: Direction) -> Point:
        if direction == Direction.UP:
            return Point(car.x, car.y - 1)
        elif direction == Direction.DOWN:
            return Point(car.x, car.y + 1)
        elif direction == Direction.LEFT:
            return Point(car.x - 1, car.y)
        elif direction == Direction.RIGHT:
            return Point(car.x + 1, car.y)
        else:
            raise ValueError(f"Invalid direction: {direction}")
    
     # Read a parking problem from text containing a grid of tiles
    @staticmethod
    def from_text(text: str) -> 'ParkingProblem':
        passages =  set()
        cars, slots, ranks = {}, {},{}
        lines = [line for line in (line.strip() for line in text.splitlines()) if line]
        width, height = max(len(line) for line in lines), len(lines)
        for y, line in enumerate(lines):
            for x, char in enumerate(line):
                if char != "#":
                    passages.add(Point(x, y))
                    if char == '.':
                        pass
                    elif char in "ABCDEFGHIJ":
                        rank = ord('Z') - ord(char) + 1
                        cars[ord(char) - ord('A')] = Point(x, y)
                        ranks[ord(char) - ord('A')] = rank
                    elif char in "0123456789":
                        slots[int(char)] = Point(x, y)
        problem = ParkingProblem()
        problem.passages = passages
        problem.cars = tuple(cars[i] for i in range(len(cars)))
        problem.slots = {position:index for index, position in slots.items()}
        problem.width = width
        problem.height = height
        problem.ranks = ranks
        return problem

    # Read a parking problem from file containing a grid of tiles
    @staticmethod
    def from_file(path: str) -> 'ParkingProblem':
        with open(path, 'r') as f:
            return ParkingProblem.from_text(f.read())
    
