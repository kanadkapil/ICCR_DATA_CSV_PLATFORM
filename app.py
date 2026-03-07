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

tab1, tab2, tab3, tab4, tab5 = st.tabs(
    [
        "📈 Trends over Time",
        "🏢 University Breakdown",
        "📚 Course Analysis",
        "🔍 Advanced Comparisons",
        "🔮 Admission Predictor",
    ]
)

with tab1:
    st.markdown("### Slot Availability and Trend Analysis")
    c1, c2 = st.columns(2)
    with c1:
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

    with c2:
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

    c3, c4 = st.columns(2)
    with c3:
        # New Graph 1: Area Chart
        grouped_level_yr = (
            filtered_df.groupby(["year", "course_level"])["available_slots"]
            .sum()
            .reset_index()
        )
        fig_area_level = px.area(
            grouped_level_yr,
            x="year",
            y="available_slots",
            color="course_level",
            title="Available Slots Trend by Course Level",
        )
        st.plotly_chart(fig_area_level, use_container_width=True)
    with c4:
        # New Graph 2: Heatmap
        grouped_yr_cat = (
            filtered_df.groupby(["year", "field_category"])["available_slots"]
            .sum()
            .reset_index()
        )
        fig_heatmap_yr_cat = px.density_heatmap(
            grouped_yr_cat,
            x="year",
            y="field_category",
            z="available_slots",
            title="Density: Slots over Time by Field",
            histfunc="sum",
        )
        st.plotly_chart(fig_heatmap_yr_cat, use_container_width=True)

with tab2:
    st.markdown("### Regional and Institutional Distribution")
    c1, c2 = st.columns(2)
    with c1:
        state_counts = (
            filtered_df.groupby("university_state")["available_slots"]
            .sum()
            .reset_index()
        )
        fig3 = px.pie(
            state_counts,
            values="available_slots",
            names="university_state",
            title="Distribution of Slots by State",
            hole=0.4,
        )
        st.plotly_chart(fig3, use_container_width=True)
    with c2:
        univ_counts = (
            filtered_df.groupby("university_name")["available_slots"]
            .sum()
            .reset_index()
            .sort_values("available_slots", ascending=False)
            .head(10)
        )
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

    # New Graph 3: Treemap
    fig_treemap = px.treemap(
        filtered_df,
        path=[
            px.Constant("All States"),
            "university_state",
            "university_type",
            "university_name",
        ],
        values="available_slots",
        title="Hierarchical view of Slots by State and University Type",
    )
    st.plotly_chart(fig_treemap, use_container_width=True)

    c3, c4 = st.columns(2)
    with c3:
        # New Graph 4: Stacked Bar
        top_states = (
            filtered_df.groupby("university_state")["available_slots"]
            .sum()
            .nlargest(5)
            .index
        )
        df_top_states = filtered_df[filtered_df["university_state"].isin(top_states)]
        grouped_state_type = (
            df_top_states.groupby(["university_state", "university_type"])[
                "available_slots"
            ]
            .sum()
            .reset_index()
        )
        fig_stacked_state_type = px.bar(
            grouped_state_type,
            x="university_state",
            y="available_slots",
            color="university_type",
            title="University Types in Top 5 States",
        )
        st.plotly_chart(fig_stacked_state_type, use_container_width=True)
    with c4:
        # New Graph 5: Box Plot
        fig_box_univ_type = px.box(
            filtered_df,
            x="university_type",
            y="available_slots",
            color="university_type",
            title="Spread of Slot Sizes by University Type",
        )
        st.plotly_chart(fig_box_univ_type, use_container_width=True)

