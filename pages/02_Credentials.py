# ============================================ CREDITS ============================================
# Author: ADOTRI Frimpong
# Mail: frimpong.adotri@efrei.net
# Streamlit App url: https://frimpong-adotri-01-dataviz-lab3-uber-app-vo4lvn.streamlit.app/
# =================================================================================================



# ============================================ MODULES IMPORT ============================================
import streamlit as st
import plotly.express as px
import pandas as pd
import snscrape.modules.twitter as twt

# ============================================ PAGE SETUP CONFIGURATION ===================================
st.set_page_config(
    page_title='Twitter NLP',
    layout="wide"
)

@st.cache_data
def stylish_page():
    st.sidebar.image("./images/twitter_icon.png")
    with open("style.css") as css:
        st.markdown(f"<style>{css.read()}</style>", unsafe_allow_html=True)
        st.sidebar.markdown("# <span style=\"color:white background:#48b4e3\" ><center>TWITTER FOR NLP <img src=\"https://img.icons8.com/fluency/154/verified-badge.png\" width=\"30\" height=\"30\"></img></center></span>", unsafe_allow_html=True)

# =========================================================================================================


# =========================================== FUNCTIONS ===========================================

@st.cache_data
def load_dataset(path:str):
    data = pd.read_csv(path)
    return data

@st.cache_data
def scrape_tweets(keywords:str, start:str, stop:str, maxTweets:int=50) -> pd.DataFrame:
    tweets_list = []
    for k,tweet in enumerate(twt.TwitterSearchScraper(f'{keywords} lang:en since:{start} until:{stop}').get_items()):
        if k>=maxTweets:
            break
        tweets_list.append([tweet.date, tweet.id, tweet.rawContent, tweet.user.username])
    data = pd.DataFrame(tweets_list, columns=['datetime', 'tweet_ID', 'text', 'username'])
    return data




@st.cache_data
def kpis(data:pd.DataFrame) -> None:
    st.markdown("---")
    st.markdown("### <span style=\"color:#2daae1\">Tweets KPIs</span>", unsafe_allow_html=True)
    data_sample = data.sample()
    lon, lat, day, hour  = st.columns(4)
    long_, lat_, day_, hour_ = data_sample["Lon"].values[0], data_sample["Lat"].values[0], data_sample["Day"].values[0], data_sample["Hour"].values[0]
    lon.metric(label="Longitude 🧭", value=long_, delta=round(data["Lon"].median()-long_, 3))  # delta = Différence entre la longitude sélectionnée et la longitude médiane
    lat.metric(label="Latitude 🧭", value=lat_, delta=round(data["Lat"].median()-lat_, 3))   # delta = Différence entre la latitude sélectionnée et la latitude médiane
    day.metric(label="Day 📆", value=day_, delta=int(data[data["Day"]==day_]["Day"].count()))   # delta = Nombre d'observations pour le jour sélectionné
    hour.metric(label="Hour ⏱", value=hour_, delta=int(data[data["Hour"]==hour_]["Hour"].count())) # delta = Nombre d'observations pour l'heure sélectionné
    st.markdown("---")
# ===================================================================================================

# =========================================== APP CODING ===========================================
def main():
    stylish_page()
    st.sidebar.markdown("***")
    st.markdown("# <span style=\"color:#2daae1\">CREDENTIALS</span>", unsafe_allow_html=True)
    st.markdown("***")
    st.markdown(f">**<span style=\"color:#2daae1\">SPECIAL THANKS TO</span>** :    **TALMATKADI Manissa**", unsafe_allow_html=True)
    st.markdown(f">**<span style=\"color:#2daae1\">AUTHOR</span>** :    **ADOTRI Frimpong**", unsafe_allow_html=True)
    st.markdown(f">**<span style=\"color:#2daae1\">RESSOURCES</span>** :", unsafe_allow_html=True)

    st.markdown(f"> >>**FROM MEDIUM : https://medium.com/machine-learning-mastery/sentiment-analysis-and-topic-modeling-of-tweets-on-ukrainerussia-war-e20a1dbca263**", unsafe_allow_html=True)
    st.markdown(f"> >>**FROM TEXTBLOB DOC :  https://textblob.readthedocs.io/en/dev/index.html**", unsafe_allow_html=True)
    st.markdown(f"> >>**FROM STREAMLIT DOC : https://docs.streamlit.io**", unsafe_allow_html=True)
    st.markdown(f"> >>**FROM GITHUB : https://github.com/Smartking1**", unsafe_allow_html=True)
    st.markdown("***")
    st.markdown(f"## <span style=\"color:#2daae1\"><center> © Copyright March 2023 </center></span>", unsafe_allow_html=True)
            

    
# ==================================================================================================
if __name__ == "__main__":
    main()