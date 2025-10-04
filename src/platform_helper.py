from urllib.parse import quote
import re


def simplify_title_for_search(title: str) -> str:
    cleaned_title = title
    remove_patterns = [
        " 第一季",
        " 第二季",
        " 第三季",
        " 第四季",
        " 第五季",
        " 第1季",
        " 第2季",
        " 第3季",
        " 第4季",
        " 第5季",
        " Season 1",
        " Season 2",
        " Season 3",
        " Season 4",
        " Season 5",
        " S1",
        " S2",
        " S3",
        " S4",
        " S5",
        " 第二季度",
        " 第三季度",
        " 第四季度",
    ]
    for patterns in remove_patterns:
        cleaned_title = cleaned_title.replace(patterns, "")

    chinese_parts = re.findall(r"[\u4e00-\u9fff]+", cleaned_title)
    if chinese_parts:
        search_keyword = "".join(chinese_parts)
    else:
        search_keyword = cleaned_title.replace("×", " ")

    suffix_patterns = [
        "的秘密",
        "的祕密",
        "的故事",
        "的日常",
        "的冒險",
        "的旅程",
        "的傳說",
        "的世界",
        "的記錄",
        "的回憶",
    ]
    for suffix in suffix_patterns:
        if search_keyword.endswith(suffix):
            search_keyword = search_keyword[: -len(suffix)]
            break

    if len(search_keyword) > 7:
        search_keyword = search_keyword[:4]
    return search_keyword


def get_platform_urls(title: str) -> dict:
    keyword = simplify_title_for_search(title)
    encoded_keyword = quote(keyword)

    youtube_keyword = title
    for pattern in [" 第1季", " 第2季", " 第3季", " 第4季", " 第5季", " 第6季"]:
        youtube_keyword = youtube_keyword.replace(pattern, "")
    encoded_youtube = quote(youtube_keyword)
    urls = {
        "anime1": f"https://anime1.me/?s={encoded_keyword}",
        "bahamut": f"https://ani.gamer.com.tw/search.php?keyword={encoded_keyword}",
        "youtube": f"https://www.youtube.com/results?search_query={encoded_youtube}",
    }
    return urls


if __name__ == "__main__":
    test_titles = [
        "Silent Witch 沉默魔女的秘密",
        "夫婦以上，戀人未滿",
        "機動戰士高達 水星的魔女",
        "SPY×FAMILY 間諜家家酒 第3季",
        "對我垂涎欲滴的非人少女",
    ]

    for title in test_titles:
        print(f"原標題：{title}")
        urls = get_platform_urls(title)
        for platform, url in urls.items():
            print(f"  {platform}: {url}")
        print()
