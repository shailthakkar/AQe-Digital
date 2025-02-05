import dash
from dash import dcc, html, Input, Output
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
from plotly.subplots import make_subplots
from flask import Flask, jsonify, request
from flask_cors import CORS
import random


X = pd.read_csv('merged_mega.csv')

# Maintain a list of name of players
player_names = X['PlayerName'].unique()

def get_player_data(player, table):
    X = table.copy()

    temp = X[X['PlayerName'] == player]
    temp.sort_values(by=['Season', 'HomerunsOfSeasonSoFar'], ascending=True, inplace=True)
    temp.reset_index(drop=True, inplace=True)

    # Plot ExitVelocity of the player's shots
    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=temp['HomerunsOfSeasonSoFar'],
        y=temp['ExitVelocity'],
        mode='lines+markers',
        line=dict(color='blue'),
        name='Exit Velocity',
        marker=dict(color=temp['Season'], showscale=True)
    ))

    fig.update_layout(
        title='Shot Speed Consistency',
        xaxis_title='Season Progress',
        yaxis_title='Speed of Shots',
        legend_title="Season"
    )

    fig.show()

    # Homerun Counts Plot (Pie chart)
    homerun_counts = temp.groupby('Season')['HomerunsOfSeasonSoFar'].max().to_dict()
    labels = list(homerun_counts.keys())
    sizes = list(homerun_counts.values())

    fig = go.Figure(data=[go.Pie(labels=labels, values=sizes, marker_colors=['red', 'blue', 'green'])])
    fig.update_layout(title="Homerun Consistency Over the Seasons")
    fig.show()

    # Hit Distance Plot (Histogram)
    fig = px.histogram(temp, x='HitDistance', nbins=20, title='Distance Travelled by the Ball')
    fig.update_layout(xaxis_title='Distance (in m)', yaxis_title='Frequency')
    fig.show()

    # Shot Direction vs Hit Distance (Bar Plot)
    fig = px.bar(temp, x='ShotDirection', y='HitDistance', color='ShotDirection',
                title='Shot Direction vs Ball Distance', color_continuous_scale='Viridis')
    fig.update_layout(xaxis_title='Direction', yaxis_title='Distance Covered by Ball')
    fig.show()

def get_best_player_data(given_table):
    table = given_table.copy()
    table.sort_values(by=['MaxHomeruns', 'PlayerName', 'ExitVelocity', 'HitDistance'], ascending=False, inplace=True)
    table.reset_index(drop=True, inplace=True)
    best_player = table['PlayerName'].iloc[0]

    return best_player


def make_comparisons(given_table, player):
    table = given_table.copy()

    temporary = table[table['PlayerName'] == player]
    temporary.sort_values(by=['Season', 'HomerunsOfSeasonSoFar'], ascending=True, inplace=True)
    temporary['HomerunsOfSeasonSoFar'] = range(1, len(temporary) + 1)
    temporary.reset_index(drop=True, inplace=True)

    # Get the best player data first
    best_player = get_best_player_data(given_table)
    temporary_best = table[table['PlayerName'] == best_player]
    temporary_best.sort_values(by=['Season', 'HomerunsOfSeasonSoFar'], ascending=True, inplace=True)
    temporary_best['HomerunsOfSeasonSoFar'] = range(1, len(temporary_best) + 1)
    temporary_best.reset_index(drop=True, inplace=True)

    mix_table = pd.concat([temporary, temporary_best], axis=0)
    mix_table.reset_index(drop=True, inplace=True)
    player_max_hit_distance = mix_table.groupby('PlayerName')['HitDistance'].max().reset_index()

    # Exit Velocity Comparison Plot
    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=temporary_best['HomerunsOfSeasonSoFar'],
        y=temporary_best['ExitVelocity'],
        mode='lines+markers',
        name=best_player,
        line=dict(color='blue')
    ))

    fig.add_trace(go.Scatter(
        x=temporary['HomerunsOfSeasonSoFar'],
        y=temporary['ExitVelocity'],
        mode='lines+markers',
        name=player,
        line=dict(color='red')
    ))

    fig.update_layout(
        title=f'Exit Velocity Comparison with Best Player',
        xaxis_title='Season Progress',
        yaxis_title='Speed of Shots',
        legend_title="Player"
    )
    fig.show()

    # Maximum Hit Distance Comparison Plot
    fig = px.bar(player_max_hit_distance, x='PlayerName', y='HitDistance',
                title='Maximum Hit Distance Comparison with Best Player')
    fig.update_layout(xaxis_title='Player Name', yaxis_title='Maximum Hit Distance')
    fig.show()


