
<template>
<div>
  <div v-if="$route.name=='market-1'" class="wrapper">
    <div class="banner">
      <div class="market_name">
        {{market_list[0].name}}
      </div>
    </div>
    <div class="main_container">
      <div class="left_container">
        <p class="title">상세정보</p>
        <div class="descrition">
          <img src="../../../../assets/춘천중앙시장.jpg" alt="">
          {{market_list[0].descrition}}
        </div>
      </div>
      <div class="right_container">
        <div class="tags">
          <div class="item">
            <div class="title">태그</div>
            <div class="tagging">
              {{market_list[0].tag}}
            </div>
          </div>
          <div class="item">
            <div class="title">주소</div>
            <div class="tagging">
              {{market_list[0].address}}
            </div>
          </div>
        </div>
        <KakaoMap></KakaoMap>
      </div>
    </div>
  </div>
  <div v-if="$route.name=='market-2'" class="wrapper">
    <div class="banner">
      <div class="market_name">
        {{market_list[1].name}}
      </div>
    </div>
    <div class="main_container">
      <div class="left_container">
        <p class="title">상세정보</p>
        <div class="descrition">
          <img src="../../../../assets/춘천중앙시장.jpg" alt="">
          {{market_list[1].descrition}}
        </div>
      </div>
      <div class="right_container">
        <div class="tags">
          <div class="item">
            <div class="title">태그</div>
            <div class="tagging">
              {{market_list[1].tag}}
            </div>
          </div>
          <div class="item">
            <div class="title">주소</div>
            <div class="tagging">
              {{market_list[1].address}}
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
  <div v-if="$route.name=='market-3'" class="wrapper">
    <div class="banner">
      <div class="market_name">
        {{market_list[2].name}}
      </div>
    </div>
    <div class="main_container">
      <div class="left_container">
        <p class="title">상세정보</p>
        <div class="descrition">
          <img src="../../../../assets/춘천중앙시장.jpg" alt="">
          {{market_list[2].descrition}}
        </div>
      </div>
      <div class="right_container">
        <div class="tags">
          <div class="item">
            <div class="title">태그</div>
            <div class="tagging">
              {{market_list[2].tag}}
            </div>
          </div>
          <div class="item">
            <div class="title">주소</div>
            <div class="tagging">
              {{market_list[2].address}}
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
  <div v-if="$route.name=='market-4'" class="wrapper">
    <div class="banner">
      <div class="market_name">
        {{market_list[3].name}}
      </div>
    </div>
    <div class="main_container">
      <div class="left_container">
        <p class="title">상세정보</p>
        <div class="descrition">
          <img src="../../../../assets/춘천중앙시장.jpg" alt="">
          {{market_list[3].descrition}}
        </div>
      </div>
      <div class="right_container">
        <div class="tags">
          <div class="item">
            <div class="title">태그</div>
            <div class="tagging">
              {{market_list[3].tag}}
            </div>
          </div>
          <div class="item">
            <div class="title">주소</div>
            <div class="tagging">
              {{market_list[3].address}}
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
  <div v-if="$route.name=='market-5'" class="wrapper">
    <div class="banner">
      <div class="market_name">
        {{market_list[4].name}}
      </div>
    </div>
    <div class="main_container">
      <div class="left_container">
        <p class="title">상세정보</p>
        <div class="descrition">
          <img src="../../../../assets/춘천중앙시장.jpg" alt="">
          {{market_list[4].descrition}}
        </div>
      </div>
      <div class="right_container">
        <div class="tags">
          <div class="item">
            <div class="title">태그</div>
            <div class="tagging">
              {{market_list[4].tag}}
            </div>
          </div>
          <div class="item">
            <div class="title">주소</div>
            <div class="tagging">
              {{market_list[4].address}}
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
  <div v-if="$route.name=='market-6'" class="wrapper">
    <div class="banner">
      <div class="market_name">
        {{market_list[5].name}}
      </div>
    </div>
    <div class="main_container">
      <div class="left_container">
        <p class="title">상세정보</p>
        <div class="descrition">
          <img src="../../../../assets/춘천중앙시장.jpg" alt="">
          {{market_list[5].descrition}}
        </div>
      </div>
      <div class="right_container">
        <div class="tags">
          <div class="item">
            <div class="title">태그</div>
            <div class="tagging">
              {{market_list[5].tag}}
            </div>
          </div>
          <div class="item">
            <div class="title">주소</div>
            <div class="tagging">
              {{market_list[5].address}}
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
  <div v-if="$route.name=='market-7'" class="wrapper">
    <div class="banner">
      <div class="market_name">
        {{market_list[6].name}}
      </div>
    </div>
    <div class="main_container">
      <div class="left_container">
        <p class="title">상세정보</p>
        <div class="descrition">
          <img src="../../../../assets/춘천중앙시장.jpg" alt="">
          {{market_list[6].descrition}}
        </div>
      </div>
      <div class="right_container">
        <div class="tags">
          <div class="item">
            <div class="title">태그</div>
            <div class="tagging">
              {{market_list[6].tag}}
            </div>
          </div>
          <div class="item">
            <div class="title">주소</div>
            <div class="tagging">
              {{market_list[6].address}}
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</div>
</template>

