import json
import time

from sudoku_solver import (
    atom,
    build_definite_kb,
    pl_fc_entails,
    pl_bc_entails,
    pl_bc_entails_with_trace,
)

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

kb = build_definite_kb(
    n,
    box_h,
    box_w,
    givens
)

query = atom("Is", 1, 4, 9)

start = time.perf_counter()
fc_result = pl_fc_entails(kb, query)
fc_time = time.perf_counter() - start

start = time.perf_counter()
bc_result = pl_bc_entails(kb, query)
bc_time = time.perf_counter() - start

print("FC result:", fc_result)
print("FC time:", fc_time)

print("BC result:", bc_result)
print("BC time:", bc_time)

start = time.perf_counter()
trace_result, trace = pl_bc_entails_with_trace(kb, query)
trace_time = time.perf_counter() - start

print("Trace result:", trace_result)
print("Trace time:", trace_time)
print("Number of trace steps:", len(trace))
