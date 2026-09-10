
# 영화 데이터 그래프 도감 1 - 시간

import streamlit as st
import pandas as pd
import plotly.express as px


# ============================================================
# 기본 설정
# ============================================================

st.set_page_config(
    page_title="영화 데이터 그래프 도감 1 - 시간",
    layout="wide"
)

st.title("영화 데이터 그래프 도감 1 - 시간")


# ============================================================
# 데이터 불러오기
# ============================================================

DATA_URL = "https://raw.githubusercontent.com/greatsong/modudata/main/data/kobis_daily.csv"


@st.cache_data
def load_data():
    # 1년치(365일) 일별 박스오피스 10위권 기록을 불러옵니다.
    df = pd.read_csv(DATA_URL)

    # 여덟 자리 숫자로 된 날짜 열을 진짜 날짜로 바꿉니다.
    df["날짜"] = pd.to_datetime(
        df["날짜"],
        format="%Y%m%d"
    )

    # 관객 수를 숫자로 변환합니다.
    df["일관객"] = pd.to_numeric(
        df["일관객"],
        errors="coerce"
    )

    return df


df = load_data()


# ============================================================
# 그래프 1. 영화 하나의 흥행 곡선
# ============================================================

st.header("1. 한 영화의 흥행 곡선")

st.write(
    "영화를 하나 고르면 날짜에 따라 하루 관객 수가 "
    "어떻게 변했는지 확인할 수 있습니다."
)

movie_list = sorted(
    df["영화명"].dropna().unique()
)

movie = st.selectbox(
    "영화를 고르세요",
    movie_list
)

one = (
    df[df["영화명"] == movie]
    .sort_values("날짜")
)

fig = px.line(
    one,
    x="날짜",
    y="일관객",
    markers=True,
    title=f"「{movie}」의 날짜별 일관객 변화",
    labels={
        "날짜": "날짜",
        "일관객": "일관객 수"
    }
)

fig.update_traces(
    hovertemplate=(
        "날짜 %{x|%Y-%m-%d}"
        "<br>"
        "관객 %{y:,}명"
        "<extra></extra>"
    )
)

fig.update_layout(
    height=500,
    hovermode="x unified"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

st.caption(
    "이 그래프로 알 수 있는 것: "
    "시간이 지나면서 한 영화의 하루 관객 수가 어떻게 변하는지 알 수 있습니다."
)


# ============================================================
# 그래프 2. 일관객 합계 TOP 5 영화 비교
# ============================================================

st.divider()

st.header("2. 일관객 합계가 가장 큰 영화 5편의 흥행 곡선")

st.write(
    "이 기간 동안 일관객의 합계가 가장 큰 5편을 골라 "
    "날짜별 관객 수를 비교합니다."
)

movie_totals = (
    df.groupby("영화명", as_index=False)["일관객"]
    .sum()
    .sort_values("일관객", ascending=False)
)

top5_movies = movie_totals.head(5)["영화명"].tolist()

top5 = df[
    df["영화명"].isin(top5_movies)
].copy()

top5 = top5.sort_values(
    ["날짜", "영화명"]
)

fig2 = px.line(
    top5,
    x="날짜",
    y="일관객",
    color="영화명",
    markers=True,
    title="일관객 합계 TOP 5 영화의 날짜별 관객 변화",
    labels={
        "날짜": "날짜",
        "일관객": "일관객 수",
        "영화명": "영화"
    },
    custom_data=["영화명"]
)

fig2.update_traces(
    hovertemplate=(
        "영화: %{customdata[0]}"
        "<br>"
        "날짜: %{x|%Y-%m-%d}"
        "<br>"
        "일관객: %{y:,}명"
        "<extra></extra>"
    )
)

fig2.update_layout(
    height=600,
    hovermode="x unified",
    legend_title_text="영화"
)

st.plotly_chart(
    fig2,
    use_container_width=True
)

st.caption(
    "이 그래프로 알 수 있는 것: "
    "기간 전체의 일관객 합계가 큰 영화들이 날짜에 따라 어떤 흥행 곡선을 그렸는지 비교할 수 있습니다."
)


# ============================================================
# 그래프 3
# ============================================================

st.divider()

st.header("3. 다음 그래프")

st.info("앞으로 새로운 그래프를 이 구역에 추가합니다.")


# ============================================================
# 그래프 4. 일관객 합계 TOP 10
# ============================================================

st.divider()

st.header("4. 일관객 합계 TOP 10")

st.write(
    "이 기간 동안 각 영화의 일관객을 모두 더해 "
    "관객 수가 많은 영화 TOP 10을 보여 줍니다."
)


# ------------------------------------------------------------
# 영화별 일관객 합계 + 10위권 기록 일수 계산
# ------------------------------------------------------------

top10 = (
    df.dropna(subset=["영화명"])
      .groupby("영화명")
      .agg(
          일관객합계=("일관객", "sum"),
          10위권_일수=("날짜", "count")
      )
      .sort_values(
          "일관객합계",
          ascending=False
      )
      .head(10)
      .reset_index()
)


# 그래프에서 위쪽에 관객이 많은 영화가 오도록
# 관객 수 기준으로 내림차순 정렬한 순서를 유지합니다.
top10["영화명"] = pd.Categorical(
    top10["영화명"],
    categories=top10["영화명"].tolist(),
    ordered=True
)


# ------------------------------------------------------------
# 가로 막대그래프
# ------------------------------------------------------------

fig4 = px.bar(
    top10,
    x="일관객합계",
    y="영화명",
    orientation="h",
    title="기간 전체 일관객 합계 TOP 10",
    labels={
        "일관객합계": "일관객 합계",
        "영화명": "영화"
    },
    custom_data=["10위권_일수"]
)


# 관객이 많은 영화가 위에 오도록
fig4.update_yaxes(
    categoryorder="array",
    categoryarray=top10["영화명"].tolist(),
    autorange="reversed"
)


# 마우스를 올렸을 때
# 일관객 합계 + 10위권에 든 날수를 함께 표시
fig4.update_traces(
    hovertemplate=(
        "영화: %{y}"
        "<br>"
        "일관객 합계: %{x:,}명"
        "<br>"
        "10위권에 든 날수: %{customdata[0]}일"
        "<extra></extra>"
    )
)


fig4.update_layout(
    height=550
)


st.plotly_chart(
    fig4,
    use_container_width=True
)


# ------------------------------------------------------------
# 그래프 4에서 알 수 있는 것
# ------------------------------------------------------------

st.caption(
    "이 그래프로 알 수 있는 것: "
    "이 기간 동안 관객을 가장 많이 모은 영화가 무엇인지와 각 영화가 10위권에 얼마나 오래 머물렀는지 비교할 수 있습니다."
)


# ============================================================
# 그래프 5
# ============================================================

st.divider()

st.header("5. 다음 그래프")

st.info("앞으로 새로운 그래프를 이 구역에 추가합니다.")
