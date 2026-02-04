# 🏃‍♀️ Personal Fitness Dashboard

A comprehensive, data-driven fitness tracking dashboard built with Streamlit and Plotly. This project transforms raw workout data into actionable insights through evidence-based visualizations and personalized recommendations.

![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![Streamlit](https://img.shields.io/badge/Streamlit-1.28%2B-red)
![Plotly](https://img.shields.io/badge/Plotly-5.17%2B-purple)
![License](https://img.shields.io/badge/License-MIT-green)

## 🎯 Overview

The Personal Fitness  Dashboard is designed for fitness enthusiasts who want to optimize their workout routines through data-driven insights rather than intuition alone. Built on evidence-based design principles from data visualization research, it answers critical questions:

- **Am I on track with my goals?**
- **What are my natural workout patterns?**
- **Which activities are most effective for me?**
- **When should I schedule workouts for best results?**

## ✨ Features

### 📊 Goal Tracking & Progress
- **Weekly goal monitoring** with status indicators (🔴 Behind, 🟡 Close, 🟢 On Track)
- **Linear progress bars** with explicit remaining values
- **Customizable targets** for calories and workout frequency

### 📈 Comprehensive Analytics

**Trends Tab:**
- Daily calorie burn with goal reference line
- Week-over-week comparison (dual-axis chart)
- Temporal pattern identification

**Activity Analysis Tab:**
- Horizontal bar charts comparing activities
- Average calories and duration by activity type
- Activity timeline showing workout mix evolution

**Timing Patterns Tab:**
- Heatmap revealing optimal workout times (Day × Time matrix)
- Day-of-week distribution
- Time-of-day performance metrics

**Performance Metrics Tab:**
- Calorie efficiency analysis (cal/min by activity)
- Intensity distribution (Low/Moderate/High)
- Consistency calendar (bubble chart)

### 💡 Smart Insights

- **Strongest Day**: Identifies peak performance days
- **Peak Performance Time**: Finds when you're most consistent
- **Consistency Scoring**: Tracks current and best streaks
- **Personalized Recommendations**: Data-driven suggestions for improvement

### 🎨 Interactive Features

- **Date range filtering**: Last 7/14/30 days, 8 weeks, or custom range
- **Activity filtering**: Focus on specific workout types
- **Hover tooltips**: Rich contextual information on all charts
- **Responsive design**: Optimized for desktop and tablet viewing

### 📖 Built-in Documentation

- **Design Choices tab**: Complete explanation of design decisions
- **Expandable sections**: Data structure, visual encodings, color system, typography
- **Color swatches**: Interactive color palette showcase

## 🚀 Installation

### Prerequisites

- Python 3.8 or higher
- pip package manager
- Git (for cloning)

### Step 1: Clone the Repository

```bash
git clone https://github.com/stesilva/fitness-dashboard.git
cd fitness-dashboard
```

### Step 2: Create Virtual Environment (Recommended)

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

**Required packages:**
```txt
streamlit>=1.28.0
pandas>=2.0.0
plotly>=5.17.0
numpy>=1.24.0
```

### Step 4: Prepare Your Data

Create a CSV file named `fitness_data.csv` with the following columns:

```csv
date,activity,duration,calories,time_of_day
2026-01-20,Running,45,540,Morning
2026-01-20,Yoga,30,90,Evening
2026-01-21,Cycling,60,480,Afternoon
```

**Or use the sample data generator** (included in the code):
```python
# The dashboard includes generate_sample_data() function
# Uncomment line 158 to use fake data for testing
df = generate_sample_data()
```

## 📖 Usage

### Running the Dashboard

```bash
streamlit run app.py
```

The dashboard will open automatically in your default browser at `http://localhost:8501`

### Filtering Data

**Sidebar Controls:**
1. **Time Period**: Select preset ranges or custom dates
2. **Activity Types**: Filter by specific activities
3. **Weekly Goals**: Adjust calorie and workout targets

### Navigating the Dashboard

1. **Start at the top**: Check your weekly goal progress
2. **Scan key metrics**: 5-column performance overview
3. **Read insights**: Personalized findings in 3 columns
4. **Explore tabs**: Deep-dive into specific analyses
5. **View design explanation**: Click "Show Explanation" button
