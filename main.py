
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
    df = pd.read_csv(DATA_URL)

    # 날짜를 진짜 날짜 형식으로 변환
    df["날짜"] = pd.to_datetime(
        df["날짜"].astype(str),
        format="%Y%m%d",
        errors="coerce"
    )

    # 숫자 열 변환
    for column in ["순위", "일관객", "누적관객", "스크린수", "상영횟수"]:
        df[column] = pd.to_numeric(
            df[column],
            errors="coerce"
        )

    return df


df = load_data()


# =========================================================
# 그래프 1
# =========================================================

st.header("1. 한 영화의 흥행 곡선")

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

one = (
    df[df["영화명"] == movie]
    .sort_values("날짜")
    .copy()
)

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
# 그래프 2
# =========================================================

st.divider()
st.header("2. 기간 일관객 합계 TOP 5")

movie_total = (
    df.groupby("영화명", as_index=False)["일관객"]
    .sum()
    .sort_values("일관객", ascending=False)
)

top5_movies = movie_total.head(5)["영화명"].tolist()

top5_df = df[
    df["영화명"].isin(top5_movies)
].copy()

top5_df = top5_df.sort_values(["날짜", "영화명"])

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

st.info(
    "💡 이 그래프로 알 수 있는 것: "
    "기간 전체에서 관객을 많이 모은 영화 5편의 날짜별 흥행 흐름을 비교할 수 있습니다."
)


# =========================================================
# 그래프 3
# =========================================================

st.divider()
st.header("3. 그래프 3")
st.caption("다음 그래프를 이 영역에 추가할 수 있습니다.")


# =========================================================
# 그래프 4
# =========================================================

st.divider()
st.header("4. 그래프 4")
st.caption("다음 그래프를 이 영역에 추가할 수 있습니다.")


# =========================================================
# 그래프 5. 월 × 요일 히트맵
# =========================================================

st.divider()

st.header("5. 월 × 요일별 일관객 히트맵")

st.write(
    "날짜에서 월과 요일을 뽑아, "
    "같은 월·요일에 기록된 일관객을 모두 합산합니다."
)


# ---------------------------------------------------------
# 월과 요일 추출
# ---------------------------------------------------------

heatmap_df = df.copy()

heatmap_df["월"] = heatmap_df["날짜"].dt.month

# weekday(): 월요일=0, 일요일=6
weekday_names = [
    "월요일",
    "화요일",
    "수요일",
    "목요일",
    "금요일",
    "토요일",
    "일요일"
]

heatmap_df["요일"] = (
    heatmap_df["날짜"]
    .dt.weekday
    .map(dict(enumerate(weekday_names)))
)


# ---------------------------------------------------------
# 월 × 요일별 일관객 합계
# ---------------------------------------------------------

heatmap_data = (
    heatmap_df
    .groupby(["월", "요일"])["일관객"]
    .sum()
    .reset_index()
)


# 요일 순서 고정
heatmap_data["요일"] = pd.Categorical(
    heatmap_data["요일"],
    categories=weekday_names,
    ordered=True
)

heatmap_data = heatmap_data.sort_values(
    ["월", "요일"]
)


# ---------------------------------------------------------
# 히트맵
# ---------------------------------------------------------

fig5 = px.density_heatmap(
    heatmap_data,
    x="요일",
    y="월",
    z="일관객",
    category_orders={
        "요일": weekday_names,
        "월": list(range(1, 13))
    },
    labels={
        "요일": "요일",
        "월": "월",
        "일관객": "일관객 합계"
    },
    text_auto=","
    # color_continuous_scale은 지정하지 않아
    # Plotly 기본 색상 그라데이션을 사용합니다.
)

fig5.update_layout(
    height=600,
    xaxis_title="요일",
    yaxis_title="월",
    coloraxis_colorbar_title="관객 수"
)

fig5.update_yaxes(
    tickmode="array",
    tickvals=list(range(1, 13)),
    ticktext=[f"{month}월" for month in range(1, 13)]
)

fig5.update_traces(
    hovertemplate=(
        "%{y}월 %{x}"
        "<br>일관객 합계: %{z:,.0f}명"
        "<extra></extra>"
    )
)

st.plotly_chart(
    fig5,
    use_container_width=True
)

st.info(
    "💡 이 그래프로 알 수 있는 것: "
    "어떤 월과 요일에 박스오피스 상위 10편의 관객이 많이 몰렸는지 한눈에 비교할 수 있습니다."
)
