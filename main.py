import heapq
import random
import time
import numpy as np
from puzzle_state import PuzzleState  # Import the PuzzleState class


def create_random_puzzle():
    """
    Generates a random but solvable 8-puzzle.

    Returns:
    - A 3x3 matrix representing the initial puzzle state.
    """
    while True:
        numbers = list(range(9))
        random.shuffle(numbers)
        array = [numbers[i:i + 3] for i in range(0, 9, 3)]
        if is_solvable(array):
            return array


def get_goal_state_puzzle():
    """
    Defines the goal state of the 8-puzzle.

    Returns:
    - A 3x3 matrix representing the goal state.
    """
    return [
        [0, 1, 2],
        [3, 4, 5],
        [6, 7, 8]
    ]


def is_solvable(puzzle):
    """
    Checks if the given puzzle state is solvable.

    Parameters:
    - puzzle: A 3x3 matrix representing the puzzle state.

    Returns:
    - True if the puzzle is solvable, False otherwise.
    """
    puzzle_numbers = sum(puzzle, [])
    puzzle_numbers.remove(0)  # Ignore the blank tile
    inversions = 0
    for i in range(len(puzzle_numbers)):
        for j in range(i + 1, len(puzzle_numbers)):
            if puzzle_numbers[i] > puzzle_numbers[j]:
                inversions += 1
    return inversions % 2 == 0


def calc_manhattan_distance(puzzle, goal_state):
    """
    Calculates the Manhattan distance between the puzzle state and the goal state.

    Parameters:
    - puzzle: The current state of the puzzle as a 3x3 matrix.
    - goal_state: The goal state of the puzzle as a 3x3 matrix.

    Returns:
    - The total Manhattan distance as an integer.
    """
    distance = 0
    for i in range(len(puzzle)):
        for j in range(len(puzzle)):
            if goal_state[i][j] != puzzle[i][j] and goal_state[i][j] != 0:
                for k in range(len(goal_state)):
                    for l in range(len(goal_state)):
                        if goal_state[k][l] == puzzle[i][j]:
                            distance += abs(k - i) + abs(j - l)
    return distance


def calc_hamming_distance(puzzle, goal_state):
    """
    Calculates the Hamming distance (number of misplaced tiles).

    Parameters:
    - puzzle: The current state of the puzzle as a 3x3 matrix.
    - goal_state: The goal state of the puzzle as a 3x3 matrix.

    Returns:
    - The Hamming distance as an integer.
    """
    distance = 0
    for i in range(3):
        for j in range(3):
            if puzzle[i][j] != goal_state[i][j] and puzzle[i][j] != 0:
                distance += 1
    return distance


def find_zero(puzzle):
    """
    Finds the position of the blank tile (0) in the puzzle.

    Parameters:
    - puzzle: A 3x3 matrix representing the current state of the puzzle.

    Returns:
    - A tuple (i, j) where:
        - i: The row index of the blank tile.
        - j: The column index of the blank tile.
    """
    for i in range(len(puzzle)):
        for j in range(len(puzzle[i])):
            if puzzle[i][j] == 0:
                return (i, j)


def generate_successors(puzzle):
    """
    Generates all possible successor states of a puzzle.

    Parameters:
    - puzzle: The current state of the puzzle as a 3x3 matrix.

    Returns:
    - A list of successor states (3x3 matrices).
    """
    successors = []
    zero_pos = find_zero(puzzle)
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    for direction in directions:
        new_zero_pos = (zero_pos[0] + direction[0], zero_pos[1] + direction[1])
        if 0 <= new_zero_pos[0] < 3 and 0 <= new_zero_pos[1] < 3:
            new_puzzle = [row[:] for row in puzzle]
            # In Python, you can swap two variables in one line:
            # a, b = b, a
            #swap both
            new_puzzle[zero_pos[0]][zero_pos[1]], new_puzzle[new_zero_pos[0]][new_zero_pos[1]] = \
                new_puzzle[new_zero_pos[0]][new_zero_pos[1]], new_puzzle[zero_pos[0]][zero_pos[1]]
            successors.append(new_puzzle)
    return successors


