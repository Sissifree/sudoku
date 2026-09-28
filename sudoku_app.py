import json

import streamlit as st

st.title("Sudoku Test")

st.write("App started")

with open("puzzles.json") as f:

    pool = json.load(f)

st.success("puzzles.json loaded successfully!")

st.write(pool.keys())
