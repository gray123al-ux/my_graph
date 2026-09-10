import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="영화 데이터 그래프 도감 1 - 시간",
    page_icon="🎬",
    layout="wide",
)

DATA_URL = "https://raw.githubusercontent.com/greatsong/modudata/main/data/kobis_daily.csv"

st.title("영화 데이터 그래프 도감 1 - 시간")
st.write("1년치 일별 박스오피스 데이터를 시간의 흐름에 따라 살펴봅니다.")

@st.cache_data
def load_data():
    df = pd.read_csv(DATA_URL)

    # 날짜: 하이픈 없는 8자리 숫자 → 실제 날짜형
    df["날짜"] = pd.to_datetime(df["날짜"].astype(str), format="%Y%m%d", errors="coerce")

    # 숫자형 열 변환
    numeric_cols = ["순위", "영화코드", "일관객", "누적관객", "스크린수", "상영횟수"]
    for col in numeric_cols:
        df[col] = pd.to_numeric(df[col], errors="coerce")

    return df.dropna(subset=["날짜", "영화명"])


try:
    df = load_data()
except Exception as e:
    st.error("데이터를 불러오는 중 문제가 발생했습니다.")
    st.exception(e)
    st.stop()


# ============================================================
# 그래프 1. 영화별 일관객 변화
# ============================================================
st.header("그래프 1. 영화별 일관객 변화")

movie_list = sorted(df["영화명"].dropna().unique())
selected_movie = st.selectbox(
    "영화를 선택하세요.",
    movie_list,
    key="movie_select",
)

movie_df = (
    df[df["영화명"] == selected_movie]
    .sort_values("날짜")
    .copy()
)

fig = px.line(
    movie_df,
    x="날짜",
    y="일관객",
    markers=True,
    labels={
        "날짜": "날짜",
        "일관객": "일관객 수",
    },
    hover_data={
        "날짜": "|%Y-%m-%d",
        "일관객": ":,",
    },
)

fig.update_traces(
    hovertemplate="날짜: %{x|%Y-%m-%d}<br>일관객: %{y:,}명<extra></extra>"
)

fig.update_layout(
    hovermode="x unified",
    height=500,
    margin=dict(l=20, r=20, t=30, b=20),
)

st.plotly_chart(fig, use_container_width=True)

st.markdown(
    "**이 그래프로 알 수 있는 것:** "
    "선의 높이와 변화 모습을 통해 이 영화의 날짜별 관객 수와 흥행 흐름을 한눈에 볼 수 있습니다."
)


# ============================================================
# 그래프 2. 일관객 합계 TOP 5 영화 비교
# ============================================================
st.divider()
st.header("그래프 2. 일관객 합계 TOP 5 영화 비교")

top5_movies = (
    df.groupby("영화명", as_index=False)["일관객"]
    .sum()
    .sort_values("일관객", ascending=False)
    .head(5)["영화명"]
    .tolist()
)

top5_df = (
    df[df["영화명"].isin(top5_movies)]
    .sort_values(["날짜", "영화명"])
    .copy()
)

fig2 = px.line(
    top5_df,
    x="날짜",
    y="일관객",
    color="영화명",
    markers=False,
    labels={
        "날짜": "날짜",
        "일관객": "일관객 수",
        "영화명": "영화",
    },
    hover_data={
        "날짜": "|%Y-%m-%d",
        "일관객": ":,",
    },
)

fig2.update_traces(
    hovertemplate="영화: %{fullData.name}<br>날짜: %{x|%Y-%m-%d}<br>일관객: %{y:,}명<extra></extra>"
)

fig2.update_layout(
    hovermode="x unified",
    height=550,
    margin=dict(l=20, r=20, t=30, b=20),
    legend_title_text="영화",
)

st.plotly_chart(fig2, use_container_width=True)

st.markdown(
    "**이 그래프로 알 수 있는 것:** "
    "기간 전체의 일관객 합계가 가장 큰 영화 5편의 날짜별 흥행 흐름을 서로 비교할 수 있습니다."
)


# ============================================================
# 그래프 3. 날짜별 10위권 일관객 합계
# ============================================================
st.divider()
st.header("그래프 3. 날짜별 10위권 일관객 합계")

daily_total = (
    df.groupby("날짜", as_index=False)["일관객"]
    .sum()
    .sort_values("날짜")
)

# 일관객 합계가 가장 큰 날 3일
top3_days = daily_total.nlargest(3, "일관객").sort_values("날짜")

fig3 = px.area(
    daily_total,
    x="날짜",
    y="일관객",
    labels={
        "날짜": "날짜",
        "일관객": "10위권 일관객 합계",
    },
)

fig3.update_traces(
    hovertemplate="날짜: %{x|%Y-%m-%d}<br>10위권 일관객 합계: %{y:,}명<extra></extra>"
)

# 그래프 위에 상위 3일의 날짜와 합계를 표시
fig3.add_scatter(
    x=top3_days["날짜"],
    y=top3_days["일관객"],
    mode="markers+text",
    text=[
        f"{date:%Y-%m-%d}<br>{value:,}명"
        for date, value in zip(top3_days["날짜"], top3_days["일관객"])
    ],
    textposition="top center",
    name="일관객 합계 TOP 3",
    hovertemplate="날짜: %{x|%Y-%m-%d}<br>합계: %{y:,}명<extra></extra>",
    showlegend=False,
)

fig3.update_layout(
    hovermode="x unified",
    height=550,
    margin=dict(l=20, r=20, t=60, b=20),
)

st.plotly_chart(fig3, use_container_width=True)

st.markdown(
    "**이 그래프로 알 수 있는 것:** "
    "날짜별로 박스오피스 10위권 영화가 기록한 일관객의 전체 규모와 관객이 가장 많이 몰린 날을 확인할 수 있습니다."
)


# ============================================================
# 앞으로 추가할 그래프 구역
# ============================================================
st.divider()
st.header("그래프 4. 추가 예정")
st.info("새로운 시간 관련 영화 데이터 그래프를 이 구역에 이어서 추가할 수 있습니다.")

