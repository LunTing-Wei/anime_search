from flask import Flask, render_template, request
from database import search_anime_advanced
from platform_helper import get_platform_urls
import os

template_dir = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "templates"
)
app = Flask(__name__, template_folder=template_dir)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/search", methods=["POST"])
def search():
    keyword = request.form.get("keyword", "")

    if not keyword:
        return render_template("index.html", error="請輸入關鍵字")
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
    return render_template("index.html", keyword=keyword, results=results_with_links)


if __name__ == "__main__":
    app.run(debug=True, port=5000)
