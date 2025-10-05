import os
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    print("❌ 找不到 GEMINI_API_KEY，請檢查 .env 檔案")
    exit(1)

genai.configure(api_key=api_key)
print("測試 Gemini API...\n")
try:
    model = genai.GenerativeModel("gemini-2.5-flash")
    response = model.generate_content("你好，請用繁體中文回答：1+1等於多少？")

    print(f"✅ Gemini 回應：\n{response.text}")
    print("\n" + "=" * 60)
    print("✅ API 測試成功！可以開始建立聊天機器人了。")

except Exception as e:
    print(f"❌ 錯誤：{e}")
