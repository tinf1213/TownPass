<script setup>
// Add any necessary imports and logic here
</script>

<template>
  <div class="container">
    <h1 class="title">
      文化時空隧道
      <!-- <span class="sparkle">✨</span> -->
    </h1>

    <p class="description">
      上傳照片，立即生成精彩描述；模擬歷史事件，體驗不同時代的故事；提問與討論，隨時解答您的好奇心；與歷史人物對話，感受他們的智慧與情感。讓我們一起探索台北的魅力吧！
    </p>


    <NuxtLink to="/chat" class="primary-button">立即使用!</NuxtLink>
    <NuxtLink to="/test" class="primary-button">測試</NuxtLink>
    <p class="subtitle">或是考慮聊聊這些話題</p>
    <div class="carousel-container">
      <Carousel />
    </div>
    <!-- <TextList :texts="['台北101', '故宮博物院', '中正紀念堂', '台北車站', '西門町']" /> -->
  </div>
</template>
<style scoped>
.container {
  max-width: 600px;
  margin: 0 auto;
  font-family: Arial, sans-serif;
  animation: fadeIn 1s ease-in-out;
}

@keyframes fadeIn {
  from { opacity: 0; }
  to { opacity: 1; }
}

.title {
  padding-left: 32px;
  padding-right: 32px;
  font-size: 52px;
  font-weight: bold;
  margin-top: 32px;
  margin-bottom: 20px;
  animation: fadeIn 1s ease-in-out 0.2s both;
}

.sparkle {
  color: gold;
  margin-left: 5px;
}

.description {
  padding-left: 32px;
  padding-right: 32px;
  margin-top: 28px;
  font-size: 20px;
  line-height: 1.5;
  margin-bottom: 20px;
  animation: fadeIn 1s ease-in-out 0.4s both;
}

.primary-button {
  display: block;
  margin: 0 auto;
  text-align: center;
  width: fit-content;
  background-color: #5fb0c9;
  color: white;
  border: none;
  padding: 12px 20px;
  border-radius: 5px;
  font-size: 20px;
  cursor: pointer;
  margin-left: auto;
  animation: fadeIn 1s ease-in-out 0.6s both;
}

.subtitle {
  padding-left: 32px;
  padding-right: 32px;
  font-size: 18px;
  margin-top: 80px;
  margin-bottom: 20px;
  animation: fadeIn 1s ease-in-out 0.8s both;
}

.carousel-container {
  margin-top: 12px;
  margin-bottom: 20px;
  animation: fadeIn 1s ease-in-out 1s both;
}
</style>