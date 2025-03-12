import dash 
from dash import dcc, html 
from dash.dependencies import Input, Output
import pandas as pd
import plotly.express as px
from dash.exceptions import PreventUpdate 

# Load CSV Data
nba_files = ["C://lakers_nba.csv", "C://warriors_nba.csv", "C://bucks_nba.csv", "C://celtics_nba.csv"]
cricket_files = ["C://india_batting.csv", "C://australia_batting.csv", "C://england_batting.csv", 
                 "C://india_bowling.csv", "C://england_bowling.csv", "C://australia_bowling.csv"]
football_files = ["C://fc_barcelona_analytics_updated.csv", "C://real_madrid_analytics_updated.csv", 
                  "C://manchester_united_analytics_updated.csv", "C://liverpool_analytics_updated.csv", 
                  "C://bayern_munich_analytics_updated.csv"]

# Load DataFrames
cricket_batting_df = pd.concat([pd.read_csv(f) for f in cricket_files[:3]], ignore_index=True)
cricket_bowling_df = pd.concat([pd.read_csv(f) for f in cricket_files[3:]], ignore_index=True)
nba_df = pd.concat([pd.read_csv(f) for f in nba_files], ignore_index=True)
football_df = pd.concat([pd.read_csv(f) for f in football_files], ignore_index=True)

# Initialize Dash App
app = dash.Dash(__name__, suppress_callback_exceptions=True)
server = app.server

# Main Dashboard Layout
app.layout = html.Div([
    html.H1("Multi-Sports Analytics Dashboard", style={'textAlign': 'center'}),
    dcc.RadioItems(
        id='sport-selection',
        options=[
            {'label': 'Cricket', 'value': 'cricket'},
            {'label': 'NBA', 'value': 'nba'},
            {'label': 'Football', 'value': 'football'}
        ],
        value='cricket',
        labelStyle={'display': 'block', 'textAlign': 'center'}
    ),
    html.Div(id='dashboard-content')
])

# Callback to Update Dashboard
@app.callback(
    Output('dashboard-content', 'children'),
    Input('sport-selection', 'value')
)
def update_dashboard(sport):
    if sport == 'cricket':
        return html.Div([
            html.H2("Cricket Analytics"),
            dcc.Dropdown(
                id='cricket-team',
                options=[{'label': team, 'value': team} for team in cricket_batting_df['Team'].unique()],
                value=cricket_batting_df['Team'].unique()[0]
            ),
            dcc.RadioItems(
                id='cricket-type',
                options=[
                    {'label': 'Batting', 'value': 'batting'},
                    {'label': 'Bowling', 'value': 'bowling'}
                ],
                value='batting',
                labelStyle={'display': 'inline-block', 'margin-right': '10px'}
            ),
            html.H3("Player Comparison"),
            html.Div(id='player-selection'),
            html.Div(id='cricket-content')  
        ])
    elif sport == 'nba':
        return html.Div([
            html.H2("NBA Team Analytics"),
            dcc.Dropdown(
                id='nba-team',
                options=[{'label': team, 'value': team} for team in nba_df['Team'].unique()],
                value=nba_df['Team'].unique()[0]
            ),
            html.Div(id='nba-content')
        ])
    elif sport == 'football':
        return html.Div([
            html.H2("Football Analytics"),
            dcc.Dropdown(
                id='football-team',
                options=[{'label': team, 'value': team} for team in football_df['Team Name'].unique()],
                value=football_df['Team Name'].unique()[0]
            ),
            html.Div(id='football-content')
        ])

# 📌 **Cricket Dashboard**
def cricket_dashboard():
    return html.Div([
        html.H2("Cricket Analytics"),
        dcc.Dropdown(
            id='cricket-team',
            options=[{'label': team, 'value': team} for team in cricket_batting_df['Team'].unique()],
            value=cricket_batting_df['Team'].unique()[0]
        ),
        dcc.RadioItems(
            id='cricket-type',
            options=[
                {'label': 'Batting', 'value': 'batting'},
                {'label': 'Bowling', 'value': 'bowling'}
            ],
            value='batting',
            labelStyle={'display': 'inline-block', 'margin-right': '10px'}
        ),
        html.H3("Player Comparison"),
        html.Div(id='player-selection'),
        html.Div(id='cricket-content')  
    ])

@app.callback(
    Output('player-selection', 'children'),
    [Input('cricket-team', 'value'),
     Input('cricket-type', 'value')]
)
def update_player_selection(selected_team, cricket_type):
    if cricket_type == 'batting':
        team_players = cricket_batting_df[cricket_batting_df['Team'] == selected_team]['Player'].unique()
    else:
        team_players = cricket_bowling_df[cricket_bowling_df['Team'] == selected_team]['Player'].unique()

    if len(team_players) == 0:
        return html.P("No players available for this team.")

    return html.Div([
        html.Label("Select Player (Section 1)"),
        dcc.Dropdown(
            id='player-1',
            options=[{'label': p, 'value': p} for p in team_players],
            value=team_players[0] if len(team_players) > 0 else None
        ),
        html.Label("Select Player (Section 2)"),
        dcc.Dropdown(
            id='player-2',
            options=[{'label': p, 'value': p} for p in team_players],
            value=team_players[1] if len(team_players) > 1 else None
        )
    ])

