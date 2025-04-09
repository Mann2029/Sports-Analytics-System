# Sports-Analytics-System

## Overvwiew
- A comprehensive and intelligent sports analytics dashboard built with Python, Dash, and Plotly. This project enables data-driven performance analysis for Cricket, NBA Basketball, and Football, empowering users with:
-  AI-powered player comparisons
-  Interactive and responsive dashboards

## Table of Contents
- Project Overview
- Features
- Directory Structure
- Requirements
- How to Run & All Dashboard
- Dataset Format
- Future Enhancements
- Conclusion

## Project Overview

### This project includes four main dashboards:

- File Name and Description:
           - cricket.py	 Visualize batting and bowling performance in international cricket.
          - nba.py        Analyze player/team performance in the NBA with stats like points, assists, rebounds, etc.
          - football.py	Track physical and AI-based performance insights for top football teams.
          - multi sports.py	A combined dashboard that allows switching between Cricket, NBA, and Football views.
- Each dashboard reads from multiple .csv files containing real player and team performance data.

## Detailed Features by Module

### Cricket Dashboard (`cricket.py`)

#### Team Selection:
- Dropdown allows users to select from international teams like India, England, Australia.
- Once selected, the dashboard shows all players from that team.

#### Team Overview:
- Displays a detailed **table** with the following batting stats:
  - Player name
  - Matches played
  - Total runs
  - Batting average
  - Strike rate
  - Number of 4s and 6s

#### Player Role Classification:
- Each player is automatically tagged as either a **Batter** or **Bowler** based on their data.

#### Batting Player Comparison:
- Select two batters from dropdowns.
- Compare their performance using interactive **bar charts** for:
  - Batting average
  - Strike rate
  - Number of 4s and 6s

#### Bowling Player Comparison:
- Select two bowlers.
- View their comparison on:
  - Total wickets
  - Bowling average
  - Economy rate

#### Fully Interactive:
- Hover effects show exact values.
- Responsive layout updates in real time when a team or player is changed.

### NBA Dashboard (`nba.py`)

#### Team Selection:
- Dropdown to choose from NBA teams like Lakers, Warriors, Bucks, Celtics.

#### Team Performance:
- Bar graph of points scored per player.

#### Player Performance:
- Scatter plot:
  - X-axis: Assists
  - Y-axis: Rebounds
  - Circle size: Matches played
  - Color: Individual player

#### Tracking Data:
- Line graph showing:
  - Points
  - Assists
  - Rebounds across matches

#### Physical Attributes:
- Bar chart comparing **steals** and **blocks** across players.
- Used for evaluating defensive skills.

#### AI-Driven Insights:
- Scatter chart comparing **steals vs. blocks**
- Circle size = Points scored
- Color = Player
- Helps identify players who perform well in both offense and defense.

---

### Football Dashboard (`football.py`)

#### Team Selection:
- Dropdown for clubs like FC Barcelona, Real Madrid, Liverpool, Bayern Munich, etc.

#### Speed Analysis:
- Bar graph showing player sprint speeds in meters/second.

#### Player Performance:
- Scatter plot of:
  - X-axis: Acceleration
  - Y-axis: Distance covered
  - Bubble size = Sprint count
  - Colored by player position (e.g., midfielder, defender)

#### Tracking Data:
- Line chart with timestamps on X-axis
- Tracks:
  - Speed
  - Acceleration
  - Distance covered over time

#### Physical Attributes:
- Grouped bar chart of:
  - Heart rate (BPM)
  - Sprint count

#### AI Insights:
- Scatter chart comparing:
  - Sprint count vs speed
  - Bubble size = acceleration
  - Colored by player position
  - Hover info includes player name, role, and position

#### Additional Metrics:
- Visualize important attributes:
  - Pass accuracy
  - Injury risk %
  - Fatigue level
  - Heatmap coverage %
  - Ball possession time
  - Optimal substitution time

---

### Multi-Sports Dashboard(`multi sports.py`)

#### Sport Selector:
- Use a radio button to choose between Cricket, NBA, and Football dashboards.

#### Dynamic Interface:
- Automatically loads relevant layout and charts based on the sport selected.

#### Cricket Section:
- Team dropdown for cricket
- Choose between Batting and Bowling stats
- Player-vs-player comparison for chosen type
- Charts shown:
  - Runs, Fours, Sixes, Strike Rate, Average
  - Bowling Wickets, Economy, Average

#### NBA Section:
- Dropdown for team
- Visualizations:
  - Points, Assists, Rebounds, Steals, Blocks

