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
import re
import datetime
# =========================================================================================================


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
def scrape_tweets(username:str, start:str, stop:str, maxTweets:int=50) -> pd.DataFrame:
    tweets_list = []
    for k,tweet in enumerate(twt.TwitterSearchScraper(f'from:{username} since:{start} until:{stop}').get_items()):
        if k>=maxTweets:
            break
        tweets_list.append([tweet.date, tweet.id, tweet.rawContent, tweet.user.username, tweet.likeCount, tweet.retweetCount, tweet.replyCount, tweet.quoteCount, tweet.url])
    data = pd.DataFrame(tweets_list, columns=['datetime', 'tweet_ID', 'text', 'username', 'likes', 'retweets', 'replies', 'quotes', 'url'])
    return data


# Function which appreciate the engagement rate
def appreciation(rate):
  assert rate >=0, "the rate must be a positive value !"
  if rate>=0 and rate<0.005:
    return "Twitter engagement rate <span style=\"color:red\">needs improvement</span> !"
  elif rate>0.005 and rate<0.037:
    return "Twitter engagement rate is <span style=\"color:orange\">not bad</span> !"
  elif rate>=0.037 and rate<0.098:
    return "Twitter engagement rate is <span style=\"color:#28b24d\">good</span> !"
  else:
    return "Twitter engagement rate is awesome !"


@st.cache_data
def kpis(data:pd.DataFrame, username:str) -> None:
    st.markdown("---")
    st.markdown("### <span style=\"color:#2daae1\">Tweets KPIs</span>", unsafe_allow_html=True)
    if len(data)==0:
        st.warning("WARNING : No Data found !", icon="⚠️")
    else:
        likes, retweets, replies, quotes  = st.columns(4)
        likes_, retweets_, replies_, quotes_ = data.likes.mean(), data.retweets.mean(), data.replies.mean(), data.quotes.mean()
        likes.metric(label="Mean of likes ❤️", value=round(likes_))  # delta = Différence entre la longitude sélectionnée et la longitude médiane
        retweets.metric(label="Mean of retweets 🔁", value=round(retweets_))   # delta = Différence entre la latitude sélectionnée et la latitude médiane
        replies.metric(label="Mean of replies  💬", value=round(replies_))   # delta = Nombre d'observations pour le jour sélectionné
        quotes.metric(label="Mean of quotes  🖇", value=round(quotes_)) # delta = Nombre d'observations pour l'heure sélectionné
        st.markdown("***")
        likes, retweets = data.likes.sum(), data.retweets.sum()
        replies, quotes = data.replies.sum(), data.quotes.sum()
        number_of_tweets = data.shape[0]
        number_of_followers = twt.TwitterUserScraper(username).entity.followersCount
        engagement_rate = (((likes+retweets+replies+quotes)/number_of_tweets)/number_of_followers)*100
        st.markdown("### <span style=\"color:#2daae1\">Engagement rate</span>", unsafe_allow_html=True)
        median, rate = st.columns(2)
        median.metric(label="Twitter median engagement rate", value="0.037 %")
        rate.metric(label=f"@{username}'s engagement rate", value=f"{engagement_rate:.5f} %", delta=f"{engagement_rate-0.037:.5f} %")
        st.markdown("---")
        st.markdown(f"## <span style=\"color:#2daae1\"><center>{appreciation(engagement_rate)}</center></span>", unsafe_allow_html=True)
        st.markdown("---")
        
        retweets_fig = px.line(data.sort_values(by="datetime"), x="datetime", y="retweets")
        quotes_fig = px.line(data.sort_values(by="datetime"), x="datetime", y="quotes")
        replies_fig = px.line(data.sort_values(by="datetime"), x="datetime", y="replies")
        likes_fig = px.line(data.sort_values(by="datetime"), x="datetime", y="likes")
        most_liked = data[data.likes==data.likes.max()].sample()
        most_retweeted = data[data.retweets==data.retweets.max()].sample()
        most_quoted = data[data.quotes==data.quotes.max()].sample()
        most_replied = data[data.replies==data.replies.max()].sample()
        st.write(f">**<span style=\"color:#2daae1\">MOST LIKED TWEET</span>** : **\"{most_liked.text.values}\"** : ({most_liked.url.values})", unsafe_allow_html=True)
        st.write(f">**<span style=\"color:#2daae1\">MOST RETWEETED TWEET</span>** : **\"{most_retweeted.text.values}\"** : ({most_retweeted.url.values})", unsafe_allow_html=True)
        st.write(f">**<span style=\"color:#2daae1\">MOST QUOTED TWEET</span>** : **\"{most_quoted.text.values}\"** : ({most_quoted.url.values})", unsafe_allow_html=True)
        st.write(f">**<span style=\"color:#2daae1\">MOST REPLIED TWEET</span>** : **\"{most_replied.text.values}\"** : ({most_replied.url.values})", unsafe_allow_html=True)
        st.markdown("### <span style=\"color:#2daae1\">Likes evolution</span>", unsafe_allow_html=True)
        st.write(likes_fig)
        st.markdown("#### <span style=\"color:#2daae1\">Replies evolution</span>", unsafe_allow_html=True)
        st.write(replies_fig)
        st.markdown("#### <span style=\"color:#2daae1\">Quotes evolution</span>", unsafe_allow_html=True)
        st.write(quotes_fig)
        st.markdown("#### <span style=\"color:#2daae1\">Retweets evolution</span>", unsafe_allow_html=True)
        st.write(retweets_fig)
        #stats_fig = likes_fig.add_traces(replies_fig.data[0]).add_traces(retweets_fig.data[0]).add_traces(quotes_fig.data[0])
        #st.write(stats_fig)


