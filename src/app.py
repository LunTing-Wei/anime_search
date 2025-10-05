from flask import Flask, render_template, request, jsonify
from database import search_anime_advanced, get_last_update_time
from platform_helper import get_platform_urls
from chatbot import process_message
import os

template_dir = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "templates"
)
app = Flask(__name__, template_folder=template_dir)


@app.route("/")
def index():
    return render_template("chatbot.html")


@app.route("/api/chat", methods=["POST"])
def chat():
    data = request.json
    message = data.get("message", "")

    if not message:
        return jsonify({"error": "訊息不能為空"}), 400
    result = process_message(message)
    return jsonify(result)


@app.route("/search")
def search_page():
    """傳統搜尋介面"""
    last_update = get_last_update_time()
    return render_template("index.html", last_update=last_update)


@app.route("/search/query", methods=["POST"])
def search():
    keyword = request.form.get("keyword", "")
    last_update = get_last_update_time()

    if not keyword:
        return render_template(
            "index.html", error="請輸入關鍵字", last_update=last_update
        )

    results = search_anime_advanced(keyword)
    results_with_links = []
    for anime in results:
        id, title, year, season, source = anime
        platform_urls = get_platform_urls(title)
        results_with_links.append(
            {
                "id": id,
                "title": title,
                "year": year,
                "season": season,
                "source": source,
                "platform_urls": platform_urls,
            }
        )
    return render_template(
        "index.html",
        keyword=keyword,
        results=results_with_links,
        last_update=last_update,
    )


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)
