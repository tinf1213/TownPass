<script setup>
// Add any necessary imports and logic here
const nowPlace = ref(false)
const navigate_to_chat = (location) => {
  if (nowPlace) {
    navigateTo(`/chat?location=${encodeURIComponent(location)}`);
  } else {
    // If there's no image, just navigate with the location
    navigateTo(`/chat?location=${encodeURIComponent(location)}`);
  }
}

const handle_image_upload = (event) => {
  const file = event.target.files[0];
  if (file) {
    tempImageFile.value = file;
    tempUserMessage.value = file.name;
    navigate_to_chat(tempUserMessage.value);
  }
}
</script>

<template>
  <div class="container">
    <h1 class="title">
      <div class="sparkle">✨</div>
      文化時空隧道
    </h1>

    <p class="description">
      上傳照片，立即生成精彩描述；提問與討論，隨時解答您的好奇心。讓我們一起探索台北的魅力吧！
    </p>


    <!-- <NuxtLink to="/chat" class="primary-button">立即聊天!</NuxtLink> -->
    <div class="input-container">
      <div class="input-wrapper">
        <textarea v-model="tempUserMessage" placeholder="輸入景點或上傳圖片" class="text-input" rows="3"></textarea>
        <div class="button-group">
          <label for="image-upload" class="image-upload-label">

            直接進入聊天室!
          </label>
          <input id="image-upload" class="image-upload" @click="navigateTo('/chat')" accept="image/*">
          <button class="send-button" @click="navigate_to_chat(tempUserMessage)">
            <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor" width="24" height="24">
              <path d="M2,21L23,12L2,3V10L17,12L2,14V21Z" />
            </svg>
          </button>
        </div>
      </div>
    </div>

    <p class="subtitle">
      您可以選擇以下地點詢問，讓我們一起探索台北的魅力！
    </p>
    <div class="location-list">
      <TextList class="location-list-item" :texts="['台北101', '故宮博物院', '中正紀念堂', '台北車站', '西門町']"
        @click="navigateTo('/chat?location=台北101')" />
    </div>
    <p class="subtitle">或是</p>
    <div class="location-button-container">
      <button class="location-button" @click="nowPlace = true; navigateTo('/chat?location=國立臺灣大學')">
        <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor" width="24" height="24">
          <path
            d="M12 2C8.13 2 5 5.13 5 9c0 5.25 7 13 7 13s7-7.75 7-13c0-3.87-3.13-7-7-7zm0 9.5c-1.38 0-2.5-1.12-2.5-2.5s1.12-2.5 2.5-2.5 2.5 1.12 2.5 2.5-1.12 2.5-2.5 2.5z" />
        </svg>
        尋找附近景點
      </button>
    </div>
    <p class="subtitle">或是看看這些景點</p>
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
  animation: fadeIn 0.7s ease-in-out;
}

@keyframes fadeIn {
  from {
    opacity: 0;
  }

  to {
    opacity: 1;
  }
}

.title {
  padding-left: 32px;
  padding-right: 32px;
  text-align: center;
  font-size: 36px;
  font-weight: bold;
  margin-top: 32px;
  margin-bottom: 20px;
  animation: fadeIn 0.7s ease-in-out 0.2s both;
}

.sparkle {
  color: gold;
  display: flex;
  align-items: center;
  justify-content: center;
}

.description {
  padding-left: 32px;
  padding-right: 32px;
  margin-top: 28px;
  font-size: 20px;
  line-height: 1.5;
  margin-bottom: 20px;
  animation: fadeIn 0.7s ease-in-out 0.4s both;
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
  animation: fadeIn 0.7s ease-in-out 0.6s both;
}

.input-container {
  padding: 20px;

  margin: 20px auto;
  background-color: #f8f8f8;
  border-radius: 12px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  width: 90%;
  max-width: 600px;
  animation: fadeIn 0.7s ease-in-out 0.8s both;
}

.input-wrapper {
  display: flex;
  flex-direction: column;
  align-items: center;
}

.text-input {
  width: 90%;
  border: 1px solid #e0e0e0;
  border-radius: 8px;
  padding: 12px;
  font-size: 16px;
  resize: none;
  margin-bottom: 12px;
  transition: border-color 0.3s ease;

}

.text-input:focus {
  outline: none;
  border-color: #5fb0c9;
}

.button-group {
  display: flex;
  justify-content: space-between;
  align-items: center;
  width: 90%;
}

.image-upload-label {
  background-color: #5fb0c9;
  display: flex;
  color: white;
  width: 60%;
  height: 40px;
  border-radius: 12px;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

.send-button {
  background-color: #5fb0c9;
  color: white;
  border: none;
  border-radius: 50%;
  width: 40px;
  height: 40px;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

.image-upload-label:hover,
.send-button:hover {
  background-color: #4a8fa5;
}

.location-button-container {
  padding-left: 32px;
  padding-right: 32px;
  margin-top: 40px;
  margin-bottom: 20px;
  animation: fadeIn 1s ease-in-out 0.8s both;
}

.location-button {
  background-color: #738995;
  color: white;
  border: none;
  border-radius: 12px;
  padding: 12px 20px;
  margin-left: auto;
  margin-right: auto;
  display: block;
  width: 90%;
  max-width: 600px;
  text-align: center;
  font-size: 18px;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

.image-upload {
  display: none;
}

.location-list {
  padding-left: 32px;
  padding-right: 32px;
  margin-top: 20px;
  margin-bottom: 20px;
  animation: fadeIn 1s ease-in-out 0.8s both;
}

.location-list-item {
  cursor: pointer;
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
  animation: fadeIn 1s ease-in-out1s both;
}
</style>