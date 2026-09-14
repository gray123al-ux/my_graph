
# 영화 데이터 그래프 도감 1 - 시간

import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="영화 데이터 그래프 도감 1 - 시간",
    page_icon="🎬",
    layout="wide"
)

st.title("🎬 영화 데이터 그래프 도감 1 - 시간")
st.write(
    "1년치 일별 박스오피스 데이터를 이용해 "
    "영화의 흥행 흐름을 시간에 따라 살펴봅니다."
)

DATA_URL = (
    "https://raw.githubusercontent.com/greatsong/modudata/"
    "main/data/kobis_daily.csv"
)


# =========================================================
# 데이터 불러오기
# =========================================================

@st.cache_data
def load_data():
    # 1년치(365일) 일별 박스오피스 10위권 기록을 불러옵니다.
    df = pd.read_csv(DATA_URL)

    # 여덟 자리 숫자로 된 날짜를 진짜 날짜로 변환합니다.
    df["날짜"] = pd.to_datetime(
        df["날짜"].astype(str),
        format="%Y%m%d",
        errors="coerce"
    )

    # 숫자 열을 숫자형으로 변환합니다.
    for column in ["순위", "일관객", "누적관객", "스크린수", "상영횟수"]:
        df[column] = pd.to_numeric(df[column], errors="coerce")

    return df


df = load_data()


# =========================================================
# 데이터 요약
# =========================================================

col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        "📅 데이터 기간",
        f"{df['날짜'].min():%Y-%m-%d} ~ {df['날짜'].max():%Y-%m-%d}"
    )

with col2:
    st.metric(
        "🎬 영화 수",
        f"{df['영화명'].nunique():,}편"
    )

with col3:
    st.metric(
        "📊 전체 기록",
        f"{len(df):,}개"
    )


st.divider()


# =========================================================
# 그래프 1. 한 영화의 흥행 곡선
# =========================================================

st.header("1. 한 영화의 흥행 곡선")

st.write(
    "영화를 하나 선택하면 그 영화의 날짜별 일관객 변화를 "
    "선 그래프로 확인할 수 있습니다."
)

# 드롭다운으로 영화를 고릅니다.
movie_list = (
    df["영화명"]
    .dropna()
    .drop_duplicates()
    .sort_values()
    .tolist()
)

movie = st.selectbox(
    "🎬 영화를 고르세요",
    movie_list
)

# 선택한 영화 데이터
one = (
    df[df["영화명"] == movie]
    .sort_values("날짜")
    .copy()
)

# 선 그래프
fig1 = px.line(
    one,
    x="날짜",
    y="일관객",
    markers=True,
    labels={
        "날짜": "날짜",
        "일관객": "일관객 수"
    }
)

fig1.update_traces(
    hovertemplate=(
        "날짜 %{x|%Y-%m-%d}"
        "<br>관객 %{y:,.0f}명"
        "<extra></extra>"
    ),
    line_width=3,
    marker_size=7
)

fig1.update_layout(
    height=500,
    hovermode="x unified",
    xaxis_title="날짜",
    yaxis_title="일관객 (명)",
    yaxis_tickformat=","
)

st.plotly_chart(
    fig1,
    use_container_width=True
)

st.info(
    "💡 이 그래프로 알 수 있는 것: "
    "영화의 날짜별 관객 수가 언제 증가하고 감소했는지 확인할 수 있습니다."
)


# =========================================================
# 그래프 2. 기간 일관객 합계 TOP 5 영화
# =========================================================

st.divider()

st.header("2. 기간 일관객 합계 TOP 5")

st.write(
    "이 기간 동안 기록된 일관객을 영화별로 모두 더해 "
    "관객 합계가 가장 큰 5편의 흥행 흐름을 비교합니다."
)


# ---------------------------------------------------------
# 영화별 기간 일관객 합계 계산
# ---------------------------------------------------------

movie_total = (
    df.groupby("영화명", as_index=False)["일관객"]
    .sum()
    .sort_values("일관객", ascending=False)
)

# 상위 5편
top5_movies = movie_total.head(5)["영화명"].tolist()


# ---------------------------------------------------------
# TOP 5 영화의 날짜별 데이터만 추출
# ---------------------------------------------------------

top5_df = df[
    df["영화명"].isin(top5_movies)
].copy()

top5_df = top5_df.sort_values(["날짜", "영화명"])


# ---------------------------------------------------------
# 여러 영화를 하나의 선 그래프로 표시
# ---------------------------------------------------------

fig2 = px.line(
    top5_df,
    x="날짜",
    y="일관객",
    color="영화명",
    markers=True,
    labels={
        "날짜": "날짜",
        "일관객": "일관객 수",
        "영화명": "영화"
    }
)

fig2.update_traces(
    hovertemplate=(
        "영화: %{fullData.name}"
        "<br>날짜: %{x|%Y-%m-%d}"
        "<br>관객: %{y:,.0f}명"
        "<extra></extra>"
    )
)

fig2.update_layout(
    height=600,
    hovermode="closest",
    xaxis_title="날짜",
    yaxis_title="일관객 (명)",
    yaxis_tickformat=",",
    legend_title="영화",
    legend=dict(
        itemclick="toggle",
        itemdoubleclick="toggleothers"
    )
)

st.plotly_chart(
    fig2,
    use_container_width=True
)


# ---------------------------------------------------------
# TOP 5 영화의 기간 합계 표시
# ---------------------------------------------------------

st.subheader("🏆 기간 일관객 합계")

for rank, row in enumerate(movie_total.head(5).itertuples(), start=1):
    st.write(
        f"**{rank}위. {row.영화명}** — "
        f"{row.일관객:,.0f}명"
    )


st.info(
    "💡 이 그래프로 알 수 있는 것: "
    "기간 전체에서 관객을 많이 모은 영화 5편의 날짜별 흥행 흐름을 한눈에 비교할 수 있습니다."
)


# =============

