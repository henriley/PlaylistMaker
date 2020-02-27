import json
import os

import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors
import requests
import youtube_dl

from secrets import spotify_client_id, spotify_secret_token

class CreatePLaylist:

    def __init__(self):
        self.youtube_client = self.get_youtube_permission()
        self.all_song_info = {}

    def get_youtube_permission(self):

        os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

        api_service_name = "youtube"
        api_version = "v3"
        client_secrets_file = "client_secret.json"

        scopes = ["https://www.googleapis.com/auth/youtube.readonly"]
        flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(client_secrets_file, scopes)
        credentials = flow.run_console()

        youtube_client = googleapiclient.discovery.build(api_service_name, api_version, credentials=credentials)

        return youtube_client

    def get_liked_video(self):
        request = self.youtube_client.videos().list(
            part='snippet,contentDetails,statistics',
            myRating='like'
        )
        response = request.execute()

        for item in response["items"]:
            video_title = item['snippet']['title']
            youtube_url = 'https://www.youtube.com/watch?v={}'.format(item['id'])

            video = youtube_dl.YouTubeDL({}).extract_info(youtube_url, download=False)

            song_name = video['track']
            artist = video['artist']

            if song_name is not None and artist is not None:
                self.all_song_info[video_title]={
                    'youtube_url':youtube_url,
                    'song_name':song_name,
                    'artist':artist,
                    'spotify_uri':self.get_spotify_uri(song_name, artist)
                }

    def create_playlist(self):
        
        request_body = json.dumps({
            'name':'Liked YouTube Videos',
            'desription':'Liked YouTube Videos',
            'public':True
        })

        query = "http://api.spotify.com/v1/users/{}/playlists".format(spotify_client_id)
        response = requests.post(
            query,
            data=request_body,
            headers={
                'Content-Type':'application/json',
                'Authorization':'Bearer {}'.format(spotify_secret_token)
            }
        )

        response_json = response.json()

        return response_json('id')

    def get_spotify_uri(self, track, artist):
        
        query = "https://api.spotify.com/v1/search?q=track%3A{}+artist%3A{}&type=track&offset=0&limit=20".format(
            track,
            artist
        )
        response=requests.get(
            query,
            headers={
                'Content-Type':'application/json',
                'Authorization':'Bearer {}'.format(spotify_secret_token)
            }
        )
        response_json = response.json()
        songs = response_json['tracks']['items']

        uri = songs[0]["uri"]

        return uri

    def add_song_to_playlist(self):
        
        self.get_liked_video()

        uris = [info["spotify_uri"] for song, info in self.all_song_info.items()]

        playlist_id = self.create_playlist()

        request_data = json.dumps(uris)

        query = 'https://api.spotify.com/v1/playlists/{}/tracks'.format(playlist_id)

        response = requests.post(
            query,
            data=request_data,
            headers={
                'Content-Type':'application/json',
                'Authorization':'Bearer {}'.format(spotify_secret_token)
            }
        )
        response_json = response.json()
        return response_json

    