@st.cache_data
def getEntityProfile(username:str) -> None:
    entity = twt.TwitterUserScraper(username).entity
    if entity == None:
        st.warning("WARNING : No Twitter user found !", icon="⚠️")
    else:
        picture = entity.profileImageUrl
        name, nbFollowers, creation = entity.displayname, entity.followersCount, entity.created
        verified = "No" if entity.verified==False else "Yes"
        pictureBox, infoBox = st.columns(2)
        with pictureBox:
            st.image(re.sub("normal", "400x400", picture))   # Picture resizing
        with infoBox:
            st.markdown(f">**<span style=\"color:#2daae1\">DISPLAY NAME</span>** :    **{name}**", unsafe_allow_html=True)
            st.markdown(f">**<span style=\"color:#2daae1\">ACCOUNT CREATION</span>** : **{creation.date()}**", unsafe_allow_html=True)
            st.write(f">**<span style=\"color:#2daae1\">FOLLOWERS</span>** : **{nbFollowers}**", unsafe_allow_html=True)
            if verified == "Yes":
                st.markdown(f">**<span style=\"color:#2daae1\">CERTIFIED</span>** : **{verified}** <img src=\"https://img.icons8.com/fluency/154/verified-badge.png\" width=\"20\" height=\"20\"></img>", unsafe_allow_html=True)
            else:
                st.markdown(f">**<span style=\"color:#2daae1\">CERTIFIED</span>** : **{verified}**", unsafe_allow_html=True)

# ===================================================================================================


# =========================================== APP CODING ===========================================
def main():
    stylish_page()
    st.sidebar.markdown("***")
    st.markdown("# <span style=\"color:#2daae1\">FOLLOWERS ENGAGMENT</span>", unsafe_allow_html=True)
    st.markdown("***")
    st.sidebar.markdown("##### <span style=\"color:#2daae1\">LET'S FIND THE FOLLOWERS ENGAGEMENT !</span> 🙃", unsafe_allow_html=True)
    number = st.sidebar.slider("Number of tweets :", min_value=10, max_value=1000)
    twittos = st.sidebar.text_input("Enter the personality username :", placeholder="Ex: Arkunir")
    start = st.sidebar.date_input("Start date :", min_value=pd.to_datetime("2007-01-01"))
    end = st.sidebar.date_input("End date :", min_value=start)
    if st.sidebar.button("Execute", key="scraping"):
        if twittos=="":
            st.warning("WARNING : No twittos name entered !", icon="⚠️")
        else:
            st.markdown("### <span style=\"color:#2daae1\">**Tweets scraped**</span>", unsafe_allow_html=True)
            tweets = scrape_tweets(username=twittos, start=start, stop=end, maxTweets=number)
            st.dataframe(tweets)
            st.markdown("***")
            st.markdown("### <span style=\"color:#2daae1\">**Profile**</span>", unsafe_allow_html=True)
            getEntityProfile(twittos)
            kpis(tweets, twittos)
            #st.markdown("***")
        

# ==================================================================================================

if __name__ == "__main__":
    main()