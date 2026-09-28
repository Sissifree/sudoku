import json
import time
import streamlit as st

from sudoku_solver import build_definite_kb, atom, pl_fc_entails

st.title("Single FC Test")

with open("puzzles.json") as f:
    pool = json.load(f)

n = pool["n"]
box_h = pool["box_h"]
box_w = pool["box_w"]

# Puzzle 5
puzzle = pool["puzzles"][4]

givens = {
    tuple(map(int, key.split("_"))): value
    for key, value in puzzle["givens"].items()
}

st.write("Puzzle 5 loaded.")
st.write(f"Number of givens: {len(givens)}")

if st.button("Run ONE pl_fc_entails"):

    # Step 1: Build KB
    st.write("1. Building KB...")
    
    start = time.perf_counter()

    kb = build_definite_kb(
        n,
        box_h,
        box_w,
        givens
    )

    kb_time = time.perf_counter() - start

    st.success(f"KB built in {kb_time:.4f} seconds")
    st.write(f"Number of clauses: {len(kb.clauses)}")

    # Step 2: Run ONE FC
    query = atom("Is", 1, 1, 1)

    st.write("2. Starting ONE pl_fc_entails...")
    st.write("Query: Is(1,1,1)")

    start = time.perf_counter()

    result = pl_fc_entails(kb, query)

    elapsed = time.perf_counter() - start

    st.success("pl_fc_entails finished!")

    st.write(f"Result: {result}")
    st.write(f"Time: {elapsed:.4f} seconds")
