<template>
  <footer>
    <div>
      <p>춘천재래시장 웹사이트</p>
      <p>Powered by <a href="https://github.com/OnlineJudgePlatformDev">일석이조</a>
        <span v-if="version">&nbsp; Version: {{ version }}</span>
      </p>
    </div>
  </footer>
<!-- <footer>
  <p v-html="website.website_footer></p>
    Online Judge Footer<br />
    Powered by COU   Version: {{version}}
  </footer> -->
</template>
<script>
import { mapActions, mapState } from 'vuex'

export default {

  data () {
    return {
      version: process.env.VERSION
    }
  },
  mounted () {
    this.getWebsiteConfig()
  },
  methods: {
    ...mapActions(['getWebsiteConfig', 'changeDomTitle'])
  },
  computed: {
    ...mapState(['website'])
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
<style lang="less" scoped>
@import '../../../styles/common.less';
  footer {
    
    position: absolute;
    bottom: 0;
    left: 0;
    // background-color: @black;
    // color: @light-gray;
    opacity: 1;
    color: @gray;
    padding: 5px 0 0 0;
    font-size: @font-micro;
    width: 100vw;
    height: 100px;
    text-align: center;
    display: flex;
    align-items: center;
    & div {
      margin: 0 auto;
    }
  }
</style>