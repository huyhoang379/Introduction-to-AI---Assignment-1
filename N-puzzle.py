import copy
import random

class NPuzzleIDDFS:
    def __init__(self, start, goal, max_depth=30):
        self.start = start
        self.goal = goal
        self.size = len(start)
        self.max_depth = max_depth

    def get_blank_position(self, state):
        for i in range(self.size):
            for j in range(self.size):
                if state[i][j] == 0:
                    return i, j

    def is_goal(self, state):
        return state == self.goal

    def move(self, state, direction):
        x, y = self.get_blank_position(state)
        new_state = copy.deepcopy(state)

        if direction == 'up' and x > 0:
            new_state[x][y], new_state[x-1][y] = new_state[x-1][y], new_state[x][y]
        elif direction == 'down' and x < self.size - 1:
            new_state[x][y], new_state[x+1][y] = new_state[x+1][y], new_state[x][y]
        elif direction == 'left' and y > 0:
            new_state[x][y], new_state[x][y-1] = new_state[x][y-1], new_state[x][y]
        elif direction == 'right' and y < self.size - 1:
            new_state[x][y], new_state[x][y+1] = new_state[x][y+1], new_state[x][y]

        return new_state

    # Iterative Deepening DFS
    def iddfs(self):
        for depth in range(1, self.max_depth + 1):
            print(f"Trying depth limit: {depth}")
            visited = set()
            result = self.dls(self.start, visited, depth, None)
            if result:
                return result
        return None

    # Depth-Limited Search
    def dls(self, state, visited, depth, last_move):
        if self.is_goal(state):
            return [state]
        if depth == 0:
            return None

        visited.add(self.state_to_tuple(state))
        directions = ['up', 'down', 'left', 'right']

        for direction in directions:
            if (last_move == 'up' and direction == 'down') or \
               (last_move == 'down' and direction == 'up') or \
               (last_move == 'left' and direction == 'right') or \
               (last_move == 'right' and direction == 'left'):
                continue

            new_state = self.move(state, direction)
            state_tuple = self.state_to_tuple(new_state)

            if state_tuple not in visited:
                result = self.dls(new_state, visited, depth - 1, direction)
                if result:
                    return [state] + result

        visited.remove(self.state_to_tuple(state))
        return None

    def state_to_tuple(self, state):
        return tuple(tuple(row) for row in state)

    def solve(self):
        return self.iddfs()
    
# Check if the puzzle is solvable
def is_solvable(state, n):
    # Flatten the puzzle and remove the blank (0)
    one_d_state = [num for row in state for num in row if num != 0]

    # Count inversions
    inversions = 0
    for i in range(len(one_d_state)):
        for j in range(i + 1, len(one_d_state)):
            if one_d_state[i] > one_d_state[j]:
                inversions += 1

    # Find the row of the blank (0) from the bottom
    blank_row_from_bottom = n - [row.index(0) for row in state if 0 in row][0] // n

    # Check solvability
    if n % 2 != 0:
        return inversions % 2 == 0
    else:
        return (inversions % 2 == 0) == (blank_row_from_bottom % 2 != 0)
    
def generate_random_puzzle(n):
    state = list(range(n * n))
    random.shuffle(state)
    puzzle = [state[i * n:(i + 1) * n] for i in range(n)]
    return puzzle

def generate_goal_state(n):
    goal = [0] + list(range(1, n * n)) 
    # goal = list(range(1, n * n)) + [0]
    return [goal[i * n:(i + 1) * n] for i in range(n)]

# Test case
n = 3
# start_state = [
#     [8, 7, 1],
# [4, 6, 2],
# [3, 5, 0]
# ]
start_state = generate_random_puzzle(n)
print("Start state:")
for row in start_state:
    print(row)
print()
goal_state = generate_goal_state(n)

# Check if the puzzle is solvable before creating the solver
if is_solvable(start_state, n):
    print("The puzzle is solvable.")
    print()
    # Create and solve
    n_puzzle_iddfs = NPuzzleIDDFS(start_state, goal_state, max_depth=30)
    solution = n_puzzle_iddfs.solve()

    if solution:
        for step, state in enumerate(solution):
            print(f"Step {step}:")
            for row in state:
                print(row)
            print()
    else:
        print("No solution found within depth limit.")
else:
    print("The puzzle is unsolvable.")