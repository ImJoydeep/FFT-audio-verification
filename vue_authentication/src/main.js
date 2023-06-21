import './assets/tailwind.css'
import axios from 'axios';
import { createApp } from 'vue'
import App from './App.vue'
import router from './router'




// Font-Awesome Configuration
import { library } from '@fortawesome/fontawesome-svg-core';
import { fas, faUserSecret} from '@fortawesome/free-solid-svg-icons'
import { far } from '@fortawesome/free-regular-svg-icons'
import { fab } from '@fortawesome/free-brands-svg-icons'
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome';
library.add(fas, far, fab, faUserSecret)

// Axios Default URL
axios.defaults.baseURL = 'http://127.0.0.1:8000'

const app = createApp(App).component("font-awesome-icon", FontAwesomeIcon)

app.use(router)

app.mount('#app')
