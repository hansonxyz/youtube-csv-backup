import os
import sys
import csv
from google.oauth2 import service_account
from google_auth_oauthlib.flow import InstalledAppFlow
from google_auth_oauthlib.flow import Flow
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

API_SERVICE_NAME = 'youtube'
API_VERSION = 'v3'
CLIENT_SECRETS_FILE = 'client_secrets.json'
SCOPES = ['https://www.googleapis.com/auth/youtube']


def get_authenticated_service():
    token_file = 'token.txt'

    flow = Flow.from_client_secrets_file(
        CLIENT_SECRETS_FILE,
        scopes=SCOPES,
        redirect_uri='urn:ietf:wg:oauth:2.0:oob'
    )

    credentials = None

    if os.path.exists(token_file):
        credentials = Credentials.from_authorized_user_file(token_file, SCOPES)

    else:
        auth_url, _ = flow.authorization_url(prompt='consent')
        print('Please go to this URL: {}'.format(auth_url))
        code = input('Enter the authorization code: ')
        flow.fetch_token(code=code)

        credentials = flow.credentials

        with open(token_file, 'w') as f:
            f.write(credentials.to_json())

    return build(API_SERVICE_NAME, API_VERSION, credentials=credentials)


def clear_playlist(youtube, playlist_id):
    request = youtube.playlistItems().list(
        part='id',
        playlistId=playlist_id,
        maxResults=50
    )
    response = request.execute()

    for item in response['items']:
        item_id = item['id']
        youtube.playlistItems().delete(id=item_id).execute()


def add_videos_to_playlist(youtube, playlist_id, video_ids):
    for video_id in video_ids:
        request_body = {
            'snippet': {
                'playlistId': playlist_id,
                'resourceId': {
                    'kind': 'youtube#video',
                    'videoId': video_id
                }
            }
        }
        youtube.playlistItems().insert(part='snippet', body=request_body).execute()


def read_video_ids_from_csv(csv_filename):
    video_ids = []

    with open(csv_filename, 'r') as csvfile:
        reader = csv.reader(csvfile)
        next(reader, None)  # Skip header
        for row in reader:
            video_ids.append(row[2])

    return video_ids


def main():
    if len(sys.argv) < 2:
        print("Usage: python youtube-set.py [csv_file_path]")
        sys.exit(1)

    csv_file_path = sys.argv[1]
    playlist_id = os.path.splitext(os.path.basename(csv_file_path))[0].split('-')[0]

    try:
        youtube = get_authenticated_service()
        clear_playlist(youtube, playlist_id)
        video_ids = read_video_ids_from_csv(csv_file_path)
        add_videos_to_playlist(youtube, playlist_id, video_ids)
        print("Playlist updated successfully")
    except HttpError as error:
        print(f'An error occurred: {error}')
        sys.exit(1)


if __name__ == '__main__':
    main()