def a_star(puzzle, goal_state, heuristic):
    """
    Runs the A* algorithm to solve the puzzle.

    Parameters:
    - puzzle: The start state of the puzzle as a 3x3 matrix.
    - goal_state: The goal state of the puzzle as a 3x3 matrix.
    - heuristic: The heuristic function (Hamming or Manhattan).

    Returns:
    - A tuple containing the path cost (g) and the number of expanded nodes.
    """
    open_list = []
    heapq.heappush(open_list, PuzzleState(puzzle, g=0, h=heuristic(puzzle, goal_state)))
    closed_list = set()
    expanded_nodes = 0

    while open_list:
        current_state = heapq.heappop(open_list)
        expanded_nodes += 1

        if str(current_state.puzzle) in closed_list:
            continue
        closed_list.add(str(current_state.puzzle))

        if current_state.puzzle == goal_state:
            return current_state.g, expanded_nodes

        for successor in generate_successors(current_state.puzzle):
            if str(successor) not in closed_list:
                new_g = current_state.g + 1
                h = heuristic(successor, goal_state)
                neighbor_state = PuzzleState(successor, new_g, h)
                heapq.heappush(open_list, neighbor_state)


def main():
    """
    Runs the 8-puzzle simulation with Hamming and Manhattan heuristics.
    Measures total time, memory effort (nodes expanded), runtime for 100 random puzzles.        Provides mean and standard deviation of these metrics for each heuristic.
    """
    print("Starting the program...")
    goal_state = get_goal_state_puzzle()
    puzzles = [create_random_puzzle() for _ in range(100)]

    hamming_results = []
    manhattan_results = []

    hamming_total_time = 0
    manhattan_total_time = 0

    for puzzle in puzzles:
        # Run A* with Hamming Heuristic
        start_time = time.time()
        cost, expanded_nodes = a_star(puzzle, goal_state, calc_hamming_distance)
        elapsed_time = time.time() - start_time
        hamming_total_time += elapsed_time
        hamming_results.append((cost, expanded_nodes, elapsed_time))

        # Run A* with Manhattan Heuristic
        start_time = time.time()
        cost, expanded_nodes = a_star(puzzle, goal_state, calc_manhattan_distance)
        elapsed_time = time.time() - start_time
        manhattan_total_time += elapsed_time
        manhattan_results.append((cost, expanded_nodes, elapsed_time))

    # Output for Hamming-Heuristic
    print("\nHamming Heuristic:")
    costs = [r[0] for r in hamming_results]
    expanded_nodes = [r[1] for r in hamming_results]
    times = [r[2] for r in hamming_results]
    print(f"Total time: {hamming_total_time:.4f} seconds")
    print(f"Average time: {sum(times) / len(times):.4f} seconds")
    print(f"Total nodes expanded: {sum(expanded_nodes)}")
    print(f"Average nodes expanded: {sum(expanded_nodes) / len(expanded_nodes):.2f}")
    print(f"Average cost: {sum(costs) / len(costs):.2f}")

    # Output for Manhattan-Heuristic
    print("\nManhattan Heuristic:")
    costs = [r[0] for r in manhattan_results]
    expanded_nodes = [r[1] for r in manhattan_results]
    times = [r[2] for r in manhattan_results]
    print(f"Total time: {manhattan_total_time:.4f} seconds")
    print(f"Average time: {sum(times) / len(times):.4f} seconds")
    print(f"Total nodes expanded: {sum(expanded_nodes)}")
    print(f"Average nodes expanded: {sum(expanded_nodes) / len(expanded_nodes):.2f}")
    print(f"Average cost: {sum(costs) / len(costs):.2f}")


if __name__ == '__main__':
    main()
