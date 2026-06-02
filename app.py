import streamlit as st
import pandas as pd
import numpy as np
from PIL import Image

st.set_page_config(
    page_title="Chart Labs",
    page_icon="📈",
    layout="wide"
)

# =========================
# STYLE
# =========================
st.markdown("""
<style>
.stApp {
    background-color: #050816;
    color: white;
}

.block-container {
    padding-top: 1.5rem;
}

.card {
    background: #0B1021;
    padding: 22px;
    border-radius: 22px;
    border: 1px solid rgba(255,255,255,0.06);
    margin-bottom: 18px;
}

.hero {
    background: linear-gradient(135deg, #0A1226, #111B36);
    padding: 40px;
    border-radius: 30px;
    border: 1px solid rgba(125,167,255,0.18);
}

.tech-card {
    background: #0C1327;
    padding: 20px;
    border-radius: 20px;
    border: 1px solid rgba(255,255,255,0.05);
    min-height: 240px;
}

.tag {
    display: inline-block;
    background: rgba(125,167,255,0.12);
    padding: 7px 14px;
    border-radius: 999px;
    margin-top: 10px;
    color: #BFD0FF;
}

.result-box {
    background: #111B36;
    padding: 15px;
    border-radius: 18px;
    margin-top: 12px;
}

.big-number {
    font-size: 34px;
    font-weight: bold;
    color: #7DA7FF;
}
</style>
""", unsafe_allow_html=True)

