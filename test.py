import json
import streamlit as st

from sudoku_solver import (
    atom,
    build_definite_kb,
    pl_fc_entails,
    pl_bc_entails,
)

st.title("Backward Chaining Test")

with open("puzzles.json", "r", encoding="utf-8") as f:
    pool = json.load(f)

n = pool["n"]
box_h = pool["box_h"]
box_w = pool["box_w"]

puzzle = pool["puzzles"][0]

givens = {
    tuple(map(int, key.split("_"))): value
    for key, value in puzzle["givens"].items()
}

st.write("Building knowledge base...")

kb = build_definite_kb(
    n,
    box_h,
    box_w,
    givens
)

st.write("Knowledge base built successfully.")

st.subheader("Test results for cell (1, 4)")

for v in range(1, n + 1):
    query = atom("Is", 1, 4, v)

    fc_result = pl_fc_entails(kb, query)
    bc_result = pl_bc_entails(kb, query)

    st.write(
        f"Value {v}: FC = {fc_result}, BC = {bc_result}"
    )
