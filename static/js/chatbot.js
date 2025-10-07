const chatMessages = document.getElementById("chatMessages");
  const chatInput = document.getElementById("chatInput");
  const sendBtn = document.getElementById("sendBtn");
  const typingIndicator = document.getElementById("typingIndicator");

  // 發送訊息
  async function sendMessage() {
    const message = chatInput.value.trim();

    if (!message) return;

    // 顯示使用者訊息
    addMessage("user", message);

    // 清空輸入框
    chatInput.value = "";

    // 禁用按鈕和輸入框
    sendBtn.disabled = true;
    chatInput.disabled = true;

    // 顯示打字中
    typingIndicator.classList.add("show");
    scrollToBottom();

    try {
      // 呼叫 API
      const response = await fetch("/api/chat", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ message: message }),
      });

      const data = await response.json();

      // 隱藏打字中
      typingIndicator.classList.remove("show");

      // 顯示機器人回應
      if (data.type === "chat") {
        addMessage("bot", data.message);
      } else if (data.type === "search") {
        addSearchResults(data);
      }
    } catch (error) {
      console.error("Error:", error);
      typingIndicator.classList.remove("show");
      addMessage("bot", "抱歉，發生錯誤了 😢");
    } finally {
      // 重新啟用
      sendBtn.disabled = false;
      chatInput.disabled = false;
      chatInput.focus();
    }
  }

  // 新增訊息到聊天室
  function addMessage(sender, text) {
    const messageDiv = document.createElement("div");
    messageDiv.className = `message ${sender}`;

    const bubble = document.createElement("div");
    bubble.className = "message-bubble";
    bubble.innerHTML = text.replace(/\n/g, "<br>");

    messageDiv.appendChild(bubble);
    chatMessages.insertBefore(messageDiv, typingIndicator.parentElement);

    scrollToBottom();
  }

  // 新增搜尋結果
  function addSearchResults(data) {
    const messageDiv = document.createElement("div");
    messageDiv.className = "message bot";

    const bubble = document.createElement("div");
    bubble.className = "message-bubble";

    let html = `找到 <strong>${data.count}</strong> 部動畫`;

    if (data.results.length === 0) {
      html += "<br><br>沒有找到相關動畫 😢";
    } else {
      data.results.forEach((anime) => {
        html += `
          <div class="anime-result">
            <div class="anime-title">${anime.title}</div>
            <div class="anime-info">${anime.year}年 第${anime.season}季</div>
            <div class="platform-buttons">
              <a href="${anime.platform_urls.anime1}" target="_blank" class="platform-btn anime1">Anime1</a>
              <a href="${anime.platform_urls.bahamut}" target="_blank" class="platform-btn bahamut">巴哈姆特</a>
              <a href="${anime.platform_urls.youtube}" target="_blank" class="platform-btn youtube">YouTube</a>
              <button class="favorite-btn" onclick="toggleFavorite(${anime.id}, this)">⭐ 收藏</button>
            </div>
          </div>
        `;
      });
    }

    bubble.innerHTML = html;
    messageDiv.appendChild(bubble);
    chatMessages.insertBefore(messageDiv, typingIndicator.parentElement);

    scrollToBottom();
  }

  // 滾動到底部
  function scrollToBottom() {
    chatMessages.scrollTop = chatMessages.scrollHeight;
  }

  // 收藏功能
  async function toggleFavorite(animeId, button) {
    const isFavorited = button.classList.contains("favorited");

    try {
      if (isFavorited) {
        // 移除收藏
        const response = await fetch(`/api/favorite/${animeId}`, {
          method: "DELETE",
        });
        const data = await response.json();

        if (data.success) {
          button.classList.remove("favorited");
          button.textContent = "⭐ 收藏";
        }
      } else {
        // 新增收藏
        const response = await fetch(`/api/favorite/${animeId}`, {
          method: "POST",
        });
        const data = await response.json();

        if (data.success) {
          button.classList.add("favorited");
          button.textContent = "❤️ 已收藏";
        } else if (response.status === 400) {
          // 已經收藏過了
          button.classList.add("favorited");
          button.textContent = "❤️ 已收藏";
        }
      }
    } catch (error) {
      console.error("收藏失敗:", error);
      alert("收藏功能發生錯誤");
    }
  }

  // 事件監聽
  sendBtn.addEventListener("click", sendMessage);

  chatInput.addEventListener("keypress", (e) => {
    if (e.key === "Enter") {
      sendMessage();
    }
  });

  // 自動聚焦
  chatInput.focus();
  