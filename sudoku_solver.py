"""IT5005 Assignment 1: student implementation file.

Implement the functions marked below. Do not modify utils.py or logic_.py.
"""

from utils import *
from logic_ import *


# Do not change this function; it is used to create atomic propositions.
def atom(prefix, r, c, v):
    """prefix is 'Is' or 'Not'. Returns the Expr for e.g. Is3_2_4."""
    return expr(f'{prefix}{r}_{c}_{v}')


def build_general_kb(n, box_h, box_w, givens):
    """Return a PropKB with Sudoku rules and the given cell values.

    Parameters
    ----------
    n, box_h, box_w : int
        Grid size and box dimensions; box_h * box_w must equal n.
    givens : dict[(int, int), int]
        Given values, with rows, columns and values numbered from 1 to n.

    Returns
    -------
    PropKB
        CNF clauses using Is symbols and their logical negations.
    """
    for size in (n, box_h, box_w):
        if type(size) is not int or size < 1:
            raise ValueError("Grid and box dimensions must be positive integers")
    if box_h * box_w != n:
        raise ValueError("Each box must contain n cells")
    for (r, c), v in givens.items():
        for number in (r, c, v):
            if type(number) is not int or not 1 <= number <= n:
                raise ValueError("Given coordinates and values must be in 1..n")

    kb = PropKB()

    # Rule 1: Each cell has at least one value.
    for r in range(1, n + 1):
        for c in range(1, n + 1):
            values = []
            for v in range(1, n + 1):
                values.append(atom("Is", r, c, v))
            kb.tell(associate("|", values))

    # Rule 2: Each cell has at most one value.
    # Starting v2 at v1 + 1 checks each pair of values once.
    for r in range(1, n + 1):
        for c in range(1, n + 1):
            for v1 in range(1, n + 1):
                for v2 in range(v1 + 1, n + 1):
                    kb.tell(~atom("Is", r, c, v1) | ~atom("Is", r, c, v2))

    # Rule 3: Two cells in the same row cannot have the same value.
    for r in range(1, n + 1):
        for v in range(1, n + 1):
            for c1 in range(1, n + 1):
                for c2 in range(c1 + 1, n + 1):
                    kb.tell(~atom("Is", r, c1, v) | ~atom("Is", r, c2, v))

    # Rule 4: Two cells in the same column cannot have the same value.
    for c in range(1, n + 1):
        for v in range(1, n + 1):
            for r1 in range(1, n + 1):
                for r2 in range(r1 + 1, n + 1):
                    kb.tell(~atom("Is", r1, c, v) | ~atom("Is", r2, c, v))

    # Rule 5: Two cells in the same box cannot have the same value.
    for box_r in range(1, n + 1, box_h):
        for box_c in range(1, n + 1, box_w):
            cells = []
            for r in range(box_r, box_r + box_h):
                for c in range(box_c, box_c + box_w):
                    cells.append((r, c))
            for i in range(len(cells)):
                for j in range(i + 1, len(cells)):
                    r1, c1 = cells[i]
                    r2, c2 = cells[j]
                    for v in range(1, n + 1):
                        kb.tell(~atom("Is", r1, c1, v) | ~atom("Is", r2, c2, v))

    # Rule 6: Add each given value as a fact (a positive unit clause).
    for (r, c), v in givens.items():
        kb.tell(atom("Is", r, c, v))

    return kb


def solve_full_grid_general(n, box_h, box_w, givens, method="resolution"):
    """Query every cell/value using the supplied general-KB algorithms.

    method is 'resolution' for pl_resolution, or 'tt' for tt_entails.
    Return {(row, column): value}; cells with no entailed value are omitted.
    Raise ValueError if more than one value is entailed for a cell.
    A 9x9 run may take too long; use a small grid to test the full loop.
    """
    if method not in ("resolution", "tt"):
        raise ValueError("method must be 'resolution' or 'tt'")

    kb = build_general_kb(n, box_h, box_w, givens)
    if method == "tt":
        sentence = associate("&", kb.clauses)

    solved = {}
    for r in range(1, n + 1):
        for c in range(1, n + 1):
            entailed_values = []
            for v in range(1, n + 1):
                query = atom("Is", r, c, v)
                if method == "resolution":
                    entailed = pl_resolution(kb, query)
                else:
                    # tt_entails takes a sentence, not a PropKB object.
                    entailed = tt_entails(sentence, query)
                if entailed:
                    entailed_values.append(v)
            if len(entailed_values) > 1:
                raise ValueError(f"Inconsistent KB at cell ({r}, {c})")
            if len(entailed_values) == 1:
                solved[(r, c)] = entailed_values[0]
    return solved