def player_performance(player, table):
    X = table.copy()
    X_speed = X.sort_values(by=['ExitVelocity'], ascending=False)
    X_speed.reset_index(drop=True, inplace=True)
    X_dist = X.sort_values(by=['HitDistance'], ascending=False)
    X_dist.reset_index(drop=True, inplace=True)
    X_pow = X.sort_values(by=['MeanPowerOfTheShot'], ascending=False)
    X_pow.reset_index(drop=True, inplace=True)

    temp = X[X['PlayerName'] == player]
    temp.sort_values(by=['Season', 'HomerunsOfSeasonSoFar'], ascending=True, inplace=True)
    temp.reset_index(drop=True, inplace=True)

    # Player stats
    exit_velocity = temp.iloc[0]['MeanExitVel']
    max_exit_velocity = X_speed.iloc[0]['ExitVelocity']

    max_hit_distance = X_dist.iloc[0]['HitDistance']
    mean_hit_distance = temp.iloc[0]['MeanHitDist']

    mean_power = temp.iloc[0]['MeanPowerOfTheShot']
    max_power = X_pow.iloc[0]['MeanPowerOfTheShot']

    # Create subplots for performance gauges
    fig = make_subplots(rows=1, cols=3,
                    specs=[[{'type': 'indicator'}, {'type': 'indicator'}, {'type': 'indicator'}]])

    # Exit Velocity Gauge
    fig.add_trace(go.Indicator(
        mode="gauge+number",
        value=exit_velocity,
        title={'text': "Mean Exit Velocity (m/s)", 'font': {'size': 14}},
        gauge={
            'axis': {'range': [0, max_exit_velocity]},
            'bar': {'color': "#000090"},
            'steps': [{'range': [0, max_exit_velocity], 'color': "lightgray"}],
            'threshold': {
                'line': {'color': "red", 'width': 4},
                'thickness': 0.75,
                'value': exit_velocity
            }
        }
    ), row=1, col=1)

    # Mean Hit Distance Gauge
    fig.add_trace(go.Indicator(
        mode="gauge+number",
        value=mean_hit_distance,
        title={'text': "Mean Hit Distance (m)", 'font': {'size': 14}},
        gauge={
            'axis': {'range': [0, max_hit_distance]},
            'bar': {'color': "#000090"},
            'steps': [{'range': [0, max_hit_distance], 'color': "lightgray"}],
            'threshold': {
                'line': {'color': "red", 'width': 4},
                'thickness': 0.75,
                'value': mean_hit_distance
            }
        }
    ), row=1, col=2)

    # Mean Power Gauge
    fig.add_trace(go.Indicator(
        mode="gauge+number",
        value=mean_power,
        title={'text': "Mean Power (kJ)", 'font': {'size': 14}},
        gauge={
            'axis': {'range': [0, max_power]},
            'bar': {'color': '#000090'},
            'steps': [{'range': [0, max_power], 'color': 'lightgray'}],
            'threshold': {
                'line': {'color': "red", 'width': 4},
                'thickness': 0.75,
                'value': mean_power
            }
        }
    ), row=1, col=3)

    fig.update_layout(title_text=f"{player}'s Performance Metrics", height=400, width=1000)
    fig.show()

app = Flask(__name__)
CORS(app)


# Load your dataset (Replace with actual file path or database query)
df = X

# Initialize Dash app
d_app = dash.Dash(__name__, server=app, url_base_pathname='/dashboard/')

# , server=app, url_base_pathname='/dashboard/'

