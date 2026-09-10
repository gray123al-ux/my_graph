import streamlit as st
import pandas as pd
import plotly.express as px

# ---------------------------------------
# 기본 설정
# ---------------------------------------
st.set_page_config(
    page_title="영화 데이터 그래프 도감 1 - 시간",
    page_icon="🎬",
    layout="wide"
)

st.title("🎬 영화 데이터 그래프 도감 1 - 시간")
st.write("1년치 일별 박스오피스 데이터를 이용해 영화의 관객 변화를 살펴봅니다.")

# ---------------------------------------
# 데이터 불러오기
# ---------------------------------------
DATA_URL = "https://raw.githubusercontent.com/greatsong/modudata/main/data/kobis_daily.csv"

@st.cache_data
def load_data():
    df = pd.read_csv(DATA_URL)

    # 날짜를 실제 날짜 형식으로 변환
    df["날짜"] = pd.to_datetime(
        df["날짜"].astype(str),
        format="%Y%m%d",
        errors="coerce"
    )

    # 숫자형 데이터 변환
    numeric_columns = [
        "순위",
        "일관객",
        "누적관객",
        "스크린수",
        "상영횟수"
    ]

    for col in numeric_columns:
        df[col] = pd.to_numeric(df[col], errors="coerce")

    return df


try:
    df = load_data()
except Exception as e:
    st.error("데이터를 불러오는 중 문제가 발생했습니다.")
    st.exception(e)
    st.stop()

# ---------------------------------------
# 데이터 확인
# ---------------------------------------
st.caption(
    f"데이터 기간: {df['날짜'].min().strftime('%Y-%m-%d')} ~ "
    f"{df['날짜'].max().strftime('%Y-%m-%d')}"
)

st.divider()

# =======================================
# 그래프 1
# =======================================
st.header("📈 그래프 1. 영화별 일관객 변화")

st.write(
    "영화를 하나 선택하면 해당 영화가 1년 동안 날짜별로 "
    "몇 명의 관객을 기록했는지 확인할 수 있습니다."
)

# 영화 목록
movie_list = (
    df["영화명"]
    .dropna()
    .drop_duplicates()
    .sort_values()
    .tolist()
)

selected_movie = st.selectbox(
    "영화를 선택하세요",
    movie_list
)

# 선택한 영화 데이터
movie_df = df[df["영화명"] == selected_movie].copy()
movie_df = movie_df.sort_values("날짜")

# 선 그래프
fig = px.line(
    movie_df,
    x="날짜",
    y="일관객",
    markers=True,
    title=f"「{selected_movie}」 날짜별 일관객 변화",
    labels={
        "날짜": "날짜",
        "일관객": "일관객"
    },
    hover_data={
        "날짜": "|%Y-%m-%d",
        "일관객": ":,.0f"
    }
)

fig.update_traces(
    hovertemplate="날짜: %{x|%Y-%m-%d}<br>관객수: %{y:,.0f}명<extra></extra>"
)

fig.update_layout(
    hovermode="x unified",
    xaxis_title="날짜",
    yaxis_title="일관객 (명)",
    height=500
)

st.plotly_chart(fig, use_container_width=True)

# 그래프로 알 수 있는 것
st.info(
    "💡 이 그래프로 알 수 있는 것: "
    "선의 높낮이를 통해 영화의 날짜별 관객 수가 어떻게 변했는지 알 수 있습니다."
)

# ---------------------------------------
# 다음 그래프를 위한 구역
# ---------------------------------------
st.divider()
st.header("📊 그래프 2")
st.caption("다음 그래프가 들어갈 자리입니다.")

st.divider()
st.header("📊 그래프 3")
st.caption("다음 그래프가 들어갈 자리입니다.")

st.divider()
st.header("📊 그래프 4")
st.caption("다음 그래프가 들어갈 자리입니다.")
