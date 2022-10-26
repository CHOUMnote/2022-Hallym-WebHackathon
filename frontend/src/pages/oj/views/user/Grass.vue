<template>
  <div>
    <div class="flex-container">
      <div class="flex-item">
      <svg class="grass-container">
        <template  v-for="(__, idx_x) in 52">
          <g>
            <rect v-for="(_, idx_y) in 7" class="grass-pointer" v-bind:style="{'x':getPositionX(idx_x) ,'y': getPositionY(idx_y)}"></rect>
          </g>
        </template>
      </svg>
      </div>
    </div>
    <div class="flex-level-container">
      <div class="flex-level-item">
        <div class="level-left"></div>
        <div class="level-right">
          <div class="text">Less</div>
          <div class="svg-level-box">
          <svg class="level-svg">
            <rect class="grass-pointer level1"></rect>
          </svg>
          <svg class="level-svg">
            <rect class="grass-pointer level2"></rect>
          </svg>
          <svg class="level-svg">
            <rect class="grass-pointer level3"></rect>
          </svg>
          <svg class="level-svg">
            <rect class="grass-pointer level4"></rect>
          </svg>
          <svg class="level-svg last">
            <rect class="grass-pointer level5"></rect>
          </svg>
          </div>
          <div class="text">
          More
          </div>
        </div>
      </div>
    </div>
  </div>
</template>
<script>
  import api from '@oj/api'
  export default {
    data () {
      return {
        grassList: []
      }
    },
    mounted () {
      this.getGrassList()
    },
    methods: {

      getGrassList () {
        api.getGrassList().then(res => {
          this.grassList = res.data.data.grass
        })
      },
      getPositionX (x) {
        return 13 * x
      },
      getPositionY (y) {
        return 13 * y
      }
    }
  }
</script>
<style lang="less" scoped>
@import '../../../../styles/common.less';
.flex-container {
  width:100%;
  text-align: center;
  font-weight: 400;
  font-size: 16px;
  margin-top: 30px;
  .flex-item {
    width:75%;
    overflow-x: auto;
  }
  .grass-container {
    width: 677px;
    height: 100px;
    margin: 0 auto;
  }
}
.grass-pointer {
  fill:@orange;
  rx: 2px;
  ry: 2px;
  height:10px; 
  width:10px;
  &.level1 {
    fill: @light-gray;
  }
  &.level2 {
    fill: @light-orange;
  }
  &.level3 {
    fill: @orange;
  }
  &.level4 {
    fill: @dark-orange;
  }
  &.level5 {
    fill: @deep-dark-orange;
  }
}
.flex-level-container {
  width:100%;
  text-align: center;
  font-weight: 400;
  font-size: 12px;
  margin-top: 10px;
  display: flex;
  flex-direction: row;
  justify-content: center;
  align-items: center;
  .flex-level-item {
    max-width: 677px;
    width:75%;
    height: 18px;
    .level-left {
      float: left;
      height: 18px;
    }
    .level-right {
      float: right;
      line-height: 18px;
      height: 18px;
      display: block;
      font-size: 12px;
      margin: auto;
      text-align: center;
      .text {
        display: block;
        float: left;
      }
      .svg-level-box {
        display: block;
        float: left;
        margin: auto 5px;
      }
      svg {
        rect {
          transform: translateY(50%);
          y: -5px;
        }
        height: 18px;
        line-height: 18px;
        margin: auto;
        text-align: center;
      }
    }
  }
  .grass-container {
    width: 677px;
    height: 100px;
    margin: 0 auto;
  }

  .level-svg {
    margin: 0 3px;
    display: block;
    float: left;
    width: 13px;
    &.last {
      width: 10px;
      margin-right: 0px;
    }
  }
}
</style>