#### Football Section:
- Team selection dropdown
- Full suite of performance analytics:
  - Speed, Sprint, Pass Accuracy, Fatigue
  - Injury Risk, Ball Possession, Heatmap
  - Substitution Suggestion via AI

#### Additional Features Across All Dashboards:
- Clean UI with styled headings and dark background for readability.
- Dynamic callbacks using Dash to refresh content based on selection.
- Server IP printed on console to access dashboard in LAN.

## Directory Structure

project/
├── cricket.py              # Cricket analytics dashboard
├── nba.py                  # NBA basketball dashboard
├── football.py             # Football performance dashboard
├── multi sports.py         # Unified multi-sport dashboard
├── datasets/               # Folder containing all CSV files

## Requirements:
- dash
- pandas
- plotly

## How to Run the Dashboards
### Run the Cricket Dashboard (Standalone)
 - python cricket.py
 - Visit: http://localhost:8010/

- You’ll see:
- A dropdown to choose the team (India, Australia, England, etc.)
- A table of batters with runs, average, strike rate, etc.
- Dropdowns to compare two batters or two bowlers visually.

### NBA Dashboard (Standalone)

-python nba.py
-Visit: http://localhost:8050/

-You’ll see:
- Dropdown to select NBA teams like Lakers or Celtics
- Player stats (points, assists, rebounds, blocks, steals)
-AI insight charts combining offensive & defensive attributes

### Football Dashboard (Standalone)
- python football.py
- Visit: http://localhost:8050/

- You’ll see:
- Dropdown for clubs like FC Barcelona, Real Madrid
- Visualizations for speed, pass accuracy, injury risk, fatigue
- AI-driven metrics like optimal substitution time

### Combined Multi-Sports Dashboard
- python "multi sports.py"
- Visit: http://127.0.0.1:8050/
- When you run multi sports.py, you’ll see a single interface with:

### 1. Sport Selector (Radio Button)
-At the top, you’ll choose one of:
- Cricket
- NBA
- Football

### 2. If Cricket is selected:
- Dropdown to pick a team
- Choose Batting or Bowling analysis
- Charts for:
  -  Player performance (runs, fours, sixes, average, strike rate)
  -  Player-vs-player comparison charts

### 3. If NBA is selected:
- Dropdown to pick an NBA team
- Charts for:
  - Points, Assists, Rebounds, Steals, Blocks
  - AI Insight using scatter plots based on performance

### 4. If Football is selected:
- Dropdown for top clubs (FC Barcelona, Liverpool, etc.)
- You’ll see visualizations for:
  - Physical metrics: speed, heart rate, fatigue, injury risk
  - Tactical insights: ball possession, heatmap coverage
  - AI-recommended substitution timing

### Real-time updates based on team selection
- Dynamic Loading
- This unified dashboard is built using Dash’s callback system with conditional layouts, meaning:
- The correct sport’s layout loads instantly based on your choice.
- All data is loaded at the start, so switching between sports is fast.

 ## Dataset Format
- Ensure that your .csv files contain at least the following columns:

### Football Datasets
- Player Name, Speed (m/s), Distance Covered (m), Sprint Count
- Pass Accuracy (%), Fatigue Level (%), Injury Risk (%)
- Ball Possession Time (s), Heatmap Coverage (%), Optimal Substitution Time (min)

### NBA Datasets
- Team, Player, Points, Assists, Rebounds, Steals, Blocks, Matches

### Cricket Datasets
#### Batting:
- Team, Player, Matches, Runs, Average, Strike Rate, Fours, Sixes

#### Bowling:
- Team, Player, Matches, Wickets, Economy, Bowling Average

Future Enhancements
- Live Data Integration: Add APIs to stream live match statistics in real time.
- Predictive Insights: Use machine learning to forecast performance trends and fatigue levels.
- Export Reports: Allow users to download player comparisons as PDF or CSV.
- Web Hosting: Deploy the dashboard online using platforms like Heroku or Render.
- User Uploads: Let users upload their own CSV files to analyze custom teams.
- 
## Conclusion
- This AI-powered Multi-Sport Analytics Dashboard demonstrates how interactive data visualization and basic artificial intelligence can enhance decision-making in sports analytics. Built using Python, Dash, Plotly, and Pandas, the project empowers users to:
    - Gain deep insights into player and team performance.
    - Make data-backed comparisons between players.
    - Visualize trends in fatigue, physical exertion, and skill.
    - Switch seamlessly between different sports — all in one dashboard.