# Define the app layout
d_app.layout = html.Div([
    html.Div([
    html.H1("Baseball Player Performance Dashboard", style={'textAlign': 'center', 'fontSize': '32px', 'fontWeight': 'bold', 'color': 'white', 'backgroundColor': '#121A22', 'marginBottom': '0px', 'padding': '10px 0'}),

    # Dropdown for selecting a player
    dcc.Dropdown(
        id='player-dropdown',
        options=[{'label': name, 'value': name} for name in player_names],
        value=player_names[0],  # Default player
        clearable=False,
        style={'width': '50%', 'margin': '0 auto', 'fontSize': '22px', 'height': '50px', 'borderRadius': '8px', 'backgroundColor': '#121A22'})
    ], style={'backgroundColor': '#121A22', 'padding': '0px', 'margin': '0px'}),

    # First Row (Performance Metrics - Centered)
    html.Div([
        dcc.Graph(id='performance-metrics', style={'width': '100%', 'margin': 'auto'}),
    ], style={'display': 'flex', 'justify-content': 'center', 'backgroundColor': '#121A22',  'padding': '20px'}),

    # Second Row (Hit Distance Histogram on Left & Pie Chart on Right)
    html.Div([
        dcc.Graph(id='hit-distance-histogram', style={'width': '49%', 'display': 'inline-block'}),
        dcc.Graph(id='homerun-pie-chart', style={'width': '49%', 'display': 'inline-block'}),
    ], style={'display': 'flex', 'justify-content': 'space-between', 'padding': '20px'}),

    # Third Row (Exit Velocity - Full Width)
    html.Div([
        dcc.Graph(id='exit-velocity-graph', style={'width': '100%'}),
    ], style={'textAlign': 'center', 'padding': '20px'}),

    # Fourth Row (Comparison Graph - Full Width)
    html.Div([
        dcc.Graph(id='comparison-graph', style={'width': '100%'}),
    ], style={'textAlign': 'center', 'padding': '20px'}),

    # Fifth Row (Custom Graph on Left & Shot Direction on Right)
    html.Div([
        dcc.Graph(id='compare-hit-distance-bar', style={'width': '49%', 'display': 'inline-block'}),
        dcc.Graph(id='shot-direction-bar', style={'width': '49%', 'display': 'inline-block'}),
    ], style={'display': 'flex', 'justify-content': 'space-between', 'padding': '20px'}),
])


# Define callback to update plots based on selected player
@d_app.callback(
    [
        Output('exit-velocity-graph', 'figure'),
        Output('homerun-pie-chart', 'figure'),
        Output('hit-distance-histogram', 'figure'),
        Output('shot-direction-bar', 'figure'),
        Output('comparison-graph', 'figure'),
        Output('performance-metrics', 'figure'),
        Output('compare-hit-distance-bar', 'figure')  # Placeholder for any additional graph
    ],
    [Input('player-dropdown', 'value')]
)

