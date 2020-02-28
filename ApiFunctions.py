import requests
import json

episode_url = "https://app.podigee.com/api/v1/episodes"


def load_apitoken():
    with open("config.json") as json_file:
        data = json.load(json_file)
        return data["token"]


def create_podigee_header():
    return {"Token": load_apitoken(), "Accept": "application / json", "Content-Type": "application/json"}


# Pull Number of Last Episode
def get_latest_episode_number(podcast_id):
    payload = {"published": True, "limit": 1, "podcast_id": podcast_id, "sort_by": "number",
               "sort_direction": "desc"}
    request = requests.get(episode_url, headers=create_podigee_header(), data=json.dumps(payload))
    return request.json()[0]['number']



def create_podcast_episode(payload):
    request = requests.post(episode_url, headers=create_podigee_header(), data=json.dumps(payload))
    print(request.status_code)
