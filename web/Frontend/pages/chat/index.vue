<script setup>
import axios from 'axios';
const config = useRuntimeConfig();

const messageLists = ref([]);
const tempUserMessage = ref('');
const tempImage = ref('');
const isLoading = ref(false);
const latitude = ref(0);
const longitude = ref(0);
const places = ref([]);

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
      console.log(gptResponse);
      const responseLines = gptResponse.split('\n');
      for (const line of responseLines) {
        if (line.trim()) {  // Check if the line is not empty or just whitespace
          messageLists.value.push({
            type: 'ai',
            text: line
          });
        }
      }
      await get_current_location(userMessage);
      await get_nearby_places(userMessage);
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
const extractLandmark = (text) => {
  const match = text.match(/Landmark: (.*?)\nQuery/);
  if (match && match[1]) {
    return match[1].trim();
  }
  return null;
};
const add_image_message = async (tempImage) => {
  if (tempImage.value) {
    messageLists.value.push({
      type: 'user',
      image: URL.createObjectURL(tempImage.value)
    });

    // Show loading state
    isLoading.value = true;
    try {
      const gptResponse = ref(await get_location_response_by_image(tempImage.value));
      const landmark = extractLandmark(gptResponse.value);
      console.log("Extracted landmark:", landmark);

      console.log(gptResponse);
      // Remove "Landmark: Taipei 101 Observatory" and "Query Result:" from the response
      const cleanedResponse = gptResponse.value.replace(/^Landmark:.*\n/, '').replace(/^Query Result:\s*/, '');
      gptResponse.value = cleanedResponse;
      const responseLines = gptResponse.value.split('\n');
      for (const line of responseLines) {
        if (line.trim()) {  // Check if the line is not empty or just whitespace
          messageLists.value.push({
            type: 'ai',
            text: line
          });
        }
      }
      if (landmark) {
        await get_current_location(landmark);
        await get_nearby_places(landmark);
      } else {
        console.error("No landmark extracted from the response");
      }
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
  console.log("location_name", location_name)
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
  console.log("image", image)

  const formData = new FormData();
  formData.append('file', image);
  console.log("formData", formData)
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

const get_nearby_places = async () => {
  isLoading.value = true;
  try {
    // Create FormData object
    const formData = new FormData();
    formData.append('lat', latitude.value);
    formData.append('lon', longitude.value);
    formData.append('radius', 1500);
    formData.append('place_type', 'tourist_attraction');

    const response = await axios.post('https://adaf-211-75-133-2.ngrok-free.app/api/data', formData, {
      headers: {
        'Content-Type': 'multipart/form-data'
      }
    });
    console.log("response", response)
    console.log("response.data", response.data)
    // Assuming response.data contains an array of places
    places.value = response.data.places || [];
    messageLists.value.push({ text: '以下是為您推薦的附近景點', type: 'ai' });
    // console.log("testing");
    console.log("get_nearby_places");
    console.log(places.value);
    console.log(places.value[0]);
    console.log(places.value[0][0].link);
    console.log(places.value[0][1].name);

  } catch (error) {
    console.error('Error fetching data:', error);
    messageLists.value.push({ text: 'Failed to fetch places', type: 'ai' });
  } finally {
    isLoading.value = false;
  }
}

const get_current_location = async (locationName) => {
  console.log("get_current_location");
  console.log(locationName)
  isLoading.value = true;
  try {
    const formData = new FormData();
    formData.append('location_name', locationName);

    const response = await axios.post('https://adaf-211-75-133-2.ngrok-free.app/api/getLL', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
        'Access-Control-Allow-Origin': '*',
      }
    });

    // Assuming response.data contains an array of places
    places.value = response.data.places || [];
    console.log("testing");
    console.log(places.value);
    latitude.value = places.value.latitude;
    longitude.value = places.value.longitude;
    console.log("latitude", latitude.value);
    console.log("longitude", longitude.value);
    console.log("latitude", latitude.value);

  } catch (error) {
    console.error('Error fetching data:', error);
    messageLists.value.push({ text: 'Failed to fetch places', type: 'ai' });
  } finally {
    isLoading.value = false;
  }
}

// 圖片上傳
const handle_image_upload = (event) => {
  const file = event.target.files[0];
  const reader = new FileReader();
  reader.readAsArrayBuffer(file);
  reader.onload = () => {
    tempImage.value = file;
    add_image_message(tempImage);
  };
};

// 取得url參數，
const checkUrlParams = () => {
  const route = useRoute();
  const location = route.query.location;
  if (location) {
    tempUserMessage.value = location;
    add_user_message();
  }
};
// 取得座標
const extractCoordinates = (url) => {
  console.log("url", url)
  const match = url.match(/q=(-?\d+\.\d+),(-?\d+\.\d+)/);
  if (match) {
    const [_, lat, lng] = match;
    return `${lat},${lng}`;
  }
  return 'Invalid coordinates';
};
// 取得地圖嵌入url
const getMapEmbedUrl = (url) => {
  const match = url.match(/q=(-?\d+\.\d+),(-?\d+\.\d+)/);
  if (match) {
    const [_, lat, lng] = match;
    return `https://www.google.com/maps/embed/v1/view?key=YOUR_API_KEY&center=${lat},${lng}&zoom=15`;
  }
  return '';
};
// Modify the onMounted hook
onMounted(() => {
  checkUrlParams();
})
</script>
<template>
  <div class="container">
    <header>
      <!-- <button class="menu-button">☰</button> -->
      <h1 class="title">
        台北景點之眼
        <span class="sparkle">✨</span>
      </h1>
    </header>
    <main>
      <p class="description">
        上傳照片，立即生成精彩描述；提問與討論，隨時解答您的好奇心。讓我們一起探索台北的魅力吧！

      </p>
      <div class="message-container">
        <div v-for="(message, index) in messageLists" :key="index"
          :class="['message', message.type === 'user' ? 'user-message' : 'ai-message']">
          {{ message.text }}
          <img v-if="message.image" :src="message.image" class="message-image">
        </div>

        <div class="" v-if="!isLoading">
          <div class="recommend-place-title">
            <h3>推薦的附近景點</h3>
          </div>
          <div class="recommend-place">
            <div class="place-cards-container">
              <div v-for="(place, index) in places" :key="index" class="place-card">
                <div class="place-info-title">
                  {{ place[1].name }}
                </div>
                <iframe width="100%" height="450" style="border:0 ;border-radius: 10px;" loading="lazy" allowfullscreen
                  referrerpolicy="no-referrer-when-downgrade"
                  :src="`https://www.google.com/maps/embed/v1/place?key=${config.public.GOOGLE_MAPS_API_KEY}&q=${extractCoordinates(place[0].link)}`">
                </iframe>
              </div>
            </div>
          </div>
        </div>
        <div v-if="isLoading" class="message ai-message">
          思考中...
        </div>
      </div>
    </main>

    <footer>
      <div class="input-container">
        <div class="input-container-left">
          <!-- <button class="voice-input">🎤</button> -->
          <label for="image-upload" class="image-upload-label">
            <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor" width="24" height="24">
              <path
                d="M19,4H5A3,3,0,0,0,2,7V17a3,3,0,0,0,3,3H19a3,3,0,0,0,3-3V7A3,3,0,0,0,19,4ZM5,6H19a1,1,0,0,1,1,1v6.39l-3.71-3.7a1,1,0,0,0-1.41,0L8.71,16H5a1,1,0,0,1-1-1V7A1,1,0,0,1,5,6ZM19,18H5l7.29-7.29L19,17.41V17A1,1,0,0,1,19,18Zm-9-6a2,2,0,1,0-2-2A2,2,0,0,0,10,12Z" />
            </svg>
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

  background-color: white;
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
  animation: fadeIn 0.5s ease-in-out;
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
  from {
    opacity: 0;
  }

  to {
    opacity: 1;
  }
}

