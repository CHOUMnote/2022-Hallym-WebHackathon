import Vue from 'vue'
import VueRouter from 'vue-router'
import routes from './routes'
import storage from '@/utils/storage'
import {STORAGE_KEY} from '@/utils/constants'
import {sync} from 'vuex-router-sync'
import {types, default as store} from '../../../store'
import api from '@oj/api'
Vue.use(VueRouter, store)

const router = new VueRouter({
  mode: 'history',
  scrollBehavior (to, from, savedPosition) {
    if (to.hash) {
      return new Promise((resolve, reject) => {
        setTimeout(() => {
          resolve({
            selector: to.hash,
            offset: { x: 0, y: 80 }
          })
        }, 500)
      })
    } else if (savedPosition) {
      return savedPosition
    } else {
      return {x: 0, y: 0}
    }
  },
  routes
})

// 글로벌 신원 확인
router.beforeEach(async(to, from, next) => {
  Vue.prototype.$Loading.config({
    color: '#5030e5'
  })
  Vue.prototype.$Loading.start()
  // if(storage === undefined) {
  //   storage = await import('../../../store/index')
  // }
  let inactivetime = (await api.getInactiveTime()).data.data
  // limit inactive time(sec)
  const limitTime = 60 * 60 * 24

  if (inactivetime !== undefined && inactivetime !== null && inactivetime > limitTime && from.path !== '/login') {
    next({
      path: '/logout'
    })
  } else if (to.matched.some(record => record.meta.requiresAuth) && from.path.substring(0, 13) !== '/verify-email') {
    if (!storage.get(STORAGE_KEY.AUTHED)) {
      Vue.prototype.$error('로그인을 해주세요')
      // store.commit(types.CHANGE_MODAL_STATUS, {mode: 'login', visible: true})
      next({
        path: '/login'
      })
    } else if (to.matched.some(record => record.meta.isEmailVerify)) {
      if (!store.getters['isVerifiedEmail'] && !store.getters['isAdminRole'] && !(from.path === '/logout')) {
        store.commit(types.CHANGE_MODAL_STATUS, {mode: 'GuardMessage', visible: true})
        next(false)
      } else {
        next()
      }
    } else {
      next()
    }
  } else {
    next()
  }
  // else {
  //   next()
  // }
})

router.afterEach((to, from, next) => {
  Vue.prototype.$Loading.finish()
})
sync(store, router)
export default router
