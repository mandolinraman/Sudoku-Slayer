def best_matching(cells, vals):
    inactive = set()
    active = set()

    def find_inactive(index=0, cell_set=set(), val_set=set()):
        # finds inactive edges and some active edges,
        # returns True if it's an imposible situation
        if index >= len(cells):
            return False

        # Case 1: index isn't in cutset:
        # Optimization: if cells[index] is a singeton set, there's no need to exclude it from the cutset:
        # including it will always be better, i.e we'll do only case 2 for those indices:
        if len(cells[index]) > 1:
            if find_inactive(index + 1, cell_set, val_set):
                return True  # impossible

        # Case 2: index is in cutset:
        new_cell_set = set.union(cell_set, {index})
        new_val_set = set.union(val_set, cells[index])
        edges = {(u, v) for v in new_val_set for u in vals[v] if u not in new_cell_set}

        num_cells = len(new_cell_set)
        num_vals = len(new_val_set)
        num_edges = len(edges)

        if num_vals < num_cells or num_vals > num_cells + num_edges:
            return True  # impossible

        if num_vals == num_cells:
            # print(f"l_set = {new_cell_set}, r_set = {new_val_set}:")
            # print(f"  -> Found inactive edges: {edges}")
            inactive.update(edges)
        elif num_vals == num_cells + num_edges:
            # print(f"l_set = {new_cell_set}, r_set = {new_val_set}:")
            # print(f"  -> Found active edges: {edges}")
            active.update(edges)  # won't find all active ones though :()

        return find_inactive(index + 1, new_cell_set, new_val_set)

    # call this local function
    if find_inactive():
        # impossible situation
        return []
    else:
        # we'd have saved the inactive and active edges detected:
        return [inactive, active]


def update_terminal_nodes(left, right, i):
    # If we have degree == 1 on the left side, then it's an active edge.
    # prune edges that are inactive and recursively process nodes on the left side.
    changed = False
    r_set = left[i]
    # r_set is a set of int values
    if len(r_set) == 1:
        r_val = list(r_set)[0]  # extract that one value
        # we pair: i <-> r_val
        l_vals = list(right[r_val])
        for j in l_vals:
            if j != i:
                # disconnect r_val and j
                left[j].remove(r_val)
                right[r_val].remove(j)
                changed = True
                _ = update_terminal_nodes(left, right, j)
        # right[r_val].intersection_update({i})

    return changed


def reduce_group(cells):
    changed = False
    vals = [set() for _ in range(10)]
    chosen = set()
    for i, val_set in enumerate(cells):
        # # if singleton, just skip it
        # if len(val_set) == 1:
        #     chosen.add(list(val_set)[0])
        # else:
        #     pass
        for val in val_set:
            vals[val].add(i)

    result = best_matching(cells, vals)
    if len(result) == 0:
        return False, True

    inactive, active = result

    # remove inactive edges
    for i, j in inactive:
        cells[i].remove(j)
        vals[j].remove(i)
        changed = True

    # Active edges? we may not have a complete list of active edges :(
    # But they'll get found in the next step where we look for nodes with degree==1.

    for i in range(len(cells)):
        changed = update_terminal_nodes(cells, vals, i) or changed

    for j in range(len(vals)):
        changed = update_terminal_nodes(vals, cells, j) or changed

    return changed, False


def int2set(n):
    result = set()
    pos = 0
    while n > 0:
        digit = n % 2
        if digit > 0:
            result.add(pos)

        n = n // 2
        pos += 1

    return result


def balanced(s, n=3):
    ns = [0] * n
    for i in s:
        ns[i // n] += 1

    return max(ns) <= min(ns) + 1


def tighten_better(cells, universal_set):
    n = len(cells)

    upper = {0: universal_set.copy()}
    lower = {0: universal_set.copy()}
    for r in range(1, 2**n - 1):
        js = int2set(r)
        i = len(js) - 1
        upper[r] = set()
        lower[r] = set()
        if balanced(js):
            for j in js:
                upper[r].update(set.intersection(cells[i][j], upper[r - 2**j]))
                lower[r].update(set.intersection(cells[n - 1 - i][j], lower[r - 2**j]))

    result = [[set() for _ in range(n)] for _ in range(n)]
    for r in range(1, 2**n):
        js = int2set(r)
        i = len(js) - 1
        rc = 2**n - 1 - r
        # this check is optional; if js is unbanalced then lower[rc] would be empty anyway
        if balanced(js):
            for j in js:
                product = set.intersection(cells[i][j], upper[r - 2**j], lower[rc])
                result[i][j].update(product)

    changed = False
    for i in range(n):
        for j in range(n):
            length = len(cells[i][j])
            cells[i][j].intersection_update(result[i][j])
            changed = changed or (len(cells[i][j]) < length)

    return changed


class Sudoku:
    def __init__(self, puzzle):
        if isinstance(puzzle, str):
            self.puzzle = [
                [(int(c) if "0" <= c <= "9" else 0) for c in puzzle[i * 9 : i * 9 + 9]]
                for i in range(9)
            ]
        else:
            self.puzzle = [row.copy() for row in puzzle]  # deep copy

        self.cells = [[set() for _ in range(9)] for _ in range(9)]
        for i in range(9):
            for j in range(9):
                c = self.puzzle[i][j]
                if c == 0:
                    self.cells[i][j] = set(range(1, 10))
                else:
                    self.cells[i][j] = {c}

        self.solution = [[0] * 9 for _ in range(9)]
        self.distance = 0
        self.update_solution()
        self.impossible = False

        self.groups = []
        for i in range(9):
            self.groups.append([self.cells[i][j] for j in range(9)])  # rows
            self.groups.append([self.cells[j][i] for j in range(9)])  # cols
            self.groups.append(
                [
                    self.cells[3 * (i // 3) + j // 3][3 * (i % 3) + j % 3]
                    for j in range(9)
                ]
            )

    def update_solution(self):
        self.distance = 0
        for i in range(9):
            for j in range(9):
                self.distance += len(self.cells[i][j]) - 1
                if len(self.cells[i][j]) == 1:
                    self.solution[i][j] = list(self.cells[i][j])[0]

        self.solved = self.distance == 0

    def iterate(self, callback=None):
        counter = 0
        while True:
            init_dist = self.distance  # get init distance from solution
            if callback is not None:
                # print(f"Counter = {counter}")
                # print(f"-> Distance = {self.distance}")
                # print(f"-> Drawing frame {counter}a")
                # self.draw(f"{callback}{counter:03}a.pdf")
                callback(self, counter)

            # exchange info within each group
            for g in range(27):
                # in each group, update the variables
                _, impossible = reduce_group(self.groups[g])
                if impossible:
                    self.impossible = True
                    break

            if callback is not None:
                # print(f"-> Distance = {self.distance}")
                # print(f"-> Drawing frame {counter}b")
                # self.draw(f"{callback}{counter:03}b.pdf")
                callback(self, counter)

            # exchange info across group
            tighten_better(self.cells, set(range(1, 10)))

            # update self.solution
            self.update_solution()

            if self.impossible or self.distance == init_dist:
                break

            counter += 1

    def solve(self, callback=None):
        # first try iterative algorithm
        self.iterate(callback)

        if self.solved or self.impossible:
            return

        # if not solved and not impossible try a tree search:
        pass
