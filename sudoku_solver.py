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
    """Return a PropKB encoding this n x n Sudoku's constraints plus the given
    cells, as general clauses.

    Parameters
    ----------
    n, box_h, box_w : int
    givens : dict[(int, int), int]

    Returns
    -------
    PropKB
    """
    raise NotImplementedError(
        'build_general_kb: encode the puzzle as general clauses'
    )


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
                        if r2 != r and c2 != c:
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
    """Your own backward-chaining implementation.

    Parameters
    ----------
    kb : PropDefiniteKB
    query : Expr

    Returns
    -------
    bool
    """
    raise NotImplementedError(
        'pl_bc_entails: implement backward chaining, soundly'
    )


def solve_full_grid_bc(n, box_h, box_w, givens):
    """Solve the whole puzzle using build_definite_kb + your own pl_bc_entails.

    For each cell, try each candidate value until pl_bc_entails confirms one
    -- the same per-cell strategy as solve_full_grid_fc, but backed by
    backward chaining instead of a single shared forward-chaining pass.

    Returns
    -------
    dict[(int, int), int] -- {(row, col): value} for every cell
    """
    raise NotImplementedError(
        'solve_full_grid_bc: solve every cell with backward chaining'
    )
