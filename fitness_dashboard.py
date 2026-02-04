import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta
import numpy as np
from pandas import Categorical


# Page configuration with custom styling
st.set_page_config(
    page_title="Fitness Tracker",
    page_icon="🏃‍♀️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;600;700;900&family=IBM+Plex+Sans:wght@300;400;500;600&display=swap');
    
    /* Root variables for cohesive theming */
    :root {
        --primary: #2E86AB;
        --secondary: #A23B72;
        --accent: #F18F01;
        --success: #06A77D;
        --warning: #D4AF37;
        --danger: #C73E1D;
        --dark: #2C3E50;
        --medium: #5D6D7E;
        --light: #ECF0F1;
        --bg: #FFFFFF;
    }
    
    /* Main container styling */
    .stApp {
        background: #F5F7FA;
    }
    
    .main .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
        background: #FFFFFF;
        border-radius: 12px;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
    }
    
    /* Typography - Clean Professional Style */
    h1, h2, h3 {
        font-family: 'Playfair Display', serif !important;
        font-weight: 700 !important;
        letter-spacing: -0.01em !important;
        line-height: 1.2 !important;
    }
    
    h1 {
        font-size: 2rem !important;
        color: var(--dark) !important;
        margin-bottom: 0.5rem !important;
        animation: fadeInDown 0.8s ease-out;
    }
    
    h2 {
        font-size: 1.75rem !important;
        color: var(--dark) !important;
        padding-left: 1rem;
        margin-top: 2rem !important;
        margin-bottom: 1rem !important;
        animation: slideInLeft 0.6s ease-out;
    }
    
    h3 {
        font-size: 1.3rem !important;
        color: var(--dark) !important;
        font-weight: 600 !important;
    }
    
    p, .stMarkdown, div {
        font-family: 'IBM Plex Sans', sans-serif !important;
        font-size: 1rem !important;
        line-height: 1.6 !important;
        color: var(--dark) !important;
    }
    
    /* Metric cards with better visibility */
    [data-testid="stMetricValue"] {
        font-family: 'Playfair Display', serif !important;
        font-size: 2.5rem !important;
        font-weight: 700 !important;
        color: var(--primary) !important;
    }
    
    [data-testid="stMetricLabel"] {
        font-family: 'IBM Plex Sans', sans-serif !important;
        font-size: 0.85rem !important;
        font-weight: 600 !important;
        text-transform: uppercase;
        letter-spacing: 0.08em;
        color: var(--medium) !important;
    }
    
    [data-testid="stMetricDelta"] {
        font-size: 0.9rem !important;
        color: var(--medium) !important;
    }
    
    /* Sidebar styling */
    [data-testid="stSidebar"] {
        background: #2C3E50;
        padding: 2rem 1rem;
    }

    
    [data-testid="stSidebar"] label {
    color: #000000 !important;  /* White labels */
    font-weight: 500 !important;
    }
    
    [data-testid="stSidebar"] h1, 
    [data-testid="stSidebar"] h2, 
    [data-testid="stSidebar"] h3 {
        color: #FFFFFF !important;
    }
    
    .stNumberInput label, .stDateInput label {
        color: #ECF0F1 !important;
        font-weight: 500 !important;
    }
    
    
    [data-testid="stSidebar"] [role="option"] {
        color: #2C3E50 !important;
        background: #FFFFFF !important;
    }

    [data-testid="stSidebar"] [role="option"]:hover {
        background: #ECF0F1 !important;
        color: #2C3E50 !important;
    }
    

    [data-testid="stSidebar"] input {
        color: #2C3E50 !important;  /* Dark text */
        background: #FFFFFF !important;  /* White background */
        font-weight: 600 !important;
        border: 2px solid #ECF0F1 !important;
    }

    [data-testid="stSidebar"] input:focus {
        border-color: #2E86AB !important;  /* Blue border on focus */
        box-shadow: 0 0 0 2px rgba(46, 134, 171, 0.2) !important;
    }

    [data-testid="stSidebar"] .stSelectbox > div > div,
    [data-testid="stSidebar"] .stMultiSelect > div > div {
        background: #FFFFFF !important;
        color: #2C3E50 !important;
        font-weight: 500 !important;
    }
    
    [data-testid="stSidebar"] label {
        color: #ECF0F1 !important;
        font-weight: 500 !important;
    }
    
    /* Buttons with hover effects */
    .stButton > button {
        font-family: 'IBM Plex Sans', sans-serif !important;
        font-weight: 600 !important;
        text-transform: uppercase;
        letter-spacing: 0.08em;
        border-radius: 8px;
        padding: 0.75rem 2rem;
        background: var(--primary);
        border: 2px solid var(--primary);
        color: white !important;
        transition: all 0.3s ease;
        box-shadow: 0 2px 8px rgba(46, 134, 171, 0.3);
    }
    
    [data-testid="stSidebar"] [role="option"] {
        color: #2C3E50 !important;
    }
    
    .stButton > button:hover {
        background: #236B8E;
        border-color: #236B8E;
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(46, 134, 171, 0.4);
    }
    
    /* Selectbox and inputs */
    .stSelectbox, .stMultiSelect {
        font-family: 'IBM Plex Sans', sans-serif !important;
    }
    
    .stSelectbox label, .stMultiSelect label {
        color: var(--dark) !important;
        font-weight: 500 !important;
    }
    
    /* Custom info boxes */
    .insight-box {
        background: linear-gradient(135deg, rgba(46, 134, 171, 0.08), rgba(162, 59, 114, 0.08));
        border-left: 4px solid var(--primary);
        padding: 1.5rem;
        border-radius: 8px;
        margin: 1rem 0;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.06);
        animation: fadeIn 0.5s ease-out;
    }
    
    .insight-box h3, .insight-box h4 {
        color: var(--dark) !important;
        margin-top: 0 !important;
    }
    
    .insight-box p {
        color: var(--dark) !important;
        margin-bottom: 0.5rem !important;
    }
    
    .goal-progress {
        background: #FFFFFF;
        border-radius: 10px;
        padding: 1.5rem;
        box-shadow: 0 2px 12px rgba(0, 0, 0, 0.08);
        margin: 1rem 0;
        border: 2px solid #E8ECF1;
        transition: all 0.3s ease;
    }
    
    .goal-progress:hover {
        transform: translateY(-3px);
        box-shadow: 0 4px 16px rgba(0, 0, 0, 0.12);
        border-color: var(--primary);
    }
    
    .goal-progress h3 {
        color: var(--dark) !important;
        margin-top: 0 !important;
        font-size: 1.1rem !important;
    }
    
    .goal-progress p {
        color: var(--dark) !important;
        font-size: 1rem !important;
    }
    
    .goal-progress strong {
        color: var(--primary) !important;
    }
    
    /* Animations */
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(20px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    @keyframes fadeInDown {
        from { opacity: 0; transform: translateY(-20px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    @keyframes slideInLeft {
        from { opacity: 0; transform: translateX(-20px); }
        to { opacity: 1; transform: translateX(0); }
    }
    
    /* Plotly chart containers */
    .js-plotly-plot {
        border-radius: 8px;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.06);
        overflow: hidden;
        background: white;
    }
    
    /* Progress bars */
    .stProgress > div > div > div {
        background: var(--primary);
        border-radius: 8px;
    }
    
    /* Tabs */
    .stTabs [data-baseweb="tab-list"] {
        gap: 1.5rem;
        border-bottom: 2px solid #E8ECF1;
    }
    
    .stTabs [data-baseweb="tab"] {
        font-family: 'IBM Plex Sans', sans-serif !important;
        font-weight: 600 !important;
        text-transform: uppercase;
        letter-spacing: 0.08em;
        font-size: 0.85rem !important;
        padding: 1rem 1.5rem;
        color: var(--medium);
        border-radius: 8px 8px 0 0;
    }
    
    .stTabs [aria-selected="true"] {
        color: var(--primary) !important;
        background: rgba(46, 134, 171, 0.05);
        border-bottom: 3px solid var(--primary);
    }
    
    /* Number inputs and date inputs */
    .stNumberInput label, .stDateInput label {
        color: #ECF0F1 !important;
        font-weight: 500 !important;
    }
    
    /* Divider */
    hr {
        border-color: #E8ECF1 !important;
        margin: 2rem 0 !important;
    }
</style>
""", unsafe_allow_html=True)

# Generate sample data
@st.cache_data
def generate_sample_data():
    """Generate realistic fitness data for demonstration"""
    np.random.seed(42)
    
    # Date range - last 8 weeks for better analysis
    end_date = datetime.now()
    start_date = end_date - timedelta(days=56)
    dates = pd.date_range(start=start_date, end=end_date, freq='D')
    
    activities = ['Running', 'Pilates', 'Cycling', 'HIIT', 'Yoga', 'Swimming', 'Strength Training']
    times_of_day = ['Morning', 'Afternoon', 'Evening']
    
    data = []
    
    for date in dates:
        # 70% chance of workout on any given day
        if np.random.random() < 0.7:
            # Sometimes do multiple activities per day
            num_activities = np.random.choice([1, 2], p=[0.8, 0.2])
            
            for _ in range(num_activities):
                activity = np.random.choice(activities, p=[0.25, 0.15, 0.20, 0.10, 0.15, 0.05, 0.10])
                
                # Activity-specific duration and calories
                if activity == 'Running':
                    duration = np.random.randint(25, 65)
                    calories = duration * np.random.uniform(9, 12)
                elif activity == 'Pilates':
                    duration = np.random.randint(45, 75)
                    calories = duration * np.random.uniform(3, 5)
                elif activity == 'Cycling':
                    duration = np.random.randint(30, 90)
                    calories = duration * np.random.uniform(7, 10)
                elif activity == 'HIIT':
                    duration = np.random.randint(20, 45)
                    calories = duration * np.random.uniform(10, 14)
                elif activity == 'Yoga':
                    duration = np.random.randint(30, 75)
                    calories = duration * np.random.uniform(2, 4)
                elif activity == 'Swimming':
                    duration = np.random.randint(30, 60)
                    calories = duration * np.random.uniform(8, 11)
                else:  # Strength Training
                    duration = np.random.randint(40, 75)
                    calories = duration * np.random.uniform(5, 8)
                
                time_of_day = np.random.choice(times_of_day, p=[0.3, 0.3, 0.4])
                
                data.append({
                    'date': date,
                    'activity': activity,
                    'duration': int(duration),
                    'calories': int(calories),
                    'time_of_day': time_of_day,
                    'day_of_week': date.strftime('%A'),
                    'week_number': date.isocalendar()[1],
                    'heart_rate_avg': np.random.randint(120, 170),
                    'intensity': np.random.choice(['Low', 'Moderate', 'High'], p=[0.2, 0.5, 0.3])
                })
    
    df = pd.DataFrame(data)
    df['date'] = pd.to_datetime(df['date'])
    return df

# Load fake data
df = generate_sample_data()

# To load the real data

@st.cache_data
def load_data():
    data = []
    
    # Read CSV and process each row
    df_raw = pd.read_csv('fitness_data.csv')
    
    for _, row in df_raw.iterrows():
        date = pd.to_datetime(row['date'])
        data.append({
            'date': date,
            'activity': row['activity'],
            'duration': int(row['duration']),
            'calories': int(row['calories']),
            'time_of_day': row['time_of_day'],
            'day_of_week': date.strftime('%A'),
            'week_number': date.isocalendar()[1],
            'heart_rate_avg': np.random.randint(120, 170),
            'intensity': np.random.choice(['Low', 'Moderate', 'High'], p=[0.2, 0.5, 0.3])
        })
    
    df = pd.DataFrame(data)
    df['date'] = pd.to_datetime(df['date'])
    return df

#df = load_data()

# Sidebar - Filters and Settings
with st.sidebar:
    st.markdown("# Filters")
    st.markdown("---")
    
    # Date range filter
    st.markdown("### Time Period")
    date_range = st.selectbox(
        "Select View",
        ["Last 7 Days", "Last 14 Days", "Last 30 Days", "Last 8 Weeks", "Custom Range"],
        index=0
    )
    
    if date_range == "Custom Range":
        col1, col2 = st.columns(2)
        with col1:
            start_date = st.date_input("From", df['date'].min())
        with col2:
            end_date = st.date_input("To", df['date'].max())
    else:
        days_map = {
            "Last 7 Days": 7,
            "Last 14 Days": 14,
            "Last 30 Days": 30,
            "Last 8 Weeks": 56
        }
        days = days_map[date_range]
        end_date = df['date'].max()
        start_date = end_date - timedelta(days=days)
    
    # Filter dataframe
    df_filtered = df[(df['date'] >= pd.Timestamp(start_date)) & (df['date'] <= pd.Timestamp(end_date))]
    
    st.markdown("---")
    
    # Activity filter
    st.markdown("### Activity Types")
    all_activities = df['activity'].unique().tolist()
    selected_activities = st.multiselect(
        "Filter by Activity",
        all_activities,
        default=all_activities
    )
    
    df_filtered = df_filtered[df_filtered['activity'].isin(selected_activities)]
    
    st.markdown("---")
    
    # Goal settings
    st.markdown("### Weekly Goals")
    weekly_calorie_goal = st.number_input("Calories per Week", min_value=500, max_value=5000, value=2000, step=100)
    weekly_workout_goal = st.number_input("Workouts per Week", min_value=1, max_value=7, value=5, step=1)
    
    st.markdown("---")

# Main dashboard
st.markdown("""
<div style='
    text-align: center;
     background: linear-gradient(rgba(100, 181, 246, 0.75), rgba(144, 202, 249, 0.75)), 
                url("https://images.unsplash.com/photo-1534438327276-14e5300c3a48?w=1200") center/cover;
    border-radius: 4px;
    margin-bottom: 1.5rem;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.15);
    padding: 2rem 1rem;
'>
    <h1 style='
        font-family: "Playfair Display", serif;
        font-size: 3.5rem;
        font-weight: 700;
        color: white;
        margin-bottom: 0.5rem;
        text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.3);
    '>Personal Fitness</h1>
    <h3 style='
        font-family: "IBM Plex Sans", sans-serif;
        font-size: 1.2rem;
        font-weight: 400;
        color: white;
        margin-top: 0;
        text-shadow: 1px 1px 2px rgba(0, 0, 0, 0.3);
    '>A look into your health journey</h3>
</div>
""", unsafe_allow_html=True)

# Check if the data exists
if df_filtered.empty:
    st.warning("⚠️ No data available for the selected filters. Please adjust your date range or activity selection.")
    st.stop()

# Calculate key metrics
total_workouts = len(df_filtered)
total_calories = df_filtered['calories'].sum()
total_duration = df_filtered['duration'].sum()
avg_calories_per_workout = total_calories / total_workouts if total_workouts > 0 else 0
unique_days = df_filtered['date'].nunique()
consistency_rate = (unique_days / ((end_date - start_date).days)) * 100

# Calculate weekly averages
weeks_in_range = ((end_date - start_date).days + 1) / 7
weekly_avg_workouts = total_workouts / weeks_in_range
weekly_avg_calories = total_calories / weeks_in_range


# Weekly goal progress section
st.markdown("## 🎯 Weekly Goal Progress")

# Calculate current week progress
current_week = df_filtered[df_filtered['week_number'] == df_filtered['date'].max().isocalendar()[1]]
current_week_calories = current_week['calories'].sum()
current_week_workouts = len(current_week)

col1, col2 = st.columns(2)

with col1:
    # Calorie progress
    calorie_progress = min(current_week_calories / weekly_calorie_goal * 100, 100)
    remaining_calories = max(weekly_calorie_goal - current_week_calories, 0)
    
    # Determine status color and message
    if calorie_progress < 50:
        status_color = "#C73E1D"
        status_text = "Behind"
        status_emoji = "🔴"
    elif calorie_progress < 80:
        status_color = "#F18F01"
        status_text = "Close"
        status_emoji = "🟡"
    else:
        status_color = "#06A77D"
        status_text = "On Track"
        status_emoji = "🟢"
    
    st.markdown(f"""
    <div style="background-color: white; padding: 1rem; border-radius: 10px; border-left: 5px solid {status_color};">
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.5rem;">
            <h3 style="margin: 0; color: #2C3E50; font-size: 2rem;">🔥 Calorie Goal</h3>
            <span style="background-color: {status_color}; color: white; padding: 0.25rem 0.75rem; border-radius: 20px; font-size: 0.85rem; font-weight: 600;">
                {status_emoji} {status_text}
            </span>
        </div>
        <div style="display: flex; justify-content: space-between; align-items: baseline; margin-bottom: 0.75rem;">
            <span style="font-size: 2rem; font-weight: 700; color: {status_color};">{int(current_week_calories):,}</span>
            <span style="font-size: 1.2rem; color: #5D6D7E;">/ {weekly_calorie_goal:,} cal</span>
        </div>
        <div style="background-color: #E8ECF1; border-radius: 10px; height: 24px; width: 100%; overflow: hidden; position: relative;">
            <div style="background: linear-gradient(90deg, {status_color}, {status_color}dd); height: 100%; width: {calorie_progress}%; transition: width 0.5s ease; border-radius: 10px; box-shadow: inset 0 2px 4px rgba(0,0,0,0.1);"></div>
            <span style="position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%); color: #2C3E50; font-weight: 600; font-size: 0.85rem;">
                {int(calorie_progress)}%
            </span>
        </div>
        <p style="margin-top: 0.75rem; margin-bottom: 0; color: #5D6D7E; font-size: 0.95rem;">
            {f"<strong style='color: {status_color};'>{int(remaining_calories)} calories</strong> remaining this week" if remaining_calories > 0 else "<strong style='color: #06A77D;'>🎉 Goal achieved!</strong> Keep up the amazing work!"}
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

with col2:
    # Workout frequency progress
    workout_progress = min(current_week_workouts / weekly_workout_goal * 100, 100)
    remaining_workouts = max(weekly_workout_goal - current_week_workouts, 0)
    
    # Determine status color and message
    if workout_progress < 50:
        status_color = "#C73E1D"
        status_text = "Behind"
        status_emoji = "🔴"
    elif workout_progress < 80:
        status_color = "#F18F01"
        status_text = "Close"
        status_emoji = "🟡"
    else:
        status_color = "#06A77D"
        status_text = "On Track"
        status_emoji = "🟢"
    
    st.markdown(f"""
    <div style="background-color: white; padding: 1rem; border-radius: 10px; border-left: 5px solid {status_color};">
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.5rem;">
            <h3 style="margin: 0; color: #2C3E50; font-size: 1.1rem;">💪 Workout Goal</h3>
            <span style="background-color: {status_color}; color: white; padding: 0.25rem 0.75rem; border-radius: 20px; font-size: 0.85rem; font-weight: 600;">
                {status_emoji} {status_text}
            </span>
        </div>
        <div style="display: flex; justify-content: space-between; align-items: baseline; margin-bottom: 0.75rem;">
            <span style="font-size: 2rem; font-weight: 700; color: {status_color};">{current_week_workouts}</span>
            <span style="font-size: 1.2rem; color: #5D6D7E;">/ {weekly_workout_goal} sessions</span>
        </div>
        <div style="background-color: #E8ECF1; border-radius: 10px; height: 24px; width: 100%; overflow: hidden; position: relative;">
            <div style="background: linear-gradient(90deg, {status_color}, {status_color}dd); height: 100%; width: {workout_progress}%; transition: width 0.5s ease; border-radius: 10px; box-shadow: inset 0 2px 4px rgba(0,0,0,0.1);"></div>
            <span style="position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%); color: #2C3E50; font-weight: 600; font-size: 0.85rem;">
                {int(workout_progress)}%
            </span>
        </div>
        <p style="margin-top: 0.75rem; margin-bottom: 0; color: #5D6D7E; font-size: 0.95rem;">
            {f"<strong style='color: {status_color};'>{int(remaining_workouts)} more workout(s)</strong> to reach your goal" if remaining_workouts > 0 else "<strong style='color: #06A77D;'>🎉 Goal smashed!</strong> You're on fire this week!"}
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
# Top metrics row
st.markdown("## 📊 Performance Overview")
col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    st.markdown(f"""
    <div style="background: white; padding: 1rem; border-radius: 10px; border-top: 4px solid #2E86AB; box-shadow: 0 2px 8px rgba(0,0,0,0.08); text-align: center; min-height: 100px; display: flex; flex-direction: column; justify-content: center;">
        <p style="color: #5D6D7E; font-size: 0.7rem; font-weight: 600; text-transform: uppercase; letter-spacing: 0.05em; margin: 0 0 0.4rem 0;">Avg Workouts/Week</p>
        <h2 style="color: #2E86AB; font-size: 2rem; font-weight: 700; margin: 0;">{int(weekly_avg_workouts)}</h2>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div style="background: white; padding: 1rem; border-radius: 10px; border-top: 4px solid #A23B72; box-shadow: 0 2px 8px rgba(0,0,0,0.08); text-align: center; min-height: 100px; display: flex; flex-direction: column; justify-content: center;">
        <p style="color: #5D6D7E; font-size: 0.7rem; font-weight: 600; text-transform: uppercase; letter-spacing: 0.05em; margin: 0 0 0.4rem 0;">Avg Calories/Week</p>
        <h2 style="color: #A23B72; font-size: 2rem; font-weight: 700; margin: 0;">{int(weekly_avg_calories):,}</h2>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown(f"""
    <div style="background: white; padding: 1rem; border-radius: 10px; border-top: 4px solid #F18F01; box-shadow: 0 2px 8px rgba(0,0,0,0.08); text-align: center; min-height: 100px; display: flex; flex-direction: column; justify-content: center;">
        <p style="color: #5D6D7E; font-size: 0.7rem; font-weight: 600; text-transform: uppercase; letter-spacing: 0.05em; margin: 0 0 0.4rem 0;">Avg Session Time</p>
        <h2 style="color: #F18F01; font-size: 2rem; font-weight: 700; margin: 0;">{int(total_duration/total_workouts)}m</h2>
    </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown(f"""
    <div style="background: white; padding: 1rem; border-radius: 10px; border-top: 4px solid #06A77D; box-shadow: 0 2px 8px rgba(0,0,0,0.08); text-align: center; min-height: 100px; display: flex; flex-direction: column; justify-content: center;">
        <p style="color: #5D6D7E; font-size: 0.7rem; font-weight: 600; text-transform: uppercase; letter-spacing: 0.05em; margin: 0 0 0.4rem 0;">Consistency Rate</p>
        <h2 style="color: #06A77D; font-size: 1.5rem; font-weight: 700; margin: 0; line-height: 1.2;">{unique_days}/{((end_date - start_date).days)} days <span style="font-size: 1.2rem;">({int(consistency_rate)}%)</span></h2>
    </div>
    """, unsafe_allow_html=True)

with col5:
    favorite_activity = df_filtered.groupby('activity')['duration'].count().idxmax()
    st.markdown(f"""
    <div style="background: white; padding: 1rem; border-radius: 10px; border-top: 4px solid #5D6D7E; box-shadow: 0 2px 8px rgba(0,0,0,0.08); text-align: center; min-height: 100px; display: flex; flex-direction: column; justify-content: center;">
        <p style="color: #5D6D7E; font-size: 0.7rem; font-weight: 600; text-transform: uppercase; letter-spacing: 0.05em; margin: 0 0 0.4rem 0;">Favorite Activity</p>
        <h2 style="color: #5D6D7E; font-size: 1.3rem; font-weight: 700; margin: 0; line-height: 1.3;">{favorite_activity}</h2>
    </div>
    """, unsafe_allow_html=True)


# Personalized insights section
st.markdown("## 💡 A look at your Best Self")

# Calculate insights
strongest_day = df_filtered.groupby('date')['calories'].sum().idxmax()
strongest_day_calories = df_filtered.groupby('date')['calories'].sum().max()
strongest_day_name = strongest_day.strftime('%A, %B %d')

best_time = df_filtered.groupby('time_of_day')['duration'].count().idxmax()
best_day_of_week = df_filtered.groupby('day_of_week')['duration'].count().idxmax()

# Calculate streak
df_sorted = df_filtered.sort_values('date')
dates_with_activity = df_sorted['date'].dt.date.unique()
current_streak = 0
max_streak = 0
temp_streak = 1

for i in range(1, len(dates_with_activity)):
    if (dates_with_activity[i] - dates_with_activity[i-1]).days == 1:
        temp_streak += 1
    else:
        max_streak = max(max_streak, temp_streak)
        temp_streak = 1
max_streak = max(max_streak, temp_streak)

# Check current streak
latest_date = df_filtered['date'].max().date()
if latest_date == datetime.now().date() or latest_date == (datetime.now() - timedelta(days=1)).date():
    for i in range(len(dates_with_activity)-1, 0, -1):
        if (dates_with_activity[i] - dates_with_activity[i-1]).days == 1:
            current_streak += 1
        else:
            break
    current_streak += 1

# Display insights in columns
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown(f"""
    <div style="background: linear-gradient(135deg, #2E86AB15, #2E86AB25); padding: 1.5rem; border-radius: 10px; border-left: 5px solid #2E86AB; box-shadow: 0 2px 8px rgba(0,0,0,0.08); min-height: 160px;">
        <div style="display: flex; align-items: center; margin-bottom: 0.75rem;">
            <span style="font-size: 2rem; margin-right: 0.5rem;">🗓️</span>
            <h3 style="margin: 0; color: #2C3E50; font-size: 1.1rem;">Strongest Day</h3>
        </div>
        <p style="color: #2E86AB; font-size: 1.1rem; font-weight: 600; margin: 0.5rem 0;">{strongest_day_name}</p>
        <p style="color: #5D6D7E; margin: 0;">You crushed it with <strong style="color: #2E86AB;">{int(strongest_day_calories)} calories</strong> burned!</p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div style="background: linear-gradient(135deg, #F18F0115, #F18F0125); padding: 1.5rem; border-radius: 10px; border-left: 5px solid #F18F01; box-shadow: 0 2px 8px rgba(0,0,0,0.08); min-height: 160px;">
        <div style="display: flex; align-items: center; margin-bottom: 0.75rem;">
            <span style="font-size: 2rem; margin-right: 0.5rem;">🏋️‍♀️</span>
            <h3 style="margin: 0; color: #2C3E50; font-size: 1.1rem;">Peak Performance</h3>
        </div>
        <p style="color: #F18F01; font-size: 1.1rem; font-weight: 600; margin: 0.5rem 0;">{best_time} Workouts</p>
        <p style="color: #5D6D7E; margin: 0;">You're most consistent during <strong style="color: #F18F01;">{best_time.lower()}</strong> sessions</p>
    </div>
    """, unsafe_allow_html=True)

with col3:
    streak_emoji = "🔥" if current_streak >= 3 else "💪"
    st.markdown(f"""
    <div style="background: linear-gradient(135deg, #06A77D15, #06A77D25); padding: 1.5rem; border-radius: 10px; border-left: 5px solid #06A77D; box-shadow: 0 2px 8px rgba(0,0,0,0.08); min-height: 160px;">
        <div style="display: flex; align-items: center; margin-bottom: 0.75rem;">
            <span style="font-size: 2rem; margin-right: 0.5rem;">{streak_emoji}</span>
            <h3 style="margin: 0; color: #2C3E50; font-size: 1.1rem;">Consistency Score</h3>
        </div>
        <p style="color: #06A77D; font-size: 1.1rem; font-weight: 600; margin: 0.5rem 0;">Current: {current_streak} days</p>
        <p style="color: #5D6D7E; margin: 0;">Best streak: <strong style="color: #06A77D;">{max_streak} days</strong></p>
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")

# Tabs for detailed visualizations
tab1, tab2, tab3, tab4 = st.tabs(["📈 Trends", "🎾 Activity Analysis", "⏱️ Timing Patterns", "📊 Performance Metrics"])

# Define consistent colors for each activity
activity_colors = {
    'Running': '#2E86AB',
    'Pilates': '#A23B72',
    'Cycling': '#F18F01',
    'HIIT': '#06A77D',
    'Yoga': '#5D6D7E',
    'Swimming': '#C73E1D',
    'Strength Training': '#4EA4C1'
}

with tab1:
    st.markdown("## 📊 Daily Calorie Trend")
    st.caption("Your daily calorie burn compared to your goal")
    
    # Daily calories with goal line - FULL WIDTH (no columns)
    daily_calories = df_filtered.groupby('date')['calories'].sum().reset_index()
    
    fig = go.Figure()
    
    fig.add_trace(go.Bar(
        x=daily_calories['date'],
        y=daily_calories['calories'],
        name='Calories Burned',
        marker=dict(color='#2E86AB', line=dict(color='white', width=2)),
        text=daily_calories['calories'].apply(lambda x: f'{int(x)}'),
        textposition='outside',
        textfont=dict(size=11, color='#2C3E50'),
        hovertemplate='<b>%{x|%A, %B %d}</b><br>Calories: %{y:,.0f}<extra></extra>'
    ))
    
    # Add goal line
    daily_goal = weekly_calorie_goal / 7
    fig.add_hline(
        y=daily_goal,
        line_dash="dash",
        line_width=3,
        line_color="#06A77D",
        annotation=dict(
            text=f"Daily Goal: {int(daily_goal)} cal",
            font=dict(size=13, color="#06A77D", family="IBM Plex Sans"),
            bgcolor="rgba(255, 255, 255, 0.9)",
            bordercolor="#06A77D",
            borderwidth=2,
            borderpad=6
        ),
        annotation_position="top right"
    )
    
    fig.update_layout(
        height=450,
        plot_bgcolor='white',
        paper_bgcolor='white',
        font=dict(family="IBM Plex Sans", size=13, color="#2C3E50"),
        margin=dict(t=40, b=80, l=70, r=40),
        xaxis=dict(
            title="<b>Date</b>", 
            showgrid=False, 
            title_font=dict(size=15, family="Playfair Display", color="#2C3E50"),
            tickfont=dict(size=12)
        ),
        yaxis=dict(
            title="<b>Calories Burned</b>", 
            showgrid=True, 
            gridcolor='rgba(232, 236, 241, 0.6)',
            gridwidth=1,
            title_font=dict(size=15, family="Playfair Display", color="#2C3E50"),
            tickfont=dict(size=12)
        ),
        hovermode='x unified',
        hoverlabel=dict(bgcolor="white", font_size=13, font_family="IBM Plex Sans", bordercolor="#2C3E50")
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    st.markdown("---")
    
    # Weekly comparison - FULL WIDTH (no columns)
    st.markdown("## Week-over-Week Comparison")
    st.caption("Total calories burned and number of workouts each week")

    # Group by actual week start date instead of ISO week number
    weekly_data = df_filtered.copy()
    weekly_data['week_start'] = weekly_data['date'].dt.to_period('W-SUN').apply(lambda x: x.start_time)
    
    weekly_agg = weekly_data.groupby('week_start').agg(
        calories=('calories', 'sum'),
        workouts=('date', 'count')
    ).reset_index()
    
    # Create readable labels like "Jan 20 – Jan 26"
    weekly_agg['label'] = weekly_agg['week_start'].apply(
        lambda x: f"{x.strftime('%b %d')} – {(x + pd.Timedelta(days=6)).strftime('%b %d')}"
    )
    
    fig = go.Figure()
    
    fig.add_trace(go.Bar(
        x=weekly_agg['label'],
        y=weekly_agg['calories'],
        name='Calories',
        marker=dict(color='#2E86AB', line=dict(color='white', width=2)),
        text=weekly_agg['calories'].apply(lambda x: f'{int(x):,}'),
        textposition='outside',
        textfont=dict(size=12, color='#2E86AB'),
        yaxis='y',
        hovertemplate='<b>%{x}</b><br>Calories: %{y:,.0f}<extra></extra>'
    ))
    
    fig.add_trace(go.Scatter(
        x=weekly_agg['label'],
        y=weekly_agg['workouts'],
        mode='lines+markers',
        name='Workouts',
        line=dict(color='#A23B72', width=4),
        marker=dict(size=12, color='#A23B72', line=dict(color='white', width=2)),
        text=weekly_agg['workouts'],
        textposition='top center',
        textfont=dict(size=12, color='#A23B72'),
        yaxis='y2',
        hovertemplate='<b>%{x}</b><br>Workouts: %{y}<extra></extra>'
    ))
    
    # Add calorie goal line
    fig.add_hline(
        y=weekly_calorie_goal,
        line_dash="dash",
        line_width=2,
        line_color="#06A77D",
        annotation=dict(
            text=f"Weekly Goal: {weekly_calorie_goal:,} cal",
            font=dict(size=12, color="#06A77D"),
            bgcolor="rgba(255,255,255,0.9)",
            bordercolor="#06A77D",
            borderwidth=2,
            borderpad=4
        ),
        annotation_position="top left"
    )
    
    fig.update_layout(
        height=420,
        plot_bgcolor='white',
        paper_bgcolor='white',
        font=dict(family="IBM Plex Sans", size=13, color="#2C3E50"),
        margin=dict(t=50, b=90, l=70, r=70),
        xaxis=dict(
            title="<b>Week</b>",
            showgrid=False,
            tickangle=-20,
            tickfont=dict(size=12),
            title_font=dict(size=14, color="#2C3E50")
        ),
        yaxis=dict(
            title="<b>Calories Burned</b>",
            showgrid=True,
            gridcolor='#E8ECF1',
            title_font=dict(size=14, color="#2C3E50"),
            tickfont=dict(size=12)
        ),
        yaxis2=dict(
            title="<b>Workouts</b>",
            overlaying='y',
            side='right',
            showgrid=False,
            title_font=dict(size=14, color="#2C3E50"),
            tickfont=dict(size=12)
        ),
        hovermode='x unified',
        hoverlabel=dict(bgcolor="white", font_size=13, bordercolor="#2C3E50"),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="center",
            x=0.5,
            font=dict(size=13),
            bgcolor="rgba(255,255,255,0.9)",
            bordercolor="#E8ECF1",
            borderwidth=1
        )
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
with tab2:
    st.markdown("## 🎾 Activity Distribution & Performance")
    st.caption("Compare calories burned and time spent across different activities")
    
    col1, col2 = st.columns(2)
    
    with col1:
        activity_data = df_filtered.groupby('activity').agg({'calories': 'mean', 'duration': 'mean', 'date': 'count'}).reset_index()
        activity_data.columns = ['activity', 'avg_calories', 'avg_duration', 'count']
        activity_data = activity_data.sort_values('avg_calories', ascending=True)
        
        colors = [activity_colors.get(act, '#5D6D7E') for act in activity_data['activity']]
        
        fig = go.Figure()
        fig.add_trace(go.Bar(
            y=activity_data['activity'],
            x=activity_data['avg_calories'],
            orientation='h',
            marker=dict(color=colors, line=dict(color='white', width=2)),
            text=activity_data['avg_calories'].apply(lambda x: f'{int(x):,} cal'),
            textposition='inside',
            textfont=dict(size=12, color="#F0F4F8"),
            hovertemplate='<b>%{y}</b><br>Avg Calories: %{x:,.0f}<br>Sessions: ' + activity_data['count'].astype(str) + '<extra></extra>'
        ))
        
        fig.update_layout(
            title="<b>Average Calories by Activity</b>",
            height=450,
            plot_bgcolor='white',
            paper_bgcolor='white',
            font=dict(family="IBM Plex Sans", size=12, color="#2C3E50"),
            margin=dict(t=70, b=50, l=140, r=80),
            xaxis=dict(
                title="<b>Average Calories</b>", 
                showgrid=True, 
                gridcolor='rgba(232, 236, 241, 0.6)',
                title_font=dict(size=14, color="#2C3E50"),
                tickfont=dict(size=11)
            ),
            yaxis=dict(
                title="", 
                showgrid=False,
                tickfont=dict(size=12)
            ),
            title_font=dict(size=16, family="Playfair Display", color="#2C3E50")
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        activity_avg = df_filtered.groupby('activity')['duration'].mean().reset_index()
        activity_avg = activity_avg.sort_values('duration', ascending=True)
        
        colors = [activity_colors.get(act, '#5D6D7E') for act in activity_avg['activity']]
        
        fig = go.Figure()
        fig.add_trace(go.Bar(
            y=activity_avg['activity'],
            x=activity_avg['duration'],
            orientation='h',
            marker=dict(color=colors, line=dict(color='white', width=2)),
            text=activity_avg['duration'].apply(lambda x: f'{int(x)} min'),
            textposition='inside',
            textfont=dict(size=12, color="#F5F7FA"),
            hovertemplate='<b>%{y}</b><br>Average Duration: %{x:.0f} minutes<extra></extra>'
        ))
        
        fig.update_layout(
            title="<b>Average Duration by Activity</b>",
            height=450,
            plot_bgcolor='white',
            paper_bgcolor='white',
            font=dict(family="IBM Plex Sans", size=12, color="#2C3E50"),
            margin=dict(t=70, b=50, l=140, r=80),
            xaxis=dict(
                title="<b>Average Minutes</b>", 
                showgrid=True, 
                gridcolor='rgba(232, 236, 241, 0.6)',
                title_font=dict(size=14, color="#2C3E50"),
                tickfont=dict(size=11)
            ),
            yaxis=dict(
                title="", 
                showgrid=False,
                tickfont=dict(size=12)
            ),
            title_font=dict(size=16, family="Playfair Display", color="#2C3E50")
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    st.markdown("---")
    
    # Activity timeline - FULL WIDTH (no columns)
    st.markdown("## 📅 Activity Timeline")
    st.caption("How your activity mix evolves week by week")
    
    activity_timeline = df_filtered.groupby([df_filtered['date'].dt.to_period('W'), 'activity']).size().reset_index()
    activity_timeline.columns = ['week', 'activity', 'count']
    activity_timeline['week'] = activity_timeline['week'].dt.to_timestamp()
    
    fig = px.line(activity_timeline, x='week', y='count', color='activity', markers=True, color_discrete_map=activity_colors)
    fig.update_traces(line=dict(width=4), marker=dict(size=10, line=dict(color='white', width=2)))
    
    fig.update_layout(
        height=450,
        plot_bgcolor='white',
        paper_bgcolor='white',
        font=dict(family="IBM Plex Sans", size=13, color="#2C3E50"),
        margin=dict(t=40, b=80, l=70, r=40),
        xaxis=dict(
            title="<b>Week</b>", 
            showgrid=True,
            gridcolor='rgba(232, 236, 241, 0.3)',
            title_font=dict(size=15, color="#2C3E50"),
            tickfont=dict(size=12)
        ),
        yaxis=dict(
            title="<b>Number of Sessions</b>", 
            showgrid=True, 
            gridcolor='rgba(232, 236, 241, 0.6)',
            title_font=dict(size=15, color="#2C3E50"),
            tickfont=dict(size=12)
        ),
        legend=dict(
            title=dict(text="<b>Activity Type</b>", font=dict(size=13)),
            orientation="v", 
            yanchor="top", 
            y=1, 
            xanchor="left", 
            x=1.02,
            font=dict(size=12),
            bgcolor="rgba(255, 255, 255, 0.9)",
            bordercolor="#E8ECF1",
            borderwidth=2
        )
    )
    
    st.plotly_chart(fig, use_container_width=True)

with tab3:
    st.markdown("## ⏱️ Workout Timing Analysis")
    st.caption("Discover when you're most active and consistent")
    
    col1, col2 = st.columns(2)
    
    with col1:
        heatmap_data = df_filtered.groupby(['day_of_week', 'time_of_day']).size().reset_index()
        heatmap_data.columns = ['day', 'time', 'count']
        heatmap_pivot = heatmap_data.pivot(index='time', columns='day', values='count').fillna(0)
        
        day_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        heatmap_pivot = heatmap_pivot.reindex(columns=[d for d in day_order if d in heatmap_pivot.columns])
        
        fig = go.Figure(data=go.Heatmap(
            z=heatmap_pivot.values,
            x=heatmap_pivot.columns,
            y=heatmap_pivot.index,
            colorscale='YlOrRd',
            text=heatmap_pivot.values.astype(int),
            texttemplate='<b>%{text}</b>',
            textfont=dict(size=16, color="black", family="IBM Plex Sans"),
            hovertemplate='<b>%{x}</b><br>%{y}<br>Workouts: %{z}<extra></extra>',
            colorbar=dict(
                title="<b>Workouts</b>",
                titlefont=dict(size=13),
                tickfont=dict(size=11),
                thickness=20,
                len=0.7
            )
        ))
        
        fig.update_layout(
            title="<b>Workout Frequency Heatmap</b>",
            height=450,
            plot_bgcolor='white',
            paper_bgcolor='white',
            font=dict(family="IBM Plex Sans", size=12, color="#2C3E50"),
            margin=dict(t=70, b=80, l=100, r=40),
            xaxis=dict(
                title="<b>Day of Week</b>", 
                tickangle=-45, 
                title_font=dict(size=14, color="#2C3E50"),
                tickfont=dict(size=12)
            ),
            yaxis=dict(
                title="<b>Time of Day</b>", 
                title_font=dict(size=14, color="#2C3E50"),
                tickfont=dict(size=12)
            ),
            title_font=dict(size=16, family="Playfair Display", color="#2C3E50")
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        day_dist = df_filtered.groupby('day_of_week').size().reset_index()
        day_dist.columns = ['day', 'count']
        
        day_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        day_dist['day'] = pd.Categorical(day_dist['day'], categories=day_order, ordered=True)
        day_dist = day_dist.sort_values('day')
        
        fig = go.Figure()
        fig.add_trace(go.Bar(
            x=day_dist['day'],
            y=day_dist['count'],
            marker=dict(
                color=['#2E86AB', "#c9737d", "#FF841F", '#06A77D', '#9B59B6', '#ff6361', '#ffa600'],
                line=dict(color='white', width=3)
            ),
            text=day_dist['count'],
            textposition='inside',
            textfont=dict(size=14, color="#F5F7FA"),
            hovertemplate='<b>%{x}</b><br>Total Workouts: %{y}<extra></extra>'
        ))
        
        fig.update_layout(
            title="<b>Workouts by Day of Week</b>",
            height=450,
            plot_bgcolor='white',
            paper_bgcolor='white',
            font=dict(family="IBM Plex Sans", size=12, color="#2C3E50"),
            margin=dict(t=70, b=100, l=70, r=40),
            xaxis=dict(
                title="", 
                showgrid=False, 
                tickangle=-45,
                tickfont=dict(size=12)
            ),
            yaxis=dict(
                title="<b>Number of Workouts</b>", 
                showgrid=True, 
                gridcolor='rgba(232, 236, 241, 0.6)',
                title_font=dict(size=14, color="#2C3E50"),
                tickfont=dict(size=11)
            ),
            title_font=dict(size=16, family="Playfair Display", color="#2C3E50")
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    st.markdown("---")
    
    # Time of day stats
    st.markdown("## ⏰ Performance by Time of Day")
    st.caption("Compare your workout stats across different times")
    
    time_analysis = df_filtered.groupby('time_of_day').agg({'calories': 'mean', 'duration': 'mean', 'date': 'count'}).reset_index()
    time_analysis.columns = ['time', 'avg_calories', 'avg_duration', 'count']

    # Sort by time column using Categorical
    time_analysis['time'] = Categorical(time_analysis['time'], categories=['Morning', 'Afternoon', 'Evening'], ordered=True)
    time_analysis = time_analysis.sort_values('time')

    time_colors = {'Morning': '#F18F01', 'Afternoon': '#2E86AB', 'Evening': '#A23B72'}
    time_emojis = {'Morning': '🌅', 'Afternoon': '☀️', 'Evening': '🌙'}

    col1, col2, col3 = st.columns(3)

    for idx, row in enumerate(time_analysis.to_dict('records')):
        color = time_colors.get(row['time'], '#5D6D7E')
        emoji = time_emojis.get(row['time'], '⏰')
        
        with [col1, col2, col3][idx]:
            st.markdown(f"""
            <div style="background: white; padding: 1.5rem; border-radius: 12px; border-top: 5px solid {color}; box-shadow: 0 4px 12px rgba(0,0,0,0.1); text-align: center;">
                <div style="font-size: 3.5rem; margin-bottom: 0.75rem;">{emoji}</div>
                <h3 style="margin: 0 0 1.25rem 0; color: #2C3E50; font-size: 1.3rem; font-weight: 700;">{row['time']}</h3>
                <div style="background: {color}15; padding: 1rem; border-radius: 8px; margin-bottom: 1rem;">
                    <p style="margin: 0; color: {color}; font-size: 2.2rem; font-weight: 700;">{int(row['count'])}</p>
                    <p style="margin: 0.25rem 0 0 0; color: #5D6D7E; font-size: 0.9rem; font-weight: 500;">Total Workouts</p>
                </div>
                <div style="border-top: 2px solid {color}30; padding-top: 1rem;">
                    <p style="margin: 0.4rem 0; color: #2C3E50; font-size: 1rem;"><strong style="color: {color}; font-size: 1.2rem;">{int(row['avg_calories'])}</strong> cal avg</p>
                    <p style="margin: 0.4rem 0; color: #2C3E50; font-size: 1rem;"><strong style="color: {color}; font-size: 1.2rem;">{int(row['avg_duration'])}</strong> min avg</p>
                </div>
            </div>
            """, unsafe_allow_html=True)

with tab4:
    st.markdown("## 📊 Advanced Performance Metrics")
    st.caption("Deep dive into efficiency and workout intensity patterns")
    
    col1, col2 = st.columns(2)
    
    with col1:
        efficiency_data = df_filtered.groupby('activity').agg({'calories': 'sum', 'duration': 'sum'}).reset_index()
        efficiency_data['cal_per_min'] = efficiency_data['calories'] / efficiency_data['duration']
        efficiency_data = efficiency_data.sort_values('cal_per_min', ascending=False)
        
        colors = [activity_colors.get(act, '#5D6D7E') for act in efficiency_data['activity']]
        
        fig = go.Figure()
        fig.add_trace(go.Bar(
            x=efficiency_data['activity'],
            y=efficiency_data['cal_per_min'],
            marker=dict(color=colors, line=dict(color='white', width=2)),
            text=efficiency_data['cal_per_min'].apply(lambda x: f'{x:.1f}'),
            textposition='inside',
            textfont=dict(size=13, color="#EFF2F5"),
            hovertemplate='<b>%{x}</b><br>Efficiency: %{y:.2f} cal/min<extra></extra>'
        ))
        
        fig.update_layout(
            title="<b>Calorie Efficiency (cal/min)</b>",
            height=450,
            plot_bgcolor='white',
            paper_bgcolor='white',
            font=dict(family="IBM Plex Sans", size=12, color="#2C3E50"),
            margin=dict(t=70, b=100, l=70, r=40),
            xaxis=dict(
                title="<b>Activity</b>", 
                showgrid=False, 
                tickangle=-45, 
                title_font=dict(size=14, color="#2C3E50"),
                tickfont=dict(size=12)
            ),
            yaxis=dict(
                title="<b>Calories per Minute</b>", 
                showgrid=True, 
                gridcolor='rgba(232, 236, 241, 0.6)',
                title_font=dict(size=14, color="#2C3E50"),
                tickfont=dict(size=11)
            ),
            title_font=dict(size=16, family="Playfair Display", color="#2C3E50")
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        intensity_dist = df_filtered.groupby('intensity').size().reset_index()
        intensity_dist.columns = ['intensity', 'count']
        
        colors_map = {'Low': '#06A77D', 'Moderate': '#F18F01', 'High': '#C73E1D'}
        
        fig = go.Figure()
        fig.add_trace(go.Pie(
            labels=intensity_dist['intensity'],
            values=intensity_dist['count'],
            marker=dict(
                colors=[colors_map[i] for i in intensity_dist['intensity']], 
                line=dict(color='white', width=4)
            ),
            textposition='inside',
            textinfo='label+percent',
            textfont=dict(size=15, color='white', family='IBM Plex Sans'),
            hovertemplate='<b>%{label} Intensity</b><br>Workouts: %{value}<br>Percentage: %{percent}<extra></extra>',
            hole=0.45
        ))
        
        fig.add_annotation(
            text=f"<b>{total_workouts}</b><br><span style='font-size: 0.8em;'>Total<br>Workouts</span>",
            font=dict(size=16, family="IBM Plex Sans", color="#2C3E50"),
            showarrow=False
        )
        
        
        fig.update_layout(
            title="<b> Workout Intensity Distribution</b>",
            height=450,
            plot_bgcolor='white',
            paper_bgcolor='white',
            font=dict(family="IBM Plex Sans", size=12, color="#2C3E50"),
            margin=dict(t=70, b=50, l=40, r=40),
            title_font=dict(size=16, family="Playfair Display", color="#2C3E50"),
            showlegend=True,
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=-0.15,
                xanchor="center",
                x=0.5,
                font=dict(size=13)
            )
        )
        
        st.plotly_chart(fig, use_container_width=True)
        st.caption("Low Intensity: AVG BPM < 100; Moderate Intensity: AVG BPM < 150; High Intensity: AVG BPM >= 150")

    
    st.markdown("---")
    
    # Consistency calendar - FULL WIDTH (no columns)
    st.markdown("## 📅 Workout Consistency Calendar")
    st.caption("Bubble size shows calories burned - bigger bubbles mean more efficient workouts")
    
    df_filtered['date_only'] = df_filtered['date'].dt.date
    daily_summary = df_filtered.groupby('date_only').agg({'calories': 'sum', 'duration': 'sum'}).reset_index()
    
    all_dates = pd.date_range(start=start_date, end=end_date, freq='D')
    date_df = pd.DataFrame({'date_only': all_dates.date})
    daily_summary = date_df.merge(daily_summary, on='date_only', how='left').fillna(0)
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=daily_summary['date_only'],
        y=[1]*len(daily_summary),
        mode='markers',
        marker=dict(
            size=daily_summary['calories']/7,
            color=daily_summary['calories'],
            colorscale='Viridis',
            showscale=True,
            colorbar=dict(
                title="<b>Calories</b>",
                titlefont=dict(size=13),
                tickfont=dict(size=11),
                thickness=20,
                len=0.6
            ),
            line=dict(width=2, color='white'),
            sizemode='diameter'
        ),
        text=daily_summary.apply(lambda x: f"<b>{x['date_only'].strftime('%b %d')}</b><br>{int(x['calories'])} cal<br>{int(x['duration'])} min", axis=1),
        hovertemplate='%{text}<extra></extra>'
    ))
    
    fig.update_layout(
        height=250,
        plot_bgcolor='white',
        paper_bgcolor='white',
        font=dict(family="IBM Plex Sans", size=12, color="#2C3E50"),
        margin=dict(t=40, b=80, l=70, r=100),
        xaxis=dict(
            title="<b>Date</b>", 
            showgrid=True,
            gridcolor='rgba(232, 236, 241, 0.3)',
            title_font=dict(size=14, color="#2C3E50"),
            tickfont=dict(size=11)
        ),
        yaxis=dict(visible=False, range=[0.5, 1.5])
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
# Footer with recommendations
st.markdown("---")
st.markdown("## Recommendations")

col1, col2, col3 = st.columns(3)

# Calculate recommendations
try:
    activity_counts = df_filtered.groupby('activity').size()
    least_frequent_activity = activity_counts.idxmin() if len(activity_counts) > 0 else "a new activity"
    least_count = activity_counts.min() if len(activity_counts) > 0 else 0
except:
    least_frequent_activity = "a new activity"
    least_count = 0

# Calculate efficiency (calories per minute) for each activity
try:
    efficiency_data = df_filtered.groupby('activity').agg({
        'calories': 'sum',
        'duration': 'sum'
    }).reset_index()
    
    # Calculate efficiency as calories per minute
    efficiency_data['efficiency'] = efficiency_data['calories'] / efficiency_data['duration']
    
    # Sort by efficiency in descending order (highest efficiency first)
    efficiency_data = efficiency_data.sort_values('efficiency', ascending=False)
    
    if not efficiency_data.empty:
        most_efficient_activity = efficiency_data.iloc[0]['activity']
        efficiency_rate = efficiency_data.iloc[0]['efficiency']
    else:
        most_efficient_activity = "your favorite activity"
        efficiency_rate = 0
except:
    most_efficient_activity = "your favorite activity"
    efficiency_rate = 0

try:
    if not day_dist.empty:
        underperforming_day = day_dist.iloc[day_dist['count'].argmin()]['day']
        day_count = day_dist['count'].min()
    else:
        underperforming_day = "a new day"
        day_count = 0
except:
    underperforming_day = "a new day"
    day_count = 0

with col1:
    st.markdown(f"""
    <div style="background: white; border: 2px solid #E8EAF6; border-left: 5px solid #667eea; padding: 1.5rem; border-radius: 12px; box-shadow: 0 2px 8px rgba(0,0,0,0.08);">
        <div style="font-size: 2rem; margin-bottom: 0.5rem;">💪</div>
        <h4 style="margin: 0 0 0.75rem 0; font-size: 1.1rem; font-weight: 600; color: #667eea;">Expand Your Routine</h4>
        <p style="margin: 0; font-size: 0.95rem; color: #4A5568;">Add more <strong style="color: #2D3748;">{least_frequent_activity}</strong> sessions{f' (only {least_count} so far)' if least_count > 0 else ''} for better variety</p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div style="background: white; border: 2px solid #FCE4EC; border-left: 5px solid #f5576c; padding: 1.5rem; border-radius: 12px; box-shadow: 0 2px 8px rgba(0,0,0,0.08);">
        <div style="font-size: 2rem; margin-bottom: 0.5rem;">🔥</div>
        <h4 style="margin: 0 0 0.75rem 0; font-size: 1.1rem; font-weight: 600; color: #f5576c;">Peak Efficiency</h4>
        <p style="margin: 0; font-size: 0.95rem; color: #4A5568;"><strong style="color: #2D3748;">{most_efficient_activity}</strong> delivers {f'{efficiency_rate:.1f} cal/min' if efficiency_rate > 0 else 'the best burn'}; maximize your workout in this activity for more gains!</p>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown(f"""
    <div style="background: white; border: 2px solid #E0F7FA; border-left: 5px solid #00bcd4; padding: 1.5rem; border-radius: 12px; box-shadow: 0 2px 8px rgba(0,0,0,0.08);">
        <div style="font-size: 2rem; margin-bottom: 0.5rem;">📅</div>
        <h4 style="margin: 0 0 0.75rem 0; font-size: 1.1rem; font-weight: 600; color: #00bcd4;">Fill the Gap</h4>
        <p style="margin: 0; font-size: 0.95rem; color: #4A5568;">Schedule a session on <strong style="color: #2D3748;">{underperforming_day}</strong>{f' (only {day_count} workout{"s" if day_count != 1 else ""})' if day_count > 0 else ''} to stay consistent</p>
    </div>
    """, unsafe_allow_html=True)