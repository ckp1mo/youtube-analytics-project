import datetime

from googleapiclient.discovery import build
import os
import isodate

api_key = os.getenv('YT_API_KEY')
youtube = build('youtube', 'v3', developerKey=api_key)


class PlayList:
    """
    Класс для плейлиста канала
    """

    def __init__(self, playlist_id):
        self.playlist_id = playlist_id
        self.playlist = youtube.playlistItems().list(playlistId=playlist_id,
                                                     part='snippet, contentDetails',
                                                     maxResults=50,
                                                     ).execute()
        self.url = f'https://www.youtube.com/playlist?list={playlist_id}'

    @property
    def title(self):
        """
        Возвращает название плейлиста
        """
        channel_id = self.playlist['items'][0]['snippet']['channelId']
        all_playlists = youtube.playlists().list(channelId=channel_id,
                                                 part='contentDetails,snippet',
                                                 maxResults=50,
                                                 ).execute()
        for plists in all_playlists['items']:
            if plists['id'] == self.playlist_id:
                return plists['snippet']['title']

    @property
    def total_duration(self):
        """
        Возвращает длительность всех видео из плейлиста в формате HH:MM:SS
        """
        video_ids: list[str] = [video['contentDetails']['videoId'] for video in self.playlist['items']]
        video_response = youtube.videos().list(part='snippet, contentDetails,statistics',
                                               id=','.join(video_ids)
                                               ).execute()
        total_time = datetime.timedelta(0)
        for video in video_response['items']:
            # YouTube video duration is in ISO 8601 format
            iso_8601_duration = video['contentDetails']['duration']
            duration = isodate.parse_duration(iso_8601_duration)
            total_time += duration
        return total_time

    def show_best_video(self):
        """
        Возвращает ссылку на самое залайканное видео
        """
        best_video = ''
        like_count = 0
        for bv in self.playlist['items']:
            lk = youtube.videos().list(part='snippet,statistics,contentDetails,topicDetails',
                                       id=bv['contentDetails']['videoId']).execute()
            if int(lk['items'][0]['statistics']['likeCount']) > like_count:
                best_video = bv['contentDetails']['videoId']

        return f'https://youtu.be/{best_video}'
