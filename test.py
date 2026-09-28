import json

from sudoku_solver import (
    atom,
    build_definite_kb,
    pl_fc_entails,
    pl_bc_entails,
)


# 读取 puzzles.json
with open("puzzles.json", "r", encoding="utf-8") as f:
    pool = json.load(f)

n = pool["n"]
box_h = pool["box_h"]
box_w = pool["box_w"]

# 测试第一个 puzzle
puzzle = pool["puzzles"][0]

givens = {
    tuple(map(int, key.split("_"))): value
    for key, value in puzzle["givens"].items()
}


# 构建 KB
kb = build_definite_kb(
    n,
    box_h,
    box_w,
    givens
)


# 测试 cell (1, 4) 的所有候选值
for v in range(1, n + 1):
    query = atom("Is", 1, 4, v)

    print(
        v,
        "FC =", pl_fc_entails(kb, query),
        "BC =", pl_bc_entails(kb, query)
    )
