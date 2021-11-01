import Vue from 'vue';
import Vuex from 'vuex';
import axios from 'axios';


Vue.use(Vuex);

export default new Vuex.Store({
        state:{
            user: {
                username: '',
                token: ''
            },
        },
        mutations: {
            setAuthUser(state, {user}) {
              state.user = user;
              console.log(user.username)
              axios.defaults.headers.common.Authorization = "Token " + user.token;
              localStorage.setItem('auth_user',JSON.stringify(state.user))
            },
          
          clearUser(state) {
            state.user = {
                username: '',
                token: ''
            };
         
            localStorage.removeItem('auth_user');
            axios.defaults.headers.common.Authorization = undefined;
            },
        },
        
        getters:{


          getUser(state){
            let user = localStorage.getItem('auth_user')
            if ( !user){
              return null
            }
            return JSON.parse(user);
          },

          getUserState(state){
            return state.user
          },
          
          isAuthenticated(state) {
            if(state.user.token != ''){
               return true;
            }
            return false;
        }
      
          
        },
          actions:{
            setAuthUser({commit},data){
                commit('setAuthUser',data);
            },
            
          }
});