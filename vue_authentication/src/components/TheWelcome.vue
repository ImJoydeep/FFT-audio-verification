<template>
  <div class="container mx-auto">
    <div class="flex justify-center">
      <div class="max-w-lg w-full py-8">
        <div class="text-center py-4">
          <div class="flex justify-between  w-full bg-black">
            <button @click="activeTab = 'login'"
              :class="{ 'bg-blue-500 text-white': activeTab === 'login', 'bg-gray-200': activeTab !== 'login' }"
              class="w-1/2 py-4">
              Login
            </button>
            <button @click="activeTab = 'register'"
              :class="{ 'bg-blue-500 text-white': activeTab === 'register', 'bg-gray-200': activeTab !== 'register' }"
              class="w-1/2 py-4">
              Register
            </button>
          </div>
          <div v-if="activeTab === 'login'" class="bg-gray-100 p-4">
            <h2 class="text-2xl font-extrabold mb-4">Login</h2>
            <div class="flex justify-center mb-4">
              <input type="text" v-model="username" placeholder="Username"
                class="border border-gray-300 px-3 py-2 rounded focus:outline-none focus:border-gray-700" />
              <input type="text" v-model="password" placeholder="Password"
                class="border border-gray-300 px-3 py-2 rounded focus:outline-none focus:border-gray-700" />
            </div>
            <div class="flex justify-center mb-4">
              <button @click="startRecording" class="bg-green-500 text-white px-4 py-2 rounded mr-2">
                {{ recording ? 'Recording...' : 'Start Recording' }}
              </button>
              <button @click="stopRecording" class="bg-red-500 text-white px-4 py-2 rounded">
                Stop Recording
              </button>
            </div>
            <div v-if="recording" class="text-lg mb-2">Recording time: {{ recordingTime }}</div>

            <div class="flex justify-center my-4"> <audio :src="loginAudioURL" v-if="loginAudioURL" controls
                class="my-4"></audio></div>
            <div v-if="!recording && loginAudioURL" class="flex justify-center">
              <button @click="playAudio(loginAudioURL)" class="bg-blue-500 text-white px-4 py-2 rounded mr-2">
                <font-awesome-icon :icon="['fas', 'volume-high']" fade />
              </button>
              <button @click="deleteAudio('login')" class="bg-red-500 text-white px-4 py-2 rounded">
                <font-awesome-icon :icon="['fas', 'trash-can']" shake />
              </button>
            </div>
            <button @click="login" class="bg-blue-500 text-white px-4 py-2 rounded mt-4">
              Submit
            </button>
          </div>

          <div v-if="activeTab === 'register'" class="bg-gray-100 p-4">
            <h2 class="text-2xl font-bold mb-4">Register</h2>
            <div class="flex justify-center mb-4">
              <input type="text" v-model="username" placeholder="Username"
                class="border border-gray-300 px-3 py-2 rounded focus:outline-none focus:border-gray-700" />
              <input type="text" v-model="password" placeholder="Password"
                class="border border-gray-300 px-3 py-2 rounded focus:outline-none focus:border-gray-700" />
            </div>
            <div class="flex justify-center mb-4">
              <button @click="startRecording" class="bg-green-500 text-white px-4 py-2 rounded mr-2">
                {{ recording ? 'Recording...' : 'Start Recording' }}
              </button>
              <button @click="stopRecording" class="bg-red-500 text-white px-4 py-2 rounded">
                Stop Recording
              </button>
            </div>
            <div v-if="recording" class="text-lg mb-2">Recording time: {{ recordingTime }}</div>
            <div class="flex justify-center my-4"> <audio :src="registerAudioURL" v-if="registerAudioURL" controls
                class="my-4"></audio> </div>
            <div v-if="!recording && registerAudioURL" class="flex justify-center">
              <button @click="playAudio(registerAudioURL)" class="bg-blue-500 text-white px-4 py-2 rounded mr-2">
                <font-awesome-icon :icon="['fas', 'volume-high']" fade />
              </button>
              <button @click="deleteAudio('register')" class="bg-red-500 text-white px-4 py-2 rounded">
                <font-awesome-icon :icon="['fas', 'trash-can']" shake />
              </button>
            </div>
            <button @click="register" class="bg-blue-500 text-white px-4 py-2 rounded mt-4">
              Submit
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, watch } from 'vue';
import axios from 'axios';

const activeTab = ref('login');
const recording = ref(false);
const recordingTime = ref(0);
const username = ref('')
const password = ref('')
const loginAudioURL = ref(localStorage.getItem('loginAudioURL') || '');
const registerAudioURL = ref(localStorage.getItem('registerAudioURL') || '');

let mediaRecorder;
let chunks = [];
let timerInterval;

const startRecording = () => {
  navigator.mediaDevices.getUserMedia({ audio: true })
    .then((stream) => {
      recording.value = true;
      recordingTime.value = 0;
      chunks = [];

      mediaRecorder = new MediaRecorder(stream);
      mediaRecorder.addEventListener('dataavailable', (event) => {
        chunks.push(event.data);
      });

      mediaRecorder.addEventListener('stop', () => {
        const blob = new Blob(chunks, { type: 'audio/ogg; codecs=opus' });
        const audioURL = URL.createObjectURL(blob);

        if (activeTab.value === 'login') {
          loginAudioURL.value = audioURL;
          localStorage.setItem('loginAudioURL', audioURL);
        } else if (activeTab.value === 'register') {
          registerAudioURL.value = audioURL;
          localStorage.setItem('registerAudioURL', audioURL);
        }
      });

      mediaRecorder.start();
      timerInterval = setInterval(() => {
        recordingTime.value += 1;
        if (recordingTime.value >= 5) {
          stopRecording();
        }
      }, 1000);
    })
    .catch((error) => {
      console.error(error);
    });
};

const stopRecording = () => {
  clearInterval(timerInterval);
  recording.value = false;
  recordingTime.value = 0;
  mediaRecorder.stop();
};

const playAudio = (audioURL) => {
  const audio = new Audio(audioURL);
  audio.play();
};

const deleteAudio = (tab) => {
  if (tab === 'login') {
    loginAudioURL.value = '';
    localStorage.removeItem('loginAudioURL');
  } else if (tab === 'register') {
    registerAudioURL.value = '';
    localStorage.removeItem('registerAudioURL');
  }
};

const login = async () => {
  const audioBlob = chunks[0]; // Assuming you are recording a single audio chunk
  const formData = new FormData();
  formData.append('username', username.value);
  formData.append('password', password.value);
  formData.append('audio', audioBlob, 'audio.wav');

  try {
    const response = await axios.post('api/users/login/', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });
    console.log(response.data);
  } catch (error) {
    console.error(error);
  }
};


const register = async () => {
  const audioBlob = chunks[0]; // Assuming you are recording a single audio chunk
  console.log(chunks)
  const formData = new FormData();
  formData.append('username', username.value);
  formData.append('password', password.value);
  formData.append('audio', audioBlob, 'audio.wav');

  try {
    const response = await axios.post('api/users/register/', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });
    console.log(response.data);
  } catch (error) {
    console.error(error);
  }
};

</script>

<style scoped>
/* Your custom styles here */
</style>
