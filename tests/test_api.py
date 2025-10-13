import pytest
import os
import sys

sys.path.insert(
    0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src"))
)
from app import app


@pytest.fixture
def client():
    """建立測試用的 Flask client"""
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


# ========== 測試：基本路由 ==========


def test_index_route(client):
    """測試：首頁"""
    response = client.get("/")
    assert response.status_code == 200
    assert b"chatbot.html" in response.data or b"<!DOCTYPE html>" in response.data


def test_search_page_route(client):
    """測試：搜尋頁面"""
    response = client.get("/search")
    assert response.status_code == 200


def test_favorites_page_route(client):
    """測試：收藏頁面"""
    response = client.get("/favorites")
    assert response.status_code == 200


# ========== 測試：API 端點 ==========


def test_api_chat_empty_message(client):
    """測試：空訊息應該回傳 400"""
    response = client.post("/api/chat", json={"message": ""})
    assert response.status_code == 400
    data = response.get_json()
    assert "error" in data


def test_api_chat_with_message(client, mocker):
    """測試：正常訊息"""
    # Mock Gemini API
    mock_response = mocker.Mock()
    mock_response.text = (
        '{"year": null, "season": null, "keywords": null, "response_type": "chat"}'
    )
    mocker.patch("chatbot.model.generate_content", return_value=mock_response)

    response = client.post("/api/chat", json={"message": "你好"})
    assert response.status_code == 200
    data = response.get_json()
    assert data["type"] == "chat"


def test_api_chat_with_pagination(client, mocker):
    """測試：分頁參數"""
    mock_response = mocker.Mock()
    mock_response.text = (
        '{"year": 2024, "season": null, "keywords": "魔女", "response_type": "search"}'
    )
    mocker.patch("chatbot.model.generate_content", return_value=mock_response)

    response = client.post(
        "/api/chat", json={"message": "2024 魔女", "offset": 10, "limit": 5}
    )
    assert response.status_code == 200
    data = response.get_json()
    assert data["type"] == "search"
    assert data["offset"] == 10
    assert data["limit"] == 5


# ========== 測試：錯誤處理 ==========


def test_404_error(client):
    """測試：404 錯誤"""
    response = client.get("/nonexistent")
    assert response.status_code == 404
    data = response.get_json()
    assert "error" in data
