<template>
  <div>
    <div class="text-box">
      <p>앗.. 이메일 인증이 되어있지 않으시네요..</p>
      <p>해당 페이지는 이메일 인증을 해야 이용하실 수 있습니다.</p>
    </div>
    <div class="l_footer">
      <Button
        type="error"
        @click="closeVisible"
        class="btn cancel-btn">
        닫기
      </Button>
      <Button
        type="primary"
        @click="goAccountSeeting"
        class="btn">
        인증하러가기
      </Button>
    </div>
  </div>
</template>

<script>
  import { mapGetters, mapActions } from 'vuex'
  import { FormMixin } from '@oj/components/mixins'

  export default {
    mixins: [FormMixin],
    name: 'guardmessage',
    data () {
      return {}
    },
    methods: {
      ...mapActions(['changeModalStatus', 'getProfile']),
      goAccountSeeting () {
        this.changeModalStatus({visible: false})
        this.$router.push({name: 'account-setting'}).catch(() => {})
      },
      closeVisible () {
        this.changeModalStatus({visible: false})
      }
    },
    computed: {
      ...mapGetters(['website', 'modalStatus']),
      visible: {
        get () {
          return this.modalStatus.visible
        },
        set (value) {
          this.changeModalStatus({visible: value})
        }
      }
    }
  }
</script>

<style scoped lang="less">
@import '../../../../styles/common.less';
  .text-box {
    font-size: 14px;
    margin: 20px 10px;
  }
  .l_footer {
    overflow: auto;
    display: flex;
    display: -webkit-box;
    display: -ms-flexbox;
    display: -webkit-flex;
    flex-direction: row;
    -webkit-box-orient: horizontal;
    -webkit-box-direction: normal;
    -ms-flex-direction: row;
    flex-direction: row;
    justify-content: space-around;
    -webkit-justify-content: space-around;
    margin-top: 40px;
    margin-bottom: -15px;
    text-align: left;
    .btn {
      width: 45%;
      margin: 0 0 15px 0;
    }
    .cancel-btn {
      &.ivu-btn:hover {
        color: @white;
        background-color: #d53912;
        border-color: #d53912;
      }
    }
  }
</style>
