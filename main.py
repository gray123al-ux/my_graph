
# 영화 데이터 그래프 도감 1 - 시간

import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="영화 데이터 그래프 도감 1 - 시간",
    layout="wide"
)

st.title("영화 데이터 그래프 도감 1 - 시간")

DATA_URL = "https://raw.githubusercontent.com/greatsong/modudata/main/data/kobis_daily.csv"


@st.cache_data
def load_data():
    # 1년치(365일) 일별 박스오피스 10위권 기록을 불러옵니다.
    df = pd.read_csv(DATA_URL)

    # 여덟 자리 숫자로 된 날짜를 진짜 날짜로 바꿉니다.
    df["날짜"] = pd.to_datetime(
        df["날짜"].astype(str),
        format="%Y%m%d",
        errors="coerce"
    )

    # 숫자 열을 숫자형으로 바꿉니다.
    for col in ["순위", "일관객", "누적관객", "스크린수", "상영횟수"]:
        df[col] = pd.to_numeric(df[col], errors="coerce")

    return df


df = load_data()


# =========================================================
# 그래프 1. 영화 하나의 흥행 곡선
# =========================================================

st.header("1. 한 영화의 흥행 곡선")

st.write("영화를 하나 골라 날짜별 일관객 변화를 확인합니다.")

movie_list = sorted(df["영화명"].dropna().unique())
movie = st.selectbox("영화를 고르세요", movie_list)

one = (
    df[df["영화명"] == movie]
    .sort_values("날짜")
)

fig1 = px.line(
    one,
    x="날짜",
    y="일관객",
    markers=True,
    labels={
        "날짜": "날짜",
        "일관객": "일관객"
    }
)

fig1.update_traces(
    hovertemplate=(
        "날짜 %{x|%Y-%m-%d}"
        "<br>관객 %{y:,.0f}명"
        "<extra></extra>"
    )
)

fig1.update_layout(
    hovermode="x unified",
    yaxis_tickformat=","
)

st.plotly_chart(
    fig1,
    use_container_width=True
)

st.caption(
    "이 그래프로 알 수 있는 것: "
    "한 영화의 관객이 시간에 따라 어떻게 증가하고 감소했는지 알 수 있습니다."
)


# =========================================================
# 그래프 2. 기간 일관객 합계 TOP 5
# =========================================================

st.divider()
st.header("2. 기간 일관객 합계 TOP 5")

st.write(
    "이 기간 동안 일관객을 모두 더해 관객 합계가 가장 큰 "
    "5편의 날짜별 흥행 흐름을 비교합니다."
)

# 영화별 일관객 합계
movie_total = (
    df.groupby("영화명", as_index=False)["일관객"]
    .sum()
    .sort_values("일관객", ascending=False)
)

top5_movies = movie_total.head(5)["영화명"].tolist()

top5 = df[
    df["영화명"].isin(top5_movies)
].sort_values("날짜")

fig2 = px.line(
    top5,
    x="날짜",
    y="일관객",
    color="영화명",
    markers=True,
    labels={
        "날짜": "날짜",
        "일관객": "일관객",
        "영화명": "영화"
    }
)

fig2.update_traces(
    hovertemplate=(
        "영화 %{fullData.name}"
        "<br>날짜 %{x|%Y-%m-%d}"
        "<br>관객 %{y:,.0f}명"
        "<extra></extra>"
    )
)

fig2.update_layout(
    hovermode="closest",
    yaxis_tickformat=",",
    legend_title="영화"
)

st.plotly_chart(
    fig2,
    use_container_width=True
)

st.caption(
    "이 그래프로 알 수 있는 것: "
    "기간 동안 가장 많은 관객을 모은 영화 5편의 흥행 흐름을 비교할 수 있습니다."
)


# =========================================================
# 그래프 3. 날짜별 10위권 일관객 합계
# =========================================================

st.divider()
st.header("3. 날짜별 10위권 일관객 합계")

st.write(
    "각 날짜의 10위권 영화 일관객을 모두 더해 "
    "하루 전체 관객 규모의 변화를 살펴봅니다."
)

daily_total = (
    df.groupby("날짜", as_index=False)["일관객"]
    .sum()
    .sort_values("날짜")
)

# 관객 합계가 가장 큰 3일
top3_days = daily_total.nlargest(3, "일관객")

fig3 = px.area(
    daily_total,
    x="날짜",
    y="일관객",
    labels={
        "날짜": "날짜",
        "일관객": "10위권 일관객 합계"
    }
)

# 상위 3일을 점과 날짜로 표시
fig3.add_scatter(
    x=top3_days["날짜"],
    y=top3_days["일관객"],
    mode="markers+text",
    text=[
        date.strftime("%m/%d")
        for date in top3_days["날짜"]
    ],
    textposition="top center",
    marker=dict(size=10),
    showlegend=False,
    hovertemplate=(
        "날짜 %{x|%Y-%m-%d}"
        "<br>10위권 관객 합계 %{y:,.0f}명"
        "<extra></extra>"
    )
)

