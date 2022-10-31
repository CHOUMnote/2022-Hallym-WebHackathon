
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
          <img src="../../../../assets/춘천중앙시장.png" alt="">
          {{market_list[0].descrition}}
        </div>
        <p class="title">평점</p>
        <div class="review">
          <div class="item" v-for="item in review_list">
            닉네임: {{item.username}}
            {{item.avatar}}
            내용: {{item.review_content}}
            별점: {{item.star}}
            작성시간: {{item.create_time}}
          </div>
        </div>
        <input type="text" class="content" placeholder="자유롭게 의견을 남겨주세요" v-model="this.review_content" style="margin-top: 20px; width:100%;height:200px;font-size:16px;">
        <select v-model="star" name="" id="">
          <option value="" selected>평점</option>
          <option value="5">5</option>
          <option value="4">4</option>
          <option value="3">3</option>
          <option value="2">2</option>
          <option value="1">1</option>
        </select>
        <input type="button" value="제출" @click="createReview(this.review_content, $route.name, this.star)">
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
          <img src="../../../../assets/춘천풍물시장.png" alt="">
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
          <img src="../../../../assets/춘천남부시장.png" alt="">
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
          <img src="../../../../assets/춘천동부시장.png" alt="">
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
          <img src="../../../../assets/춘천중앙시장.png" alt="">
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
          <img src="../../../../assets/춘천중앙시장.png" alt="">
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
          <img src="../../../../assets/춘천중앙시장.png" alt="">
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
import api from "../../api";
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
          descrition: '춘천의 대표적 재래시장으로서 2002년부터 실시한 활성화 사업으로 현대화 모습을 갖추었으며, 한복, 가방, 신발, 의류, 가전, 귀금속, 각종 먹거리 등이 있는 시장이다. TV드라마 "겨울연가"의 인기로 일본 및 동남아 관광객들이 찾아옴에 따라 시장에서 소비자들을 위한 이벤트사업을 유치하고 있다. 한국관광공사가 뽑은 외국인이 가기 좋은 전통시장으로 선정되었다',
          image: [],
          tag: '#쇼핑 #재래시장 #반찬',
          address: '강원 춘천시 중앙로 83'
        },
        {
          id: 2,
          name: '춘천풍물시장',
          descrition: '강원도 춘천시 영서로에 위치한 5일장으로 복선전철 하부공간을 이용한 전국 최초의 전통시장이다. 원래 풍물시장은 춘천의 명동과 인근에서 산발적으로 노점을 운영하던 100여명의 상인들이 도로정비 사업의 일환으로 집단으로 옮겨간 약사동 복개하천지역에 위치하였지만 그곳에 터를 잡아 20여년 동안 장사를 하다가 다시 시의 생태하천 복원사업에 의해 지금의 전철하부공간으로 자리를 옮긴 것이다. 5일장이 펼쳐지는 장날(2, 7일)에는 수도권의 관광객과 인근 시군의 손님들이 넘쳐나 발 디딜틈이 없을 정도로 인산인해를 이루는 것이 장관이며 토속음식인 전병, 빈대떡, 장떡, 춘천막걸리에서부터 돼지부속고기, 닭갈비 등을 저렴한 가격에 먹을 수 있다. 봄철에서 가을까지는 근교에서 농사를 짓는 사람들이 그날그날 수확한 싱싱한 농산물을 가지고 나와 저렴한 가격에 팔기도 한다. 또한 할머니들이 직접 담근 된장, 막장, 고추장이나, 짱아치는 물론 직접 수확한 깨로 짠 참기름, 들기름 등을 판매하기도 한다.',
          image: [],
          tag: '#개꿀교통 #지하철 #5일장',
          address: '강원도 춘천시 온의동 29-3'
        },
        {
          id: 3,
          name: '춘천남부시장',
          descrition: '춘천남부시장은 1970년대에 가건물 노점 형태로 자연스레 형성되었던 것을 1980년대에 이르러 건물을 신축, 종합 시장으로 새롭게 문을 연 것이다. 춘천남부시장의 특징은 지하에 먹자골목이 형성되어 있다는 것이다. 막국수, 주물럭 등의 다양한 메뉴가 여행자들을 기다리고 있다. 음식 맛을 보러 일부러 먼 곳에서 찾아올 정도로 소문난 막국수 전문점이 위치해 있는 곳 또한 바로 이 춘천남부시장이다.',
          image: [],
          tag: '#식료품 #막국수 #지역상품',
          address: '강원도 춘천시 공지로 367'
        },
        {
          id: 4,
          name: '춘천제일종합시장',
          descrition: '1984년 12월에 생긴 춘천 첫 백화점이다. 대도시의 백화점처럼 삐까번쩍 하지는 않지만, 춘천에서는 지금까지 보지 못했던 대형 건물에 메이커 의류를 비롯한 패션잡화와 생활용품이 백화점을 가득 메웠다. 지하 1층, 지상 3층, 연건평 1만 26㎡ 규모에 총 260여 개의 점포가 들어섰다. 브랜드 의류부터 중장년층 의류, 신발, 한복, 홈패션, 이불, 그릇, 가구, 시계, 귀금속 등 살림살이에 필요한 물건이 지상 3층에 빼곡히 채워졌다. 지하 1층은 식당가로 중국집, 한식당, 순댓국집 등이 성업했다. 한때는 대형 나이트클럽이 생겨 춘천의 밤 문화를 주름잡았다. 춤을 가르치는 교습소도 있었다. 가볍게 한잔 걸치는 선술집에는 동네 남자들이 북적거렸다.  2002년부터 2003년까지는 1년 1개월 동안 춘천시의 지원을 받아 재래시장 현대화사업을 했다. 그때부터 지금까지 제일종합시장 상인들은 한결같이 한 자리에서 영업을 이어오고 있다.',
          image: [],
          tag: '#쇼핑 #재래시장 #반찬',
          address: '강원 춘천시 중앙로 83'
        },
        {
          id: 5,
          name: '춘천동부시장',
          descrition: '1988년 개설된 상가건물형의 중형시장. 춘천시 동부 팔호광장에서 중앙로로 이어지는 길목에 있으며 1969년 개장하였다. 농산물을 비롯하여 각종 공산품과 생활필수품 등을 취급하며, 특히 먹을거리가 유명하여 복합상가 지하에 있는 몇몇 떡집과 음식점은 명소로 알려져 있다. 1988년에 시장의 활성화를 위하여 현대화된 주상복합건물을 증축하였으며, 점포는 복합상가의 141개와 노점, 인근 점포 등을 포함하여 모두 500여 개에 이른다.',
          image: [],
          tag: '#전통음식 #떡 #전',
          address: '강원도 춘천시 운교동 183'
        },
        {
          id: 6,
          name: '춘천제일시장',
          descrition: '춘천제일시장은 70년대 부터 시장이 형성되었으며 춘천낭만시장과 이웃해 있습니다.',
          image: [],
          tag: '#농수산 #과일 #소규모',
          address: '강원 춘천시 중앙로 83'
        },
        {
          id: 7,
          name: '춘천번개시장',
          descrition: '도시재생사업 일환으로 문화관광형 시장으로 탈바꿈을 꿈꾸는 춘천시 소양로 번개시장에서 매주 토요일 소양로 번개시장에서 ‘야시장’이 열린다. 인근 소양강스카이워크 연계된 춘천 밤문화 관광코스로써 특히 스카이워크 이용 시 발급되는 춘천사랑상품권과 번개야시장 이용고객에게 한하여 스카이워크 주차장 무료주차권도 증정한다. 매주 토요일 오후 5시~ 11시 열린다. 뚝방마켓(프리마켓)과 문화공연(거리공연) 등이 같이 운영되며 이색 먹거리, 추억의 먹거리 음식 장터를 벌이고 뚝방마켓은 수공예품과 공예 체험프로그램을 만날 수 있다.',
          image: [],
          tag: '#쇼핑 #재래시장 #반찬',
          address: '강원도 춘천시 소양로1가'
        }
      ],
      review_content: '',
      articleId: '',
      star: '',
      review_list: []
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
    api.getReviewList($route.name).then(resp => {
      this.review_list = resp.data.data
    }, () => {
    })

    var map = new kakao.maps.Map(container, options)
  },
  methods: {
    createReview(content, id, star) {
      console.log(this.content, this.star);
      api.createReview(content, id, star)
    }
  }
}
</script>

<style lang="less" scoped>
.wrapper {
  .banner {
    width: 100%;
    height: 500px;
    background-image: url('../../../../assets/춘천중앙시장.png');
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
      select, input {
        float: right;
        width: 60px;
        height: 30px;
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