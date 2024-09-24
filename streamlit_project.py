import streamlit as st 
import pandas as pd 
import json
from mplsoccer import VerticalPitch

# Caching the data loading
@st.cache_data
def load_data():
    df = pd.read_csv('euros_2024_shot_map(1).csv')
    df = df[df['type'] == 'Shot'].reset_index(drop=True)
    df['location'] = df['location'].apply(json.loads)
    return df

st.title("Euro 2024 Shots Map")
st.subheader('Filter to any team/player to see all the shots that were taken')

# Load the data once and cache it
df = load_data()

# Team selection
team = st.selectbox('Select a team', df['team'].sort_values().unique(), index=None)

# Filter by team first
filtered_team_df = df[df['team'] == team] if team else df

# Player selection
player = st.selectbox('Select a player', filtered_team_df['player'].sort_values().unique(), index=None)

# Further filter by player
filtered_df = filtered_team_df[filtered_team_df['player'] == player] if player else filtered_team_df

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

# Plot the shots
if not filtered_df.empty:
    plot_shots(filtered_df, ax, pitch)

# Display the plot
st.pyplot(fig)
