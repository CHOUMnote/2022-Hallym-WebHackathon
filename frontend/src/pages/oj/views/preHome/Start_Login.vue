<template>
  <div class="start_login">

      <div class="form">
        <Form ref="formLogin" :model="formLogin" :rules="ruleLogin">
          <!-- 로그인 박스 title-->
          <div class="login_title"><p @click="goRoute('/')">COU</p></div>
                  
          <div class = "login_edge">
          <!-- 로그인 username textbox -->
            <FormItem prop="username">
              <p class="form_title">아이디</p>
              <Input class ="login_input" type="text" v-model="formLogin.username" placeholder="아이디를 입력해주세요" size="large" @on-enter="handleLogin">
              </Input>
            </FormItem>
            <!-- 로그인 password textbox -->
            <!-- <input type="password" v-model="formLogin.password" @on-enter="handleLogin" placeholder="비밀번호를 입력하세요"/> -->
            <FormItem prop="password">
              <p class="form_title">비밀번호</p>
              <Input class ="login_input" type="password" v-model="formLogin.password" placeholder="비밀번호를 입력해주세요" size="large" @on-enter="handleLogin">
                <!-- <Icon type="ios-lock-outline" slot="prepend"></Icon> -->
              </Input>
              <div class = "login_foot">
              <a class="foot_password" @click.stop="goResetPassword" style="float: right">{{$t('m.Forget_Password')}}</a>     
            </div>
            </FormItem>
            <!-- 로그인 상태 체크박스 -->
            
            <FormItem>
              <div class="login_btn">
                <Button 
                  type="primary"
                  @click="handleLogin"
                  class="primary btn" long
                  :loading="btnLoginLoading">
                  {{$t('m.UserLogin')}}
                </Button>
              </div>
              <div class="register_btn">
                <Button @click="$router.push('/join').catch(() => {})" class="second btn" long
                  :loading="btnLoginLoading">{{$t('m.No_Account')}} </Button>
              </div>
            </FormItem>
          </div>
        </Form>
      </div>
  </div>
  
</template>

<script>
import { mapGetters, mapActions } from 'vuex'
import api from '@oj/api'
import { FormMixin } from '@oj/components/mixins'
import register from '@oj/views/user/Register'
export default {
  mixins: [FormMixin],
  components: {
    register
  },
  data () {
    // LoginStaus :false;  //로그인 상태 초기값 : false
    const CheckRequiredTFA = (rule, value, callback) => {
      if (value !== '') {
        api.tfaRequiredCheck(value).then(res => {
          this.tfaRequired = res.data.data.result
        })
      }
      callback()
    }

    return {
      lastURL: '',
      tfaRequired: false,
      btnLoginLoading: false,
      formLogin: {
        username: '',
        password: '',
        // 로그인 상태  prop 값
        login_status: false,
        tfa_code: ''
      },
      ruleLogin: {
        username: [
          {required: true, trigger: 'blur', message: '아이디를 입력해주세요'},
          {validator: CheckRequiredTFA, trigger: 'blur'}
        ],
        password: [
          {required: true, trigger: 'change', message: '6~20자 사이로 입력해주세요', min: 6, max: 20}
        ]
      }
    }
  },
  methods: {
    ...mapActions(['changeModalStatus', 'getProfile']),
    handleBtnClick (mode) {
      this.changeModalStatus({
        visible: true,
        mode: mode
      })
    },
    changeInputText (event) {
      this.formLogin.username = event
    },
    changeInputTextP (event) {
      this.formLogin.password = event
    },

    handleLogin () {
      this.validateForm('formLogin').then(valid => {
        this.btnLoginLoading = true
        let formData = Object.assign({}, this.formLogin)
        if (!this.tfaRequired) {
          delete formData['tfa_code']
        }
        api.login(formData).then(res => {       // login : api.js파일의 login 함수를 사용하게 함
          this.btnLoginLoading = false
          this.changeModalStatus({visible: false})
          this.getProfile()
          this.$success(this.$i18n.t('m.Welcome_back'))
          setTimeout(() => {
            this.afterlogin(this.lastURL)
          }, 500)
        }, _ => {
          this.btnLoginLoading = false
        })
      })
    },
    afterlogin (route) {
      if (route) {
        if (route.path === '/logout' || route.path === '/join') {
          this.$router.push({path: '/'}).catch(() => {})
        } else {
          this.$router.push({path: route.path}).catch(() => {})
        }
      } else {
        this.$router.push({path: '/'}).catch(() => {})
      }
    },
    goRoute (route) {
      if (route) {
        this.$router.push({path: route}).catch(() => {})
      } else {
        this.$router.push({path: '/'}).catch(() => {})
      }
    },
    goResetPassword () {
      this.changeModalStatus({visible: false})
      this.$router.push({name: 'apply-reset-password'}).catch(() => {})
    },
    isAlreadyLoggedin () {
      if (this.$store.getters.isAuthenticated === true) {
        this.$router.push({
          name: 'home'
        }).catch(() => {})
      }
    }
  },
  beforeRouteEnter (to, from, next) {
    next(vm => {
      vm.lastURL = from
    })
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
  },
  mounted () {
    this.isAlreadyLoggedin()
  }
}
</script>

<style scoped lang="less">
@import '../../../../styles/common.less';

.start_login {
  display: flex;
  justify-content: center;
  align-items: center;
  height: calc(~"100vh - 80px");
  .form {
    min-width: 40vw;
    max-width: 600px;
  }
}
// .form {
//   position: absolute;
//   left: 50%;
//   top: 50%;
//   background-color: rgb(243, 243, 243);
//   border: solid 1px rgb(170, 170, 170);
//   width: 602px;
//   height: 350px;
//   margin: 0 auto;
//   padding: 0px;
//   margin-left: -300px;
//   margin-top: -170px;