<script>
/* eslint-disable */
import KakaoMap from "../../components/KakaoMap.vue";

export default {
  name: 'MarketDetail',
  components: {
    KakaoMap
  },
  data () {
    return {
      market_list: [
        {
          id: 1,
          name: '춘천중앙시장',
          descrition: '춘천 재래시장에 대한 설명글입니다. 춘천 재래시장에 대한 설명글입니다.춘천 재래시장에 대한 설명글입니다.춘천 재래시장에 대한 설명글입니다.춘천 재래시장에 대한 설명글입니다.춘천 재래시장에 대한 설명글입니다.춘천 재래시장에 대한 설명글입니다.춘천 재래시장에 대한 설명글입니다.춘천 재래시장에 대한 설명글입니다.춘천 재래시장에 대한 설명글입니다.춘천 재래시장에 대한 설명글입니다.춘천 재래시장에 대한 설명글입니다.춘천 재래시장에 대한 설명글입니다.춘천 재래시장에 대한 설명글입니다.춘천 재래시장에 대한 설명글입니다.춘천 재래시장에 대한 설명글입니다.',
          image: [],
          tag: '#쇼핑 #재래시장 #반찬',
          address: '강원 춘천시 중앙로 83'
        },
        {
          id: 2,
          name: '춘천풍물시장',
          descrition: '춘천 재래시장에 대한 설명글입니다. 춘천 재래시장에 대한 설명글입니다.춘천 재래시장에 대한 설명글입니다.춘천 재래시장에 대한 설명글입니다.춘천 재래시장에 대한 설명글입니다.춘천 재래시장에 대한 설명글입니다.춘천 재래시장에 대한 설명글입니다.춘천 재래시장에 대한 설명글입니다.춘천 재래시장에 대한 설명글입니다.춘천 재래시장에 대한 설명글입니다.춘천 재래시장에 대한 설명글입니다.춘천 재래시장에 대한 설명글입니다.춘천 재래시장에 대한 설명글입니다.춘천 재래시장에 대한 설명글입니다.춘천 재래시장에 대한 설명글입니다.춘천 재래시장에 대한 설명글입니다.',
          image: [],
          tag: '#쇼핑 #재래시장 #반찬',
          address: '강원 춘천시 중앙로 83'
        },
        {
          id: 3,
          name: '춘천중앙시장',
          descrition: '춘천 재래시장에 대한 설명글입니다. 춘천 재래시장에 대한 설명글입니다.춘천 재래시장에 대한 설명글입니다.춘천 재래시장에 대한 설명글입니다.춘천 재래시장에 대한 설명글입니다.춘천 재래시장에 대한 설명글입니다.춘천 재래시장에 대한 설명글입니다.춘천 재래시장에 대한 설명글입니다.춘천 재래시장에 대한 설명글입니다.춘천 재래시장에 대한 설명글입니다.춘천 재래시장에 대한 설명글입니다.춘천 재래시장에 대한 설명글입니다.춘천 재래시장에 대한 설명글입니다.춘천 재래시장에 대한 설명글입니다.춘천 재래시장에 대한 설명글입니다.춘천 재래시장에 대한 설명글입니다.',
          image: [],
          tag: '#쇼핑 #재래시장 #반찬',
          address: '강원 춘천시 중앙로 83'
        },
        {
          id: 4,
          name: '춘천중앙시장',
          descrition: '춘천 재래시장에 대한 설명글입니다. 춘천 재래시장에 대한 설명글입니다.춘천 재래시장에 대한 설명글입니다.춘천 재래시장에 대한 설명글입니다.춘천 재래시장에 대한 설명글입니다.춘천 재래시장에 대한 설명글입니다.춘천 재래시장에 대한 설명글입니다.춘천 재래시장에 대한 설명글입니다.춘천 재래시장에 대한 설명글입니다.춘천 재래시장에 대한 설명글입니다.춘천 재래시장에 대한 설명글입니다.춘천 재래시장에 대한 설명글입니다.춘천 재래시장에 대한 설명글입니다.춘천 재래시장에 대한 설명글입니다.춘천 재래시장에 대한 설명글입니다.춘천 재래시장에 대한 설명글입니다.',
          image: [],
          tag: '#쇼핑 #재래시장 #반찬',
          address: '강원 춘천시 중앙로 83'
        },
        {
          id: 5,
          name: '춘천중앙시장',
          descrition: '춘천 재래시장에 대한 설명글입니다. 춘천 재래시장에 대한 설명글입니다.춘천 재래시장에 대한 설명글입니다.춘천 재래시장에 대한 설명글입니다.춘천 재래시장에 대한 설명글입니다.춘천 재래시장에 대한 설명글입니다.춘천 재래시장에 대한 설명글입니다.춘천 재래시장에 대한 설명글입니다.춘천 재래시장에 대한 설명글입니다.춘천 재래시장에 대한 설명글입니다.춘천 재래시장에 대한 설명글입니다.춘천 재래시장에 대한 설명글입니다.춘천 재래시장에 대한 설명글입니다.춘천 재래시장에 대한 설명글입니다.춘천 재래시장에 대한 설명글입니다.춘천 재래시장에 대한 설명글입니다.',
          image: [],
          tag: '#쇼핑 #재래시장 #반찬',
          address: '강원 춘천시 중앙로 83'
        },
        {
          id: 6,
          name: '춘천중앙시장',
          descrition: '춘천 재래시장에 대한 설명글입니다. 춘천 재래시장에 대한 설명글입니다.춘천 재래시장에 대한 설명글입니다.춘천 재래시장에 대한 설명글입니다.춘천 재래시장에 대한 설명글입니다.춘천 재래시장에 대한 설명글입니다.춘천 재래시장에 대한 설명글입니다.춘천 재래시장에 대한 설명글입니다.춘천 재래시장에 대한 설명글입니다.춘천 재래시장에 대한 설명글입니다.춘천 재래시장에 대한 설명글입니다.춘천 재래시장에 대한 설명글입니다.춘천 재래시장에 대한 설명글입니다.춘천 재래시장에 대한 설명글입니다.춘천 재래시장에 대한 설명글입니다.춘천 재래시장에 대한 설명글입니다.',
          image: [],
          tag: '#쇼핑 #재래시장 #반찬',
          address: '강원 춘천시 중앙로 83'
        },
        {
          id: 7,
          name: '춘천중앙시장',
          descrition: '춘천 재래시장에 대한 설명글입니다. 춘천 재래시장에 대한 설명글입니다.춘천 재래시장에 대한 설명글입니다.춘천 재래시장에 대한 설명글입니다.춘천 재래시장에 대한 설명글입니다.춘천 재래시장에 대한 설명글입니다.춘천 재래시장에 대한 설명글입니다.춘천 재래시장에 대한 설명글입니다.춘천 재래시장에 대한 설명글입니다.춘천 재래시장에 대한 설명글입니다.춘천 재래시장에 대한 설명글입니다.춘천 재래시장에 대한 설명글입니다.춘천 재래시장에 대한 설명글입니다.춘천 재래시장에 대한 설명글입니다.춘천 재래시장에 대한 설명글입니다.춘천 재래시장에 대한 설명글입니다.',
          image: [],
          tag: '#쇼핑 #재래시장 #반찬',
          address: '강원 춘천시 중앙로 83'
        }
      ]
    }
  },
  mounted () {
    // 지도그리기
    const script = document.createElement('script')
    script.type = 'text/javascript'
    script.src = '//dapi.kakao.com/v2/maps/sdk.js?appkey=fe4d8746500baab5293f057a594f6653'
    document.head.appendChild(script)
    var container = document.getElementById('map')
    var options = {
      center: new kakao.maps.LatLng(33.450701, 126.570667),
      level: 3
    };

    var map = new kakao.maps.Map(container, options)
  }
}
</script>

<style lang="less" scoped>
.wrapper {
  .banner {
    width: 100%;
    height: 500px;
    background-image: url('../../../../assets/춘천중앙시장.jpg');
    background-size: cover;
    .market_name {
      text-align: center;
      font-size: 36px;
      font-weight: 800;
      color: #222;
      padding: 50px;
    }
  }
  .main_container {
    display: flex;
    margin-top: 30px;
    .left_container {
      width: 70%;
      .title {
        background-color: #F9CBBB;
        color: #F4815A;
        padding: 5px;
        font-size: 20px;
        font-weight: 800;
      }
      img {
        margin: 20px auto;
        display: block;
      }
      .descrition {
        font-size: 16px;
        color: #222;
        padding: 10px;
      }
    }
    .right_container {
      width: 30%;
      padding: 0 20px;
      .tags {
        .item {
          margin-bottom: 20px;
          .title {
            border: 1.5px solid #C0C0C0;
            width: 60px;
            text-align: center;
            border-radius: 10px;
            font-size: 20px;
            margin-bottom: 10px;
          }
          .tagging {
            font-size: 16px;
          }
        }
      }
    }
  }
}
</style>