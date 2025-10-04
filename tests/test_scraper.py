import requests
from bs4 import BeautifulSoup


def test_youranimes(year, month):
    """測試 youranimes.tw"""
    url = f"https://youranimes.tw/bangumi/{year}{month:02d}"

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
    }

    print(f"正在測試：{url}")

    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()

        print(f"✅ HTTP 狀態碼：{response.status_code}")

        soup = BeautifulSoup(response.content, "lxml")

        line_clamp_divs = soup.find_all("div", class_="line-clamp-1")
        print(f"\n✅ 找到 {len(line_clamp_divs)} 個 line-clamp-1 元素")

        print("\n前 10 個 line-clamp-1 內容：")
        for i, div in enumerate(line_clamp_divs[:10]):
            text = div.text.strip()
            print(f"{i+1}. {text}")
        print("\n\n=== h3 標題 ===")
        h3_titles = soup.find_all("h3")
        print(f"找到 {len(h3_titles)} 個 h3")
        if h3_titles:
            print("前 10 個 h3：")
            for i, h3 in enumerate(h3_titles[:10]):
                print(f"{i+1}. {h3.text.strip()}")
        if h3_titles:
            print("\n\n=== 第一個 h3 的 HTML 結構 ===")
            print(h3_titles[0].prettify()[:500])
        return True
    except Exception as e:
        print(f"❌ 錯誤：{e}")
        return False


if __name__ == "__main__":
    # 測試 2012 年 1 月
    test_youranimes(2012, 1)