//   // position: relative;
//   // width: 30%;
//   // background-color: rgb(201, 201, 201);
//   // margin-top: 350px;
//   // // margin-right: 650px;
//   // padding: 40px;

// }

// .form {
//   overflow: auto;
//   // margin-top: 20px;
//   margin-bottom: -15px;
//   // text-align: left;
//   .btn {
//     margin: 0 0 10px 0;
//     &:last-child {
//       margin: 0;
//     }
//   }
// }

// .start_login{
  // margin: -80px -50px -154px -50px;
  // margin-bottom: -150px;
// }

@media screen and (max-width: 1200px) {
  .start_login {
    margin: -80px -50px -190px -50px;
    // margin-top: 160px;
    // height: calc(~"100vh - 80px");
    // min-height: 100%;
    position: relative;
    // padding-bottom: 80px;
  }
}

@media screen and (max-width: 900px) {
  .start_login {
    margin: -80px -50px -190px -50px;
    // margin-top: 160px;
    // min-height: 725px;
    // height: calc(~"100vh - 80px");
    // min-height: 100%;
    position: relative;
    // padding-bottom: 80px;
    min-width: 100vw;
    .form {
      min-width: 90vw;
      .login_edge {
        padding: 0px 44px 20px;
      }
    }
  }
}

@media screen and (min-width: 1200px) {
  .start_login {
    margin: -80px -50px -190px -50px;
    // padding-bottom: 96px;
    // margin-top: 80px;calc(28.125vw + 262.84px - 80px)
    // height: 100vh;
    // height: calc(~"100vh - 80px");
    // height: calc(~"28.125vw + 262.84px");
    // min-height: 100%;
    // position: relative;
    // padding-bottom: 90px;
  }
}

.nav {
  top: -80px;
  position: absolute;
}
.image{
  // position: fixed;
  display: block;
  left: -20px;
  top: 0px;
  width: 100%;
  // height : 56.25vw;
  // height: 56.25vw;
  height: 60vh;
  
  // height: 77.78vh;
  // height: 28.125vw;  // ultra-wide screen size (32:9)
  // height: 500px;
  background-color: rgb(39, 39, 39);
  color: white;
  font-size: 36px;
  font-weight: bold;
}
.form {
  display: inline-block;
  background-color: @white;
  box-shadow: 2px 5px 20px 2px rgba(90, 82, 128, 0.31);
  border-radius: @size-border-radius;
  width: 30%;
  max-width: 500px;
  overflow: auto;
  // position: fixed;
  // margin-top: 500px;
  // margin-bottom: -15px;
  // margin: 25px 0 50px 35%;
  // margin: 3vh 0 3vh 35%;
  // top: 500px;
  // left: 35%;
  // height: 33vh;
  // padding: 0 0 0 10px;
  // text-align: left;
  .btn {
    margin: 0 0 0 0;
    &:last-child {
      margin: 0;
    }
  }
}

// Form{
//   margin: 25px 0 10px 35%;
// }



//css 추가

// .logo_img {
//     width : 100%;
//     height : 450px;
//     position: relative;
//     background-color: linear-gradient(0deg, #8497B0, white)fixed;
//     text-align: left;
// }


// .logo_img > div{
//     padding-left: 20px;
//     padding-top: 10px;
//     font-size: 32px;
// }

/* 로그인 박스의 Coding Platform Dev title css */
.login_title{
  width: 100%;
  height: 13%;
  margin: 30px 0;
  background: @white;
  padding: 0px;
  text-align: center;
  font-size: @font-large;
  font-weight: @weight-bold;
  line-height: 50px;
  color: @purple;
  p {
    display:inline-block;
    cursor: pointer;
    margin: 0 auto;
    -webkit-text-stroke: 2px;
  }
}

/* 로그인 입력 박스 css */
.login_edge{
  // margin-top: 10px;
  padding: 0px 60px 30px;
  background-color: @white;
  .form_title {
    font-size: @font-micro;
    font-weight: bold;
    color: @purple;
  }
}


/* 로그인 입력 textbox css */
.login_input {
  // width: 390px;
  // height: 32px;
  // border: solid 1px black;
  // border-radius: 7px;
  // margin-top : 5px;
  // padding: 0px 10px;
  // padding: 0 10px 0 10px;
  // margin-bottom: -15px;
  text-justify: center;
  font-size: 18px;
}

/* 로그인 상태 유지 checkbox css */
.login_check{
  text-align: left;   
  // margin-top: 10px;
  // margin-left: 10px;
  // margin-bottom:-10px;
  // background-color: aqua;
  // font-size: 12px;
}

.register_btn{
  // background: aqua;
  margin-top: 20px;
}

.btn {
  // position: relative;
  // width: 580px;
  // height: 38px;
  border: none;
  border-radius: @size-border-radius;
  text-justify: center;
  padding: 12px 0;
  color: white;
  font-size: @font-small;
  font-weight: bold;
  &.primary {
    background: @purple;
  }
  &.second {
    background: @light-gray;
    color: @gray;
  }
}

/* 로그인 회원가입하기 & 아이디/비밀번호 찾기 */
.login_foot{
  .foot_password {
    color: @gray;
    font-weight: @weight-bold;
  }
  // margin: 5px 0 5px 0;
}

.footer {
    background-color: @black;
    position: relative;
    left: 0;
    bottom: 0;
    width: 100%;
    height: 10vh;
    text-align: center;
    font-size: small;
  }

</style>
