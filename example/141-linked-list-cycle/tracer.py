# example/141-linked-list-cycle/tracer.py
import json
from typing import Optional, List

class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next

def build_cycle_list(values: List[int], cycle_pos: int):
    """
    构建带环链表
    :param values: 节点值列表
    :param cycle_pos: 环起点索引（-1 表示无环）
    :return: 头节点
    """
    if not values:
        return None
    nodes = [ListNode(val) for val in values]
    for i in range(len(nodes) - 1):
        nodes[i].next = nodes[i + 1]
    if cycle_pos >= 0:
        nodes[-1].next = nodes[cycle_pos]  # 尾部指向 cycle_pos 节点
    return nodes[0]

def has_cycle_with_trace(head: Optional[ListNode]):
    trace = []
    
    # 先序列化链表结构（最多前20个节点，防死循环）
    node_vals = []
    visited_ids = set()
    current = head
    while current and id(current) not in visited_ids and len(node_vals) < 20:
        visited_ids.add(id(current))
        node_vals.append(current.val)
        current = current.next
    
    # 如果有环，标记环起点（通过值可能不唯一，但用于展示足够）
    has_real_cycle = False
    if head and head.next:
        slow, fast = head, head.next
        temp_visited = set()
        while fast and fast.next:
            if id(slow) == id(fast):
                has_real_cycle = True
                break
            if id(slow) in temp_visited:
                break
            temp_visited.add(id(slow))
            slow = slow.next
            fast = fast.next.next

    trace.append({
        "step": "初始状态",
        "explanation": "开始检测链表是否存在环",
        "list_vals": node_vals,
        "has_cycle": has_real_cycle,
        "slow_index": None,
        "fast_index": None,
        "result": None
    })

    if not head or not head.next:
        trace.append({
            "step": "结束",
            "explanation": "链表为空或只有一个节点，不可能有环",
            "list_vals": node_vals,
            "has_cycle": False,
            "slow_index": None,
            "fast_index": None,
            "result": False
        })
        return False, trace

    slow = head
    fast = head.next
    step_count = 0

    # 为了定位索引，我们建立节点 -> 索引映射（仅前20个）
    node_to_index = {}
    current = head
    idx = 0
    seen = set()
    while current and id(current) not in seen and idx < 20:
        node_to_index[id(current)] = idx
        seen.add(id(current))
        current = current.next
        idx += 1

    def get_index(node):
        return node_to_index.get(id(node), -1)

    while fast and fast.next:
        slow_idx = get_index(slow)
        fast_idx = get_index(fast)

        trace.append({
            "step": f"第 {step_count + 1} 步",
            "explanation": f"慢指针在节点{slow_idx}（值={slow.val}），快指针在节点{fast_idx}（值={fast.val}）",
            "list_vals": node_vals,
            "has_cycle": has_real_cycle,
            "slow_index": slow_idx,
            "fast_index": fast_idx,
            "result": None
        })

        if slow == fast:
            trace.append({
                "step": "检测到环！",
                "explanation": f"慢指针与快指针在节点{slow_idx}（值={slow.val}）相遇，存在环！",
                "list_vals": node_vals,
                "has_cycle": True,
                "slow_index": slow_idx,
                "fast_index": fast_idx,
                "result": True
            })
            return True, trace

        slow = slow.next
        fast = fast.next.next
        step_count += 1

    # 未相遇
    final_slow = get_index(slow) if slow else -1
    final_fast = get_index(fast) if fast else -1
    trace.append({
        "step": "结束",
        "explanation": "快指针到达链表末尾，未检测到环",
        "list_vals": node_vals,
        "has_cycle": False,
        "slow_index": final_slow,
        "fast_index": final_fast,
        "result": False
    })
    return False, trace

# 示例：有环链表 [3,2,0,-4]，环起点索引=1（即节点2）
if __name__ == "__main__":
    # 测试用例1：有环
    head = build_cycle_list([3, 2, 0, -4], cycle_pos=1)
    result, trace = has_cycle_with_trace(head)
    print(f"有环测试: {result}")

    with open("./example/141-linked-list-cycle/trace.json", "w", encoding="utf-8") as f:
        json.dump(trace, f, ensure_ascii=False, indent=2)

    # 测试用例2：无环
    head2 = build_cycle_list([1, 2], cycle_pos=-1)
    result2, trace2 = has_cycle_with_trace(head2)
    print(f"无环测试: {result2}")

    with open("trace_no_cycle.json", "w", encoding="utf-8") as f:
        json.dump(trace2, f, ensure_ascii=False, indent=2)

    print("轨迹已保存到 trace_cycle.json 和 trace_no_cycle.json")
    print("请将其中一个重命名为 trace.json 用于播放器")