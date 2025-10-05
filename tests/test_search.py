import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.platform_helper import simplify_title_for_search

test_cases = [
    "魔女",
    "間諜家家酒",
    "Silent Witch 沉默魔女的秘密",
    "機動戰士高達 水星的魔女",
    "SPY×FAMILY 間諜家家酒 第二季度",
    "我們仍未知道那天所看見的花名",
    "夫婦以上，戀人未滿",
    "關於我轉生變成史萊姆這檔事",
]

print("=" * 70)
for title in test_cases:
    keyword = simplify_title_for_search(title)
    print(f"原標題（{len(title)}字）：{title}")
    print(f"搜尋關鍵字（{len(keyword)}字）：{keyword}")
    print()