@app.callback(
    Output('cricket-content', 'children'),
    [Input('cricket-team', 'value'), 
     Input('cricket-type', 'value'),
     Input('player-1', 'value'),  # Dynamically generated
     Input('player-2', 'value')]  # Dynamically generated
)
def cricket_type_dashboard(selected_team, cricket_type, player1=None, player2=None):
    if not selected_team:
        raise PreventUpdate

    ctx = dash.callback_context
    input_ids = [inp['prop_id'].split('.')[0] for inp in ctx.triggered]

    if 'player-1' not in input_ids:
        player1 = None
    if 'player-2' not in input_ids:
        player2 = None
    if cricket_type == 'batting':
        batting_df = cricket_batting_df[cricket_batting_df['Team'] == selected_team]
        return html.Div([
            html.H3(f"{selected_team} - Batting Stats"),
            dcc.Graph(figure=px.bar(batting_df, x='Player', y='Runs', title="Total Runs")),
            dcc.Graph(figure=px.bar(batting_df, x='Player', y='Fours', title="Fours")),
            dcc.Graph(figure=px.bar(batting_df, x='Player', y='Sixes', title="Sixes")),
            dcc.Graph(figure=px.bar(batting_df, x='Player', y='Strike Rate', title="Strike Rate")),
            dcc.Graph(figure=px.bar(batting_df, x='Player', y='Average', title="Batting Average")),
            html.H4("Player Comparison"),
            dcc.Graph(figure=px.bar(batting_df[batting_df['Player'].isin([player1, player2])], x='Player', y='Runs', title="Runs Comparison")),
            dcc.Graph(figure=px.bar(batting_df[batting_df['Player'].isin([player1, player2])], x='Player', y='Fours', title="Fours Comparison")), 
            dcc.Graph(figure=px.bar(batting_df[batting_df['Player'].isin([player1, player2])], x='Player', y='Sixes', title="Sixes Comparison")),
            dcc.Graph(figure=px.bar(batting_df[batting_df['Player'].isin([player1, player2])], x='Player', y='Strike Rate', title="Strike Rate Comparison")), 
            dcc.Graph(figure=px.bar(batting_df[batting_df['Player'].isin([player1, player2])], x='Player', y='Average', title="Batting Average Comparison"))
        ])
    else:
        bowling_df = cricket_bowling_df[cricket_bowling_df['Team'] == selected_team]
        return html.Div([
            html.H3(f"{selected_team} - Bowling Stats"),
            dcc.Graph(figure=px.bar(bowling_df, x='Player', y='Wickets', title="Wickets")),
            dcc.Graph(figure=px.bar(bowling_df, x='Player', y='Economy', title="Economy")),
            dcc.Graph(figure=px.bar(bowling_df, x='Player', y='Bowling Average', title="Bowling Average")),
            html.H4("Player Comparison"),
            dcc.Graph(figure=px.bar(bowling_df[bowling_df['Player'].isin([player1, player2])], x='Player', y='Wickets', title="Wickets Comparison")),
            dcc.Graph(figure=px.bar(bowling_df[bowling_df['Player'].isin([player1, player2])], x='Player', y='Economy', title="Economy Comparison")),
            dcc.Graph(figure=px.bar(bowling_df[bowling_df['Player'].isin([player1, player2])], x='Player', y='Bowling Average', title="Bowling Average Comparison"))
        ])

# **NBA Callback**
@app.callback(
    Output('nba-content', 'children'),
    Input('nba-team', 'value')
)
def update_nba_dashboard(selected_team):
    team_df = nba_df[nba_df['Team'] == selected_team]
    return html.Div([
        html.H3(f"{selected_team} - NBA Stats"),
        dcc.Graph(figure=px.bar(team_df, x='Player', y='Points', title="Points")),
        dcc.Graph(figure=px.bar(team_df, x='Player', y='Assists', title="Assists")),
        dcc.Graph(figure=px.bar(team_df, x='Player', y='Rebounds', title="Rebounds")),
        dcc.Graph(figure=px.bar(team_df, x='Player', y='Steals', title="Steals")),
        dcc.Graph(figure=px.bar(team_df, x='Player', y='Blocks', title="Blocks"))
    ])

# 📌 Football Dashboard
def football_dashboard():
    return html.Div([
        html.H2("Football Analytics"),
        dcc.Dropdown(
            id='football-team',
            options=[{'label': team, 'value': team} for team in football_df['Team Name'].unique()],
            value=football_df['Team Name'].unique()[0]
        ),
        html.Div(id='football-content')
    ])

@app.callback(
    Output('football-content', 'children'),
    Input('football-team', 'value')
)
def update_football_dashboard(selected_team):
    team_df = football_df[football_df['Team Name'] == selected_team]

    return html.Div([
        html.H3(f"{selected_team} - Football Stats"),
        dcc.Graph(figure=px.bar(team_df, x='Player Name', y='Speed (m/s)', title="Speed")),
        dcc.Graph(figure=px.bar(team_df, x='Player Name', y='Pass Accuracy (%)', title="Pass Accuracy")),
        dcc.Graph(figure=px.bar(team_df, x='Player Name', y='Injury Risk (%)', title="Injury Risk", color='Player Name')),
        dcc.Graph(figure=px.bar(team_df, x='Player Name', y='Fatigue Level (%)', title="Fatigue Level", color='Player Name')),
        dcc.Graph(figure=px.bar(team_df, x='Player Name', y='Heatmap Coverage (%)', title="Heatmap Coverage")),
        dcc.Graph(figure=px.bar(team_df, x='Player Name', y='Ball Possession Time (s)', title="Ball Possession Time")),
        dcc.Graph(figure=px.bar(team_df, x='Player Name', y='Sprint Count', title="Sprint Count")),
        dcc.Graph(figure=px.bar(team_df, x='Player Name', y='Distance Covered (m)', title="Distance Covered")),
        dcc.Graph(figure=px.bar(team_df, x='Player Name', y='Optimal Substitution Time (min)', title="Optimal Substitution Time"))
    ])


# Run Server
if __name__ == '__main__':
    app.run_server(host='127.0.0.1', port=8050, debug=True)
