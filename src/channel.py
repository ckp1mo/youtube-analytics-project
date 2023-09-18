import os
from googleapiclient.discovery import build
import json
from pathlib import Path


api_key = os.getenv('YT_API_KEY')
youtube = build('youtube', 'v3', developerKey=api_key)


class Channel:
    """Класс для ютуб-канала"""

    def __init__(self, channel_id: str) -> None:
        """Экземпляр инициализируется id канала. Дальше все данные будут подтягиваться по API."""
        self.__channel_id = channel_id
        self.channel_info = youtube.channels().list(id=self.__channel_id, part='snippet,statistics').execute()
        self.title = self.channel_info['items'][0]['snippet']['title']
        self.description = self.channel_info['items'][0]['snippet']['description']
        self.subscribers = self.channel_info['items'][0]['statistics']['subscriberCount']
        self.video_count = self.channel_info['items'][0]['statistics']['videoCount']
        self.views = self.channel_info['items'][0]['statistics']['viewCount']
        self.url = f'https://www.youtube.com/channel/{self.__channel_id}'

    def __str__(self):
        return f'{self.title} {self.url}'

    def __add__(self, other):
        return int(self.subscribers) + int(other.subscribers)

    def __sub__(self, other):
        return int(self.subscribers) - int(other.subscribers)

    def __gt__(self, other):
        return int(self.subscribers) > int(other.subscribers)

    def __ge__(self, other):
        return int(self.subscribers) >= int(other.subscribers)

    def __lt__(self, other):
        return int(self.subscribers) < int(other.subscribers)

    def __le__(self, other):
        return int(self.subscribers) <= int(other.subscribers)

    def __eq__(self, other):
        return int(self.subscribers) == int(other.subscribers)

    def print_info(self) -> None:
        """Выводит в консоль информацию о канале."""
        print(self.channel_info)

    @classmethod
    def get_service(cls):
        return youtube

    def to_json(self, file_name):
        """
        Конструктор для создания словаря с атрибутами канала.
        Конвертирование в json словарь, создание и запись в файл.
        """
        outpath = Path.cwd() / file_name
        channel_value = {
            'channel_id': self.__channel_id,
            'title': self.title,
            'description': self.description,
            'url': self.url,
            'subscribers': self.subscribers,
            'videoCount': self.video_count,
            'viewCount': self.views
        }
        channel_value_to_json = json.dumps(channel_value, ensure_ascii=False, indent=4)
        outpath.write_text(channel_value_to_json)
