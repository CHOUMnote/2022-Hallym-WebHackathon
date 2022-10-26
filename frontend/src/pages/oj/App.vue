<template>
  <div class="content_container" style="overflow-x: hidden;">
    <div class="blockingdrag">
      <NavBar v-show="$route.name !== 'start-login' && $route.name !== 'contest-problem-submission' && $route.name !== 'problem-submission' && $route.name !== 'join'"></NavBar>
    </div>
    <div class="content-app">
      <!-- disabled SessionExpire -->
      <!-- <SessionExpire v-if="isIdle && $route.name !== 'start-login'  && $route.name !== 'join'"/> -->
      <transition name="fadeInUp" mode="out-in">
        <router-view></router-view>
      </transition>
      <!-- <div class="footer">
        <p v-html="website.website_footer"></p>
        <p>Powered by <a href="https://github.com/OnlineJudgePlatformDev">OnlineJudge</a>
          <span v-if="version">&nbsp; Version: {{ version }}</span>
        </p>
      </div> -->
    </div>
    <BackTop></BackTop>
    <Footer v-show="$route.name !== 'contest-problem-submission' && $route.name !== 'problem-submission'"></Footer>
  </div>
  <!-- <div class="footer" c>
    <p v-html="website.website_footer"></p>
    <p>Poweredaaa by <a href="https://github.com/OnlineJudgePlatformDev">COU</a>
      <span v-if="version">&nbsp; Version: {{ version }}</span>
    </p>
  </div> -->
</template>

<script>
  import { mapActions, mapState } from 'vuex'
  import NavBar from '@oj/components/NavBar.vue'
  import SessionExpire from '@oj/components/SessionExpire.vue'
  import Footer from '@oj/components/Footer'

  export default {
    name: 'app',
    components: {
      NavBar,
      SessionExpire,
      Footer
    },
    data () {
      return {
        version: process.env.VERSION
      }
    },
    created () {
      try {
        document.body.removeChild(document.getElementById('app-loader'))
      } catch (e) {
      }
    },
    mounted () {
      this.getWebsiteConfig()
    },
    methods: {
      ...mapActions(['getWebsiteConfig', 'changeDomTitle'])
    },
    computed: {
      ...mapState(['website']),
      isIdle () {
        return this.$store.state.idleVue.isIdle
      }
    },
    watch: {
      'website' () {
        this.changeDomTitle()
      },
      '$route' () {
        this.changeDomTitle()
      }
    }
  }
</script>

<style lang="less">

  * {
    -webkit-box-sizing: border-box;
    -moz-box-sizing: border-box;
    box-sizing: border-box;
  }

  a {
    text-decoration: none;
    background-color: transparent;
    &:active, &:hover {
      outline-width: 0;
    }
  }

  .content_container {
    // screen height - navigation bar height - footer height - contanier bottom margin
    // min-height: calc(~"100vh - 80px - 80px - 20px");
    min-height: 100%;
    position: relative;
    overflow-x: hidden;
  }

  .content-app {
    margin-top: 100px;
    padding-bottom: 280px;
  }
  @media screen and (max-width: 1200px) {
    .content-app {
      margin-top: 80px;
      min-height: 100vh;
      position: relative;
    }
  }

  @media screen and (min-width: 1200px) {
    .content-app {
      margin-top: 80px;
      min-height: 100vh;
      position: relative;
    }
  }
  .blockingdrag {
    -webkit-user-select:none;
    -moz-user-select:none;
    -ms-user-select:none;
    user-select:none
  }



  .footer {
    background-color: rgb(41, 41, 41);
    position: relative;
    left: 0px;
    bottom: 0;
    width: 100%;
    height: 80px;
    text-align: center;
    font-size: small;
  }

  .fadeInUp-enter-active {
    animation: fadeInUp .8s;
  }

  @media screen and (max-width: 900px) {
    .content_container {
      max-width: 100vw;
      overflow-x: hidden;
      margin-right: 0 !important;
    }
    .content-app {
      max-width: 100vw;
      overflow-x: hidden
    }
  }


</style>
