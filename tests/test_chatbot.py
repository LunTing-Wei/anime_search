import pytest
import os
import sys
import json

sys.path.insert(
    0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src"))
)
from chatbot import (
    parse_user_message,
    handle_chat,
    CHAT_RESPONSES,
    DEFAULT_CHAT_RESPONSE,
)

# ========== 測試：聊天回應 ==========


def test_handle_chat_greeting():
    """測試：問候語"""
    result = handle_chat("你好")
    assert "動畫查詢助手" in result


def test_handle_chat_thanks():
    """測試：感謝"""
    result = handle_chat("謝謝")
    assert "不客氣" in result


def test_handle_chat_unknown():
    """測試：未知訊息"""
    result = handle_chat("隨便說點什麼")
    assert result == DEFAULT_CHAT_RESPONSE


# ========== 測試：Gemini 解析（Mock）==========


def test_parse_user_message_with_mock(mocker):
    """測試：模擬 Gemini API 回應"""
    # 模擬 Gemini 的回應
    mock_response = mocker.Mock()
    mock_response.text = (
        '{"year": 2024, "season": null, "keywords": "魔女", "response_type": "search"}'
    )

    # 替換 model.generate_content
    mocker.patch("chatbot.model.generate_content", return_value=mock_response)

    # 測試
    result = parse_user_message("2024 年的魔女動畫")

    assert result["year"] == 2024
    assert result["season"] is None
    assert result["keywords"] == "魔女"
    assert result["response_type"] == "search"


def test_parse_user_message_api_failure(mocker):
    """測試：API 失敗時的降級處理"""
    # 模擬 API 錯誤
    mocker.patch("chatbot.model.generate_content", side_effect=Exception("API Error"))

    # 測試
    result = parse_user_message("測試訊息")

    # 應該降級成直接搜尋
    assert result["response_type"] == "search"
    assert result["keywords"] == "測試訊息"
