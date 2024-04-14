from googleapiclient.discovery import build
from googleapiclient.errors import HttpError


def get_video_info(api_key, video_id):
    try:
        # YouTube API 클라이언트 생성
        youtube = build('youtube', 'v3', developerKey=api_key)

        # 동영상 정보 가져오기
        response = youtube.videos().list(
            part='snippet',
            id=video_id
        ).execute()

        # 동영상 정보 출력
        if 'items' in response and len(response['items']) > 0:
            video_info = response['items'][0]['snippet']
            print('제목:', video_info['title'])
            print('설명:', video_info['description'])
            print('태그:', ', '.join(video_info['tags']))
            print('썸네일 URL:', video_info['thumbnails']['default']['url'])
        else:
            print('해당 동영상이 없습니다.')

    except HttpError as e:
        print('API 요청 중 오류 발생:', e)


if __name__ == '__main__':
    # YouTube Data API v3의 API 키를 넣어주세요.
    api_key = 'AIzaSyAV2lvIc-KtLj51DjTwb5w7QsGUb7KsAZ4'
    # 가져올 동영상의 ID를 넣어주세요.
    video_id = 'YOUR_VIDEO_ID_HERE'
    get_video_info(api_key, video_id)
