<template>
  <div class="grid place-items-center bg-gray-800">
    <div class="grid grid-cols-1 md:grid-cols-2 gap-4 bg-gray-900 shadow-lg shadow-gray-500 p-4 rounded-lg ">
      <div class="p-6">
        <img src="../assets/working_late.png" alt="Image"
          class="w-[500px] h-[450px] hover:brightness-150 hover:cursor-pointer" />
      </div>
      <div class="p-4 shadow-md shadow-gray-800 rounded-lg">
        <div class="hover:text-teal-400 text-cyan-300">
          <h2 class="text-2xl font-bold ">Register Form</h2>
          <p class="mb-4">Create Account</p>
        </div>

        <form @submit.prevent>
          <div class="my-6">
            <div class="relative flex items-center gap-2">
              <font-awesome-icon :icon="['fas', 'user']" style="color: #eeeeec;" />
              <input type="text" id="username" v-model="username"
                class="border-2 rounded px-3 py-2  w-full focus:border-secondary focus:outline-none focus:shadow-[0px_1px_0_0_#004E71]"
                placeholder="Userame" required/>
            </div>
          </div>
          <div class="mb-6">
            <div class="relative flex items-center gap-2">
              <font-awesome-icon :icon="['fas', 'envelope']" style="color: #eeeeec;" />
              <input type="email" id="email" v-model="email"
                class="border rounded px-3 py-2 w-full focus:border-secondary focus:outline-none focus:shadow-[0px_1px_0_0_#004E71]"
                placeholder="Email" required/>
            </div>
          </div>
          <div class="mb-6">
            <!-- <div class="relative flex items-center gap-2">
              <font-awesome-icon :icon="['fas', 'lock']" style="color: #eeeeec;" />
              <input type="password" id="password" v-model="password"
                class="border rounded px-3 py-2 w-full focus:border-secondary focus:outline-none focus:shadow-[0px_1px_0_0_#004E71]"
                placeholder="Password" />
            </div> -->
          </div>
          <div class="flex justify-center mb-4">
            <button v-if="!record" @click="startRecording" class="bg-green-500 text-white px-4 py-2 rounded mr-2">
              Start Recording
            </button>
          </div>
          <div v-if="!record" class="relative flex items-center gap-2 mx-10">
              <!-- <p class="text-yellow-300">Hint: </p> -->
              <p class="text-red-300 items-center ml-4">Please record 5 seconds of audio for voice verification</p>
            </div>
          <div v-if="recording" class="text-lg mb-2 text-indigo-400">Recording time: {{ recordingTime }}</div>
          <div v-if="!recording && registerAudioURL" class="flex justify-center">
            <button @click="playAudio(registerAudioURL)" class="bg-blue-500 text-white px-4 py-2 rounded mr-2">
              <font-awesome-icon :icon="['fas', 'volume-high']" fade />
            </button>
            <button @click="deleteAudio()" class="bg-red-500 text-white px-4 py-2 rounded">
              <font-awesome-icon :icon="['fas', 'trash-can']" shake />
            </button>
          </div>
          <button @click="register" type="submit"
            class="bg-gray-800 hover:bg-gray-600 text-white font-bold py-2 w-11/12 ml-5 my-2 rounded">
            Register
          </button>
        </form>
        <p class="text-gray-300">Already have account? <RouterLink to="/login" class="text-blue-700 mx-1">Login</RouterLink>
        </p>
      </div>
    </div>
  </div>
</template>


<script setup>
import { ref, watch } from 'vue';
import axios from 'axios';

const recording = ref(false);
const record = ref(false);
const recordingTime = ref(0);
const username = ref('')
const password = ref('')
const email = ref('')
const registerAudioURL = ref(localStorage.getItem('registerAudioURL') || '');
let mediaRecorder;
let chunks = [];
let timerInterval;

const startRecording = () => {
  navigator.mediaDevices.getUserMedia({ audio: true })
    .then((stream) => {
      recording.value = true;
      record.value = true;
      recordingTime.value = 0;
      chunks = [];

      mediaRecorder = new MediaRecorder(stream);
      mediaRecorder.addEventListener('dataavailable', (event) => {
        chunks.push(event.data);
      });

      mediaRecorder.addEventListener('stop', () => {
        const blob = new Blob(chunks, { type: 'audio/ogg' });
        const audioURL = URL.createObjectURL(blob);
        registerAudioURL.value = audioURL;
        localStorage.setItem('registerAudioURL', audioURL);
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
  registerAudioURL.value = '';
  localStorage.removeItem('registerAudioURL');
  record.value = false;
};

const register = async () => {
  const audioBlob = chunks[0]; // Assuming you are recording a single audio chunk
  const audioFile = new File([audioBlob], `audio.wav`, { type: 'audio/wav' });
  console.log(chunks)
  const formData = new FormData();
  formData.append('username', username.value);
  formData.append('password', password.value);
  formData.append('email', email.value);
  formData.append('audio', audioFile);

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



