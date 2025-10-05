import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from src.database import init_db, insert_anime
import requests
from bs4 import BeautifulSoup
from datetime import datetime
import time


def get_current_season():
    now = datetime.now()
    year = now.year
    month = now.month
    season = (month - 1) // 3 + 1

    season_months = {1: 1, 2: 4, 3: 7, 4: 10}
    month = season_months[season]

    return year, month, season


def scrap_acgsecrets_season(year: int, month: int):
    url = f"https://acgsecrets.hk/bangumi/{year}{month:02d}/"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
    }

    print(f"正在爬取：{url}")
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()

        soup = BeautifulSoup(response.content, "lxml")
        anime_containers = soup.find_all("div", attrs={"acgs-bangumi-data-id": True})

        season = (month - 1) // 3 + 1
        count = 0

        for container in anime_containers:
            title_elem = container.find("div", class_="anime_name")
            if title_elem:
                title = title_elem.text.strip()
                insert_anime(title, year, season, url)
                count += 1
            print(f"✅ {year}年第{season}季：成功插入 {count} 部動畫")
            return count
    except Exception as e:
        print(f"❌ 錯誤：{e}")
        return 0


def update_latest_season():
    print("=" * 60)
    print("動畫資料庫更新工具")
    print("=" * 60)

    init_db()
    year, month, season = get_current_season()
    print(f"\n當前季度：{year}年第{season}季（{month}月）\n")

    count = scrap_acgsecrets_season(year, month)
    update_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    update_file = os.path.join(base_dir, "data", "last_update.txt")

    with open(update_file, "w", encoding="utf-8") as f:
        f.write(f"{update_time}\n")
        f.write(f"更新了 {year}年第{season}季，新增 {count} 部動畫")

    print(f"\n{'=' * 60}")
    print(f"✅ 更新完成！")
    print(f"📅 更新時間：{update_time}")
    print(f"📊 新增動畫：{count} 部")
    print(f"{'=' * 60}")


if __name__ == "__main__":
    update_latest_season()