def build_definite_kb(n, box_h, box_w, givens):
    """Return a PropDefiniteKB encoding this n x n Sudoku's constraints plus
    the given cells, using elimination + last-candidate reasoning.

    Parameters
    ----------
    n, box_h, box_w : int
    givens : dict[(int, int), int] -- {(row, col): value}, 1-indexed

    Returns
    -------
    PropDefiniteKB
    """
    # raise NotImplementedError(
    #     'build_definite_kb: encode the puzzle as definite clauses'
    # )

    kb = PropDefiniteKB()

    # Rule 1:
    # Every cell has at least one value.
    # If all values except v have been eliminated,
    # the cell must have value v.
    for r in range(1, n+1):
        for c in range(1, n+1):
            for v in range(1, n+1):
                not_atoms = [atom("Not", r, c, v2) for v2 in range(1, n+1) if v2 != v]
                kb.tell(Expr('==>', associate("&", not_atoms), atom("Is", r, c, v)))

    # Rule 2:
    # Every cell has at most one value.
    # Is_r_c_v => Not_r_c_v2 for all v2 != v
    for r in range(1, n+1):
        for c in range(1, n+1):
            for v in range(1, n+1):
                for v2 in range(1, n+1):
                    if v != v2:
                        kb.tell(Expr('==>', atom("Is", r, c, v), atom("Not", r, c, v2)))

    # Rule 3:
    # No two cells in the same row have the same value.
    # Is_r_c_v => Not_r_c2_v for all c2 != c
    for r in range(1, n+1):
        for c in range(1, n+1):
            for v in range(1, n+1):
                for c2 in range(1, n+1):
                    if c != c2:
                        kb.tell(Expr('==>', atom("Is", r, c, v), atom("Not", r, c2, v)))

    # Rule 4:
    # No two cells in the same column have the same value.
    # Is_r_c_v => Not_r2_c_v for all r2 != r
    for c in range(1, n+1):
        for r in range(1, n+1):
            for v in range(1, n+1):
                for r2 in range(1, n+1):
                    if r != r2:
                        kb.tell(Expr('==>', atom("Is", r, c, v), atom("Not", r2, c, v)))

    # Rule 5:
    # No two cells in the same box have the same value.
    # Is_r_c_v => Not_r2_c2_v for all (r2, c2) in the same box as (r, c)
    for r in range(1, n+1):
        for c in range(1, n+1):
            for v in range(1, n+1):
                box_start_r = r - (r - 1) % box_h
                box_start_c = c - (c - 1) % box_w
                for r2 in range(box_start_r, box_start_r + box_h):
                    for c2 in range(box_start_c, box_start_c + box_w):
                        if (r2, c2) != (r, c):
                            kb.tell(Expr('==>', atom("Is", r, c, v), atom("Not", r2, c2, v)))

    # Rule 6:
    # Every given cell has its stated value.
    for (r, c), v in givens.items():
        kb.tell(atom("Is", r, c, v))

    return kb



def solve_full_grid_fc(n, box_h, box_w, givens):
    """Solve the whole puzzle using build_definite_kb + pl_fc_entails.

    Returns
    -------
    dict[(int, int), int] -- {(row, col): value} for every cell
    """
    # raise NotImplementedError(
    #     'solve_full_grid_fc: solve every cell with forward chaining'
    # )

    kb = build_definite_kb(n, box_h, box_w, givens)
    solution = {}
    for r in range(1, n+1):
        for c in range(1, n+1):
            for v in range(1, n+1):
                if pl_fc_entails(kb, atom("Is", r, c, v)):
                    solution[(r, c)] = v
                    break
            if (r, c) not in solution:
                raise ValueError(f"No entailed value for cell ({r}, {c})")

    return solution


def pl_bc_entails(kb, query):
    """Backward chaining for a definite-clause knowledge base."""

    # 根据规则结论建立索引
    rules_by_conclusion = {}

    for clause in kb.clauses:
        if clause.op == "==>":
            conclusion = clause.args[1]

            rules_by_conclusion.setdefault(
                conclusion, []
            ).append(clause)

    # 只缓存已经成功证明的目标
    proven = set()

    def prove(goal, visiting):
        # 1. 如果 goal 是已知事实，直接成功
        if goal in kb.clauses:
            return True

        # 2. 如果之前已经成功证明过，直接成功
        if goal in proven:
            return True

        # 3. 当前路径出现循环，停止这条路径
        if goal in visiting:
            return False

        new_visiting = visiting | {goal}

        # 4. 查找所有结论等于 goal 的规则
        for rule in rules_by_conclusion.get(goal, []):
            premises = conjuncts(rule.args[0])

            # 规则的所有前提都必须能够证明
            all_proved = True

            for premise in premises:
                if not prove(premise, new_visiting):
                    all_proved = False
                    break

            if all_proved:
                proven.add(goal)
                return True

        # 不缓存 False，避免循环导致错误的永久失败
        return False

    return prove(query, set())


def solve_full_grid_bc(n, box_h, box_w, givens):
    """Solve the whole puzzle using build_definite_kb + pl_bc_entails.

    Returns
    -------
    dict[(int, int), int] -- {(row, col): value} for every cell
    """
    kb = build_definite_kb(n, box_h, box_w, givens)
    solution = {}

    for r in range(1, n + 1):
        for c in range(1, n + 1):
            for v in range(1, n + 1):
                if pl_bc_entails(kb, atom("Is", r, c, v)):
                    solution[(r, c)] = v
                    break

            if (r, c) not in solution:
                raise ValueError(f"No entailed value for cell ({r}, {c})")

    return solution

