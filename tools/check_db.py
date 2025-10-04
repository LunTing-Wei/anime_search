import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from src.database import get_all_anime

all_anime = get_all_anime()
print(f"資料庫共有 {len(all_anime)} 部動畫\n")

print("前 10 筆資料：")
for anime in all_anime[:10]:
    id, title, year, season, source = anime
    print(f"{id}. {title} ({year}年第{season}季)")
