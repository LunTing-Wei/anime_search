import requests
from bs4 import BeautifulSoup
import time
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from src.database import init_db, insert_anime


def scrape_season(year: int, month: int):

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


def scrape_all():
    season_months = [1, 4, 7, 10]
    total = 0

    for year in range(2012, 2026):
        for month in season_months:
            if year == 2025 and month > 10:
                break
            count = scrape_season(year, month)
            total += count

            time.sleep(1)
    print(f"\n{'='*50}")
    print(f"🎉 全部完成！共爬取 {total} 部動畫")
    print(f"{'='*50}")


if __name__ == "__main__":
    init_db()

    scrape_all()
