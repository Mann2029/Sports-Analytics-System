import pandas as pd
from dash import Dash, dcc, html
from dash.dependencies import Input, Output
import plotly.express as px
import socket

# Get local IP address
hostname = socket.gethostname()
local_ip = socket.gethostbyname(hostname)

# Load CSV files
file_paths = [
    "C://india_batting.csv", "C://australia_batting.csv", "C://england_batting.csv",
    "C://india_bowling.csv", "C://england_bowling.csv", "C://australia_bowling.csv"
]

df_list = [pd.read_csv(file, header=0) for file in file_paths]
df = pd.concat(df_list, ignore_index=True)

# Standardize column names
df.columns = df.columns.str.strip().str.lower()

# Identify player roles
df['role'] = df.apply(lambda row: 'Batter' if 'runs' in row and not pd.isna(row['runs']) else 'Bowler', axis=1)

# Initialize Dash app
app = Dash(__name__)

app.layout = html.Div(style={'backgroundColor': '#121212', 'padding': '20px'}, children=[
    html.H1("Cricket Analytics Dashboard", style={'textAlign': 'center', 'color': '#FFD700'}),

    # Team Selection
    dcc.Dropdown(
        id='team-dropdown',
        options=[{'label': team, 'value': team} for team in df['team'].unique()],
        placeholder='Select a Team',
        clearable=True,
        style={'width': '50%', 'margin': 'auto'}
    ),

    html.Div(id='team-overview'),

    # Player Comparison (Batting)
    html.Div([
        html.H3("Batting Comparison", style={'textAlign': 'center', 'color': '#FFD700'}),

        # Player Selection Dropdowns for Batting Comparison
        html.Div([
            dcc.Dropdown(id='batting-player1-dropdown', placeholder="Select Batting Player 1", style={'width': '45%', 'display': 'inline-block'}),
            dcc.Dropdown(id='batting-player2-dropdown', placeholder="Select Batting Player 2", style={'width': '45%', 'display': 'inline-block', 'marginLeft': '5%'})
        ], style={'textAlign': 'center'}),

        html.Div(id='batting-comparison-output')
    ]),

    # Player Comparison (Bowling)
    html.Div([
        html.H3("Bowling Comparison", style={'textAlign': 'center', 'color': '#FFD700'}),

        # Player Selection Dropdowns for Bowling Comparison
        html.Div([
            dcc.Dropdown(id='bowling-player1-dropdown', placeholder="Select Bowling Player 1", style={'width': '45%', 'display': 'inline-block'}),
            dcc.Dropdown(id='bowling-player2-dropdown', placeholder="Select Bowling Player 2", style={'width': '45%', 'display': 'inline-block', 'marginLeft': '5%'})
        ], style={'textAlign': 'center'}),

        html.Div(id='bowling-comparison-output')
    ])
])

# Callback for Team Overview (ONLY TABLE, NO BAR CHART)
@app.callback(
    [Output('team-overview', 'children'),
     Output('batting-player1-dropdown', 'options'),
     Output('batting-player2-dropdown', 'options'),
     Output('bowling-player1-dropdown', 'options'),
     Output('bowling-player2-dropdown', 'options')],
    [Input('team-dropdown', 'value')]
)
def update_team_overview(selected_team):
    if not selected_team:
        return html.P("Select a team to view stats.", style={'color': 'white', 'textAlign': 'center'}), [], [], [], []

    team_df = df[df['team'] == selected_team]

    # Filter based on role
    batting_df = team_df[team_df['role'] == 'Batter']
    bowling_df = team_df[team_df['role'] == 'Bowler']

    # Team Overview Table (Only for Batters)
    table_header = [html.Th(col.title(), style={'color': 'gold'}) for col in ['Player', 'Matches', 'Runs', 'Average', 'Strike Rate', 'Fours', 'Sixes']]
    table_rows = [html.Tr([html.Td(batting_df.iloc[i][col]) for col in ['player', 'matches', 'runs', 'average', 'strike rate', 'fours', 'sixes']]) for i in range(len(batting_df))]
    
    team_table = html.Table([html.Tr(table_header)] + table_rows, style={'width': '100%', 'border': '1px solid white', 'color': 'white', 'textAlign': 'center'})

    # Separate dropdown options for Batters & Bowlers
    batters = [{'label': player, 'value': player} for player in batting_df['player'].unique()]
    bowlers = [{'label': player, 'value': player} for player in bowling_df['player'].unique()]
    
    return team_table, batters, batters, bowlers, bowlers