with tab3:
    st.markdown("### Academic Offerings Breakdown")
    c1, c2 = st.columns(2)
    with c1:
        # New Graph 6: Donut Pie Chart
        grouped_level = (
            filtered_df.groupby("course_level")["available_slots"].sum().reset_index()
        )
        fig_pie_level = px.pie(
            grouped_level,
            values="available_slots",
            names="course_level",
            hole=0.5,
            title="Slots Proportion by Course Level",
        )
        st.plotly_chart(fig_pie_level, use_container_width=True)
    with c2:
        # New Graph 7: Horizontal Bar Chart
        top_spec = (
            filtered_df.groupby("specialization")["available_slots"]
            .sum()
            .reset_index()
            .sort_values("available_slots", ascending=False)
            .head(10)
        )
        fig_bar_spec = px.bar(
            top_spec,
            x="available_slots",
            y="specialization",
            orientation="h",
            color="available_slots",
            title="Top 10 Specializations",
        )
        fig_bar_spec.update_layout(yaxis={"categoryorder": "total ascending"})
        st.plotly_chart(fig_bar_spec, use_container_width=True)

    c3, c4 = st.columns(2)
    with c3:
        fig5 = px.sunburst(
            filtered_df,
            path=["course_level", "field_category", "course_name"],
            values="available_slots",
            title="Course Hierarchy Breakdown",
        )
        st.plotly_chart(fig5, use_container_width=True)
    with c4:
        # New Graph 8: Stacked Histogram
        grouped_cat_level = (
            filtered_df.groupby(["field_category", "course_level"])["available_slots"]
            .sum()
            .reset_index()
        )
        fig_hist_cat_level = px.bar(
            grouped_cat_level,
            x="field_category",
            y="available_slots",
            color="course_level",
            title="Field Category across Course Levels",
            barmode="stack",
        )
        st.plotly_chart(fig_hist_cat_level, use_container_width=True)

with tab4:
    st.markdown("### Institutional Comparisons & Metrics")
    c1, c2 = st.columns(2)
    with c1:
        # New Graph 9: Scatter Plot
        grouped_univ = (
            filtered_df.groupby(["university_name", "university_type"])
            .agg({"available_slots": "sum", "estimated_selected_students": "sum"})
            .reset_index()
        )
        fig_scatter_univ = px.scatter(
            grouped_univ,
            x="available_slots",
            y="estimated_selected_students",
            color="university_type",
            hover_name="university_name",
            size="available_slots",
            title="Availability vs Expected Selection Location",
        )
        st.plotly_chart(fig_scatter_univ, use_container_width=True)
    with c2:
        # New Graph 10: Selection Rate Bar
        grouped_cat_sel = (
            filtered_df.groupby("field_category")
            .agg({"available_slots": "sum", "estimated_selected_students": "sum"})
            .reset_index()
        )
        # Ensure no division by zero
        grouped_cat_sel = grouped_cat_sel[grouped_cat_sel["available_slots"] > 0]
        grouped_cat_sel["selection_rate"] = (
            grouped_cat_sel["estimated_selected_students"]
            / grouped_cat_sel["available_slots"]
        ) * 100
        fig_bar_selection_rate = px.bar(
            grouped_cat_sel,
            x="field_category",
            y="selection_rate",
            color="selection_rate",
            title="Avg Selection Rate (%) by Field Category",
        )
        st.plotly_chart(fig_bar_selection_rate, use_container_width=True)

