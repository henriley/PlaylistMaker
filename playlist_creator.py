import json
import requests
from secrets import spotify_client_id, spotify_secret_token

class CreatePLaylist:

    def __init__(self):
        self.user_id = spotify_client_id
        self.spotify_token = spotify_secret_token

    def get_youtube_permission(self):
        pass

    def get_liked_video(self):
        pass

    def create_playlist(self):
        
        request_body = json.dumps({
            'name':'Liked YouTube Videos',
            'desription':'Liked YouTube Videos',
            'public':True
        })

        query = "http://api.spotify.com/v1/users/{}/playlists".format(self.user_id)
        response = requests.post(
            query,
            data=requests.body,
            headers={
                'Content-Type':'application/json',
                'Authorization':'Bearer {}'.format()
            }
        )

        response_json = response.json()

        return response_json('id')

    def get_spotify_uri(self, track, artist):
        pass

    def add_song_to_playlist(self):
        pass

    