# =========================
# DATA
# =========================
techniques = [
    {
        "name": "MACD",
        "category": "모멘텀 분석",
        "description": "추세 전환과 모멘텀 강도를 확인하는 대표적인 보조지표",
        "usage": "골든크로스와 데드크로스를 통해 매수·매도 타이밍 판단"
    },
    {
        "name": "RSI",
        "category": "모멘텀 분석",
        "description": "과매수·과매도 상태를 분석하는 지표",
        "usage": "70 이상 과매수, 30 이하 과매도 구간 확인"
    },
    {
        "name": "스토캐스틱",
        "category": "모멘텀 분석",
        "description": "가격 움직임의 속도를 측정하는 오실레이터",
        "usage": "단기 반등 및 하락 타이밍 분석"
    },
    {
        "name": "CCI",
        "category": "모멘텀 분석",
        "description": "평균 가격 대비 현재 가격의 위치 분석",
        "usage": "강한 추세 진입 여부 판단"
    },
    {
        "name": "ADX",
        "category": "추세 분석",
        "description": "추세 강도를 측정하는 지표",
        "usage": "강한 상승·하락 추세 여부 확인"
    },
    {
        "name": "볼린저밴드",
        "category": "변동성 분석",
        "description": "가격 변동성 확대와 축소를 파악하는 지표",
        "usage": "밴드 수축 후 강한 움직임 발생 가능성 분석"
    },
    {
        "name": "ATR",
        "category": "변동성 분석",
        "description": "평균 변동폭을 측정하는 지표",
        "usage": "손절 범위와 변동성 판단"
    },
    {
        "name": "켈트너 채널",
        "category": "변동성 분석",
        "description": "변동성 기반 채널 지표",
        "usage": "추세 지속 여부 판단"
    },
    {
        "name": "돈치안 채널",
        "category": "변동성 분석",
        "description": "고점·저점 돌파를 확인하는 채널 지표",
        "usage": "추세 돌파 전략 활용"
    },
    {
        "name": "일목균형표",
        "category": "추세 분석",
        "description": "추세와 지지·저항을 종합적으로 보여주는 지표",
        "usage": "구름대 돌파를 통한 추세 판단"
    },
    {
        "name": "이동평균선",
        "category": "추세 분석",
        "description": "가격 평균 흐름을 나타내는 기본 지표",
        "usage": "장기·단기 추세 방향 판단"
    },
    {
        "name": "EMA",
        "category": "추세 분석",
        "description": "최근 가격에 가중치를 둔 이동평균선",
        "usage": "빠른 추세 전환 포착"
    },
    {
        "name": "VWAP",
        "category": "추세 분석",
        "description": "거래량 가중 평균 가격 지표",
        "usage": "기관 평균 매입 단가 분석"
    },
    {
        "name": "추세선",
        "category": "추세 분석",
        "description": "고점과 저점을 연결한 선",
        "usage": "추세 지속 및 이탈 분석"
    },
    {
        "name": "삼각수렴",
        "category": "패턴 분석",
        "description": "가격 변동폭이 점점 줄어드는 패턴",
        "usage": "수렴 이후 강한 방향성 돌파 가능성 분석"
    },
    {
        "name": "상승삼각형",
        "category": "패턴 분석",
        "description": "상승 돌파 가능성이 높은 패턴",
        "usage": "저항선 돌파 시 강세 판단"
    },
    {
        "name": "하락삼각형",
        "category": "패턴 분석",
        "description": "하락 돌파 가능성이 높은 패턴",
        "usage": "지지선 붕괴 여부 확인"
    },
    {
        "name": "쐐기형 패턴",
        "category": "패턴 분석",
        "description": "가격 범위가 좁아지는 패턴",
        "usage": "추세 반전 가능성 분석"
    },
    {
        "name": "헤드앤숄더",
        "category": "패턴 분석",
        "description": "대표적인 하락 반전 패턴",
        "usage": "목선 이탈 시 하락 가능성 판단"
    },
    {
        "name": "역헤드앤숄더",
        "category": "패턴 분석",
        "description": "대표적인 상승 반전 패턴",
        "usage": "상승 추세 전환 판단"
    },
    {
        "name": "더블탑",
        "category": "패턴 분석",
        "description": "고점 두 개가 형성되는 하락 패턴",
        "usage": "저항 확인 후 하락 가능성 분석"
    },
    {
        "name": "더블바텀",
        "category": "패턴 분석",
        "description": "저점 두 개가 형성되는 상승 패턴",
        "usage": "바닥 형성 여부 판단"
    },
    {
        "name": "박스권",
        "category": "패턴 분석",
        "description": "일정 범위 내 횡보 패턴",
        "usage": "상단·하단 돌파 분석"
    },
    {
        "name": "깃발형 패턴",
        "category": "패턴 분석",
        "description": "강한 추세 이후 잠시 쉬는 패턴",
        "usage": "추세 지속 가능성 분석"
    },
    {
        "name": "페넌트 패턴",
        "category": "패턴 분석",
        "description": "짧은 수렴 이후 돌파 패턴",
        "usage": "강한 추세 지속 가능성 확인"
    },
    {
        "name": "오더블럭",
        "category": "수급 분석",
        "description": "기관 매집 및 수급 구간을 찾는 기법",
        "usage": "강한 매수·매도 구간 파악"
    },
    {
        "name": "거래량 분석",
        "category": "수급 분석",
        "description": "거래량을 통한 매수·매도 강도 분석",
        "usage": "돌파 신뢰도 판단"
    },
    {
        "name": "매물대 분석",
        "category": "수급 분석",
        "description": "가격대별 거래량 분석",
        "usage": "강한 지지·저항 구간 확인"
    },
    {
        "name": "OBV",
        "category": "수급 분석",
        "description": "거래량 흐름 누적 지표",
        "usage": "수급 방향 분석"
    },
    {
        "name": "피보나치 되돌림",
        "category": "패턴 분석",
        "description": "되돌림 구간을 예측하는 도구",
        "usage": "지지·저항 예상 구간 분석"
    },
    {
        "name": "엘리엇 파동",
        "category": "패턴 분석",
        "description": "시장 파동 구조를 분석하는 이론",
        "usage": "시장 사이클 및 목표가 분석"
    },
    {
        "name": "망치형 캔들",
        "category": "캔들 분석",
        "description": "하락 후 반등 가능성을 암시하는 캔들",
        "usage": "바닥 반전 신호 확인"
    },
    {
        "name": "도지 캔들",
        "category": "캔들 분석",
        "description": "매수·매도 힘이 균형인 상태",
        "usage": "추세 전환 가능성 분석"
    },
    {
        "name": "장악형 패턴",
        "category": "캔들 분석",
        "description": "이전 캔들을 완전히 덮는 패턴",
        "usage": "강한 반전 가능성 판단"
    },
    {
        "name": "샛별형 패턴",
        "category": "캔들 분석",
        "description": "상승 반전 가능성을 나타내는 패턴",
        "usage": "추세 전환 분석"
    },
    {
        "name": "석별형 패턴",
        "category": "캔들 분석",
        "description": "하락 반전 가능성을 나타내는 패턴",
        "usage": "고점 반전 분석"
    }
]

# =========================
# SIDEBAR
# =========================
st.sidebar.title("📈 Chart Labs")
menu = st.sidebar.radio(
    "메뉴",
    ["홈", "차트 기법 도감", "AI 차트 분석", "대시보드"]
)

