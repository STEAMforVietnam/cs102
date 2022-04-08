from typing import List


def sum(items: List[float]) -> float:
    total: float = 0.0
    for item in items:
        total += item
    return total


danh_sach_diem: List[float] = [2.5, 1.5, 2, 3.25]
tong: float = sum(danh_sach_diem)

print(tong)
