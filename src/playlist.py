import datetime

from googleapiclient.discovery import build
import isodate


class PlayList:
    """ Класс для плейлиста """
    api_key: str = 'AIzaSyAvSJwZZPDCUm5njvSBpnx-41ubiskiQXg'
    youtube = build('youtube', 'v3', developerKey=api_key)

    def __init__(self, id_playlist):
        self.id_playlist = id_playlist
        self.title = self.get_title()
        self.url = 'https://www.youtube.com/playlist?list=' + self.id_playlist
        self.__duration = self.total_duration

    def get_playlist_id(self):
        """ Функция выводит информиацию о видеороликах в плейлисте в виде списка """
        playlist_id = self.id_playlist
        playlist_videos = self.youtube.playlistItems().list(playlistId=playlist_id,
                                                            part='contentDetails',
                                                            maxResults=50,
                                                            ).execute()
        video_ids: list[str] = [video['contentDetails']['videoId'] for video in playlist_videos['items']]
        return video_ids

    @property
    def total_duration(self):
        """ Функция выводит общую длительность видеороликов в плейлисте """
        list_of_duration = []
        video_response = self.youtube.videos().list(part='contentDetails,statistics',
                                                    id=','.join(self.get_playlist_id())
                                                    ).execute()
        for video in video_response['items']:
            iso_8601_duration = video['contentDetails']['duration']
            duration = isodate.parse_duration(iso_8601_duration)
            list_of_duration.append(duration)
        result = sum(list_of_duration, datetime.timedelta())
        return result

    def get_title(self):
        """ Функция возвращает название плейлиста """
        video_response = self.youtube.videos().list(part='snippet,statistics,contentDetails,topicDetails',
                                                    id=self.get_playlist_id()
                                                    ).execute()
        video_title: str = video_response['items'][0]['snippet']['title']
        spliting = video_title.split('.')
        return spliting[0]

    def show_best_video(self):
        """ Функция выводит статистику в список.
        Находит самое большое кол-во лайков в списке, индекс этого значения в списке.
        Возвращает ссылку с самым большим кол-вом лайков"""
        list_of_like = []
        for videos in self.get_playlist_id():
            video_response = self.youtube.videos().list(part='snippet,statistics,contentDetails,topicDetails',
                                                        id=videos
                                                        ).execute()
            like_count: int = video_response['items'][0]['statistics']['likeCount']
            list_of_like.append(like_count)
        max_likes = max(list_of_like)
        index_max_like = list_of_like.index(max_likes)
        return f'https://youtu.be/{self.get_playlist_id()[index_max_like]}'
