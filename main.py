import heapq
import random
import time
import numpy as np


def create_random_puzzle():
    while True:
        numbers = list(range(9))
        random.shuffle(numbers)
        array = [numbers[i:i + 3] for i in range(0, 9, 3)]
        if is_solvable(array):
            return array


def get_goal_state_puzzle():
    return [
        [0, 1, 2],
        [3, 4, 5],
        [6, 7, 8]
    ]


def is_solvable(puzzle):
    puzzle_numbers = sum(puzzle, [])
    puzzle_numbers.remove(0)
    inversions = 0
    for i in range(len(puzzle_numbers)):
        for j in range(i + 1, len(puzzle_numbers)):
            if puzzle_numbers[i] > puzzle_numbers[j]:
                inversions += 1
    return inversions % 2 == 0


def calc_manhattan_distance(puzzle, goal_state):
    distance = 0

    for i in range(len(puzzle)):
        for j in range(len(puzzle)):
            if goal_state[i][j] != puzzle[i][j] and goal_state[i][j] != 0:
                # oberhalb findet er alle ungleichen
                # unten sucht er die dann im goalstate array
                for k in range(len(goal_state)):
                    for l in range(len(goal_state)):
                        # und wenn er dann die pos im goal state hat, berechnet er die manhattan distance :D
                        if goal_state[k][l]  == puzzle[i][j]:
                            distance += abs(k - i) + abs(j - l)

    return distance


def calc_hamming_distance(puzzle, goal_state):
    distance = 0
    for i in range(3):
        for j in range(3):
            if puzzle[i][j] != goal_state[i][j] and puzzle[i][j] != 0:
                distance += 1
    return distance


def generate_successors(puzzle):
    successors = []
    zero_pos = [(i, row.index(0)) for i, row in enumerate(puzzle) if 0 in row][0]
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    for direction in directions:
        new_zero_pos = (zero_pos[0] + direction[0], zero_pos[1] + direction[1])
        if 0 <= new_zero_pos[0] < 3 and 0 <= new_zero_pos[1] < 3:
            new_puzzle = [row[:] for row in puzzle]
            new_puzzle[zero_pos[0]][zero_pos[1]], new_puzzle[new_zero_pos[0]][new_zero_pos[1]] = \
                new_puzzle[new_zero_pos[0]][new_zero_pos[1]], new_puzzle[zero_pos[0]][zero_pos[1]]
            successors.append(new_puzzle)
    return successors


def a_star(puzzle, goal_state, heuristic):
    open_list = []
    heapq.heappush(open_list, (0, puzzle, 0))
    closed_list = set()
    expanded_nodes = 0

    while open_list:
        _, current, cost = heapq.heappop(open_list)
        expanded_nodes += 1
        if str(current) in closed_list:
            continue
        closed_list.add(str(current))

        if current == goal_state:
            return cost, expanded_nodes

        for successor in generate_successors(current):
            if str(successor) not in closed_list:
                new_cost = cost + 1
                heuristic_cost = heuristic(successor, goal_state)
                heapq.heappush(open_list, (new_cost + heuristic_cost, successor, new_cost))


def main():
    goal_state = get_goal_state_puzzle()
    puzzles = [create_random_puzzle() for _ in range(100)]

    hamming_results = []
    manhattan_results = []

    for puzzle in puzzles:
        for heuristic, results in [(calc_hamming_distance, hamming_results), (calc_manhattan_distance, manhattan_results)]:
            start_time = time.time()
            cost, expanded_nodes = a_star(puzzle, goal_state, heuristic)
            elapsed_time = time.time() - start_time
            results.append((cost, expanded_nodes, elapsed_time))

    for name, results in [("Hamming", hamming_results), ("Manhattan", manhattan_results)]:
        costs, expanded_nodes, times = zip(*results)
        print(f"\n{name} Heuristic:")
        print(f"Average cost: {np.mean(costs):.2f}, Std Dev: {np.std(costs):.2f}")
        print(f"Average expanded nodes: {np.mean(expanded_nodes):.2f}, Std Dev: {np.std(expanded_nodes):.2f}")
        print(f"Average time: {np.mean(times):.4f} seconds, Std Dev: {np.std(times):.4f}")


if __name__ == '__main__':
    main()
