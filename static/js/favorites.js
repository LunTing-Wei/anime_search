const loading = document.getElementById("loading");
  const emptyMessage = document.getElementById("emptyMessage");
  const favoritesList = document.getElementById("favoritesList");

  // 載入收藏列表
  async function loadFavorites() {
    try {
      const response = await fetch("/api/favorites");
      const data = await response.json();

      loading.style.display = "none";

      if (data.favorites.length === 0) {
        emptyMessage.style.display = "block";
      } else {
        renderFavorites(data.favorites);
      }
    } catch (error) {
      console.error("載入失敗:", error);
      loading.textContent = "載入失敗，請重新整理頁面";
    }
  }

  // 渲染收藏列表
  function renderFavorites(favorites) {
    favoritesList.innerHTML = "";

    favorites.forEach((anime) => {
      const card = document.createElement("div");
      card.className = "anime-card";
      card.id = `anime-${anime.id}`;

      card.innerHTML = `
        <div class="anime-info-section">
          <div class="anime-title">${anime.title}</div>
          <div class="anime-meta">${anime.year}年 第${anime.season}季 | 收藏於 ${formatDate(anime.created_at)}</div>
          <div class="platform-buttons">
            <a href="${anime.platform_urls.anime1}" target="_blank" class="platform-btn anime1">Anime1</a>
            <a href="${anime.platform_urls.bahamut}" target="_blank" class="platform-btn bahamut">巴哈姆特</a>
            <a href="${anime.platform_urls.youtube}" target="_blank" class="platform-btn youtube">YouTube</a>
          </div>
        </div>
        <button class="remove-btn" onclick="removeFavorite(${anime.id})">移除</button>
      `;

      favoritesList.appendChild(card);
    });
  }

  // 移除收藏
  async function removeFavorite(animeId) {
    if (!confirm("確定要移除此收藏嗎？")) return;

    try {
      const response = await fetch(`/api/favorite/${animeId}`, {
        method: "DELETE",
      });
      const data = await response.json();

      if (data.success) {
        // 移除卡片
        const card = document.getElementById(`anime-${animeId}`);
        card.style.transition = "all 0.3s";
        card.style.opacity = "0";
        card.style.transform = "translateX(-20px)";

        setTimeout(() => {
          card.remove();

          // 檢查是否為空
          if (favoritesList.children.length === 0) {
            emptyMessage.style.display = "block";
          }
        }, 300);
      }
    } catch (error) {
      console.error("移除失敗:", error);
      alert("移除失敗，請稍後再試");
    }
  }

  // 格式化日期
  function formatDate(dateString) {
    const date = new Date(dateString);
    return `${date.getFullYear()}/${String(date.getMonth() + 1).padStart(2, '0')}/${String(date.getDate()).padStart(2, '0')}`;
  }

  // 頁面載入時執行
  loadFavorites();