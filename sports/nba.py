import pandas as pd
from dash import Dash, dcc, html
from dash.dependencies import Input, Output
import plotly.express as px
import socket

# Get local IP address
hostname = socket.gethostname()
local_ip = socket.gethostbyname(hostname)

# Load multiple CSV files and merge them into one DataFrame
file_paths = [
    "C://lakers_nba.csv",
    "C://warriors_nba.csv",
    "C://bucks_nba.csv",
    "C://celtics_nba.csv",
]

df_list = [pd.read_csv(file, header=0) for file in file_paths]
df = pd.concat(df_list, ignore_index=True)

# Standardize column names (strip spaces & lowercase)
df.columns = df.columns.str.strip().str.lower()

# Ensure required columns exist
required_columns = {'team', 'player', 'matches', 'points', 'assists', 'rebounds', 'steals', 'blocks'}
missing_columns = required_columns - set(df.columns)
if missing_columns:
    raise ValueError(f"Missing columns in CSV files: {missing_columns}")

# Create Dash app
app = Dash(__name__)

app.layout = html.Div(children=[
    html.H1("NBA Analytics Dashboard", style={'textAlign': 'center', 'color': '#FFD700', 'fontFamily': 'Arial Black'}),
    
    dcc.Dropdown(
        id='team-dropdown',
        options=[{'label': team, 'value': team} for team in df['team'].unique()],
        value=df['team'].unique()[0],
        clearable=False,
        style={'width': '50%', 'margin': 'auto'}
    ),
    
    html.Div([
        dcc.Graph(id='team-performance'),
        dcc.Graph(id='player-performance'),
        dcc.Graph(id='tracking-data'),
        dcc.Graph(id='physical-attributes'),
        dcc.Graph(id='ai-insights')
    ], style={'padding': '20px'})
])

@app.callback(
    [Output('team-performance', 'figure'),
     Output('player-performance', 'figure'),
     Output('tracking-data', 'figure'),
     Output('physical-attributes', 'figure'),
     Output('ai-insights', 'figure')],
    [Input('team-dropdown', 'value')]
)
def update_graphs(selected_team):
    team_df = df[df['team'] == selected_team]
    
    # Team Performance Graph
    team_fig = px.bar(team_df, x='player', y='points', 
                      title=f'Points Per Game - {selected_team}',
                      color_discrete_sequence=['#FFD700'])
    
    # Player Performance Graph
    player_fig = px.scatter(team_df, x='assists', y='rebounds',
                            size='matches', color='player',
                            title=f'Player Performance for {selected_team}')
    
    # Tracking Data Graph
    tracking_fig = px.line(team_df, x='matches', y=['points', 'assists', 'rebounds'],
                           title=f'Tracking Data for {selected_team}')
    
    # Physical Attributes Graph
    physical_fig = px.bar(team_df, x='player', y=['steals', 'blocks'],
                          title=f'Defensive Attributes of {selected_team}', barmode='group')

    # AI Insights Graph
    ai_fig = px.scatter(team_df, x='steals', y='blocks',
                        color='player', size='points',
                        title=f'AI-Driven Insights for {selected_team}')
    
    return team_fig, player_fig, tracking_fig, physical_fig, ai_fig

if __name__ == '__main__':
    print(f"\nServer running at: http://{local_ip}:8050/\n")
    app.run_server(host='0.0.0.0', port=8050)