def update_plots(player):
    temp = df[df['PlayerName'] == player].copy()
    if temp.empty:
        # Handle case where player data is not found
        return go.Figure(), go.Figure(), go.Figure(), go.Figure(), go.Figure(), go.Figure(), go.Figure()

    temp.sort_values(by=['Season', 'HomerunsOfSeasonSoFar'], ascending=True, inplace=True)
    temp.reset_index(drop=True, inplace=True)

    X = df.copy()
    X_speed = X.sort_values(by=['ExitVelocity'], ascending=False)
    X_speed.reset_index(drop=True, inplace=True)
    X_dist = X.sort_values(by=['HitDistance'], ascending=False)
    X_dist.reset_index(drop=True, inplace=True)
    X_pow = X.sort_values(by=['MeanPowerOfTheShot'], ascending=False)
    X_pow.reset_index(drop=True, inplace=True)

    # Handle potential NaN values
    exit_velocity = temp.iloc[0]['MeanExitVel'] if not pd.isna(temp.iloc[0]['MeanExitVel']) else 0
    max_exit_velocity = X_speed.iloc[0]['ExitVelocity'] if not pd.isna(X_speed.iloc[0]['ExitVelocity']) else 100

    max_hit_distance = X_dist.iloc[0]['HitDistance'] if not pd.isna(X_dist.iloc[0]['HitDistance']) else 100
    mean_hit_distance = temp.iloc[0]['MeanHitDist'] if not pd.isna(temp.iloc[0]['MeanHitDist']) else 0

    mean_power = temp.iloc[0]['MeanPowerOfTheShot'] if not pd.isna(temp.iloc[0]['MeanPowerOfTheShot']) else 0
    max_power = X_pow.iloc[0]['MeanPowerOfTheShot'] if not pd.isna(X_pow.iloc[0]['MeanPowerOfTheShot']) else 100
    
    temp['EvConsistencyPr'] = (100 - round((temp['PlayerEvVariance'] / exit_velocity) * 100, 2))
    shot_speed_consistency_val = (100 - temp['EvConsistencyPr'].max())
    if shot_speed_consistency_val >= 0:
        shot_speed_consistency_percentage = shot_speed_consistency_val
    else:
        shot_speed_consistency_percentage = 0

    # Exit Velocity Plot
    fig1 = go.Figure()
    fig1.add_trace(go.Scatter(
        x=temp['HomerunsOfSeasonSoFar'],
        y=temp['ExitVelocity'],
        mode='lines+markers',
        line=dict(color='blue'),
        name='Exit Velocity',
        marker=dict(color=temp['Season'], showscale=True)
    ))
    fig1.update_layout(title='Shot Speed Consistency', xaxis_title='Season Progress', yaxis_title='Speed of Shots', font=dict(size=18), height=500, width=1113.11)

    # Homerun Pie Chart
    homerun_counts = temp.groupby('Season')['HomerunsOfSeasonSoFar'].max().to_dict()
    fig2 = go.Figure(data=[go.Pie(labels=list(homerun_counts.keys()), values=list(homerun_counts.values()))])
    fig2.update_layout(title="Homerun Consistency Over the Seasons", font=dict(size=18), height=500, width=1113.11)

    # Hit Distance Histogram
    fig3 = px.histogram(temp, x='HitDistance', nbins=20, title='Distance Travelled by the Ball')
    fig3.update_layout(xaxis_title='Distance (in m)', yaxis_title='Frequency', font=dict(size=18), height=500, width=1113.11)

    # Shot Direction vs Hit Distance Bar Plot
    fig4 = px.bar(temp, x='ShotDirection', y='HitDistance', color='ShotDirection', title='Shot Direction vs Ball Distance')
    fig4.update_layout(font=dict(size=18), height=500, width=1113.11)

    # Comparison with Best Player
    best_player = df.sort_values(by=['MaxHomeruns', 'PlayerName', 'ExitVelocity', 'HitDistance'], ascending=False)['PlayerName'].iloc[0]
    temp_best = df[df['PlayerName'] == best_player].copy()
    temp_best.sort_values(by=['Season', 'HomerunsOfSeasonSoFar'], ascending=True, inplace=True)

    fig5 = go.Figure()
    fig5.add_trace(go.Scatter(x=temp_best['HomerunsOfSeasonSoFar'], y=temp_best['ExitVelocity'], mode='lines+markers', name=best_player, line=dict(color='blue')))
    fig5.add_trace(go.Scatter(x=temp['HomerunsOfSeasonSoFar'], y=temp['ExitVelocity'], mode='lines+markers', name=player, line=dict(color='red')))
    fig5.update_layout(title=dict(text=f'Exit Velocity Comparison with Best Player', font=dict(size=18)), xaxis_title='Season Progress', yaxis_title='Speed of Shots', legend=dict(font=dict(size=18)), height=500, width=1113.11)

    # Player Performance Metrics
    fig6 = make_subplots(rows=1, cols=4, specs=[[
        {'type': 'indicator'}, {'type': 'indicator'}, {'type': 'indicator'}, {'type': 'indicator'}
    ]])
    fig6.add_trace(go.Indicator(mode="gauge+number", value=exit_velocity, title={'text': "Mean Exit Velocity"},
                                gauge={
            'axis': {'range': [0, max_exit_velocity]},
            'bar': {'color': "#000090"},
            'steps': [{'range': [0, max_exit_velocity], 'color': "lightgray"}],
            'threshold': {
                'line': {'color': "red", 'width': 4},
                'thickness': 0.75,
                'value': exit_velocity
            }
        }), row=1, col=1)
    fig6.add_trace(go.Indicator(mode="gauge+number", value=mean_hit_distance, title={'text': "Mean Hit Distance"},
                                gauge={
            'axis': {'range': [0, max_hit_distance]},
            'bar': {'color': "#000090"},
            'steps': [{'range': [0, max_hit_distance], 'color': "lightgray"}],
            'threshold': {
                'line': {'color': "red", 'width': 4},
                'thickness': 0.75,
                'value': mean_hit_distance
            }
        }), row=1, col=2)
    fig6.add_trace(go.Indicator(mode="gauge+number", value=mean_power, title={'text': "Mean Power"},
                                gauge={
            'axis': {'range': [0, max_power]},
            'bar': {'color': "#000090"},
            'steps': [{'range': [0, max_power], 'color': "lightgray"}],
            'threshold': {
                'line': {'color': "red", 'width': 4},
                'thickness': 0.75,
                'value': mean_power
            }
        }), row=1, col=3)
    fig6.add_trace(go.Indicator(mode="gauge+number", value=temp.iloc[0]['EvConsistencyPr'], title={'text': "Shot Speed Consistency (%)"},
                                gauge={
            'axis': {'range': [0, 100]},
            'bar': {'color': "#000090"},
            'steps': [{'range': [0, 100], 'color': "lightgray"}],
            'threshold': {
                'line': {'color': "red", 'width': 4},
                'thickness': 0.75,
                'value': (100 - shot_speed_consistency_percentage)
            }
        }), row=1, col=4)
    fig6.update_layout(grid={'rows': 1, 'columns': 3}, height=300, width=1325, font=dict(size=18))

    temp = df[df['PlayerName'] == player].copy()
    temp.sort_values(by=['Season', 'HomerunsOfSeasonSoFar'], ascending=True, inplace=True)

    # Get best player data
    best_player = get_best_player_data(df)
    temp_best = df[df['PlayerName'] == best_player].copy()
    temp_best.sort_values(by=['Season', 'HomerunsOfSeasonSoFar'], ascending=True, inplace=True)

    # Maximum Hit Distance Comparison Plot
    mix_table = pd.concat([temp, temp_best], axis=0)
    player_max_hit_distance = mix_table.groupby('PlayerName')['HitDistance'].max().reset_index()
    fig7 = px.bar(player_max_hit_distance, x='PlayerName', y='HitDistance', title='Maximum Hit Distance Comparison with Best Player')
    fig7.update_layout(xaxis_title='Player Name', yaxis_title='Maximum Hit Distance', font=dict(size=18), height=500, width=1113.11)

    return fig6, fig1, fig5, fig7, fig4, fig2, fig3

