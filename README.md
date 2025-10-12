AI 驅動的動畫查詢聊天機器人，收錄 2012-2025 年近 3000 部日本動畫。

## ✨ 功能特色

- 🤖 **智慧對話**：用自然語言查詢動畫（例如：「2024 年有什麼魔女動畫？」）
- 🔍 **進階搜尋**：支援年份、季度、關鍵字篩選
- 🎥 **多平台連結**：一鍵跳轉 Anime1、巴哈姆特、YouTube
- 🔄 **資料更新**：一鍵更新最新一季動畫
- 💬 **雙介面**：聊天機器人 + 傳統搜尋

## 🚀 快速開始

### 1. 安裝依賴

確保已安裝 [uv](https://github.com/astral-sh/uv)，然後執行：

```bash
uv sync

2. 設定 API Key

建立 .env 檔案並加入 Google Gemini API Key：

GEMINI_API_KEY=你的_API_Key

取得免費 API Key： https://aistudio.google.com/app/apikey

3. 啟動服務

uv run src/app.py

訪問：http://127.0.0.1:5000

📖 使用範例

聊天機器人模式

你：2024 年有什麼魔女動畫？
機器人：找到 1 部動畫
  • 魔女與野獸 (2024年第1季)
    [Anime1] [巴哈姆特] [YouTube]

你：第4季的間諜動畫
機器人：找到 3 部動畫
  • SPY×FAMILY 間諜家家酒 第3季 (2025年第4季)
  ...

傳統搜尋

訪問：http://127.0.0.1:5000/search

輸入關鍵字：2024 魔女

🔧 維護指令

更新動畫資料

每季開始時執行（建議在季度前 1-2 週執行）：

uv run tools/update_database.py

檢查資料庫

uv run tools/check_db.py

測試聊天機器人

uv run src/chatbot.py

📁 專案結構

anime_bot/
├── src/                      # 主程式碼
│   ├── app.py                # Flask 伺服器
│   ├── chatbot.py            # 聊天機器人邏輯
│   ├── database.py           # 資料庫操作
│   └── platform_helper.py    # 平台連結生成
├── scrapers/                 # 爬蟲腳本
│   ├── scraper_acgsecrets.py # 2017-2025 爬蟲
│   └── scraper_youranimes.py # 2012-2016 爬蟲
├── templates/                # HTML 模板
│   ├── chatbot.html          # 聊天介面
│   └── index.html            # 傳統搜尋介面
├── data/                     # 資料庫檔案
│   ├── anime.db              # SQLite 資料庫
│   └── last_update.txt       # 最後更新時間
├── tools/                    # 工具腳本
│   ├── update_database.py    # 更新資料
│   └── check_db.py           # 檢查資料庫
└── tests/                    # 測試檔案

🛠 技術棧

- 後端：Flask + Python 3.13
- AI：Google Gemini 2.5 Flash（免費版）
- 資料庫：SQLite
- 爬蟲：BeautifulSoup4 + Requests
- 套件管理：uv

📊 資料來源

- 2017-2025：https://acgsecrets.hk
- 2012-2016：https://youranimes.tw

總計：2981 部動畫

🔒 安全性

- .env 檔案已加入 .gitignore，不會被推送到 GitHub
- API Key 僅存於本地環境變數
- 爬蟲設有延遲機制，避免對網站造成負擔


📝 授權

MIT License

🙏 致謝

- Google Gemini API
- acgsecrets.hk
- youranimes.tw
- Claude Code（專案開發助手）

---
🎬 開始查詢你的下一部動畫吧！
```
