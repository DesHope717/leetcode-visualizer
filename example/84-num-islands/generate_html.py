# generate_html.py
from island_tracer import IslandTracer
import json

# 示例输入
grid = [
    ["1","1","0","0","0"],
    ["1","1","0","0","0"],
    ["0","0","1","0","0"],
    ["0","0","0","1","1"]
]

tracer = IslandTracer(grid)
trace = tracer.run()

# 保存为 JSON
with open("trace.json", "w") as f:
    json.dump(trace, f, indent=2)

print("Trace saved to trace.json")