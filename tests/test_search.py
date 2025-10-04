import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.database import search_anime_advanced

# 測試案例
test_queries = [
    "沉默魔女",
    "夫婦以上",
    "水星的魔女",
]

for query in test_queries:
    print(f"\n搜尋：「{query}」")
    print("=" * 50)
    results = search_anime_advanced(query)
    print(f"找到 {len(results)} 部動畫")
    for anime in results[:5]:  # 只顯示前 5 筆
        id, title, year, season, source = anime
        print(f"  • {title} ({year}年第{season}季)")