def best_commentary(player):
    temp = df[df['PlayerName'] == player].copy()
    
    temp.sort_values(by=['Season', 'HitDistance', 'ExitVelocity'], ascending=False, inplace=True)
    temp.reset_index(drop=True, inplace=True)
    commentary = [
        f'An exceptional shot by {player}. The ball’s velocity was approximately {temp["ExitVelocity"].iloc[0]} meters per second, propelling it a distance of {temp["HitDistance"].iloc[0]} meters. The ball subsequently entered the {temp["ShotDirection"].iloc[0]}.',
        f'{player} shots the ball {temp["HitDistance"].iloc[0]} m far in the {temp["ShotDirection"].iloc[0]} at a speed of {temp["ExitVelocity"].iloc[0]} m/s. The ball flies into the {temp["ShotDirection"].iloc[0]}.',
        f'The ball goes in the {temp["ShotDirection"].iloc[0]} at the speed of {temp["ExitVelocity"].iloc[0]} m/s, with an incredible launch angle of {temp["LaunchAngle"].iloc[0]} by {player}.'
        ]
    return temp["video"].iloc[0], random.choice(commentary)

@app.route('/api/players', methods=['GET'])
def get_players():
    player_names = df['PlayerName'].unique().tolist()
    return jsonify(player_names)

@app.route('/api/best-commentary', methods=['GET'])
def get_best_commentary():
    player = request.args.get('player')
    if not player:
        return jsonify({"error": "Player name is required"}), 400

    video_link, commentary = best_commentary(player)
    return jsonify({
        "video_link": video_link,
        "commentary": commentary
    })

@app.route('/api/dashboard.json', methods=['GET'])
def get_dashboard_json():
    player = request.args.get('player')
    if not player:
        return jsonify({"error": "Player name is required"}), 400

    figures = update_plots(player)
    if not figures:
        return jsonify({"error": "No data found for the player"}), 404

    # Convert figures to JSON
    figures_json = [fig.to_json() for fig in figures]

    return jsonify({
        "dashboard": figures_json
    })


# Run the app
if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True, port=8000)
    
# host="0.0.0.0", debug=True, port=8000
