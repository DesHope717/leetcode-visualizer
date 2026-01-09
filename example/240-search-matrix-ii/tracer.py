# example/240-search-matrix-ii/tracer.py
import json
from typing import List

def search_matrix_with_trace(matrix: List[List[int]], target: int):
    if not matrix or not matrix[0]:
        return False, [{"step": "空矩阵", "explanation": "输入矩阵为空", "matrix": matrix, "current": None, "found": False}]

    trace = []
    m, n = len(matrix), len(matrix[0])
    i, j = 0, n - 1

    # 初始状态
    trace.append({
        "step": "初始状态",
        "explanation": f"从右上角 (0, {n-1}) 开始搜索，目标值 target = {target}",
        "matrix": [row[:] for row in matrix],
        "current": [i, j],
        "target": target,
        "found": False
    })

    while i < m and j >= 0:
        cur = matrix[i][j]
        if cur == target:
            trace.append({
                "step": "找到目标",
                "explanation": f"在位置 ({i}, {j}) 找到目标值 {target}！",
                "matrix": [row[:] for row in matrix],
                "current": [i, j],
                "target": target,
                "found": True
            })
            return True, trace

        if target < cur:
            trace.append({
                "step": f"比较 ({i}, {j})",
                "explanation": f"当前值 matrix[{i}][{j}] = {cur} > target {target}，向左移动（j--）",
                "matrix": [row[:] for row in matrix],
                "current": [i, j],
                "target": target,
                "found": False
            })
            j -= 1
        elif target > cur:
            trace.append({
                "step": f"比较 ({i}, {j})",
                "explanation": f"当前值 matrix[{i}][{j}] = {cur} < target {target}，向下移动（i++）",
                "matrix": [row[:] for row in matrix],
                "current": [i, j],
                "target": target,
                "found": False
            })
            i += 1

    # 未找到
    trace.append({
        "step": "搜索结束",
        "explanation": "指针越界，未找到目标值",
        "matrix": [row[:] for row in matrix],
        "current": None,
        "target": target,
        "found": False
    })
    return False, trace

# 示例测试
if __name__ == "__main__":
    matrix = [
        [1,   4,  7, 11],
        [2,   5,  8, 12],
        [3,   6,  9, 16],
        [10, 13, 14, 17]
    ]
    target = 10

    result, trace = search_matrix_with_trace(matrix, target)
    print(f"搜索结果: {result}")

    with open("./example/240-search-matrix-ii/trace.json", "w", encoding="utf-8") as f:
        json.dump(trace, f, ensure_ascii=False, indent=2)
    print("轨迹已保存到 trace.json")