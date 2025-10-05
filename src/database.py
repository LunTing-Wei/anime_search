import sqlite3
from typing import List, Tuple
import re
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_FILE = os.path.join(BASE_DIR, "data", "anime.db")


def normalize_text(text: str) -> str:
    text = text.lower()
    text = re.sub(r"[，。、；：！？（）「」『』《》〈〉【】〔〕,.\-\s×·]+", "", text)
    common_variants = {
        "沈": "沉",
        "祕": "秘",
        "麽": "麼",
        "么": "麼",
    }
    for old, new in common_variants.items():
        text = text.replace(old, new)

    return text


def init_db():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    cursor.execute(
        """
          CREATE TABLE IF NOT EXISTS anime (
              id INTEGER PRIMARY KEY AUTOINCREMENT,
              title TEXT NOT NULL,
              year INTEGER NOT NULL,
              season INTEGER NOT NULL,
              source_url TEXT NOT NULL,
              UNIQUE(title, year, season)
          )
      """
    )
    conn.commit()
    conn.close()
    print(f"✅ 資料庫初始化完成：{DB_FILE}")


def insert_anime(title: str, year: int, season: int, source_url: str):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    try:
        cursor.execute(
            """
              INSERT OR IGNORE INTO anime (title, year, season, source_url)
              VALUES (?, ?, ?, ?)
          """,
            (title, year, season, source_url),
        )
        conn.commit()
    except Exception as e:
        print(f"❌ 插入失敗：{e}")
    finally:
        conn.close()


def get_all_anime() -> List[Tuple]:
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM anime ORDER BY year DESC, season DESC")
    result = cursor.fetchall()
    conn.close()
    return result


def search_anime_advanced(keyword: str) -> List[Tuple]:
    """進階搜尋：容錯性高的模糊搜尋"""

    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    # 拆分關鍵字
    keywords = keyword.split()

    # 分離年份和文字關鍵字
    year_filter = None
    season_filter = None
    text_keywords = []

    for kw in keywords:
        if kw.isdigit() and len(kw) == 4:
            year_filter = int(kw)
        elif "季" in kw:
            season_match = re.search(r"\d+", kw)
            if season_match:
                season_filter = int(season_match.group())
        else:
            text_keywords.append(kw)

    # 建立查詢
    query = "SELECT * FROM anime WHERE 1=1"
    params = []

    if year_filter:
        query += " AND year = ?"
        params.append(year_filter)

    if season_filter:
        query += " AND season = ?"
        params.append(season_filter)

    query += " ORDER BY year DESC, season DESC"

    cursor.execute(query, params)
    all_results = cursor.fetchall()
    conn.close()

    # 如果沒有文字關鍵字，直接回傳
    if not text_keywords:
        return all_results

    # 正規化關鍵字
    normalized_keywords = [normalize_text(kw) for kw in text_keywords]

    # 對結果進行模糊匹配和評分
    scored_results = []

    for anime in all_results[:5]:  # 先只測試前5筆
        id, title, year, season, source = anime
        normalized_title = normalize_text(title)

    for anime in all_results:
        id, title, year, season, source = anime
        normalized_title = normalize_text(title)

        # 計算匹配分數
        score = 0
        matched_keywords = 0

        for norm_kw in normalized_keywords:
            if norm_kw in normalized_title:
                matched_keywords += 1
                if norm_kw == normalized_title:
                    score += 100
                elif normalized_title.startswith(norm_kw):
                    score += 50
                else:
                    score += 10

        if matched_keywords > 0:
            scored_results.append((score, anime))

    # 按分數排序
    scored_results.sort(reverse=True, key=lambda x: x[0])
    return [anime for score, anime in scored_results]


if __name__ == "__main__":
    init_db()
    insert_anime("測試動畫", 2025, 4, "https://test.com")
    print(get_all_anime())


def get_last_update_time() -> str:
    update_file = os.path.join(BASE_DIR, "data", "last_update.txt")
    try:
        with open(update_file, "r", encoding="utf-8") as f:
            lines = f.readlines()
            if lines:
                return lines[0].strip()
    except FileNotFoundError:
        pass
    return "未知"
