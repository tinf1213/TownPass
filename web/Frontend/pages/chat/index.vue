<template>
  <div class="container">
    <header>
      <button class="menu-button">☰</button>
      <h1 class="title">
        文化時空隧道
        <span class="sparkle">✨</span>
      </h1>
    </header>

    <main>
      <p class="description">
        上傳照片，立即生成精彩描述；模擬歷史事件，體驗不同時代的故事；提問與討論，隨時解答您的好奇心；與歷史人物對話，感受他們的智慧與情感。讓我們一起探索台北的魅力吧！
      </p>
    </main>

    <footer>
      <div class="input-container">
        <button class="voice-input">🎤</button>
        <input type="text" placeholder="輸入訊息" class="text-input">
        <button class="image-upload">🖼️</button>
        <button class="send-message">✏️</button>
      </div>
    </footer>
  </div>
</template>

<style scoped>
.container {
  display: flex;
  flex-direction: column;
  height: 100vh;
  font-family: Arial, sans-serif;
}

header {
  display: flex;
  align-items: center;
  padding: 10px;
}

.menu-button {
  font-size: 24px;
  background: none;
  border: none;
  cursor: pointer;
}

.title {
  font-size: 24px;
  margin-left: 20px;
}

.sparkle {
  color: gold;
}

main {
  flex-grow: 1;
  padding: 20px;
  overflow-y: auto;
}

.description {
  font-size: 16px;
  line-height: 1.5;
}

footer {
  padding: 10px;
}

.input-container {
  display: flex;
  align-items: center;
  background-color: #f0f0f0;
  border-radius: 20px;
  padding: 5px;
}

.voice-input, .image-upload, .send-message {
  background: none;
  border: none;
  font-size: 20px;
  cursor: pointer;
  padding: 5px;
}

.text-input {
  flex-grow: 1;
  border: none;
  background: none;
  padding: 10px;
  font-size: 16px;
}

.send-message {
  background-color: #5fb0c9;
  color: white;
  border-radius: 50%;
  width: 40px;
  height: 40px;
  display: flex;
  align-items: center;
  justify-content: center;
}
</style>
