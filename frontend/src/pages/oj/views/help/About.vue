<template>
  <div>
    <panel :padding="15" class="container">
      <div slot="title">오시는 길</div>
      <div class="content markdown-body">
        <ul>
          <li v-for="lang in languages">{{lang.name}} ( {{lang.description}} )
            <p>컴파일 : <b>{{lang.config.compile.compile_command.substring(9)}}</b></p>
          </li>
        </ul>
      </div>
    </panel>
  </div>
</template>

<script>
  import utils from '@/utils/utils'

  export default {
    data () {
      return {
        languages: []
      }
    }
  }
</script>

<style scoped lang="less">
@import '../../../../styles/common.less';
  .container {
    margin-bottom: 20px;
    
    .content {
      font-size: 16px;
      margin: 0 50px 20px 50px;
      > ul {
        list-style: disc;
        li {
          line-height: 2;
          .title {
            font-weight: 500;
          }
        }
      }
    }

    span {
      color: @purple;
    }
  }
</style>
