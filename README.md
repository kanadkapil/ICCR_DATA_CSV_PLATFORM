# 🎓 Scholarship Data Research Dashboard

Welcome to the **Scholarship Data Research Dashboard**!

This interactive, fast, and feature-rich Streamlit application provides an intuitive way to explore, filter, and analyze large datasets of scholarship distributions across various academic offerings in India.

Built specifically for comprehensive data analysis and comparative research, the tool enables dynamic filtering and high-level analytical breakdowns using Plotly Express visual graphics.

---

## 🚀 Getting Started

### 1. Prerequisites

Ensure you have Python installed on your machine. You will also need to install the required libraries to run this project seamlessly:

```bash
pip install -r requirements.txt
```

_(The required packages are: `streamlit`, `pandas`, and `plotly`)_.

### 2. How to Run Locally

Once the dependencies are installed, you can start the dashboard on your local server. Open your terminal or powershell in the project folder and type:

```bash
python -m streamlit run app.py
```

This will start up a local server. If your browser does not open automatically, navigate to [http://localhost:8501](http://localhost:8501).

---

## 🔥 Features and Functionalities

The dashboard offers an immersive layout with dynamic features for detailed scholarship research.

### 🎛️ Interactive Filters

The left sidebar contains reactive filters to pinpoint exactly the data you want to investigate:

- **Year Range Slider:** A continuous slider allowing you to view and compare slot availability from a defined period (e.g., 2016-2025).
- **Scholarship Scheme Filter:** Refine queries based on specific funding types (e.g., Suborno Jayanti Scholarship, ICCR).
- **Geographical (State) Filter:** Analyze the allocation density across different regions like Delhi, Telangana, or West Bengal.
- **Academic Offering Filters (Course Level & Category):** Drill down to see slots given specifically to UG/PG/PhD or targeted to disciplines like STEM vs Business/Management.
- **University Search Bar:** An advanced multiple-selection dropdown enabling specific comparison across single or grouped institutions (e.g., comparing Banaras Hindu University with NIT's or University of Delhi).

---

### 📊 In-Depth Analytics (The 5-Tab Interface)

The center console is cleanly segmented by a tab interface offering 16 dynamic charts and analytics, built leveraging Plotly!

#### 📈 Tab 1: Trends over Time

1. **Histogram:** A breakdown of available slots distributed by scholarship scheme per year.
2. **Line Chart:** Tracks the growth/decline of Total "Available Slots" against "Estimated Selected Students" sequentially.
3. **Area Chart:** Visualizes exactly how slots trend over time strictly separated by their overarching Course Level.
4. **Heatmap:** Maps the density and growth of available slots inside specific Field Categories against particular years.

#### 🏢 Tab 2: University and State Breakdown

1. **State Distribution Pie:** A clean visualization depicting global slot allocations pieced by state.
2. **Top 10 University Bar Chart:** Instantly queries the top 10 ranked universities based on pure availability.
3. **Interactive Treemap:** Drill down dynamically from Top-Level State variables directly to nested University Types and Institution Names.
4. **Stacked Regional Bar:** Analyzes within the highest-ranking states their exact breakdown of University Types (Central vs State vs NIT).
5. **Box Plot:** Explores statistical variance, average spread, and extreme outlier capacities isolated by University Types.

#### 📚 Tab 3: Course Analysis

1. **Donut Proportions Chart:** Provides exact percent breakdown of allocations (e.g., UG vs PG vs PhD).
2. **Horizontal Specialization Chart:** Displays and compares exclusively the Top 10 academic specializations currently offered.
3. **Sunburst Diagram:** A massive interactive flowchart bridging down the hierarchy path from Course Path -> Field Category -> Specific Academic Names.
4. **Stacked Course Level Histogram:** Showcases exactly how many Course Levels exist across specific Field Categories.

#### 🔍 Tab 4: Advanced Institutional Metrics

1. **Hoverable Scatter Bubble Plot:** Maps raw selection numbers (Y) against pure availability (X), where the bubble size acts as availability and the color signifies Institutional Type!
2. **Selection Rate (%) Visualization:** Direct calculation graph breaking down theoretical Acceptance Chances / Selection Probabilities grouped specifically by the Field of Study applied for.

#### 🔮 Tab 5: Admission Predictor

1. **Interactive Profile Builder:** Input custom parameters such as CGPA, Work Experience, Publication History, and relevant Certifications to test application competitiveness against historically real data!
2. **Dynamic Waterfall Breakdown Chart:** Upon running a customized prediction query, a comprehensive Plotly bar chart is rendered tracking the positive or negative algorithmic impact values stemming from your individual profile stats.

---

### 📖 Data Expectations

By default, the application checks the root folder for `data2.csv`. If absent, it automatically defaults its research and calculations using the baseline `data.csv`. Both must follow a clear 14-column schematic (Year, Names, Type, Seats Available, Categories, etc.).

---

💻 **Developed by Kanad Kapil**
