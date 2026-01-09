# example/033-search-rotated-sorted-array/tracer.py
import json
from typing import List

def search_rotated_with_trace(nums: List[int], target: int):
    if not nums:
        return -1, [{"step": "空数组", "explanation": "输入数组为空", "nums": [], "left": None, "mid": None, "right": None, "found": False}]

    trace = []
    left, right = 0, len(nums) - 1

    # 初始状态
    trace.append({
        "step": "初始状态",
        "explanation": f"在旋转排序数组中搜索目标值 {target}，初始搜索范围：left=0, right={len(nums)-1}",
        "nums": nums[:],
        "left": left,
        "mid": None,
        "right": right,
        "target": target,
        "found": False
    })

    while left <= right:
        mid = (left + right) // 2
        cur = nums[mid]

        if cur == target:
            trace.append({
                "step": "找到目标",
                "explanation": f"在索引 {mid} 处找到目标值 {target}！",
                "nums": nums[:],
                "left": left,
                "mid": mid,
                "right": right,
                "target": target,
                "found": True
            })
            return mid, trace

        # 判断 [left, mid] 是否有序
        if nums[left] <= nums[mid]:
            # 左半段有序
            if nums[left] <= target < nums[mid]:
                explanation = f"左半段 [{left}, {mid}] 有序（值域 [{nums[left]}, {nums[mid]}]），且 target={target} 在此区间内 → 搜索左半段"
                new_right = mid - 1
                new_left = left
            else:
                explanation = f"左半段 [{left}, {mid}] 有序，但 target={target} 不在 [{nums[left]}, {nums[mid]}) 内 → 搜索右半段"
                new_left = mid + 1
                new_right = right
        else:
            # 右半段 [mid, right] 有序
            if nums[mid] < target <= nums[right]:
                explanation = f"右半段 [{mid}, {right}] 有序（值域 ({nums[mid]}, {nums[right]}]），且 target={target} 在此区间内 → 搜索右半段"
                new_left = mid + 1
                new_right = right
            else:
                explanation = f"右半段 [{mid}, {right}] 有序，但 target={target} 不在 ({nums[mid]}, {nums[right]}] 内 → 搜索左半段"
                new_left = left
                new_right = mid - 1

        trace.append({
            "step": f"第 {len(trace)} 步",
            "explanation": explanation,
            "nums": nums[:],
            "left": left,
            "mid": mid,
            "right": right,
            "target": target,
            "found": False
        })

        left, right = new_left, new_right

    # 未找到
    trace.append({
        "step": "搜索结束",
        "explanation": "搜索范围耗尽，未找到目标值",
        "nums": nums[:],
        "left": None,
        "mid": None,
        "right": None,
        "target": target,
        "found": False
    })
    return -1, trace

# 示例测试
if __name__ == "__main__":
    nums = [4, 5, 6, 7, 8, 9, 0, 1, 2, 3]
    target = 0

    result, trace = search_rotated_with_trace(nums, target)
    print(f"搜索结果: 索引 = {result}")

    with open("./example/033-search-rotated-sorted-array/trace.json", "w", encoding="utf-8") as f:
        json.dump(trace, f, ensure_ascii=False, indent=2)
    print("轨迹已保存到 trace.json")