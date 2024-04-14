from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from oauth2client.tools import argparser

import pandas as pd

API_KEY = 'AIzaSyAV2lvIc-KtLj51DjTwb5w7QsGUb7KsAZ4'
SERVICE_NAME = 'youtube'
API_VERSION = 'v3'

youtube = build(SERVICE_NAME, API_VERSION, developerKey=API_KEY)

search_response = youtube.search().list(
    q="슈카월드",
    order="relevance",
    part="snippet",
    maxResults=50
).execute()

# print(search_response)
channel_id = search_response['items'][0]['id']['channelId']

# print(channel_id)
playlists=youtube.playlists().list(
    channelId=channel_id,
    part="snippet",
    maxResults=1000
).execute()

playlist_titles = []
playlist_ids = []

for i in playlists['items']:
    playlist_titles.append(i['snippet']['title'])
    playlist_ids.append(i['id'])


df = pd.DataFrame([playlist_titles, playlist_ids]).T
df.columns = ['playlist', 'playlist_id']

# print(df)

video_ids = []
video_titles = []
video_published_times = []
video_channel_ids = []
video_channel_titles = []
video_descriptions = []
video_owners = []

#
for av in df['playlist_id']:
    if av != 'PLJPjg3It2DXQUdlAocHh5FASozqwtJavv':
        continue

    playlist_videos=youtube.playlistItems().list(
        playlistId=av,
        part="snippet",
        maxResults=50
    )
    while playlist_videos:
        playlistItems_list_response = playlist_videos.execute()

        for playlist_item in playlistItems_list_response["items"]:
            title = playlist_item["snippet"]["title"]
            published_time = playlist_item["snippet"]["publishedAt"]
            this_channel_id = playlist_item["snippet"]["channelId"]
            this_channel_title = playlist_item["snippet"]["channelTitle"]
            video_id = playlist_item["snippet"]["resourceId"]["videoId"]
            description = playlist_item["snippet"]["description"]
            # video_owner = playlist_item["snippet"]["videoOwnerChannelTitle"]

            video_ids.append(video_id)
            video_published_times.append(published_time)
            video_channel_titles.append(this_channel_title)
            video_descriptions.append(description)
            # video_owners.append(video_owner)
            video_titles.append(title)

        playlist_videos = youtube.playlistItems().list_next(
            playlist_videos, playlistItems_list_response
        )

video_df = pd.DataFrame()
video_df['title'] = video_titles
video_df['videoId'] = video_ids
video_df['publishedTime'] = video_published_times
video_df['channelTitle'] = video_channel_titles
# video_df['owner'] = video_owners
video_df['desc'] = video_descriptions
video_df.to_csv("test_data_shuka.csv", index=False)
# print(video_df)

