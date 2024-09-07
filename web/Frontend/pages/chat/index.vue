<script setup>
const config = useRuntimeConfig();

const messageLists = ref([]);
const tempUserMessage = ref('');
const tempImage = ref('');

const isLoading = ref(false);

const add_user_message = async () => {
  if (tempUserMessage.value.trim()) {
    messageLists.value.push({
      type: 'user',
      text: tempUserMessage.value
    });
    const userMessage = tempUserMessage.value;
    tempUserMessage.value = '';

    // Show loading state
    isLoading.value = true;
    try {
      const gptResponse = await get_location_response(userMessage);
      console.log(gptResponse)
      messageLists.value.push({
        type: 'ai',
        text: gptResponse
      });
    } catch (error) {
      console.error('Error getting GPT response:', error);
      messageLists.value.push({
        type: 'ai',
        text: 'Sorry, I encountered an error. Please try again.'
      });
    } finally {
      isLoading.value = false;
    }
  }
};

const add_image_message = async (tempImage) => {
  console.log("add_image_message", tempImage.value)
  if (tempImage.value) {
    // Create a blob from the Uint8Array
    const blob = new Blob([tempImage.value], { type: 'application/octet-stream' });
    
    messageLists.value.push({
      type: 'user',
      image: URL.createObjectURL(blob) // Create a URL for display
    });

    // Show loading state
    isLoading.value = true;
    try {
      const gptResponse = await get_location_response_by_image(blob);

      console.log(gptResponse)
      messageLists.value.push({
        type: 'ai',
        text: gptResponse
      });
    } catch (error) {
      console.error('Error getting GPT response:', error);
      messageLists.value.push({
        type: 'ai',
        text: 'Sorry, I encountered an error. Please try again.'
      });
    } finally {
      isLoading.value = false;
    }
  }
  // Clear the tempImage

  tempImage.value = null;
};


// 取得地點回應
const get_location_response = async (location_name) => {
  const formData = new FormData();
  formData.append('location_name', location_name); // Add the key-value pair
  console.log(formData)

  // 如果tempImage有值，則使用upload-image

  const { data, error } = await useFetch('https://adaf-211-75-133-2.ngrok-free.app/query-location', {
    method: 'POST',
    body: formData, // Send the form data
  });
  if (error.value) {
    console.error('Error during the request:', error.value);
    return null; // Handle error appropriately
  }

  return data.value; // Assuming a successful JSON response

};

const get_location_response_by_image = async (image) => {
  const formData = new FormData();
  formData.append('file', image, 'image.bin'); // Append as binary file

  console.log(formData)

  const { data, error } = await useFetch('https://adaf-211-75-133-2.ngrok-free.app/upload-image', {
    method: 'POST',
    headers: {
      'Accept': 'text/plain', // Expect plain text response
    },

    body: formData, // Send the form data
  });

  if (error.value) {
    console.error('Error during the request:', error.value);
    return null; // Handle error appropriately
  }

  return data.value; // Assuming a successful JSON response
};



// 圖片上傳
const handle_image_upload = (event) => {
  const file = event.target.files[0];
  const reader = new FileReader();
  reader.readAsArrayBuffer(file);
  reader.onload = () => {
    const arrayBuffer = reader.result;
    const uint8Array = new Uint8Array(arrayBuffer);
    tempImage.value = uint8Array;
    add_image_message(tempImage);
  };
};

const checkUrlParams = () => {
  const route = useRoute();
  const location = route.query.location;
  if (location) {
    tempUserMessage.value = location;
    add_user_message();
  }
};

// Modify the onMounted hook
onMounted(() => {
  checkUrlParams();
})

</script>
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
      <div class="message-container">
        <div v-for="(message, index) in messageLists" :key="index"
          :class="['message', message.type === 'user' ? 'user-message' : 'ai-message']">
          {{ message.text }}
          <img v-if="message.image" :src="message.image" class="message-image">
        </div>
        <div v-if="isLoading" class="message ai-message">
          Thinking...
        </div>
      </div>
    </main>

    <footer>
      <div class="input-container">
        <div class="input-container-left">
          <!-- <button class="voice-input">🎤</button> -->
          <label for="image-upload" class="image-upload-label">
            <span class="image-icon">🖼️</span>
            <span class="upload-text">Upload Image</span>
          </label>
          <input type="file" id="image-upload" class="image-upload" @change="handle_image_upload" accept="image/*">
        </div>
        <div class="input-container-middle">
          <!-- <img v-show"tempImage" :src="tempImage" class="image-preview"> -->
          <input type="text" placeholder="輸入訊息" class="text-input" v-model="tempUserMessage">
        </div>

        <div class="send-message" @click="add_user_message">
          <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="white" width="20" height="20">
            <path d="M2,21L23,12L2,3V10L17,12L2,14V21Z" />
          </svg>
        </div>
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
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  border-bottom: 1px solid rgba(0, 0, 0, 0.1);

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

.message-container {
  display: flex;
  flex-direction: column;
}

.message {
  max-width: 80%;
  margin-bottom: 10px;
  padding: 10px;
  border-radius: 10px;
}

.message-image {
  max-width: 100%;
  max-height: 100%;
  object-fit: cover;
  border-radius: 10px;
}

@keyframes fadeIn {
  from { opacity: 0; }
  to { opacity: 1; }
}

.user-message {
  align-self: flex-end;
  background-color: #e6f3ff;
  animation: fadeIn 0.5s ease-in-out;

}

.ai-message {
  align-self: flex-start;
  background-color: #f0f0f0;
  animation: fadeIn 1s ease-in-out;

}

footer {
  padding: 10px;
}

.input-container {
  display: flex;
  align-items: center;
  justify-content: space-between;
  background-color: #f0f0f0;
  border-radius: 20px;
  height: 100%;
  padding: 5px;
}

.voice-input,
.image-upload {
  width: 40px;
  background: none;
  border: none;
  font-size: 20px;
  cursor: pointer;
  padding: 5px;
}

.send-message {
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
  width: 30px;
  height: 30px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.image-upload-label {
  display: flex;
  align-items: center;
  cursor: pointer;
  padding: 5px 10px;
  background-color: #5fb0c9;
  color: white;
  border-radius: 15px;
  font-size: 14px;
  transition: background-color 0.3s ease;
}

.input-container-left {
  height: 100%;
  margin-right: 10px;
  display: flex;
  flex-direction: row;
  align-items: center;
  justify-content: center;
}

.input-container-middle {
  height: 100%;
  margin-right: 10px;
  display: flex;
  flex-direction: row;
  align-items: center;
  justify-content: center;
}

.image-upload-label:hover {
  background-color: #4a8fa5;
}

.image-icon {
  margin-right: 5px;
}

.upload-text {
  display: none;
}

.image-upload {
  display: none;
}

@media (min-width: 768px) {
  .upload-text {
    display: inline;
  }
}

.image-preview {
  max-width: 100px;
  max-height: 40px;
  object-fit: cover;
  margin-right: 10px;
  border-radius: 5px;
}
</style>