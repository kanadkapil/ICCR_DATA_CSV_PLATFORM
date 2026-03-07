import streamlit as st
import pandas as pd
import plotly.express as px
import pathlib

# Set page configuration
st.set_page_config(page_title="Scholarship Dashboard", layout="wide", page_icon="🎓")


@st.cache_data
def load_data():
    file_path = pathlib.Path(__file__).parent / "data2.csv"
    if file_path.exists():
        df = pd.read_csv(file_path)
    else:
        # Fallback if running from a different directory
        df = pd.read_csv("data.csv")

    # Convert types
    numeric_cols = [
        "year",
        "course_duration",
        "available_slots",
        "estimated_selected_students",
    ]
    for col in numeric_cols:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")

    return df


try:
    df = load_data()
except Exception as e:
    st.error(f"Error loading data: {e}")
    st.stop()

# --- SIDEBAR: Filters ---
st.sidebar.header("Filter Data")

# Year filter
years = sorted(df["year"].dropna().unique().tolist())
if years:
    # Use slider
    selected_year = st.sidebar.slider(
        "Select Year Range",
        int(min(years)),
        int(max(years)),
        (int(min(years)), int(max(years))),
    )
else:
    selected_year = (2016, 2025)

# Scheme filter
schemes = df["scholarship_scheme"].dropna().unique().tolist()
selected_schemes = st.sidebar.multiselect(
    "Scholarship Scheme", schemes, default=schemes
)

# University State filter
states = df["university_state"].dropna().unique().tolist()
selected_states = st.sidebar.multiselect("University State", states, default=states)

# Course Level filter
levels = df["course_level"].dropna().unique().tolist()
selected_levels = st.sidebar.multiselect("Course Level", levels, default=levels)

# Field Category filter
categories = df["field_category"].dropna().unique().tolist()
selected_categories = st.sidebar.multiselect(
    "Field Category", categories, default=categories
)

# University Name filter
universities = sorted(df["university_name"].dropna().unique().tolist())
selected_universities = st.sidebar.multiselect(
    "University Name", universities, default=universities
)

# Apply filters
filtered_df = df[
    (df["year"].between(selected_year[0], selected_year[1]))
    & (df["scholarship_scheme"].isin(selected_schemes if selected_schemes else schemes))
    & (df["university_state"].isin(selected_states if selected_states else states))
    & (df["course_level"].isin(selected_levels if selected_levels else levels))
    & (
        df["field_category"].isin(
            selected_categories if selected_categories else categories
        )
    )
    & (
        df["university_name"].isin(
            selected_universities if selected_universities else universities
        )
    )
]

# --- MAIN PAGE: Dashboard ---
st.title("🎓 Scholarship Data Research Dashboard")

st.markdown(
    "This dashboard provides an interactive way to explore scholarship patterns, university allocations, and selection estimates over time."
)

if len(filtered_df) == 0:
    st.warning(
        "No records found matching your exact filter criteria. Please broaden your selection."
    )
    st.stop()


# Metrics
col1, col2, col3, col4 = st.columns(4)
col1.metric(
    "Total Scholarships Available", f"{filtered_df['available_slots'].sum():,.0f}"
)
col2.metric("Total Universities", f"{filtered_df['university_name'].nunique()}")
col3.metric("Total Fields of Study", f"{filtered_df['specialization'].nunique()}")
col4.metric(
    "Estimated Selected", f"{filtered_df['estimated_selected_students'].sum():,.0f}"
)

st.divider()

# List View (Data Table)
st.subheader("📋 Scholarship Data View")
st.dataframe(filtered_df, use_container_width=True, hide_index=True)

st.divider()

# Charts
st.subheader("📊 Analytics")

tab1, tab2, tab3 = st.tabs(
    ["Trends over Time", "University & State Breakdown", "Course Analysis"]
)

with tab1:
    fig1 = px.histogram(
        filtered_df,
        x="year",
        y="available_slots",
        color="scholarship_scheme",
        title="Available Slots Over Time by Scheme",
        barmode="group",
    )
    fig1.update_layout(xaxis_title="Year", yaxis_title="Total Available Slots")
    st.plotly_chart(fig1, use_container_width=True)

    grouped = (
        filtered_df.groupby("year")
        .agg({"available_slots": "sum", "estimated_selected_students": "sum"})
        .reset_index()
    )
    fig2 = px.line(
        grouped,
        x="year",
        y=["available_slots", "estimated_selected_students"],
        title="Availability vs Estimated Selection",
        markers=True,
    )
    fig2.update_layout(yaxis_title="Number of Students", xaxis_title="Year")
    st.plotly_chart(fig2, use_container_width=True)

with tab2:
    state_counts = (
        filtered_df.groupby("university_state")["available_slots"].sum().reset_index()
    )
    fig3 = px.pie(
        state_counts,
        values="available_slots",
        names="university_state",
        title="Distribution of Slots by State",
        hole=0.4,
    )
    st.plotly_chart(fig3, use_container_width=True)

    c1, c2 = st.columns(2)
    with c1:
        univ_counts = (
            filtered_df.groupby("university_name")["available_slots"]
            .sum()
            .reset_index()
            .sort_values("available_slots", ascending=False)
            .head(10)
        )
        st.markdown("**Top 10 Universities (Table)**")
        st.dataframe(univ_counts, use_container_width=True, hide_index=True)
    with c2:
        fig4 = px.bar(
            univ_counts,
            x="available_slots",
            y="university_name",
            orientation="h",
            title="Top 10 Universities by Available Slots",
            color="available_slots",
        )
        fig4.update_layout(yaxis={"categoryorder": "total ascending"})
        st.plotly_chart(fig4, use_container_width=True)


with tab3:
    fig5 = px.sunburst(
        filtered_df,
        path=["course_level", "field_category", "course_name"],
        values="available_slots",
        title="Course Hierarchy Breakdown",
    )
    st.plotly_chart(fig5, use_container_width=True)
