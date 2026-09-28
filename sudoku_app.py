import json
import streamlit as st

from sudoku_solver import (
    atom,
    build_definite_kb,
    build_general_kb,
    solve_full_grid_fc,
    solve_full_grid_bc,
    pl_bc_entails,
)

st.title("Sudoku Test")

st.write("App started")

with open("puzzles.json") as f:
    pool = json.load(f)

st.success("puzzles.json loaded successfully!")

st.success("sudoku_solver imported successfully!")

st.write(pool.keys())
