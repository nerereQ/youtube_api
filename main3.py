import pandas as pd

df = pd.read_csv("test_data_shuka.csv")
# print(df)

category_ids = []
views = []
likes = []
dislikes = []
comments = []
mins = []
seconds = []
titles = []
ids = []

from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from oauth2client.tools import argparser

API_KEY = 'AIzaSyAV2lvIc-KtLj51DjTwb5w7QsGUb7KsAZ4'
SERVICE_NAME = 'youtube'
API_VERSION = 'v3'

youtube = build(SERVICE_NAME, API_VERSION, developerKey=API_KEY)


for i in range(len(df)):
    videoId = df['videoId'][i]
    print(i, videoId)
    request = youtube.videos().list(
        part="snippet, contentDetails, statistics",
        id=videoId
    )
    response = request.execute()

    if response['items']==[]:
        titles.append('-')
        ids.append('-')
        category_ids.append('-')
        views.append('-')
        likes.append('-')
        dislikes.append('-')
        comments.append('-')

    else:
        titles.append(response['items'][0]['snippet']['title'])
        ids.append(videoId)
        category_ids.append(response['items'][0]['snippet']['categoryId'])
        views.append(response['items'][0]['statistics']['viewCount'])
        likes.append(response['items'][0]['statistics']['likeCount'])
        # dislikes.append(response['items'][0]['statistics']['dislikeCount'])
        comments.append(response['items'][0]['statistics']['commentCount'])


shuka_df = pd.DataFrame([titles, ids, category_ids, views, likes, comments])
# shuka_df.columns = ['title', 'id', 'category', 'views', 'likes', 'comments']
shuka_df.to_csv("test_data_shuka2.csv", index=False)



