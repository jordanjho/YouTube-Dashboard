from googleapiclient.discovery import build
import pandas as pd
import time
from config import API_KEY, CHANNEL_ID

# Load variables from .env

youtube = build('youtube', 'v3', developerKey=API_KEY)

def get_uploads_playlist_id(channel_id):
    response = youtube.channels().list(
        part="contentDetails",
        id=channel_id
    ).execute()
    return response['items'][0]['contentDetails']['relatedPlaylists']['uploads']

def get_video_ids(playlist_id, max_videos=200):
    video_ids = []
    next_page_token = None

    while True:
        res = youtube.playlistItems().list(
            part="snippet",
            playlistId=playlist_id,
            maxResults=50,
            pageToken=next_page_token
        ).execute()

        items = res.get("items", [])
        for item in items:
            video_ids.append(item['snippet']['resourceId']['videoId'])

        print(f"Fetched {len(video_ids)} total so far...")

        next_page_token = res.get('nextPageToken')
        if not next_page_token or len(video_ids) >= max_videos:
            break

        time.sleep(0.1)

    return video_ids[:max_videos]

def get_video_details(video_ids):
    data = []
    for i in range(0, len(video_ids), 50):
        try:
            res = youtube.videos().list(
                part="snippet,contentDetails,statistics",
                id=",".join(video_ids[i:i+50])
            ).execute()
        except Exception as e:
            print(f"API error: {e}")
            continue
        for vid in res.get('items', []):
            stats = vid.get('statistics', {})
            snippet = vid.get('snippet', {})
            content = vid.get('contentDetails', {})
            data.append({
                "id": vid.get('id', ''),
                "title": snippet.get('title', ''),
                "description": snippet.get('description', ''),
                "published": snippet.get('publishedAt', ''),
                "views": int(stats.get('viewCount', 0)),
                "likes": int(stats.get('likeCount', 0)),
                "duration": content.get('duration', ''),
                "tags": snippet.get('tags', [])
            })
    return pd.DataFrame(data)

if __name__ == "__main__":
    playlist_id = get_uploads_playlist_id(CHANNEL_ID)
    video_ids = get_video_ids(playlist_id, max_videos=200)
    df = get_video_details(video_ids)
    df.to_csv("data/videos.csv", index=False)
    print("Saved", len(df), "videos")