# =========================
# HOME
# =========================
if menu == "홈":

    st.markdown("""
    <div class="hero">
        <h1>Chart Labs</h1>
        <h3>AI 기반 차트 분석 도감 플랫폼</h3>
        <p>
        다양한 차트 기법을 학습하고,
        차트 이미지를 AI로 분석하여 적용 가능한 기법을 추천받아보세요.
        </p>
    </div>
    """, unsafe_allow_html=True)

    st.write("")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("""
        <div class="card">
            <div class="big-number">120+</div>
            <h3>차트 기법</h3>
            <p>다양한 보조지표와 패턴 제공</p>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div class="card">
            <div class="big-number">AI</div>
            <h3>차트 분석</h3>
            <p>이미지 기반 자동 분석 지원</p>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown("""
        <div class="card">
            <div class="big-number">6</div>
            <h3>카테고리</h3>
            <p>추세·패턴·변동성 등 분류</p>
        </div>
        """, unsafe_allow_html=True)

    st.subheader("🔥 인기 차트 기법")

    cols = st.columns(3)

    for i, tech in enumerate(techniques[:3]):
        with cols[i]:
            st.markdown(f"""
            <div class="tech-card">
                <h2>{tech['name']}</h2>
                <p><b>{tech['category']}</b></p>
                <p>{tech['description']}</p>
                <div class="tag">실전 활용 가능</div>
            </div>
            """, unsafe_allow_html=True)

# =========================
# TECHNIQUE HUB
# =========================
elif menu == "차트 기법 도감":

    st.title("📚 차트 기법 도감")

    search = st.text_input(
        "차트 기법 검색",
        placeholder="MACD, 볼린저밴드, 오더블럭..."
    )

    category = st.selectbox(
        "카테고리 선택",
        ["전체", "추세 분석", "모멘텀 분석", "변동성 분석", "패턴 분석", "수급 분석"]
    )

    filtered = []

    for tech in techniques:
        if category != "전체" and tech["category"] != category:
            continue

        if search:
            if search.lower() not in tech["name"].lower():
                continue

        filtered.append(tech)

    for tech in filtered:
        st.markdown(f"""
        <div class="card">
            <h2>{tech['name']}</h2>
            <p><b>카테고리:</b> {tech['category']}</p>
            <p>{tech['description']}</p>
            <div class="result-box">
                <b>활용 방법</b><br>
                {tech['usage']}
            </div>
        </div>
        """, unsafe_allow_html=True)

# =========================
# AI ANALYSIS
# =========================
elif menu == "AI 차트 분석":

    st.title("🤖 AI 차트 분석")
    st.write("차트 이미지를 업로드하면 AI가 분석 결과를 제공합니다.")

    uploaded = st.file_uploader(
        "차트 이미지 업로드",
        type=["png", "jpg", "jpeg"]
    )

    if uploaded:
        image = Image.open(uploaded)
        st.image(image, caption="업로드된 차트", use_container_width=True)

        if st.button("AI 분석 시작"):

            progress = st.progress(0)

            for i in range(100):
                progress.progress(i + 1)

            st.success("분석 완료")

            st.markdown("""
            <div class="card">
                <h2>📊 AI 분석 결과</h2>

                <div class="result-box">
                <h4>감지된 패턴</h4>
                ✔ 삼각수렴 패턴 가능성 높음<br>
                ✔ 상승 추세 유지 중
                </div>

                <div class="result-box">
                <h4>추천 보조지표</h4>
                • MACD 골든크로스 발생 가능성<br>
                • 볼린저밴드 수축 구간 감지<br>
                • RSI 과매수 진입 직전
                </div>

                <div class="result-box">
                <h4>AI 종합 해석</h4>
                현재 차트는 변동성이 축소되며 수렴 중인 형태로,
                추후 강한 방향성 돌파 가능성이 존재합니다.
                </div>
            </div>
            """, unsafe_allow_html=True)

# =========================
# DASHBOARD
# =========================
elif menu == "대시보드":

    st.title("📊 시장 분석 대시보드")

    dates = pd.date_range("2025-01-01", periods=50)
    prices = np.cumsum(np.random.randn(50)) + 100

    df = pd.DataFrame({
        "Date": dates,
        "Price": prices
    })

    st.line_chart(df.set_index("Date"))

    col1, col2 = st.columns(2)

    with col1:
        st.metric("BTC 추세", "상승", "+4.2%")
        st.metric("MACD 시그널", "골든크로스")

    with col2:
        st.metric("RSI", "68")
        st.metric("변동성", "축소 중")

    st.subheader("AI 추천 기법")

    rec_df = pd.DataFrame({
        "추천 기법": ["MACD", "볼린저밴드", "삼각수렴"],
        "신뢰도": [92, 88, 84]
    })

    st.dataframe(rec_df, use_container_width=True)

