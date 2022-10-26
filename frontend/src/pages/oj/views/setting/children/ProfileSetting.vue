<template>
  <div class="mypage">
    <div class="section-title-profile">{{$t('m.Profile_Setting')}}</div>  
      <!-- <Form ref="formProfile" :model="formProfile">         -->
        <div class="subtitle">프로필 사진</div>
        <div class="mypage_main">
          <div class="mypage_img" >
            <template class="container_img" v-if="!avatarOption.imgSrc">
              <div class="avatar"><img :src="profile.avatar"/></div>
              <Upload type="drag"
                      class="container_img"
                      accept=".jpg,.jpeg,.png,.bmp,.gif"
                      action=""
                      :before-upload="handleSelectFile">
                  <p>프로필 사진 변경</p>
              </Upload>
            </template>
        
            <template v-else>
              <div class="flex-container">
                <div class="cropper-main inline">
                  <vueCropper
                    ref="cropper"
                    autoCrop
                    :fixed="true"
                    :fixedBox="false"
                    :canMove="false"
                    :canScale="false"
                    :autoCropWidth="150"
                    :autoCropHeight="150"
                    :img="avatarOption.imgSrc"
                    :outputSize="avatarOption.size"
                    :outputType="avatarOption.outputType"
                    :info="true"
                    @realTime="realTime">
                  </vueCropper>
                </div>
                <ButtonGroup vertical class="cropper-btn">
                  <Button @click="rotate('left')">
                    <Icon type="md-return-right" size="20"></Icon>
                  </Button>
                  <Button @click="rotate('right')">
                    <Icon type="md-return-left" size="20"></Icon>
                  </Button>
                  <Button @click="openReselectModalVisible">
                    <Icon type="md-refresh" size="20"></Icon>
                  </Button>
                  <Button @click="finishCrop">
                    <Icon type="md-checkmark-circle-outline" size="20"></Icon>
                  </Button>
                </ButtonGroup>
                <!-- <div class="cropper-preview" :style="previewStyle">
                  <div :style="preview.div">
                    <img :src="avatarOption.imgSrc" :style="preview.img">
                  </div>
                </div> -->
              </div>
            </template>
            <Modal v-model="reselectModalVisible" class-name="vertical-center-modal" width="400" :footer-hide="footerhide" :closable="false" >
                <div class="icon-header-box">
                  <i class="mdi mdi-alert-circle-outline warning-icon" :aria-hidden="true"></i>
                </div>
                <div class="modal-text">
                  <p>변경사항을 취소하시겠습니까?</p>
                </div>
                
                <div class="modal-footer">
                  <Button @click="closeReselectModalVisible">아니요</Button>
                  <Button @click="reselectOnOk">예</Button>
                </div>
            </Modal>
            <Modal v-model="uploadModalVisible"
                  class-name="vertical-center-modal" :footer-hide="footerhide" :closable="false" title="프로필 업로드">
              <div class="modal-text">
                <p>프로필 사진이 다음과 같이 보여지게 됩니다</p>
                <img class="modal-img" :src="uploadImgSrc"/>
              </div>
              <div class="modal-footer">
                <Button @click="finishCropModalClose">취소</Button>
                <Button @click="uploadAvatar" :loading="loadingUploadBtn">업로드</Button>
              </div>
            </Modal>
            <!-- 레거시 Modal -->
            <!-- <Modal v-model="uploadModalVisible"
                  title="프로필 업로드">
              <div class="upload-modal">
                <p class="notice">프로필 사진이 다음과 같이 보여지게 됩니다</p>
                <img :src="uploadImgSrc"/>
              </div>
              <div slot="footer">
                <Button @click="uploadAvatar" :loading="loadingUploadBtn">업로드</Button>
              </div>
            </Modal> -->

          </div>
          <div class="subtitle">기본정보</div>
          <Form ref="formProfile" :model="formProfile">
          <div class="mypage_info">
            <div class="mypage_info_input" label="이름"> 
              <div>이름</div>
              <div class="data">{{profile.real_name}}</div>
            </div>
            <div class="mypage_info_input" label="학교">
              <div>학교</div>
              <div class="data">{{profile.school}}</div>
            </div>
            <div class="mypage_info_input" label="전공">
              <div>전공</div>
              <div class="data">{{profile.major}}</div>
            </div>
            <div class="mypage_info_input" label="회원분류">
              <div>회원 등급</div>
              <div class="data">{{user.admin_type}}</div>
              <!-- <Input v-model="formProfile.classification"/> -->
            </div>
            <div class="mypage_info_input" label="이메일">
              <div>이메일</div>
              <div class="data">{{user.email}}</div>
              <!-- <Input v-model="formProfile.email"/> -->
            </div>
            <div class="mypage_info_input" label="Github">
              <div class="div-inline">
                <div class="text">GitHub</div>
                <div>
                  <Button class="edit-btn" @click="changeGithubEditMode"><Icon color="#5030e5" size=15 type="md-create" /></Button>
                </div>
              </div>
              <div class="data">{{profile.github}}</div>
              <!-- <transition name="slide-fade" mode="out-in">
                <div class="edit-input" v-show="githubEditMode">
                  <Input v-model="viewgithub">
                    <span slot="prepend">https://github.com/</span>
                  </Input>
                  <div style="float:right"><Button @click="updateGithub">확인</Button></div>
                  <div style="clear: both;"></div>
                </div>
              </transition> -->
            </div>
            <div>
              <transition name="slide-fade" mode="out-in">
                <div class="edit-input" v-show="githubEditMode">
                  <Input v-model="viewgithub">
                    <span slot="prepend">https://github.com/</span>
                  </Input>
                  <div style="margin-left:5px;"><Button @click="updateGithub">확인</Button></div>
                </div>
              </transition>
            </div>
            <div class="mypage_info_input" label="Github">
              <div class="div-inline">
                <div class="text">블로그</div>
                <div>
                  <Button class="edit-btn" @click="changeBlogEditMode"><Icon color="#5030e5" size=15 type="md-create" /></Button>
                </div>
              </div>
              <div class="data">{{profile.blog}}</div>
            </div>
            <transition name="slide-fade" mode="out-in">
                <div class="edit-input" v-show="blogEditMode">
                  <Input v-model="viewblog">
                    <span slot="prepend">https://</span>
                  </Input>
                  <div style="margin-left:5px;"><Button @click="updateBlog">확인</Button></div>
                </div>
              </transition>
          </div>
          </Form>
        </div>
  </div>
