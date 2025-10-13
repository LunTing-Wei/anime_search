import pytest
import os
import sys

sys.path.insert(
    0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src"))
)

import database
from database import (
    search_anime_advanced,
    normalize_text,
    init_db,
    insert_anime,
)

TEST_DB = "/tmp/test_anime.db"


@pytest.fixture
def test_db():
    original_db = database.DB_FILE
    database.DB_FILE = TEST_DB

    init_db()
    test_data = [
        ("魔女與野獸", 2024, 1, "https://test.com/1"),
        ("沉默魔女的秘密", 2024, 3, "https://test.com/2"),
        ("SPY×FAMILY 間諜家家酒", 2025, 4, "https://test.com/3"),
        ("關於我轉生變成史萊姆這檔事", 2023, 2, "https://test.com/4"),
        ("遊戲人生", 2014, 2, "https://test.com/5"),
    ]
    for title, year, season, url in test_data:
        insert_anime(title, year, season, url)
    yield
    database.DB_FILE = original_db
    if os.path.exists(TEST_DB):
        os.remove(TEST_DB)


# ========== 測試：文字正規化 ==========


def test_normalize_text_removes_punctuation():
    """測試：移除標點符號"""
    assert normalize_text("魔女、與。野獸") == "魔女與野獸"


def test_normalize_text_converts_variants():
    """測試：異體字轉換"""
    assert normalize_text("沈默") == "沉默"
    assert normalize_text("祕密") == "秘密"


def test_normalize_text_lowercase():
    """測試：轉小寫"""
    assert normalize_text("SPY×FAMILY") == "spyfamily"


# ========== 測試：搜尋功能 ==========
def test_search_by_year(test_db):
    results = search_anime_advanced("2024")
    assert len(results) == 2
    for anime in results:
        _, title, year, season, _ = anime
        assert year == 2024


def test_search_by_season(test_db):
    """測試：純季度搜尋"""
    results = search_anime_advanced("第2季")

    # 應該找到 2 部第 2 季的動畫
    assert len(results) == 2

    for anime in results:
        _, title, year, season, _ = anime
        assert season == 2


def test_search_by_keyword(test_db):
    """測試：關鍵字搜尋"""
    results = search_anime_advanced("魔女")

    # 應該找到 2 部含「魔女」的動畫
    assert len(results) == 2

    titles = [anime[1] for anime in results]
    assert "魔女與野獸" in titles
    assert "沉默魔女的秘密" in titles


def test_search_combined(test_db):
    """測試：年份 + 關鍵字組合"""
    results = search_anime_advanced("2024 魔女")

    # 應該找到 2 部 2024 年的「魔女」動畫
    assert len(results) == 2

    for anime in results:
        _, title, year, season, _ = anime
        assert year == 2024
        assert "魔女" in title


def test_search_variant_character(test_db):
    """測試：異體字搜尋"""
    results = search_anime_advanced("沈默")  # 用「沈」搜尋

    # 應該能找到「沉默魔女的秘密」
    assert len(results) == 1
    assert "沉默魔女的秘密" in results[0][1]


def test_search_not_found(test_db):
    """測試：找不到結果"""
    results = search_anime_advanced("不存在的動畫XYZ")

    # 應該回傳空列表
    assert len(results) == 0


def test_search_empty_string(test_db):
    """測試：空字串搜尋"""
    results = search_anime_advanced("")

    # 應該回傳所有動畫（5 部）
    assert len(results) == 5
