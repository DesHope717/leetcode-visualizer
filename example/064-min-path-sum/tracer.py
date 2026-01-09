# example/064-min-path-sum/tracer.py
import json
from typing import List

def min_path_sum_with_trace(grid: List[List[int]]):
    if not grid or not grid[0]:
        return 0, []

    trace = []
    m, n = len(grid), len(grid[0])
    dp = [0] * n

    # 初始状态
    trace.append({
        "step": "初始网格",
        "explanation": "开始计算最小路径和",
        "grid": [row[:] for row in grid],
        "dp": dp[:],
        "current_cell": None
    })

    # 初始化第一个位置
    dp[0] = grid[0][0]
    trace.append({
        "step": "初始化起点",
        "explanation": f"起点 grid[0][0] = {grid[0][0]}，dp[0] = {dp[0]}",
        "grid": [row[:] for row in grid],
        "dp": dp[:],
        "current_cell": [0, 0]
    })

    # 填充第一行
    for j in range(1, n):
        dp[j] = dp[j-1] + grid[0][j]
        trace.append({
            "step": f"初始化第一行第 {j} 列",
            "explanation": f"第一行只能从左来：dp[{j-1}] = {dp[j-1]} + grid[0][{j}] = {grid[0][j]} → dp[{j}] = {dp[j]}",
            "grid": [row[:] for row in grid],
            "dp": dp[:],
            "current_cell": [0, j]
        })

    # 填充后续行
    for i in range(1, m):
        # 更新当前行第一个位置（只能从上边来）
        dp[0] = dp[0] + grid[i][0]
        trace.append({
            "step": f"处理第 {i} 行第 0 列",
            "explanation": f"第一列只能从上来：dp[0] = {dp[0] - grid[i][0]} + grid[{i}][0] = {grid[i][0]} → dp[0] = {dp[0]}",
            "grid": [row[:] for row in grid],
            "dp": dp[:],
            "current_cell": [i, 0]
        })

        # 填充当前行其他位置
        for j in range(1, n):
            top = dp[j]      # 上方（旧 dp[j]）
            left = dp[j-1]   # 左方
            chosen = min(top, left)
            dp[j] = chosen + grid[i][j]
            direction = "上方" if chosen == top else "左方"
            trace.append({
                "step": f"处理格子 ({i}, {j})",
                "explanation": f"在 ({i},{j}) 处，比较上方 dp[{j}]={top} 和左方 dp[{j-1}]={left}，选择较小的 {chosen}（来自{direction}），加上 grid[{i}][{j}]={grid[i][j]}，得到 dp[{j}] = {dp[j]}",
                "grid": [row[:] for row in grid],
                "dp": dp[:],
                "current_cell": [i, j]
            })

    trace.append({
        "step": "完成",
        "explanation": f"最终结果：dp[-1] = {dp[-1]}",
        "grid": [row[:] for row in grid],
        "dp": dp[:],
        "current_cell": None,
        "result": dp[-1]
    })

    return dp[-1], trace

# 示例输入
if __name__ == "__main__":
    grid = [
        [1, 3, 1],
        [1, 5, 1],
        [4, 2, 1]
    ]
    result, trace = min_path_sum_with_trace(grid)
    print(f"最小路径和: {result}")
    
    # 保存 trace.json
    with open("./example/064-min-path-sum/trace.json", "w", encoding="utf-8") as f:
        json.dump(trace, f, ensure_ascii=False, indent=2)
    print("轨迹已保存到 trace.json")