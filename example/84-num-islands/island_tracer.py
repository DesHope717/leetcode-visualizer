# island_tracer.py
from typing import List, Any
import json

class IslandTracer:
    def __init__(self, grid: List[List[str]]):
        self.original_grid = [row[:] for row in grid]
        self.rows = len(grid)
        self.cols = len(grid[0]) if grid else 0
        self.trace = []
        self.call_stack = []
        self.count = 0

    def get_explanation(self, action: str, i: int, j: int) -> str:
        """根据动作类型生成中文解释"""
        if action == "start":
            return "开始遍历网格，寻找岛屿。"
        elif action == "found_island":
            return f"在位置 ({i}, {j}) 发现新岛屿！岛屿数量 +1，开始深度优先搜索（DFS）淹没整个岛屿。"
        elif action == "enter_dfs":
            if i < 0 or i >= self.rows or j < 0 or j >= self.cols:
                return f"尝试访问越界位置 ({i}, {j})，无效，返回。"
            elif self.grid[i][j] == '0':
                return f"位置 ({i}, {j}) 是水域，无需处理，返回。"
            else:
                return f"进入 DFS，正在处理陆地 ({i}, {j})，将其标记为已访问（淹没）。"
        elif action == "exit_dfs":
            return f"完成对位置 ({i}, {j}) 的 DFS 处理，回溯。"
        elif action == "end":
            return f"遍历完成！总共找到 {self.count} 个岛屿。"
        else:
            return "未知操作。"

    def record_step(self, action: str, i: int = -1, j: int = -1):
        """记录当前状态快照，并添加中文解释"""
        explanation = self.get_explanation(action, i, j)
        self.trace.append({
            "action": action,
            "i": i,
            "j": j,
            "grid": [row[:] for row in self.grid],
            "count": self.count,
            "call_stack": self.call_stack.copy(),
            "explanation": explanation  # ← 新增字段
        })

    def run(self):
        self.grid = [row[:] for row in self.original_grid]
        self.trace = []
        self.count = 0
        self.call_stack = []

        self.record_step("start")

        for i in range(self.rows):
            for j in range(self.cols):
                if self.grid[i][j] == '1':
                    self.count += 1
                    self.record_step("found_island", i, j)
                    self._dfs(i, j)

        self.record_step("end")
        return self.trace

    def _dfs(self, i: int, j: int):
        self.call_stack.append((i, j))
        self.record_step("enter_dfs", i, j)

        # 检查是否越界或为水域
        if i < 0 or i >= self.rows or j < 0 or j >= self.cols or self.grid[i][j] == '0':
            self.call_stack.pop()
            self.record_step("exit_dfs", i, j)
            return

        # 淹没当前陆地
        self.grid[i][j] = '0'

        # 递归四个方向：上、下、左、右
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        for di, dj in directions:
            self._dfs(i + di, j + dj)

        self.call_stack.pop()
        self.record_step("exit_dfs", i, j)