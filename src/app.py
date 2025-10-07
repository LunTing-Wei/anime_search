from flask import Flask, render_template, request, jsonify
from database import (
    search_anime_advanced,
    get_last_update_time,
    add_favorite,
    remove_favorite,
    get_favorites,
    is_favorited,
)
from platform_helper import get_platform_urls
from chatbot import process_message
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
template_dir = os.path.join(BASE_DIR, "templates")
static_dir = os.path.join(BASE_DIR, "static")

app = Flask(__name__, template_folder=template_dir, static_folder=static_dir)


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


@app.route("/favorites")
def favorites_page():
    """我的收藏頁面"""
    return render_template("favorites.html")


@app.route("/api/favorites", methods=["GET"])
def api_get_favorite():
    favorites = get_favorites()
    results = []
    for fav in favorites:
        id, title, year, season, source, created_at = fav
        platform_urls = get_platform_urls(title)
        results.append(
            {
                "id": id,
                "title": title,
                "year": year,
                "season": season,
                "platform_urls": platform_urls,
                "created_at": created_at,
            }
        )
    return jsonify({"favorites": results})


@app.route("/api/favorite/<int:anime_id>", methods=["POST"])
def api_add_favorite(anime_id):
    success = add_favorite(anime_id)
    if success:
        return jsonify({"success": True, "message": "已加入收藏"})
    else:
        return jsonify({"success": False, "message": "已經收藏過了"}), 400


@app.route("/api/favorite/<int:anime_id>", methods=["DELETE"])
def api_delete_favorite(anime_id):
    success = remove_favorite(anime_id)
    if success:
        return jsonify({"success": True, "message": "已移除收藏"})
    else:
        return jsonify({"success": False, "message": "找不到此收藏"}), 404


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
