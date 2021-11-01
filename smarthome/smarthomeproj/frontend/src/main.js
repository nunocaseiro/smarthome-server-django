// The Vue build version to load with the `import` command
// (runtime-only or standalone) has been set in webpack.base.conf with an alias.
import Vue from 'vue'
import App from './App'
import router from './routes/router';
import { BootstrapVue, IconsPlugin } from 'bootstrap-vue'
import 'bootstrap/dist/css/bootstrap.css'
import 'bootstrap-vue/dist/bootstrap-vue.css'
import Dashboard from '@/plugins/dashboard-plugin'
import Vuex from 'vuex';
import axios from 'axios';
import store from './store/store.js';
import SensorDetail from './views/Dashboard/SensorDetail.vue'
import dropdown from 'vue-dropdowns';
import VueMqtt from 'vue-mqtt';
Vue.use(BootstrapVue)
Vue.use(IconsPlugin)
Vue.use(Dashboard);
Vue.use(Vuex);
Vue.config.productionTip = false

Vue.component(SensorDetail)
Vue.component('dropdown', dropdown)
Vue.use(VueMqtt, 'ws://161.35.8.148:8083/ws', {clientId: 'WebClient-' + parseInt(Math.random() * 100000), defaultProcotcol: "mqtt", username: "smarthome", password:""});

if (store.getters.getUser != null){
  store.state.user = store.getters.getUser;
  axios.defaults.headers.common['Authorization'] = "Token " + store.state.user.token;
}

axios.defaults.headers["content-type"] = "application/json";


new Vue({
  el: '#app',
  render: h => h(App),
  router,
  store,
  mounted(){
    this.$mqtt.subscribe('#')
  }
});




