import streamlit as st 
import pandas as pd 
import json
from mplsoccer import VerticalPitch

@st.cache_resource
def load_data():
    df = pd.read_csv('euros_2024_shot_map(1).csv')
    df = df[df['type'] == 'Shot'].reset_index(drop=True)
    df['location'] = df['location'].apply(json.loads)
    return df

@st.cache_data
def get_teams(df):
    return df['team'].sort_values().unique()

@st.cache_data
def get_players(df, team):
    return df[df['team'] == team]['player'].sort_values().unique()

st.title("Euro 2024 Shots Map")
st.subheader('Filter to any team/player to see all the shots that were taken')

# Load the data once
df = load_data()

# Get teams
teams = get_teams(df)

# Team selection
team = st.selectbox('Select a team', teams, index=None)

# Get players for the selected team
if team:
    players = get_players(df, team)
    player = st.selectbox('Select a player', players, index=None)
else:
    player = None

# Filter data based on selections
filtered_df = df[df['team'] == team]
if player:
    filtered_df = filtered_df[filtered_df['player'] == player]

# Limit number of shots for visualization
LIMIT = 100  # Adjust this limit as necessary
filtered_df = filtered_df.head(LIMIT)

# Prepare the pitch
pitch = VerticalPitch(pitch_type='statsbomb', half=True)
fig, ax = pitch.draw(figsize=(10, 10))

# Plot shots function
def plot_shots(df, ax, pitch):
    for x in df.to_dict(orient='records'):
        pitch.scatter(
            x=float(x['location'][0]),
            y=float(x['location'][1]),
            ax=ax,
            s=1000 * x['shot_statsbomb_xg'],
            color='green' if x['shot_outcome'] == 'Goal' else 'white',
            edgecolors='black',
            alpha=1 if x['shot_outcome'] == 'Goal' else 0.5,
            zorder=2 if x['shot_outcome'] == 'Goal' else 1 
        )

# Plot the shots if there are any
if not filtered_df.empty:
    plot_shots(filtered_df, ax, pitch)

# Display the plot
st.pyplot(fig)
