from googleapiclient.discovery import build
import os


class Video:
    api_key: str = os.getenv('YT_API_KEY')
    youtube = build('youtube', 'v3', developerKey=api_key)

    def __init__(self, video_id: str) -> None:
        self.video_id = video_id
        self.video_name = self.get_video_name()[0]
        self.link_to_video = 'https://www.youtube.com/' + self.video_id
        self.number_views = self.get_video_name()[1]
        self.number_of_likes = self.get_video_name()[2]

    def get_video_name(self):
        video_info = []
        video_id = self.video_id
        video_response = self.youtube.videos().list(part='snippet,statistics,contentDetails,topicDetails',
                                                    id=video_id
                                                    ).execute()
        video_title: str = video_response['items'][0]['snippet']['title']
        video_info.append(video_title)
        view_count: int = video_response['items'][0]['statistics']['viewCount']
        video_info.append(view_count)
        like_count: int = video_response['items'][0]['statistics']['likeCount']
        video_info.append(like_count)
        comment_count: int = video_response['items'][0]['statistics']['commentCount']
        video_info.append(comment_count)
        return video_info

    def __str__(self):
        return str(self.video_name)


class PLVideo(Video):

    def __init__(self, video_id, playlist_id):
        super().__init__(video_id)
        self.playlist_id = playlist_id

    def __str__(self):
        return str(self.video_name)
