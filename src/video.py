from googleapiclient.discovery import build
import os

api_key = os.getenv('YT_API_KEY')
youtube = build('youtube', 'v3', developerKey=api_key)


class Video:
    """
    Класс для видео ютубканала
    """
    def __init__(self, video_id):
        self.__video_id = video_id
        self.info = youtube.videos().list(part='snippet,statistics,contentDetails,topicDetails',
                                          id=video_id).execute()
        self.video_title = self.info['items'][0]['snippet']['title']
        self.view_count = self.info['items'][0]['statistics']['viewCount']
        self.like_count = self.info['items'][0]['statistics']['likeCount']
        self.comment_count = self.info['items'][0]['statistics']['commentCount']
        self.video_url = f'https://www.youtube.com/watch?v={video_id}'

    def __str__(self):
        return f"{self.video_title}"

    @property
    def video_id(self):
        return self.__video_id


class PLVideo(Video):
    """
    Класс для плейлиста ютубканала
    """
    def __init__(self, video_id, plvideo_id):
        super().__init__(video_id)
        self.__plvideo_id = plvideo_id
        self.pl_info = youtube.playlistItems().list(playlistId=plvideo_id, part='contentDetails',
                                                    maxResults=50).execute()
        # self.plvideo_url = f'https://www.youtube.com/playlist?list={self.__plvideo_id}'

    @property
    def plvideo_id(self):
        return self.__plvideo_id
