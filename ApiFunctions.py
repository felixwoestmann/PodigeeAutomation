import requests
import json
from pathlib import Path

podigee_api_url = "https://app.podigee.com/api/v1/"
contributor_id_albert = 1394
contributor_id_felix = 1395


# Loads the API token from a config.json file and returns it
def load_apitoken():
    path = Path(__file__).parent / "config.json"
    with open(path) as json_file:
        data = json.load(json_file)
        return data["token"]


# Creates a HEADER for podigee requests containing the ApiKey and specified types
def create_podigee_header():
    return {"Token": load_apitoken(), "Accept": "application / json", "Content-Type": "application/json"}


# Pull Number of Last Episode
def get_latest_episode_number(podcast_id):
    payload = {"published": True, "limit": 1, "podcast_id": podcast_id, "sort_by": "number",
               "sort_direction": "desc"}
    request = requests.get(podigee_api_url + "episodes", headers=create_podigee_header(), data=json.dumps(payload))
    return request.json()[0]['number']


# Creates a Podcast Episode
# Param: payload is a dictionary with all the data
# Return: the episode_id of the created episode
# Reference: https://app.podigee.com/api-docs#!/Episodes/create
def create_podcast_episode(payload):
    request = requests.post(podigee_api_url + "episodes", headers=create_podigee_header(), data=json.dumps(payload))
    return request.json()['id']


# Uploads the given file
# Works by using Podigee API to create an URL to Upload to
# Param: The path to a file
# Return: Returns the URL at which the file can be found
def upload_file(filename):
    # Create Upload URL
    create_upload_url_request = requests.post(podigee_api_url + "uploads", headers=create_podigee_header(),
                                              data=json.dumps({"filename": filename}))
    # Upload file to created URL
    upload_file_request = requests.put(create_upload_url_request.json()['upload_url'],
                                       headers={"Content-Type": create_upload_url_request.json()['content_type']},
                                       data=open(filename, 'rb').read())
    return create_upload_url_request.json()['file_url']


# Takes:
# episode_id _ files
def create_production(episode_id, file_urls):
    production_files = []
    for f in file_urls:
        production_file = {"url": f['url']}
        if 'albert' in str(f['name']).lower() or 'studiolink' in str(f['name']).lower():
            production_file['contributor_id'] = contributor_id_albert
        if 'felix' in str(f['name']).lower():
            production_file['contributor_id'] = contributor_id_felix
        if "contributor_id" not in production_file:
            production_file['custom_name'] = "Music"
        production_files.append(production_file)
    payload = {"episode_id": episode_id, "files": production_files}
    print(json.dumps(payload))
    request = requests.post(podigee_api_url + "productions", headers=create_podigee_header(), data=json.dumps(payload))
