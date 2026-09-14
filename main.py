```python
# 영화 데이터 그래프 도감 1 - 시간

import streamlit as st
import pandas as pd
import plotly.express as px


# =========================================================
# 기본 설정
# =========================================================

st.set_page_config(
    page_title="영화 데이터 그래프 도감 1 - 시간",
    page_icon="🎬",
    layout="wide"
)

st.title("🎬 영화 데이터 그래프 도감 1 - 시간")
st.markdown(
    "1년치 일별 박스오피스 데이터를 이용해 "
    "영화의 흥행 흐름을 시간에 따라 살펴봅니다."
)


# =========================================================
# 데이터 불러오기
# =========================================================

DATA_URL = (
    "https://raw.githubusercontent.com/greatsong/modudata/"
    "main/data/kobis_daily.csv"
)


@st.cache_data
def load_data():
    # 1년치 일별 박스오피스 10위권 기록
    df = pd.read_csv(DATA_URL)

    # 날짜를 실제 날짜 형식으로 변환
    df["날짜"] = pd.to_datetime(
        df["날짜"].astype(str),
        format="%Y%m%d",
        errors="coerce"
    )

    # 숫자 데이터는 확실하게 숫자로 변환
    numeric_columns = [
        "순위",
        "일관객",
        "누적관객",
        "스크린수",
        "상영횟수"
    ]

    for column in numeric_columns:
        df[column] = pd.to_numeric(
            df[column],
            errors="coerce"
        )

    # 날짜순으로 정렬
    df = df.sort_values("날짜").reset_index(drop=True)

    return df


try:
    df = load_data()

except Exception as e:
    st.error("데이터를 불러오지 못했습니다.")
    st.exception(e)
    st.stop()


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


# 영화 목록
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


# 선택한 영화의 데이터
one = (
    df[df["영화명"] == movie]
    .sort_values("날짜")
    .copy()
)


# 선 그래프
fig = px.line(
    one,
    x="날짜",
    y="일관객",
    markers=True,
    labels={
        "날짜": "날짜",
        "일관객": "일관객 수"
    }
)

fig.update_traces(
    hovertemplate=(
        "날짜 %{x|%Y-%m-%d}"
        "<br>관객 %{y:,.0f}명"
        "<extra></extra>"
    ),
    line_width=3,
    marker_size=7
)

fig.update_layout(
    height=500,
    margin=dict(l=20, r=20, t=30, b=20),
    hovermode="x unified",
    xaxis=dict(
        showgrid=True
    ),
    yaxis=dict(
        title="일관객 (명)",
        tickformat=","
    )
)

st.plotly_chart(
    fig,
    use_container_width=True
)


# 그래프로 알 수 있는 것
st.info(
    "💡 이 그래프로 알 수 있는 것: "
    "영화의 날짜별 관객 수가 언제 증가하고 감소했는지 확인할 수 있습니다."
)


# =========================================================
# 그래프 2
# =========================================================

st.divider()

st.header("2. 그래프 2")
st.caption("다음 그래프를 이 영역에 추가할 수 있습니다.")


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
# 그래프 5
# =========================================================

st.divider()

st.header("5. 그래프 5")
st.caption("다음 그래프를 이 영역에 추가할 수 있습니다.")
```
