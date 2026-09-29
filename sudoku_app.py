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
    pl_bc_entails_with_trace,
)

st.title('Sudoku Solver')

with open('puzzles.json') as f:
    pool = json.load(f)

n = pool["n"]
box_h = pool["box_h"]
box_w = pool["box_w"]
puzzles = pool["puzzles"]

# --- 1. Puzzle selection & visual board display ---
# TODO: a dropdown/selectbox to pick a puzzle by index from pool['puzzles'].
# TODO: render the grid (e.g. a table or grid of st.columns), showing given
# cells and empty cells differently (e.g. bold givens, blank otherwise).
st.header("1. Puzzle Selection")

puzzle_index = st.selectbox(
    "Choose a puzzle",
    range(len(puzzles)),
    format_func=lambda x: f"Puzzle {x + 1}"
)

puzzle = puzzles[puzzle_index]

# Convert JSON keys such as "2_1"
# into tuple keys such as (2, 1)
givens = {
    tuple(map(int, key.split("_"))): value
    for key, value in puzzle["givens"].items()
}
st.write(
    f"Number of given cells: {puzzle['given_count']}"
)

# Display the original Sudoku puzzle

st.subheader("Sudoku Puzzle")

for r in range(1, n + 1):
    cols = st.columns(n)
    for c in range(1, n + 1):
        if (r, c) in givens:
            cols[c - 1].markdown(
                f"**{givens[(r, c)]}**"
            )
        else:
            cols[c - 1].write("·")
# --- 2. Full-grid auto-solver, with algorithm selection ---
# TODO: a radio/selectbox letting the user choose forward chaining
# (solve_full_grid_fc) or backward chaining (solve_full_grid_bc).
# TODO: a button that times and calls the chosen solver on
# (n, box_h, box_w, givens), then displays the solved grid and the elapsed
# time.
st.header("2. Full-grid Solver")

algorithm = st.radio(
    "Choose solving algorithm",
    ["Forward Chaining", "Backward Chaining"]
)

if st.button("Solve Full Grid"):

    start_time = time.perf_counter()

    if algorithm == "Forward Chaining":
        solution = solve_full_grid_fc(
            n,
            box_h,
            box_w,
            givens
        )

    else:
        solution = solve_full_grid_bc(
            n,
            box_h,
            box_w,
            givens
        )

    elapsed_time = time.perf_counter() - start_time
    st.success("Puzzle solved!")
    st.write(
        f"Elapsed time: {elapsed_time:.6f} seconds"
    )

    st.subheader("Solved Grid")

    for r in range(1, n + 1):
        cols = st.columns(n)
        for c in range(1, n + 1):
            value = solution[(r, c)]
            cols[c - 1].markdown(
                f"**{value}**"
            )


# --- 3. Targeted cell entailment query ---
# TODO: number inputs for row (r), column (c), value (v).
# TODO: a button that builds the definite KB, calls
# pl_bc_entails(kb, atom('Is', r, c, v)), and displays True/False.
st.header("3. Targeted Cell Entailment")

col1, col2, col3 = st.columns(3)

with col1:
    row = st.number_input(
        "Row",
        min_value=1,
        max_value=n,
        value=1,
        step=1
    )

with col2:
    col = st.number_input(
        "Column",
        min_value=1,
        max_value=n,
        value=1,
        step=1
    )

with col3:
    value = st.number_input(
        "Value",
        min_value=1,
        max_value=n,
        value=1,
        step=1
    )

if st.button("Check Entailment"):
    kb = build_definite_kb(
        n,
        box_h,
        box_w,
        givens
    )

    query = atom(
        "Is",
        row,
        col,
        value
    )

    result = pl_bc_entails(
        kb,
        query
    )

    if result:
        st.success(
            f"True: Cell ({row}, {col}) is entailed to be {value}."
        )

    else:
        st.info(
            f"False: Cell ({row}, {col}) is not entailed to be {value}."
        )

# --- 4. Reasoning trace ("tutor mode") ---
# TODO: instrument your forward- or backward-chaining approach to record each
# reasoning step (which rule fired, on what premises, producing what
# conclusion) as it answers the query above.
# TODO: render that trace as human-readable output -- e.g. a sequence of
# st.expander(...) blocks, one per step, each with a plain-English sentence
# -- not a raw list/dict dump.
#
# Keep the core solver functions in sudoku_solver.py; do not duplicate them here.
st.header("4. Tutor Mode")

st.write(
    "Display the backward-chaining reasoning "
    "steps for the selected query."
)

if st.button("Show Reasoning Trace"):
    kb = build_definite_kb(
        n,
        box_h,
        box_w,
        givens
    )

    query = atom(
        "Is",
        int(row),
        int(col),
        int(value)
    )

    result, trace = pl_bc_entails_with_trace(
        kb,
        query
    )

    if result:
        st.success(
            f"Query Is({row}, {col}, {value}) "
            "is entailed."
        )
    else:
        st.error(
            f"Query Is({row}, {col}, {value}) "
            "is not entailed."
        )

    st.subheader("Reasoning Steps")

    if trace:
        for i, step in enumerate(trace, start=1):
            with st.expander(f"Step {i}"):
                st.write(step)
    else:
        st.info("No reasoning steps were recorded.")
