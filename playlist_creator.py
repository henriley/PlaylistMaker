import json
import requests
import os

import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors
import youtube_dl

from secrets import spotify_client_id, spotify_secret_token

class CreatePLaylist:

    def __init__(self):
        self.user_id = spotify_client_id
        self.spotify_token = spotify_secret_token
        self.youtube_client = self.get_youtube_permission()
        self.all_song_info = {}

    def get_youtube_permission(self):
        """ Log Into Youtube, Copied from Youtube Data API """
        # Disable OAuthlib's HTTPS verification when running locally.
        # *DO NOT* leave this option enabled in production.
        os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

        api_service_name = "youtube"
        api_version = "v3"
        client_secrets_file = "client_secret.json"

        # Get credentials and create an API client
        scopes = ["https://www.googleapis.com/auth/youtube.readonly"]
        flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(client_secrets_file, scopes)
        credentials = flow.run_console()

        # from the Youtube DATA API
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

            self.all_song_info[video_title]={
                'youtube_url':youtube_url,
                'song_name':song_name,
                'artist':artist,
                'spotify_uri':get_spotify_uri(song_name, artist)
            }

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
                'Authorization':'Bearer {}'.format(spotify_secret_token)
            }
        )

        response_json = response.json()

        return response_json('id')

    def get_spotify_uri(self, track, artist):
        
        query ="https://api.spotify.com/v1/search?q=track%3A{}+artist%3A{}&type=track&offset=0&limit=20".format(
            track,
            artist_name
        )
        response=requests.get(
            query,
            headers={
                'Content-Type':'application/json',
                'Authorization':'Bearer {}'.format(spotify_secret_token)
            }
        )
        response_json = response.json()
        songs = response.json['tracks']['items']

    def add_song_to_playlist(self):
        pass

    