</template>

<script>
  import { mapGetters, mapActions } from 'vuex'
  import api from '@oj/api'
  import utils from '@/utils/utils'
  import {VueCropper} from 'vue-cropper'
  import {types} from '@/store'
  import {languages} from '@/i18n'
  import Button from 'iview/src/components/button/button.vue'
  import GuardMessage from '@oj/views/user/GuardMessage.vue'
  export default {
    components: {
      VueCropper,
      GuardMessage,
      Button
    },
    data () {
      return {
        githubEditMode: false,
        blogEditMode: false,
        loadingSaveBtn: false,
        loadingUploadBtn: false,
        uploadModalVisible: false,
        reselectModalVisible: false,
        preview: {},
        uploadImgSrc: '',
        avatarOption: {
          imgSrc: '',
          size: 0.8,
          outputType: 'png'
        },
        languages: languages,
        formProfile: {
          real_name: '',
          mood: '',
          major: '',
          classification: '',
          email: '',
          blog: '',
          school: '',
          github: '',
          language: ''
        },
        viewgithub: '',
        viewblog: ''
      }
    },
    mounted () {
      this.init()
    },
    methods: {
      ...mapActions(['getProfile', 'changeModalStatus']),
      init () {
        let profile = this.$store.state.user.profile
        new Promise((resolve, reject) => {
          Object.keys(this.formProfile).forEach(element => {
            if (profile[element] !== undefined) {
              this.formProfile[element] = profile[element]
            }
          })
          resolve()
        }).then(res => {
          this.viewgithub = this.formProfile.github
          if (this.viewgithub != null) {
            this.viewgithub = this.viewgithub.replace('https://github.com/', '')
          } else {
            this.viewgithub = ''
          }
          this.viewblog = this.formProfile.blog
          if (this.viewblog != null) {
            this.viewblog = this.viewblog.replace('https://', '')
          }
        })
      },
      checkFileType (file) {
        if (!/\.(gif|jpg|jpeg|png|bmp|GIF|JPG|PNG)$/.test(file.name)) {
          this.$Notice.warning({
            title: 'File type not support',
            desc: 'The format of ' + file.name + ' is incorrect ，please choose image only.'
          })
          return false
        }
        return true
      },
      checkFileSize (file) {
        // max size is 2MB
        if (file.size > 2 * 1024 * 1024) {
          this.$Notice.warning({
            title: 'Exceed max size limit',
            desc: 'File ' + file.name + ' is too big, you can upload a image up to 2MB in size'
          })
          return false
        }
        return true
      },
      handleSelectFile (file) {
        if (!this.isVerifiedEmail) {
          this.modalVisible = true
          return false
        }
        let isOk = this.checkFileType(file) && this.checkFileSize(file)
        if (!isOk) {
          return false
        }
        let reader = new window.FileReader()
        reader.onload = (e) => {
          this.avatarOption.imgSrc = e.target.result
        }
        reader.readAsDataURL(file)
        return false
      },
      realTime (data) {
        console.log(data)
        this.preview = data
      },
      rotate (direction) {
        if (direction === 'left') {
          this.$refs.cropper.rotateLeft()
        } else {
          this.$refs.cropper.rotateRight()
        }
      },
      openReselectModalVisible () {
        this.reselectModalVisible = true
      },
      closeReselectModalVisible () {
        this.reselectModalVisible = false
      },
      reselectOnOk () {
        this.avatarOption.imgSrc = ''
        this.reselectModalVisible = false
      },
      reselect () {
        this.$Modal.confirm({
          content: '변경사항을 취소하시겠습니까?',
          style: 'margin: 0 auto;',
          onOk: () => {
            this.avatarOption.imgSrc = ''
          }
        })
      },
      finishCrop () {
        this.$refs.cropper.getCropData(data => {
          this.uploadImgSrc = data
          this.uploadModalVisible = true
        })
      },
      finishCropModalClose () {
        this.uploadModalVisible = false
      },
      uploadAvatar () {
        this.$refs.cropper.getCropBlob(blob => {
          let form = new window.FormData()
          let file = new window.File([blob], 'avatar.' + this.avatarOption.outputType)
          form.append('image', file)
          this.loadingUploadBtn = true
          this.$http({
            method: 'post',
            url: 'upload_avatar',
            data: form,
            headers: {'content-type': 'multipart/form-data'}
          }).then(res => {
            this.loadingUploadBtn = false
            this.$success('새 프로필 업로드에 성공하였습니다')
            this.uploadModalVisible = false
            this.avatarOption.imgSrc = ''
            this.$store.dispatch('getProfile')
          }, () => {
            this.$success('새 프로필 업로드에 실패하였습니다')
            this.loadingUploadBtn = false
          })
        })
      },
      updateGithub () {
        if (this.viewgithub === '' || this.viewgithub === ' ' || this.viewgithub === null || this.viewgithub === undefined) {
          this.formProfile.github = ' '
        } else {
          this.formProfile.github = 'https://github.com/' + this.viewgithub
        }
        this.updateProfile()
      },
      updateBlog () {
        if (this.viewblog === '' || this.viewblog === ' ' || this.viewblog === null || this.viewblog === undefined) {
          this.formProfile.blog = ' '
        } else {
          this.formProfile.blog = 'https://' + this.viewblog
        }
        this.updateProfile()
      },
      updateProfile () {
        this.loadingSaveBtn = true
        let updateData = utils.filterEmptyValue(Object.assign({}, this.formProfile))
        api.updateProfile(updateData).then(_ => {
          this.$success('Success')
          api.getUserInfo(this.$store.state.user.username).then(res => {
            setTimeout(() => {
              this.$store.commit(types.CHANGE_PROFILE, {profile: res.data.data})
            }, 100)
            this.loadingSaveBtn = false
            this.githubEditMode = false
            this.blogEditMode = false
          })
        }, _ => {
          this.loadingSaveBtn = false
        })
      },
      changeGithubEditMode () {
        this.githubEditMode = !this.githubEditMode
      },
      changeBlogEditMode () {
        this.blogEditMode = !this.blogEditMode
      }
    },
    computed: {
      ...mapGetters(['website', 'modalStatus', 'user', 'isVerifiedEmail', 'profile']),
      footerhide () {
        return true
      },
      previewStyle () {
        return {
          'width': this.preview.w + 'px',
          'height': this.preview.h + 'px',
          'overflow': 'hidden'
        }
      },
      modalVisible: {
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

<style lang="less" scoped>
  @import '../../../../../styles/common.less';
  .inline {
    display: inline-block;
  }

  .copper-img {
    width: 400px;
    height: 300px;
  }

  .flex-container {
    flex-wrap: wrap;
    justify-content: flex-start;
    margin-bottom: 10px;
    .cropper-main {
      flex: none;
      .copper-img;
      margin: 0 auto;
      padding: 0;
    }
    .cropper-btn {
      flex: none;
      vertical-align: top;
    }
    .cropper-preview {
      flex: none;
      /*margin: 10px;*/
      margin-left: 20px;
      box-shadow: 0 0 1px 0;
      .copper-img;
    }
  }

  .upload-modal {
    .notice {
      font-size: 16px;
      display: inline-block;
      vertical-align: top;
      padding: 10px;
      padding-right: 15px;
    }
    img {
      box-shadow: 0 0 1px 0;
      border-radius: 50%;
    }
  }



  .mypage{
    margin: 20px;
  }

  .section-title-profile{
    font-size: 25px;
    color: @purple;
    -webkit-text-stroke: 1px;
    // background-color: magenta;
  }

  .mypage_main{
    margin-top: 2%;
    // background-color: aqua;

  }

  .container_img{
    width: 150px;
    margin: auto;
    margin-top: 10px;
    font-size: 120%;
    -webkit-text-stroke: .2px;
    &:hover {
      color: @purple;
      transition: color .2s ease;
    }
  }

  .mypage_info{
  }

  .mypage_info_submit{
    display: flex;
    justify-content: right;

  }


// modal창 design
  .icon-header-box {
    display: inline-block;
    text-align: center;
    width: 100%;
    .warning-icon {
      font-size: 120px;
      color: @purple;
      opacity: 0.65;
    }
  }
  .modal-footer {
    margin-top: 50px;
    display: flex;
    .ivu-btn {
      width: 50%;
      height: 50px;
      font-size: @font-micro;
      &:first-child {
        border-radius: 0 0 0px 6px;
        color: @default-font-color;
        -webkit-transition: all .2s ease-in;
        -moz-transition: all .2s ease-in;
        -ms-transition: all .2s ease-in;
        -o-transition: all .2s ease-in;
        transition: all .2s ease-in;
        &:hover {
          border-color: @dark-orange;
          background-color: @dark-orange;
          color: @white;
        }
      }
      &:last-child {
        border-radius: 0 0 6px 0px;
        color: white;
        border-color: @purple;
        background-color: @purple;
        opacity: 0.65;
        -webkit-transition: all .2s ease-in;
        -moz-transition: all .2s ease-in;
        -ms-transition: all .2s ease-in;
        -o-transition: all .2s ease-in;
        transition: all .2s ease-in;
        &:hover {
          opacity: 1;
        }
      }
    }
  }
  .modal-text {
    text-align: center;
    font-size: @font-regular;
    font-weight: bold;
  }
  .modal-img {
    margin-top: 20px;
    box-shadow: 0 0 1px 0;
    border-radius: 50%;
  }
  .mypage_info_input {
    width: 100%;
    display: flex;
    position: relative;
    .data {
      width: 100%;
      border-bottom: 1px solid @dark-white;
      line-height: 60px;
      font-size: 110%;
      padding: 0 10px 10px 10px;
    }
    & div:first-child, .text {
      height: 44px;
      min-width: 80px;
      line-height: 60px;
      font-size: 110%;
      font-weight: 300;
      -webkit-text-stroke: .5px;
      color: @purple;
    }
    & div:nth-child(2) {
      font-weight: @weight-semi-bold;
      height: 44px;
    }
    .div-inline {
      display: flex;
    }
    .edit-btn {
      width:fit-content;
      padding: 0;
      padding-top: 15px;
      position: absolute;
      right: 10px;
      background-color: transparent;
      border: none;
      &:focus {
        border: none;
        box-shadow: none;
      }
    }
  }
  .edit-input {
    margin-left: 80px;
    margin-top: 20px;
    display: flex;
  }


  // transition mode 
    .fade-enter {
    opacity: 0;
  }
  
  .fade-enter-active,
  .fade-leave-active {
    transition: opacity 0.5s ease-out;
  }
  
  .fade-leave-to {
    opacity: 0;
  }
  
  .slide-fade-enter {
    transform: translateY(-10px);
    opacity: 0;
  }
  
  .slide-fade-enter-active,
  .slide-fade-leave-active {
    transition: all 0.5s ease;
  }
  
  .slide-fade-leave-to {
    transform: translateY(-10px);
    opacity: 0;
  }

  .subtitle {
    color: @purple;
    font-size: 120%;
    -webkit-text-stroke: .5px;
    padding: 5px 0;
    border-bottom: 1.5px solid @purple;
  }

  .avatar {
    display: flex;
    justify-content: center;
    img {
      height: 150px;
      width: 150px;
      border-radius: 50%;
    }
  }

</style>
<style lang="less">
      .vertical-center-modal {
        .ivu-modal-content {
          .ivu-modal-body {
            padding-bottom: 0px;
            padding-left: 0px;
            padding-right: 0px;
          }
        }
    }
    .cropper-box-canvas {
      align-items: center;
      display: flex;
      justify-content: center;
    }
    .cropper-view-box {
      img {
        visibility: hidden;
      }
    }
</style>
