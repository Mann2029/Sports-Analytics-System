import pandas as pd
from dash import Dash, dcc, html
from dash.dependencies import Input, Output
import plotly.express as px
import socket

# Get the local IP address
hostname = socket.gethostname()
local_ip = socket.gethostbyname(hostname)

# Load multiple CSV files and merge them into one DataFrame
file_paths = [
    "C:/fc_barcelona_analytics_updated.csv",
    "C:/real_madrid_analytics_updated.csv",
    "C:/manchester_united_analytics_updated.csv",
    "C:/liverpool_analytics_updated.csv",
    "C:/bayern_munich_analytics_updated.csv"
]

df_list = [pd.read_csv(file, header=0) for file in file_paths]  # Ensure header row is read correctly
df = pd.concat(df_list, ignore_index=True)

# Standardize column names (strip spaces & lowercase)
df.columns = df.columns.str.strip()
df.columns = df.columns.str.lower()

# Debug: Print column names to check if 'team name' exists
print("Columns in DataFrame:", df.columns)

# Check if 'team name' exists
if 'team name' not in df.columns:
    raise ValueError("Column 'Team Name' not found in CSV files! Check column names.")

# Create Dash app
app = Dash(__name__)

app.layout = html.Div(children=[
    html.H1("Sports Analytics Dashboard", style={
        'textAlign': 'center', 'color': '#FFD700', 'fontFamily': 'Arial Black', 'textShadow': '2px 2px 10px #000000'
    }),
    
    dcc.Dropdown(
        id='team-dropdown',
        options=[{'label': team, 'value': team} for team in df['team name'].unique()],
        value=df['team name'].unique()[0],
        clearable=False,
        style={
            'width': '50%', 'margin': 'auto', 'backgroundColor': '#101010', 'borderRadius': '10px',
            'fontFamily': 'Arial Black', 'color': '#FFD700', 'textAlign': 'center'
        }
    ),
    
    html.Div([
        dcc.Graph(id='team-performance'),
        dcc.Graph(id='player-performance'),
        dcc.Graph(id='tracking-data'),
        dcc.Graph(id='physical-attributes'),
        dcc.Graph(id='ai-insights')
    ], style={'padding': '20px'}),

], style={
    'backgroundImage': 'url("https://web-assets.hyscaler.com/wp-content/uploads-webpc/uploads/2023/11/ai-in-sports-4.png.webp")',
    'backgroundSize': 'cover', 'padding': '20px', 'color': 'white'
})

@app.callback(
    [Output('team-performance', 'figure'),
     Output('player-performance', 'figure'),
     Output('tracking-data', 'figure'),
     Output('physical-attributes', 'figure'),
     Output('ai-insights', 'figure')],
    [Input('team-dropdown', 'value')]
)
def update_graphs(selected_team):
    team_df = df[df['team name'] == selected_team]
    
    # Team Performance Graph
    team_fig = px.bar(team_df, x='player name', y='speed (m/s)', 
                      title=f'Speed Analysis of {selected_team}',
                      color_discrete_sequence=['#FFD700'])
    
    # Player Performance Graph
    player_fig = px.scatter(team_df, x='acceleration (m/s²)', y='distance covered (m)', 
                            size='sprint count', color='position',
                            title=f'Player Performance for {selected_team}',
                            facet_col='player name',
                            facet_col_wrap=4,
                            labels={'player name': ''},
                            color_discrete_sequence=['#8B0000'])
    
    # Tracking Data Graph
    tracking_fig = px.line(team_df, x='timestamp', 
                           y=['speed (m/s)', 'acceleration (m/s²)', 'distance covered (m)'],
                           title=f'Tracking Data for {selected_team}',
                           color_discrete_sequence=['#1E90FF', '#DC143C', '#32CD32'])

    # Physical Attributes Graph
    physical_fig = px.bar(team_df, x='player name', y=['heart rate (bpm)', 'sprint count'],
                          title=f'Physical Attributes of {selected_team}', barmode='group',
                          color_discrete_sequence=['#9400D3', '#FF4500'])

    # AI Insights Graph
    hover_columns = ['player name', 'position']
    if 'role' in team_df.columns:
        hover_columns.append('role')

    ai_fig = px.scatter(team_df, x='sprint count', y='speed (m/s)',
                        color='position', size='acceleration (m/s²)',
                        title=f'AI-Driven Insights for {selected_team}',
                        hover_data=hover_columns,
                        color_discrete_sequence=['#FF1493'])
    
    return team_fig, player_fig, tracking_fig, physical_fig, ai_fig

if __name__ == '__main__':
    print(f"\nServer running at: http://{local_ip}:8050/\n")
    app.run_server(host='0.0.0.0', port=8050)



