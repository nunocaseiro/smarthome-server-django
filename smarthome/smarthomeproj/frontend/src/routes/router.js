import Vue from 'vue';
import VueRouter from 'vue-router';
import routes from './routes';
import store from '../store/store.js';

Vue.use(VueRouter);

// configure router
const router = new VueRouter({
  routes, // short for routes: routes
  linkActiveClass: 'active',
  scrollBehavior: (to, from ,savedPosition) => {
    if (savedPosition) {
      return savedPosition;
    }
    if (to.hash) {
      return { selector: to.hash };
    }
    return { x: 0, y: 0 };
  }
  
});

router.beforeEach((to,from,next)=>{
  
  
 if(to.matched.some(record=>record.meta.forAuth)) {
    if (!store.getters.isAuthenticated) {
        next({
            path: '/login'
        })
    } else next()
  
  }  else if(to.matched.some(record=>record.meta.forVisitors)) {
      if (store.getters.isAuthenticated) {
          next({
              path: '/'
          })
      } next()
    
  }else next()
    
    
    })

export default router;
