import time
from collections import deque
from Utilities import GlobalVariables


class WaterSortSolver:

    COMBO_SCORES = (0, 0, 1, 2, 4, 7)

    def __init__(self, original_state, height):
        self._height = height
        self._original_state = original_state

    def solve(self):
        start_time = time.time()
        time_limit = GlobalVariables.WS_SOLVER_TIME_LIMIT

        initial_state = []
        for i in range(len(self._original_state)):
            additional = [-1] * (self._height - len(self._original_state[i]))
            initial_state.append(tuple(self._original_state[i] + additional))

        initial_state = tuple(initial_state)

        visited = set()
        solution_path = {}
        queue_states = deque([initial_state])

        while len(queue_states):
            current_time = time.time()
            if current_time - start_time > time_limit:
                #print("Time!")
                return None

            queue_states = deque(sorted(queue_states, key=WaterSortSolver._calculate_score, reverse=True))
            current_state = queue_states.popleft()
            if current_state in visited:
                continue

            if WaterSortSolver._solved(current_state):
                #print(f"Done!: {len(visited)}")
                #print(current_time - start_time)
                path = []
                while current_state in solution_path:
                    path.append(current_state)
                    current_state = solution_path[current_state]
                path.append(initial_state)
                path.reverse()
                return path

            visited.add(current_state)

            for i in range(len(current_state)):
                if WaterSortSolver._is_row_filled(current_state[i]):
                    continue

                for j in range(len(current_state)):
                    if i == j:
                        continue
                    if WaterSortSolver._is_row_filled(current_state[j]) and current_state[j][0] != -1:
                        continue

                    moved_state = WaterSortSolver._move(current_state, i, j)
                    if moved_state and moved_state not in visited and moved_state not in solution_path:
                        queue_states.append(moved_state)
                        solution_path[moved_state] = current_state

        return None

    @staticmethod
    def _calculate_score(state):
        score = 0
        for flask in state:
            if flask[0] == -1:
                score += 5
            else:
                consecutive_count = 1
                for i in range(1, len(flask)):
                    if flask[i] != -1 and flask[i] == flask[i - 1]:
                        consecutive_count += 1
                    else:
                        if consecutive_count > 1:
                            score += WaterSortSolver._calculate_consecutive_score(consecutive_count,
                                                                                  i - consecutive_count == 0)
                        consecutive_count = 1
                if consecutive_count > 1:
                    score += WaterSortSolver._calculate_consecutive_score(consecutive_count, True)
        return score

    @staticmethod
    def _calculate_consecutive_score(count, at_bottom):
        score = 0
        if count >= len(WaterSortSolver.COMBO_SCORES):
            score = WaterSortSolver.COMBO_SCORES[-1]
        else:
            score = WaterSortSolver.COMBO_SCORES[count]

        return score << 1 if at_bottom else score

    @staticmethod
    def _is_row_filled(row):
        return all(element == row[-1] for element in row)

    @staticmethod
    def _solved(game_state):
        return all(WaterSortSolver._is_row_filled(row) for row in game_state)

    @staticmethod
    def _can_move(row_from, row_to):
        if row_from[0] == -1:
            return False
        if row_to[-1] != -1:
            return False
        if row_to[0] == -1:
            return True

        return WaterSortSolver._last_filled_element(row_from) == WaterSortSolver._last_filled_element(row_to)

    @staticmethod
    def _last_filled_index(row):
        i = 0
        while i < len(row) and row[i] != -1:
            i += 1
        if i:
            i -= 1
        return i

    @staticmethod
    def _last_filled_element(row):
        return row[WaterSortSolver._last_filled_index(row)]

    @staticmethod
    def _move(current_state, from_idx, to_idx):
        row_from = current_state[from_idx]
        row_to = current_state[to_idx]

        if not WaterSortSolver._can_move(row_from, row_to):
            return None

        state_list = list(current_state)
        row_from = list(row_from)
        row_to = list(row_to)

        i = WaterSortSolver._last_filled_index(row_from)
        j = WaterSortSolver._last_filled_index(row_to)
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