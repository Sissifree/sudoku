import json
import time

from sudoku_solver import build_definite_kb, atom, pl_fc_entails

# 读取 puzzles.json
with open("puzzles.json") as f:
    pool = json.load(f)

n = pool["n"]
box_h = pool["box_h"]
box_w = pool["box_w"]

# Puzzle 5
puzzle = pool["puzzles"][4]

# JSON 的 "2_1" 转成 (2, 1)
givens = {
    tuple(map(int, key.split("_"))): value
    for key, value in puzzle["givens"].items()
}

print("Building KB...")
start = time.perf_counter()

kb = build_definite_kb(n, box_h, box_w, givens)

kb_time = time.perf_counter() - start

print(f"KB built in {kb_time:.4f} seconds")
print(f"Number of clauses: {len(kb.clauses)}")

# 只测试一个 query
query = atom("Is", 1, 1, 1)

print(f"Testing query: Is(1,1,1)")
print("Starting pl_fc_entails...")

start = time.perf_counter()

result = pl_fc_entails(kb, query)

elapsed = time.perf_counter() - start

print("Finished!")
print(f"Result: {result}")
print(f"pl_fc_entails time: {elapsed:.4f} seconds")
