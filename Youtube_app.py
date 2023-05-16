import streamlit as st
import isodate
from st_aggrid import GridOptionsBuilder, AgGrid, GridUpdateMode, ColumnsAutoSizeMode


import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import seaborn as sns
#sns.set(style="darkgrid", color_codes=True)
st.set_page_config(layout="wide",)

st.title('Youtube channel statistics dashboard  :tv:')


st.header('Channel overview')
st.write(f""" This shows the youtube channels with the region code 'MN', source from the youtube api delayed a day""")

# for calling the youtube api

def build_youtube_client():
    api_service_name = 'youtube'
    api_version = 'v3'
    DEVELOPER_KEY = 'AIzaSyCpe4xFpaHG9PAf1NgMuf25sixxMz9BL38'
    
    youtube = googleapiclient.discovery.build(api_service_name, api_version, developerKey = DEVELOPER_KEY)
    
    return youtube

# function to get channel ids with the region code of MN
def get_channels(youtube):
    """
    Getting mongolian content creators with the search api
    Params:
    q = search string
    regionCode = region
    
    Output:
    a list of channel ids
    
    """
   
    request = youtube.search().list(
        part='snippet', 
        q = 'mongolian content', 
        maxResults = 50,
        type = 'video',
        regionCode = 'MN')
    
    response = request.execute() 
    channel_ids = []
    
    for i in range(len(response['items'])):
        channel_ids.append(response['items'][i]['snippet']['channelId'])
        
    next_page_token = response.get('nextPageToken')
    more_pages = True
    
    while more_pages:
        if next_page_token is None:
            more_pages = False
        else:
            request = youtube.search().list(
                part='snippet', 
                q = 'mongolian content', 
                maxResults = 50,
                type = 'video',
                regionCode = 'MN',
                pageToken = next_page_token)
            response = request.execute()
    
            for i in range(len(response['items'])):
                channel_ids.append(response['items'][i]['snippet']['channelId'])
            
            next_page_token = response.get('nextPageToken')
    
    return channel_ids

#function to get the statistics of the scraped channels
def get_channel_stats(youtube, channel_ids):
    """
    Getting channel statistics
    Params:
    
    youtube: the build object from googleapiclient.discovery
    channel_ids: list of channel_ids
    
    Returns:
    Dataframe with channel_name, subscribers, views, total_videos, and playlistId. PLaylistId it has all the 
    uploaded vieos. (video_ids[i:i+50])
    
    """
    all_data = []
    for i in range(0, len(channel_ids), 50):
        request = youtube.channels().list(
                    part='snippet,contentDetails,statistics',
                    id=','.join(channel_ids[i:i+50]))
        response = request.execute() 
    
        for i in range(len(response['items'])):
            data = dict(channel_name = response['items'][i]['snippet']['title'],
                        subscribers = response['items'][i]['statistics']['subscriberCount'],
                        views = response['items'][i]['statistics']['viewCount'],
                        total_videos = response['items'][i]['statistics']['videoCount'],
                        playlist_id = response['items'][i]['contentDetails']['relatedPlaylists']['uploads'])
            all_data.append(data)
    
    return all_data

#channel_ids = get_channels(youtube)
#channel_stats = get_channel_stats(youtube, channel_ids)
df = pd.read_csv('channels.csv')
channel_df = df[['channel_name', 'description','subscribers', 'views', 'total_videos']]

vdf = pd.read_csv("\releases\vdf_edited.csv")
#vdf = vdf.drop(columns = {'index'})

st.subheader("Top channels with highest features")

column1, column2, column3 = st.columns(3)
column1.metric("Highest subscribers: " + df['channel_name'][df['subscribers'].idxmax()], int(df['subscribers'].max()))
column2.metric("Highest views: " + df['channel_name'][df['views'].idxmax()], int(df['views'].max()))
column3.metric(df['channel_name'][df['total_videos'].idxmax()], int(df['total_videos'].max()))

st.dataframe(channel_df, use_container_width=True)


st.subheader("Video features :video_camera:")
st.markdown(f"""The video features scraped are the:
\n Video title, description, duration, views, likes, favorites, and comment count """)


col1, col2, col3 = st.columns(3)
with col1:
    st.write("Top 10 videos with the highest views")
    top10_videos = vdf.sort_values(by='views', ascending=False).head(10)
    top10_videos = top10_videos[['channel_name', 'title', 'views', 'likes','engagement']]
    st.dataframe(top10_videos.reset_index(drop=True))
    
with col2:
    st.write("Top 10 videos with the most likes")
    top10_likes = vdf.sort_values(by='likes', ascending=False).head(10)
    top10_likes = top10_likes[['channel_name', 'title', 'views', 'likes','engagement']]
    st.dataframe(top10_likes.reset_index(drop=True))

with col3:
    st.write("Top 10 videos with the most engagement")
    top10_engagement = vdf.sort_values(by='engagement', ascending=False).head(10)
    top10_engagement = top10_engagement[['channel_name', 'title', 'views', 'likes','engagement']]
    st.dataframe(top10_engagement.reset_index(drop=True))





