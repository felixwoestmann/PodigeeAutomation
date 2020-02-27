import requests
import json

episode_url = "https://app.podigee.com/api/v1/episodes"


def load_apitoken():
    with open("config.json") as json_file:
        data = json.load(json_file)
        return data["token"]


# Pull Number of Last Episode
def get_latest_episodenumber(podcast_id):
    headers = {"Token": load_apitoken(), "Accept": "application / json", "Content-Type": "application/json"}
    payload = {"published": True, "limit": 1, "podcast_id": podcast_id, "sort_by": "number",
               "sort_direction": "desc"}
    request = requests.get(episode_url, headers=headers, data=json.dumps(payload))
    if request.status_code == 200:
        return request.json()['number']
    else:
        return -1


def create_podcast_episode(headers, payload):
    request = requests.post(episode_url, headers=headers, data=json.dumps(payload))
    print(request.status_code)