with tab5:
    st.markdown("### 🔮 Scholarship Admission Predictor")
    st.markdown(
        "Estimate your chances of getting admitted based on historical selection data, your academic profile, and the university competitiveness."
    )

    with st.expander("📝 Fill out your profile", expanded=True):
        col_form1, col_form2 = st.columns(2)

        with col_form1:
            user_cgpa = st.number_input(
                "Your CGPA (out of 10.0)",
                min_value=0.0,
                max_value=10.0,
                value=8.0,
                step=0.1,
            )
            user_course_lvl = st.selectbox(
                "Target Course Level",
                options=sorted(df["course_level"].dropna().unique().tolist()),
            )
            user_exp = st.number_input(
                "Years of Work/Research Experience",
                min_value=0,
                max_value=20,
                value=0,
                step=1,
            )

        with col_form2:
            target_university = st.selectbox(
                "Target University",
                options=sorted(df["university_name"].dropna().unique().tolist()),
            )
            user_publications = st.number_input(
                "Number of Publications (if any)",
                min_value=0,
                max_value=50,
                value=0,
                step=1,
            )
            is_language_cert = st.checkbox("Have IELTS/TOEFL Certification?")

    if st.button("Predict Admission Chances", type="primary"):
        # Get historical data for the selected university and course level
        history_df = df[
            (df["university_name"] == target_university)
            & (df["course_level"] == user_course_lvl)
        ]

        if len(history_df) == 0:
            st.warning(
                "Insufficient historical data for this specific University + Course Level combination. Showing a general estimate instead."
            )
            history_df = df[df["university_name"] == target_university]

        if len(history_df) == 0:
            history_df = df  # Fallback to global

        # Calculate base acceptance rate from historical stats
        total_slots = history_df["available_slots"].sum()
        total_selected = history_df["estimated_selected_students"].sum()

        base_rate = (total_selected / total_slots) if total_slots > 0 else 0.5

        # Modifier limits (Algorithm simulated for estimations)
        cgpa_mod = (user_cgpa - 7.5) * 0.1  # If cgpa is 9.5 -> +20%, if 6.0 -> -15%
        exp_mod = min(user_exp * 0.02, 0.10)  # Up to 10% boost for experience
        pub_mod = min(
            user_publications * 0.03, 0.15
        )  # Up to 15% boost for publications
        cert_mod = 0.05 if is_language_cert else 0.0  # 5% boost for language cert

        final_probability = base_rate + cgpa_mod + exp_mod + pub_mod + cert_mod

        # Enforce bounds [5%, 95%]
        final_probability = max(0.05, min(0.95, final_probability))

        # Display Results
        st.divider()
        st.subheader("Results")

        res_col1, res_col2 = st.columns([1, 2])

        with res_col1:
            st.metric(
                "Estimated Admission Probability", f"{final_probability * 100:.1f}%"
            )
            if final_probability >= 0.75:
                st.success("Excellent Chances! You have a highly competitive profile.")
            elif final_probability >= 0.50:
                st.info("Good Chances. You are well within the running.")
            elif final_probability >= 0.30:
                st.warning(
                    "Fair Chances. Consider improving your profile or adding backup universities."
                )
            else:
                st.error(
                    "Low Chances. This is a highly competitive track for your current profile."
                )

        with res_col2:
            st.markdown("#### Probability Factors")
            factors = pd.DataFrame(
                {
                    "Factor": [
                        "Historical Acceptance Base",
                        "CGPA Impact",
                        "Experience Bonus",
                        "Publications Bonus",
                        "Certifications Bonus",
                    ],
                    "Impact": [base_rate, cgpa_mod, exp_mod, pub_mod, cert_mod],
                }
            )
            # Filter zero/negative impacts out conditionally or just show them
            fig_factors = px.bar(
                factors,
                x="Factor",
                y="Impact",
                title="How Your Profile Influences Admission Chances",
                text=[f"{v * 100:+.1f}%" for v in factors["Impact"]],
                color="Factor",
            )
            fig_factors.update_layout(showlegend=False)
            st.plotly_chart(fig_factors, use_container_width=True)

        st.caption(
            "Note: This is a simulated algorithmic prediction built for research and planning purposes. Actual admission decisions are made by university committees based on comprehensive profile reviews and available seats."
        )


st.divider()
st.markdown(
    "<div style='text-align: center; color: gray;'>"
    "Developed by <b>Kanad Kapil</b><br>"
    "GitHub: <a href='https://github.com/kanadkapil' target='_blank'>github.com/kanadkapil</a>"
    "</div>",
    unsafe_allow_html=True,
)