.user-message {
  align-self: flex-end;
  background-color: #B4E2EA;
  animation: fadeIn 0.5s ease-in-out;
}

.ai-message {
  align-self: flex-start;
  background-color: #EDF8FA;
  animation: fadeIn 1s ease-in-out;
}

.recommend-place-title {
  margin-top: 12px;
  border-radius: 10px;
  animation: fadeIn 0.2s ease-in-out;
}

.recommend-place {
  padding: 10px;
  margin-top: 4px;
  margin-bottom: 10px;
  border-radius: 10px;
  overflow-x: auto;
  /* Enable horizontal scrolling */
}


.place-cards-container {
  display: flex;
  flex-direction: row;
  /* Ensure cards are in a row */
  gap: 10px;
  /* Space between cards */
  padding-bottom: 10px;
  /* Add some padding at the bottom for scrollbar */
  animation: fadeIn 0.6s ease-in-out;
}

.place-card {
  background-color: #DBF1F5;
  flex: 0 0 auto;
  /* Prevent cards from shrinking */
  width: 280px;
  /* Set a fixed width for each card */
  padding: 10px;
  border-radius: 10px;
}

.place-info {
  border-radius: 10px;
}

.place-info-title {
  margin-top: 10px;
  margin-bottom: 20px;
  height: 40px;
  font-size: 20px;
  font-weight: bold;
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
  padding-left: 20px;
  padding-right: 20px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
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
  width: full;
  border: 1px solid #e0e0e0;
  border-radius: 8px;
  padding: 12px;
  font-size: 16px;
  resize: none;
  transition: border-color 0.3s ease;
}

.text-input:focus {
  outline: none;
  border-color: #5fb0c9;
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
  padding: 5px 5px;
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