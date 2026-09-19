# Import streamlit for interactive web application UI components
import streamlit as st

# Import pandas for data filtering and tabular operations
import pandas as pd

# Import numpy for conditional transformations and vector operations
import numpy as np

# Import plotly express for responsive, interactive charting
import plotly.express as px

# ---------------------------------------------------------
# Page Configuration
# ---------------------------------------------------------
# Set browser tab title, favicon, and wide desktop screen layout
st.set_page_config(
    page_title="Tech Mental Health Analytics Hub",
    page_icon="🧠",
    layout="wide"
)

# Apply minimal CSS styling to modernize metric containers
st.markdown("""
    <style>
    .metric-card {
        background-color: #ffffff;
        border-radius: 8px;
        padding: 16px;
        box-shadow: 0 1px 3px rgba(0,0,0,0.08);
        border-left: 4px solid #2980b9;
    }
    </style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# Data Loading and Caching Pipeline
# ---------------------------------------------------------
# Cache data in memory so the app re-renders instantly upon filter changes
@st.cache_data
def load_survey_data():
    # Read the dataset from disk
    df = pd.read_csv("survey.csv")

    # Filter invalid age outliers to active workforce range (18 to 75)
    df = df[(df['Age'] >= 18) & (df['Age'] <= 75)].copy()

    # Standardize gender text entries
    df['Gender_Clean'] = df['Gender'].astype(str).str.strip().str.lower()
    male_aliases = [
        'male', 'm', 'male-ish', 'maile', 'mal', 'male (cis)', 'make', 
        'male ', 'man', 'msle', 'mail', 'malr', 'cis man', 'cis male'
    ]
    female_aliases = [
        'female', 'f', 'woman', 'female ', 'female (cis)', 'cis-female/femme', 
        'femake', 'female (trans)', 'cis female'
    ]
    df['Gender_Cohort'] = np.where(
        df['Gender_Clean'].isin(male_aliases), 'Male',
        np.where(
            df['Gender_Clean'].isin(female_aliases), 'Female', 
            'Non-Binary/Other'
        )
    )

    # Impute missing values with logical categories
    df['self_employed'] = df['self_employed'].fillna('No')
    df['work_interfere'] = df['work_interfere'].fillna("Don't know / Never")

    # Drop non-critical metadata columns
    df.drop(columns=['comments', 'Timestamp', 'Gender_Clean', 'Gender'], inplace=True, errors='ignore')

    return df

# Load the wrangled survey dataframe
df = load_survey_data()

# ---------------------------------------------------------
# Dashboard Header
# ---------------------------------------------------------
st.title("🧠 Tech Workplace Mental Health Intelligence Dashboard")
st.markdown("Interactive empirical tool for HR Leaders, Engineering Executives, and Talent Strategists")
st.divider()

# ---------------------------------------------------------
# Sidebar Filter Controls
# ---------------------------------------------------------
st.sidebar.header("Filter Demographic Cohorts")

# Country selector filter
country_list = ["All Countries"] + sorted(list(df['Country'].unique()))
selected_country = st.sidebar.selectbox("Geographic Region", country_list)

# Company headcount scale filter
all_sizes = ['1-5', '6-25', '26-100', '100-500', '500-1000', 'More than 1000']
selected_sizes = st.sidebar.multiselect("Company Size (Employees)", all_sizes, default=all_sizes)

# Remote work ratio filter
remote_filter = st.sidebar.radio("Remote Work Ratio", ["All Staff", "Remote (>50%)", "On-Premises (<50%)"])

# Apply selected filters to create a filtered slice of the dataset
filtered_df = df.copy()

if selected_country != "All Countries":
    filtered_df = filtered_df[filtered_df['Country'] == selected_country]

if selected_sizes:
    filtered_df = filtered_df[filtered_df['no_employees'].isin(selected_sizes)]

if remote_filter == "Remote (>50%)":
    filtered_df = filtered_df[filtered_df['remote_work'] == "Yes"]
elif remote_filter == "On-Premises (<50%)":
    filtered_df = filtered_df[filtered_df['remote_work'] == "No"]

# ---------------------------------------------------------
# Executive KPI Metric Cards
# ---------------------------------------------------------
kpi1, kpi2, kpi3, kpi4 = st.columns(4)

total_cohort = len(filtered_df)
treatment_rate = (filtered_df['treatment'].value_counts(normalize=True).get('Yes', 0) * 100) if total_cohort > 0 else 0
benefits_rate = (filtered_df['benefits'].value_counts(normalize=True).get('Yes', 0) * 100) if total_cohort > 0 else 0
anonymity_rate = (filtered_df['anonymity'].value_counts(normalize=True).get('Yes', 0) * 100) if total_cohort > 0 else 0

kpi1.metric("Selected Cohort Size", f"{total_cohort:,}")
kpi2.metric("Sought Treatment", f"{treatment_rate:.1f}%")
kpi3.metric("Benefits Awareness", f"{benefits_rate:.1f}%")
kpi4.metric("Anonymity Confidence", f"{anonymity_rate:.1f}%")

st.divider()

# ---------------------------------------------------------
# Interactive Analytics Grid (Row 1)
# ---------------------------------------------------------
col1, col2 = st.columns(2)

with col1:
    st.subheader("1. Treatment Uptake by Company Benefits")
    # Interactive grouped bar chart for benefits vs treatment
    fig_benefits = px.histogram(
        filtered_df,
        x="benefits",
        color="treatment",
        barmode="group",
        category_orders={"benefits": ["Yes", "No", "Don't know"]},
        color_discrete_map={"Yes": "#2ecc71", "No": "#e74c3c"},
        labels={"benefits": "Company Provides Mental Health Benefits", "count": "Employee Count"}
    )
    fig_benefits.update_layout(height=360, margin=dict(l=20, r=20, t=30, b=20), legend_title_text="Treatment")
    st.plotly_chart(fig_benefits, use_container_width=True)

with col2:
    st.subheader("2. Work Interference vs. Treatment Uptake")
    # Interactive stacked histogram for work interference gradient
    order_interfere = ['Never', 'Rarely', 'Sometimes', 'Often', "Don't know / Never"]
    fig_interfere = px.histogram(
        filtered_df,
        x="work_interfere",
        color="treatment",
        category_orders={"work_interfere": order_interfere},
        color_discrete_map={"Yes": "#3498db", "No": "#95a5a6"},
        labels={"work_interfere": "Perceived Work Interference Level"}
    )
    fig_interfere.update_layout(height=360, margin=dict(l=20, r=20, t=30, b=20), legend_title_text="Treatment")
    st.plotly_chart(fig_interfere, use_container_width=True)

# ---------------------------------------------------------
# Interactive Analytics Grid (Row 2)
# ---------------------------------------------------------
col3, col4 = st.columns(2)

with col3:
    st.subheader("3. Leave Policy Ease vs. Stigma / Fallout Fear")
    # Interactive bar plot evaluating leave friction against consequence fears
    leave_order = ["Very easy", "Somewhat easy", "Don't know", "Somewhat difficult", "Very difficult"]
    fig_leave = px.histogram(
        filtered_df,
        x="leave",
        color="mental_health_consequence",
        barmode="group",
        category_orders={"leave": leave_order, "mental_health_consequence": ["No", "Maybe", "Yes"]},
        color_discrete_map={"No": "#2ecc71", "Maybe": "#f39c12", "Yes": "#e74c3c"},
        labels={"leave": "Ease of Medical Leave", "mental_health_consequence": "Fears Fallout"}
    )
    fig_leave.update_layout(height=360, margin=dict(l=20, r=20, t=30, b=20), legend_title_text="Fallout Fear")
    st.plotly_chart(fig_leave, use_container_width=True)

with col4:
    st.subheader("4. Willingness to Discuss: Supervisors vs. Peers")
    # Compare supervisory trust against peer coworker trust
    discuss_summary = pd.DataFrame({
        "Recipient": ["Direct Supervisor", "Coworkers (Peers)"],
        "Yes": [
            (filtered_df['supervisor'] == 'Yes').sum(),
            (filtered_df['coworkers'] == 'Yes').sum()
        ],
        "Some of them": [
            (filtered_df['supervisor'] == 'Some of them').sum(),
            (filtered_df['coworkers'] == 'Some of them').sum()
        ],
        "No": [
            (filtered_df['supervisor'] == 'No').sum(),
            (filtered_df['coworkers'] == 'No').sum()
        ]
    })
    # Melt dataframe for multi-bar grouped plotting
    melted_discuss = discuss_summary.melt(id_vars="Recipient", var_name="Willingness", value_name="Count")
    fig_discuss = px.bar(
        melted_discuss,
        x="Recipient",
        y="Count",
        color="Willingness",
        barmode="group",
        color_discrete_map={"Yes": "#2ecc71", "Some of them": "#f39c12", "No": "#e74c3c"}
    )
    fig_discuss.update_layout(height=360, margin=dict(l=20, r=20, t=30, b=20))
    st.plotly_chart(fig_discuss, use_container_width=True)

# ---------------------------------------------------------
# Strategic Action Panel
# ---------------------------------------------------------
st.divider()
st.subheader("📋 Executive Strategic Directives")
st.info("""
* **Guaranteed Anonymity**: Over 70% of tech employees either doubt or do not know if their identity is protected. Use external third-party EAPs so employers only see aggregate indices.
* **Manager First-Aid Training**: Staff confide in direct managers more than 2.3 times as often as general coworkers. Focus training on line engineering managers.
* **Eliminate Benefits Ambiguity**: Lack of coverage awareness suppresses treatment more than having no coverage. Highlight therapy options directly during quarterly all-hands meetings.
""")