# Callback for Batting Player Comparison
@app.callback(
    Output('batting-comparison-output', 'children'),
    [Input('batting-player1-dropdown', 'value'), Input('batting-player2-dropdown', 'value')]
)
def compare_batting_players(player1, player2):
    if not player1 or not player2:
        return html.P("Select two batting players to compare.", style={'color': 'white', 'textAlign': 'center'})

    player1_df = df[df['player'] == player1]
    player2_df = df[df['player'] == player2]

    if player1_df.empty or player2_df.empty:
        return html.P("No data available for one or both players.", style={'color': 'white', 'textAlign': 'center'})

    # Extract Stats
    p1_stats = player1_df.iloc[0]
    p2_stats = player2_df.iloc[0]

    # Batting Comparison (ONLY FOR BATTERS)
    if p1_stats['role'] == 'Batter' and p2_stats['role'] == 'Batter':
        batting_charts = [
            create_comparison_chart(player1, player2, 'average', 'Batting Average', [30, 100]),
            create_comparison_chart(player1, player2, 'strike rate', 'Strike Rate', [100, 195]),
            create_comparison_chart(player1, player2, 'fours', 'Fours Scored', [100, 1300]),
            create_comparison_chart(player1, player2, 'sixes', 'Sixes Scored', [1, 200])
        ]
        return html.Div(batting_charts)
    
    return html.P("Players must both be batters for comparison.", style={'color': 'white', 'textAlign': 'center'})

# Callback for Bowling Player Comparison
@app.callback(
    Output('bowling-comparison-output', 'children'),
    [Input('bowling-player1-dropdown', 'value'), Input('bowling-player2-dropdown', 'value')]
)
def compare_bowling_players(player1, player2):
    if not player1 or not player2:
        return html.P("Select two bowling players to compare.", style={'color': 'white', 'textAlign': 'center'})

    player1_df = df[df['player'] == player1]
    player2_df = df[df['player'] == player2]

    if player1_df.empty or player2_df.empty:
        return html.P("No data available for one or both players.", style={'color': 'white', 'textAlign': 'center'})

    # Extract Stats
    p1_stats = player1_df.iloc[0]
    p2_stats = player2_df.iloc[0]

    # Bowling Comparison (ONLY FOR BOWLERS)
    if p1_stats['role'] == 'Bowler' and p2_stats['role'] == 'Bowler':
        bowling_charts = [
            create_comparison_chart(player1, player2, 'wickets', 'Total Wickets', [1, 800]),
            create_comparison_chart(player1, player2, 'economy', 'Bowling Economy', [2, 10]),
            create_comparison_chart(player1, player2, 'bowling average', 'Bowling Average', [10, 50])
        ]
        return html.Div(bowling_charts)
    
    return html.P("Players must both be bowlers for comparison.", style={'color': 'white', 'textAlign': 'center'})

# Function to create bar charts
def create_comparison_chart(player1, player2, stat, title, y_range=None):
    comp_df = pd.DataFrame({'Player': [player1, player2], title: [df[df['player'] == player1][stat].values[0], df[df['player'] == player2][stat].values[0]]})
    fig = px.bar(comp_df, x='Player', y=title, title=title, color='Player')
    fig.update_layout(plot_bgcolor='#101010', paper_bgcolor='#101010', font=dict(color='white'))
    if y_range:
        fig.update_yaxes(range=y_range)
    return dcc.Graph(figure=fig)

if __name__ == '__main__':
    print(f"\nServer running at: http://{local_ip}:8010/\n")
    app.run_server(host='0.0.0.0', port=8010, debug=True)