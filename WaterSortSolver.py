import time
from collections import deque

class Solver:

    TIME_LIMIT = 5

    def __init__(self, original_state, height):
        self.height = height
        self.original_state = original_state

    def solve(self):
        start_time = time.time()
        time_limit = Solver.TIME_LIMIT

        initial_state = []
        for i in range(len(self.original_state)):
            additional = [-1] * (self.height - len(self.original_state[i]))
            initial_state.append(tuple(self.original_state[i] + additional))

        initial_state = tuple(initial_state)

        visited = set()
        solution_path = {}
        queue_states = deque([initial_state])

        while len(queue_states):
            current_time = time.time()
            if current_time - start_time > time_limit:
                print("Time!")
                return None

            current_state = queue_states.popleft()
            if current_state in visited:
                continue

            if Solver.solved(current_state):
                print(f"Done!: {len(visited)}")
                path = []
                while current_state in solution_path:
                    path.append(current_state)
                    current_state = solution_path[current_state]
                path.append(initial_state)
                path.reverse()
                return path

            visited.add(current_state)

            for i in range(len(current_state)):
                if Solver.is_row_filled(current_state[i]):
                    continue

                for j in range(len(current_state)):
                    if i == j:
                        continue
                    if Solver.is_row_filled(current_state[j]) and current_state[j][0] != -1:
                        continue

                    moved_state = Solver.move(current_state, i, j)
                    if moved_state and moved_state not in visited and moved_state not in solution_path:
                        queue_states.append(moved_state)
                        solution_path[moved_state] = current_state

        return None

    def set_up(self, list_for_array):
        additional = [-1] * (self.height - len(list_for_array))
        return tuple(list_for_array + additional)

    @staticmethod
    def is_row_filled(row):
        return all(element == row[-1] for element in row)

    @staticmethod
    def solved(game_state):
        return all(Solver.is_row_filled(row) for row in game_state)

    @staticmethod
    def can_move(row_from, row_to):
        if row_from[0] == -1:
            return False
        if row_to[-1] != -1:
            return False
        if row_to[0] == -1:
            return True

        return Solver.last_filled_element(row_from) == Solver.last_filled_element(row_to)

    @staticmethod
    def last_filled_index(row):
        i = 0
        while i < len(row) and row[i] != -1:
            i += 1
        if i:
            i -= 1
        return i

    @staticmethod
    def last_filled_element(row):
        return row[Solver.last_filled_index(row)]

    @staticmethod
    def move(current_state, from_idx, to_idx):
        row_from = current_state[from_idx]
        row_to = current_state[to_idx]

        if not Solver.can_move(row_from, row_to):
            return None

        state_list = list(current_state)
        row_from = list(row_from)
        row_to = list(row_to)

        i = Solver.last_filled_index(row_from)
        j = Solver.last_filled_index(row_to)
        if row_to[j] != -1:
            j += 1

        while i >= 0 and j < len(row_to) and (row_from[i] == row_to[j - 1] or row_to[j - 1] == -1):
            row_to[j] = row_from[i]
            row_from[i] = -1
            i -= 1
            j += 1

        state_list[from_idx] = tuple(row_from)
        state_list[to_idx] = tuple(row_to)

        return tuple(state_list)