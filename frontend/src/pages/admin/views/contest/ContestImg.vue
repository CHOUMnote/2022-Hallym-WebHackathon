<template>
  <div class="view">
    <Panel :title="title">
      <el-form label-position="top">
        <el-row :gutter="20">
          <el-col :span="24">
            <el-form-item label="메인 타이틀 이미지">
              <div class="mypage_img" >
            
                <template class="container_img" v-if="!imgOption.imgSrc">
                  <Upload type="drag"
                          class="container_img"
                          accept=".jpg,.jpeg,.png,.bmp,.gif"
                          action=""
                          :before-upload="handleSelectFile">
                    <div style="padding: 30px 0">
                      <Icon type="ios-cloud-upload" size="52" style="color: #3399ff"></Icon>
                      <p>마우스로 파일을 끌어오거나 클릭하세요</p>
                    </div>
                  </Upload>
                </template>

                <template v-else>
                  <div class="flex-container">
                    <div class="cropper-main inline">
                      <vueCropper
                        ref="cropper"
                        autoCrop
                        fixed
                        :autoCropWidth="200"
                        :autoCropHeight="200"
                        :img="imgOption.imgSrc"
                        :outputSize="imgOption.size"
                        :outputType="imgOption.outputType"
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
                      <div :style=" preview.div">
                        <img :src="imgOption.imgSrc" :style="preview.img">
                      </div>
                    </div> -->
                  </div>
                </template>
                <Modal v-model="reselectModalVisible" class-name="vertical-center-modal" width="400" :footer-hide="footerhide" :closable="false" >
                    <div class="icon-header-box">
                      <i class="mdi mdi-alert-circle-outline warning-icon" aria-hidden="true"></i>
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
                    <p>대회 메인 사진이 다음과 같이 보여지게 됩니다</p>
                    <img class="modal-img" :src="uploadImgSrc"/>
                  </div>
                  <div class="modal-footer">
                    <Button @click="finishCropModalClose">취소</Button>
                    <Button @click="uploadAvatar" :loading="loadingUploadBtn">업로드</Button>
                  </div>
                </Modal>

              </div>
            </el-form-item>
          </el-col>
        </el-row>
      </el-form>
    </Panel>
  </div>
</template>

<script>
  import api from '../../api.js'
  import {VueCropper} from 'vue-cropper'
  import GuardMessage from '@oj/views/user/GuardMessage.vue'

  export default {
    components: {
      VueCropper,
      GuardMessage
    },
    data () {
      return {
        title: 'Upload Contest Image',
        contestId: '',
        uploadModalVisible: false,
        loadingUploadBtn: false,
        uploadImgSrc: '',
        reselectModalVisible: false,
        preview: {},
        imgOption: {
          imgSrc: '',
          size: 0.8,
          outputType: 'png'
        }
      }
    },
    methods: {
      // imgs
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
        let isOk = this.checkFileType(file) && this.checkFileSize(file)
        if (!isOk) {
          return false
        }
        let reader = new window.FileReader()
        reader.onload = (e) => {
          this.imgOption.imgSrc = e.target.result
        }
        reader.readAsDataURL(file)
        return false
      },
      realTime (data) {
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
        this.imgOption.imgSrc = ''
      },
      reselect () {
        this.$Modal.confirm({
          content: '변경사항을 취소하시겠습니까?',
          style: 'margin: 0 auto;',
          onOk: () => {
            this.imgOption.imgSrc = ''
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
          let file = new window.File([blob], 'avatar.' + this.imgOption.outputType)
          form.append('contest_id', this.contestID)
          form.append('image', file)
          this.loadingUploadBtn = true
          this.$http({
            method: 'post',
            url: 'admin/upload_contest_img',
            data: form,
            headers: {'content-type': 'multipart/form-data'}
          }).then(res => {
            this.loadingUploadBtn = false
            this.$success('새 프로필 업로드에 성공하였습니다')
            this.uploadModalVisible = false
            this.imgOption.imgSrc = ''
            this.$store.dispatch('getProfile')
          }, () => {
            this.$success('새 프로필 업로드에 실패하였습니다')
            this.loadingUploadBtn = false
          })
        })
      }
    },
    computed: {
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
    },
    mounted () {
      this.contestID = this.$route.params.contestId
    }
  }
</script>
<style lang="less" scoped>
@import '../../../../styles/common.less';
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
    margin: 1% 2% 2% 3%;
  }

  .section-title{
    font-size: 28px;
    // background-color: magenta;
  }

  .mypage_main{
    margin-top: 2%;
    // background-color: aqua;

  }

  .mypage_img{
    // display: inline-block;
    // vertical-align: top;
    margin: 1% 0 0 5%;
    width: 300px;

  }

  .container_img{
    width: 300px;
    height: auto;
  }

  .mypage_info{
    margin: 5% 0 5% 5%;
    // padding-left: 200px;
    // display: inline-block;
    // vertical-align: top;
    width: 400px;
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
</style>
