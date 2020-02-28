import requests
import json

podigee_api_url = "https://app.podigee.com/api/v1/"


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
    request = requests.get(podigee_api_url + "episodes", headers=create_podigee_header(), data=json.dumps(payload))
    return request.json()[0]['number']


def create_podcast_episode(payload):
    request = requests.post(podigee_api_url + "episodes", headers=create_podigee_header(), data=json.dumps(payload))
    print(request.status_code)


def upload_file(filename):
    # Create Upload URL
    create_upload_url_request = requests.post(podigee_api_url + "uploads", headers=create_podigee_header(),
                                              data=json.dumps({"filename": filename}))
    # Upload file to created URL
    upload_file_request = requests.put(create_upload_url_request.json()['upload_url'],
                                       headers={"Content-Type": create_upload_url_request.json()['content_type']},
                                       data=open(filename, 'rb').read())
    print("Upload File Code: " + str(upload_file_request.status_code))
    return create_upload_url_request.json()['file_url']
