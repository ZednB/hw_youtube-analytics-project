from googleapiclient.discovery import build
import os


class Video:
    api_key: str = os.getenv('YT_API_KEY')
    youtube = build('youtube', 'v3', developerKey=api_key)

    def __init__(self, id_video):
        self.id_video = id_video
        self.title = self.get_video_name()[0]
        self.video_url = 'https://www.youtube.com/watch?v=' + self.id_video
        self.view_count = self.get_video_name()[1]
        self.like_count = self.get_video_name()[2]

    def get_video_name(self):
        list_value = []
        video_id = self.id_video
        try:
            video_response = self.youtube.videos().list(part='snippet,statistics,contentDetails,topicDetails',
                                                        id=video_id
                                                        ).execute()
            video_title: str = video_response['items'][0]['snippet']['title']
            list_value.append(video_title)
            view_count: int = video_response['items'][0]['statistics']['viewCount']
            list_value.append(view_count)
            like_count: int = video_response['items'][0]['statistics']['likeCount']
            list_value.append(like_count)
        except IndexError:
            list_value.append(None)
            list_value.append(None)
            list_value.append(None)
        return list_value

    def __str__(self):
        return str(self.title)


class PLVideo(Video):

    def __init__(self, video_id, playlist_id):
        super().__init__(video_id)
        self.playlist_id = playlist_id

    def __str__(self):
        return str(self.title)
