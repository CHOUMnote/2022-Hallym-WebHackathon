<template>
  <div>
    <div class="l_footer">
        <div class="textbox">
        <p>You have left this browser idle for 10 minutes.</p>
        <p>{{ time }} second left</p>
        </div>
    </div>
  </div>
</template>

<script>
export default {
  data () {
    return {
      time: 15
    }
  },
  created () {
    let timerId = setInterval(() => {
      this.time -= 1
      if (!this.$store.state.idleVue.isIdle) clearInterval(timerId)
      if (this.time < 1) {
        clearInterval(timerId)
        // Your logout function should be over here
        // this.$router.push({name: 'logout'})
        console.log('logout user....')
      }
    }, 1000)
  }
}
</script>

<style scoped lang="less">
  .textbox {
    font-size: 20px;
    font-weight: 700;
    text-align: center;
    margin: 0 auto;
  }
  .l_footer {
    position: fixed;
    display: flex;
    align-items: center;
    top: 0px;
    left: 0px;
    z-index: 10000;
    width: 100vw;
    height: 100vh;
    overflow: auto;
    background-color: rgba(167, 167, 167, 0.527);
    .btn {
      margin: 0 0 15px 0;
      &:last-child {
        margin: 0;
      }
    }
  }
</style>
