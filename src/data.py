import requests

def get_video_data(video_id):
    url = f"https://api.douyin.com/video/{video_id}"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"Failed to get video data: {response.status_code}")

def get_account_data(account_id):
    url = f"https://api.douyin.com/account/{account_id}"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"Failed to get account data: {response.status_code}")

def get_comments_data(video_id):
    url = f"https://api.douyin.com/video/{video_id}/comments"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"Failed to get comments data: {response.status_code}")
