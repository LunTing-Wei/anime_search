import os
from dotenv import load_dotenv
import google.generativeai as genai
import json
from database import search_anime_advanced
from platform_helper import get_platform_urls

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel("gemini-2.5-flash")

SYSTEM_PROMPT = """你是一個動畫查詢助手。使用者會詢問動畫相關問題，你需要：

  1. 解析使用者的問題，提取：
     - 年份（如果有，例如：2024、去年、今年）
     - 季度（如果有，1-4，或冬季=1、春季=2、夏季=3、秋季=4）
     - 關鍵字（動畫名稱或類型）

  2. 用以下 JSON 格式回應（**只輸出 JSON，不要其他文字**）：
     {
       "year": 2024 或 null,
       "season": 1-4 或 null,
       "keywords": "關鍵字" 或 null,
       "response_type": "search" 或 "chat"
     }

  3. response_type 判斷：
     - "search"：使用者想搜尋動畫
     - "chat"：使用者在閒聊（例如：你好、謝謝、介紹一下等）

  範例：
  使用者：「我想找 2024 年的魔女動畫」
  你回應：{"year": 2024, "season": null, "keywords": "魔女", "response_type": "search"}

  使用者：「第4季有什麼好看的間諜動畫」
  你回應：{"year": null, "season": 4, "keywords": "間諜", "response_type": "search"}

  使用者：「你好」
  你回應：{"year": null, "season": null, "keywords": null, "response_type": "chat"}

  使用者：「謝謝」
  你回應：{"year": null, "season": null, "keywords": null, "response_type": "chat"}

  **重要：只輸出 JSON，不要任何其他文字或解釋。**
  """


def parse_user_message(message: str) -> dict:
    try:
        full_prompt = f"{SYSTEM_PROMPT}\n\n使用者：「{message}」\n你回應："
        response = model.generate_content(full_prompt)
        result_text = response.text.strip()

        if result_text.startswith("```"):
            result_text = result_text.split("\n", 1)[1]
            result_text = result_text.rsplit("\n", 1)[0]
        parsed = json.loads(result_text)
        return parsed
    except Exception as e:
        print(f"[ERROR] 解析失敗：{e}")
        print(f"[DEBUG] Gemini 回應：{response.text}")
        return {"year": None, "season": None, "keywords": None, "response_type": "chat"}


def handle_chat(message: str) -> str:
    chat_responses = {
        "你好": "你好！我是動畫查詢助手 🎬\n\n你可以問我：\n- 「2024 年有什麼魔女動畫？」\n- 「第4季的間諜動畫」\n- 「沉默魔女在哪看？」",
        "謝謝": "不客氣！有其他動畫想查詢嗎？ 😊",
        "介紹": "我可以幫你查詢 2012-2025 年的動畫資料，共收錄近 3000 部動畫！\n\n試試問我：\n- 年份 + 關鍵字\n- 季度 + 類型\n- 動畫名稱",
    }
    message_lower = message.lower()

    for keyword, response in chat_responses.items():
        if keyword in message_lower or keyword in message:
            return response
    return "我是動畫查詢助手！你可以問我關於動畫的問題，例如「2024 年的魔女動畫」😊"


def process_message(message: str) -> dict:
    parsed = parse_user_message(message)

    if parsed["response_type"] == "chat":
        return {"type": "chat", "message": handle_chat(message)}

    else:
        year = parsed.get("year")
        season = parsed.get("season")
        keywords = parsed.get("keywords")

        search_query = ""
        if year:
            search_query += f"{year} "
        if season:
            search_query += f"第{season}季 "
        if keywords:
            search_query += keywords

        search_query = search_query.strip()

        if not search_query:
            return {
                "type": "chat",
                "message": "請告訴我你想找什麼動畫？例如：「2024 年的魔女動畫」",
            }
        results = search_anime_advanced(search_query)

        anime_list = []
        for anime in results[:10]:
            id, title, year, season, source = anime
            platform_urls = get_platform_urls(title)
            anime_list.append(
                {
                    "id": id,
                    "title": title,
                    "year": year,
                    "season": season,
                    "platform_urls": platform_urls,
                }
            )
        return {
            "type": "search",
            "query": search_query,
            "count": len(results),
            "results": anime_list,
        }


if __name__ == "__main__":
    test_messages = [
        "你好",
        "我想找 2024 年的魔女動畫",
        "第4季有什麼間諜動畫",
        "沉默魔女",
    ]
    for msg in test_messages:
        print(f"\n使用者：{msg}")
        print("=" * 60)

        result = process_message(msg)

        if result["type"] == "chat":
            print(f"機器人：{result['message']}")
        else:
            print(f"搜尋：{result['query']}")
            print(f"找到：{result['count']} 部動畫")
            for anime in result["results"][:3]:
                print(f"  - {anime['title']} ({anime['year']}年第{anime['season']}季)")
