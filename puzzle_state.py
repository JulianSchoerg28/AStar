class PuzzleState:
    """
    Class representing a state in the 8-puzzle problem.

    Attributes:
    - puzzle: The current state of the puzzle as a 3x3 matrix.
    - g: The cost from the start state to this state (path cost).
    - h: The heuristic cost (estimated cost to the goal).
    - f: The total cost, calculated as f = g + h.
    """
    def __init__(self, puzzle, g, h):
        """
        Initialize a new PuzzleState.

        Parameters:
        - puzzle: A 3x3 matrix representing the puzzle state.
        - g: The cost from the start state to this state.
        - h: The heuristic cost (estimated cost to the goal).
        """
        self.puzzle = puzzle
        self.g = g
        self.h = h
        self.f = g + h

    def __lt__(self, other):
        """
        Comparison operator for priority queue sorting.
        States with lower total cost (f) are given priority.

        Parameters:
        - other: Another PuzzleState to compare against.
        """
        return self.f < other.f