fig3.update_layout(
    hovermode="x unified",
    yaxis_tickformat=","
)

st.plotly_chart(
    fig3,
    use_container_width=True
)

st.caption(
    "이 그래프로 알 수 있는 것: "
    "날짜별 극장가 전체 관객 규모의 변화를 보고 관객이 가장 많이 몰린 날을 찾을 수 있습니다."
)


# =========================================================
# 그래프 4. 영화별 기간 관객 TOP 10
# =========================================================

st.divider()
st.header("4. 영화별 기간 관객 TOP 10")

st.write(
    "영화별로 이 기간의 일관객을 모두 더해 "
    "관객이 가장 많았던 영화 10편을 비교합니다."
)

# 영화별 기간 관객 합계
movie_total = (
    df.groupby("영화명", as_index=False)["일관객"]
    .sum()
    .rename(columns={"일관객": "관객합계"})
)

# 영화별 10위권 등장 날짜 수
movie_days = (
    df.groupby("영화명")["날짜"]
    .nunique()
    .reset_index()
    .rename(columns={"날짜": "10위권 등장일수"})
)

# 두 데이터 합치기
movie_rank = pd.merge(
    movie_total,
    movie_days,
    on="영화명"
)

# TOP 10
top10 = (
    movie_rank
    .sort_values("관객합계", ascending=False)
    .head(10)
    .sort_values("관객합계", ascending=True)
)

fig4 = px.bar(
    top10,
    x="관객합계",
    y="영화명",
    orientation="h",
    text="관객합계",
    custom_data=["10위권 등장일수"],
    labels={
        "관객합계": "기간 일관객 합계",
        "영화명": "영화"
    }
)

fig4.update_traces(
    texttemplate="%{x:,.0f}",
    textposition="outside",
    hovertemplate=(
        "영화 %{y}"
        "<br>기간 일관객 합계 %{x:,.0f}명"
        "<br>개봉 후 10위권 등장일수 %{customdata[0]}일"
        "<extra></extra>"
    )
)

fig4.update_layout(
    height=600,
    xaxis_tickformat=",",
    xaxis_title="기간 일관객 합계 (명)",
    yaxis_title=""
)

st.plotly_chart(
    fig4,
    use_container_width=True
)

st.caption(
    "이 그래프로 알 수 있는 것: "
    "영화별 기간 관객 규모와 개봉 후 10위권에 머문 기간을 함께 비교할 수 있습니다."
)


# =========================================================
# 그래프 5. 월 × 요일별 일관객 합계 히트맵
# =========================================================

st.divider()
st.header("5. 월 × 요일별 일관객 합계")

st.write(
    "날짜에서 월과 요일을 뽑아 월·요일별 일관객 합계를 "
    "히트맵으로 보여 줍니다."
)

heatmap_df = df.copy()

# 월 추출
heatmap_df["월"] = heatmap_df["날짜"].dt.month

# 요일 추출
weekday_names = [
    "월요일",
    "화요일",
    "수요일",
    "목요일",
    "금요일",
    "토요일",
    "일요일"
]

heatmap_df["요일"] = heatmap_df["날짜"].dt.weekday.map(
    dict(enumerate(weekday_names))
)

# 월 × 요일별 일관객 합계
heatmap_data = (
    heatmap_df
    .groupby(["월", "요일"], as_index=False)["일관객"]
    .sum()
)

# 요일 순서를 월요일 → 일요일로 고정
heatmap_data["요일"] = pd.Categorical(
    heatmap_data["요일"],
    categories=weekday_names,
    ordered=True
)

heatmap_data = heatmap_data.sort_values(
    ["월", "요일"]
)

fig5 = px.density_heatmap(
    heatmap_data,
    x="요일",
    y="월",
    z="일관객",
    text_auto=",",
    category_orders={
        "요일": weekday_names,
        "월": list(range(1, 13))
    },
    labels={
        "요일": "요일",
        "월": "월",
        "일관객": "일관객 합계"
    }
)

fig5.update_traces(
    hovertemplate=(
        "%{y}월 %{x}"
        "<br>일관객 합계 %{z:,.0f}명"
        "<extra></extra>"
    )
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
    ticktext=[f"{i}월" for i in range(1, 13)]
)

st.plotly_chart(
    fig5,
    use_container_width=True
)

st.caption(
    "이 그래프로 알 수 있는 것: "
    "어떤 월과 요일에 박스오피스 10위권 관객이 많이 몰렸는지 한눈에 비교할 수 있습니다."
)
