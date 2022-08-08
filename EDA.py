import streamlit as st
import pandas as pd
import numpy as np
import base64
import seaborn as sns
import matplotlib.pyplot as plt


st.title("NBA Player Stats Explorer")

st.markdown(
    """This App performs web scrapping of NBA playeer stats and visualizes the data using Streamlit.""")
(""" * **Python libraries:** pandas, numpy, seaborn, matplotlib.pyplot, streamlit""")
("""* **Data Source:** [NBA.com](https://www.nba.com/) 
            """)
st.sidebar.header("User Input Features")
selected_year = st.sidebar.selectbox('Year', list(reversed(range(1990, 2022))))


@st.cache
def load_data(year):
    url = "https://www.basketball-reference.com/leagues/NBA_" + \
        str(year) + "_per_game.html"
    df = pd.read_html(url)[0]
    raw = df.drop(df[df.Age == 'Age'].index)
    raw = raw.drop(raw[raw.Tm == 'Tm'].index)
    raw = raw.fillna(0)
    playerstats = raw.drop(['RK'], axis=1)
    return raw


playerstats = load_data(selected_year)
# playerstats

sorted_unique_teams = sorted(playerstats['Tm'].unique())
selected_team = st.sidebar.multiselect("Team", sorted_unique_teams)


unique_pos = playerstats['Pos'].unique()
selected_pos = st.sidebar.multiselect("Position", unique_pos)

df_selected_team = playerstats[playerstats['Tm'].isin(selected_team)]







