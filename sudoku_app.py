import json
import time
import streamlit as st

from sudoku_solver import solve_full_grid_fc

st.title("Sudoku Solver Test")

with open("puzzles.json") as f:
    pool = json.load(f)

n = pool["n"]
box_h = pool["box_h"]
box_w = pool["box_w"]

puzzle = pool["puzzles"][0]

givens = {
    tuple(map(int, key.split("_"))): value
    for key, value in puzzle["givens"].items()
}

st.write("FC solver imported successfully!")

if st.button("Test FC Solver"):
    st.write("Starting FC solver...")

    start_time = time.perf_counter()

    solution = solve_full_grid_fc(
        n,
        box_h,
        box_w,
        givens
    )

    elapsed_time = time.perf_counter() - start_time

    st.success("FC solver finished!")

    st.write(f"Time: {elapsed_time:.4f} seconds")
    st.write(solution)
