import json
import time
import streamlit as st
from utils import *
from logic_ import *
from sudoku_solver import (
    atom,
    build_definite_kb,
    build_general_kb,
    solve_full_grid_fc,
    solve_full_grid_bc,
    pl_bc_entails,
)

st.title('Sudoku Solver')

with open('puzzles.json') as f:
    pool = json.load(f)

# --- 1. Puzzle selection & visual board display ---
# TODO: a dropdown/selectbox to pick a puzzle by index from pool['puzzles'].
# TODO: render the grid (e.g. a table or grid of st.columns), showing given
# cells and empty cells differently (e.g. bold givens, blank otherwise).
st.subheader("Sudoku Board")

givens = puzzles["givens"]

for row in givens:

    cols = st.columns(len(row))

    for i, value in enumerate(row):

        if value == 0:

            cols[i].write("")

        else:

            cols[i].write(f"**{value}**")
# --- 2. Full-grid auto-solver, with algorithm selection ---
# TODO: a radio/selectbox letting the user choose forward chaining
# (solve_full_grid_fc) or backward chaining (solve_full_grid_bc).
# TODO: a button that times and calls the chosen solver on
# (n, box_h, box_w, givens), then displays the solved grid and the elapsed
# time.
st.subheader("Full-grid Solver")

algorithm = st.radio(

    "Choose algorithm",

    ["Forward Chaining", "Backward Chaining"]

)

if st.button("Solve Full Grid"):

    if algorithm == "Forward Chaining":

        start_time = time.perf_counter()

        solution = solve_full_grid_fc(

            n,

            box_h,

            box_w,

            givens

        )

        elapsed = time.perf_counter() - start_time

        st.success("Solved using Forward Chaining!")

        st.write(f"Elapsed time: {elapsed:.6f} seconds")

        for r in range(1, n + 1):

            cols = st.columns(n)

            for c in range(1, n + 1):

                cols[c - 1].write(f"**{solution[(r, c)]}**")

    else:

        st.info("Backward Chaining is not implemented yet.")

# --- 3. Targeted cell entailment query ---
# TODO: number inputs for row (r), column (c), value (v).
# TODO: a button that builds the definite KB, calls
# pl_bc_entails(kb, atom('Is', r, c, v)), and displays True/False.

# --- 4. Reasoning trace ("tutor mode") ---
# TODO: instrument your forward- or backward-chaining approach to record each
# reasoning step (which rule fired, on what premises, producing what
# conclusion) as it answers the query above.
# TODO: render that trace as human-readable output -- e.g. a sequence of
# st.expander(...) blocks, one per step, each with a plain-English sentence
# -- not a raw list/dict dump.
#
# Keep the core solver functions in sudoku_solver.py; do not duplicate them here.
