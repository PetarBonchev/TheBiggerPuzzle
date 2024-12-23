import io
import pickle
from collections import deque

import numpy as np


class Solver:
    def __init__(self, original_state, height):
        self.height = height
        self.original_state = original_state

    def solve(self):
        initial_state = []
        for i in range(len(self.original_state)):
            additional = [-1] * (self.height - len(self.original_state[i]))
            initial_state.append(np.array(self.original_state[i] + additional))

        initial_state = np.array(initial_state, dtype=object)

        visited = set()

        queue_states = deque([initial_state])

        while len(queue_states):

            current_state = queue_states.popleft()
            hashed_state = Solver.encode_state(current_state)

            if hashed_state in visited:
                continue

            if Solver.solved(current_state):
                print(current_state)
                print(len(visited))
                break

            visited.add(hashed_state)

            for i in range(len(current_state)):
                if Solver.is_row_filled(current_state[i]):
                    continue

                for j in range(len(current_state)):
                    if i == j:
                        continue
                    if Solver.is_row_filled(current_state[j]) and current_state[j][0] != -1:
                        continue

                    moved_state = current_state.copy()
                    Solver.move(moved_state[i], moved_state[j])
                    queue_states.append(moved_state)


    def set_up(self, list_for_array):
        additional = [-1] * (self.height - len(list_for_array))
        return np.array(list_for_array + additional)


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
    def move(row_from, row_to):
        if not Solver.can_move(row_from, row_to):
            return

        i = Solver.last_filled_index(row_from)
        j = Solver.last_filled_index(row_to)
        if row_to[j] != -1:
            j += 1

        while i >= 0 and j < len(row_to) and (row_from[i] == row_to[j - 1] or row_to[j - 1] == -1):
            row_to[j] = row_from[i]
            row_from[i] = -1
            i -= 1
            j += 1

    @staticmethod
    def encode_state(state):
        buffer = io.BytesIO()
        pickle.dump(state, buffer)
        return buffer.getvalue().decode('latin1')

# Example usage:
s = Solver([ [0,2,3,1], [2,0,1,3], [2,3,0,1], [1,0,3,2], [], []], 4)
s.solve()

