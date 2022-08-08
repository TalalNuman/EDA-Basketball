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
    raw = raw.fillna(0)
    playerstats = raw.drop(['Rk'], axis=1)
    return playerstats


playerstats = load_data(selected_year)
# playerstats

sorted_unique_teams = sorted(playerstats['Tm'].unique())
selected_team = st.sidebar.multiselect(
    "Team", sorted_unique_teams, sorted_unique_teams)


unique_pos = playerstats['Pos'].unique()
selected_pos = st.sidebar.multiselect("Position", unique_pos, unique_pos)
df_selected_team = playerstats[(playerstats.Tm.isin(
    selected_team)) & (playerstats.Pos.isin(selected_pos))]

st.header("Player Stats of Selected Teams")
st.write('Data Dimension: ',
         df_selected_team.shape[0], 'rows and', df_selected_team.shape[1], "columns")

st.dataframe(df_selected_team.astype(str))

def filedownload(df):
    csv = df.to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode()  # strings <-> bytes conversions
    href = f'<a href="data:file/csv;base64,{b64}" download="playerstats.csv">Download CSV File</a>'
    return href

st.markdown(filedownload(df_selected_team), unsafe_allow_html=True)

if st.button('Intercorrelation Heatmap'):
    st.header('Intercorrelation Matrix Heatmap')
    df_selected_team.to_csv('output.csv',index=False)
    df = pd.read_csv('output.csv')

    corr = df.corr()
    mask = np.zeros_like(corr)
    mask[np.triu_indices_from(mask)] = True
    with sns.axes_style("white"):
        f, ax = plt.subplots(figsize=(7, 5))
        ax = sns.heatmap(corr, mask=mask, vmax=1, square=True)
    st.pyplot()





