import Vue from 'vue'
import Router from 'vue-router'
import AppMain from '@/components/AppMain'

Vue.use(Router)

export default new Router({
  routes: [
    {
      path: '/',
      name: 'LCMS',
      component: AppMain
    }
  ]
})
