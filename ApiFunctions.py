import requests
import json

podigee_api_url = "https://app.podigee.com/api/v1/"


# Loads the API token from a config.json file and returns it
def load_apitoken():
    with open("config.json") as json_file:
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
# TODO: Add ChapterMarks
def create_podcast_episode(payload):
    request = requests.post(podigee_api_url + "episodes", headers=create_podigee_header(), data=json.dumps(payload))
    return request.json()['episode_id']


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
        production_file = {"url": f}
        production_files.append(production_file)
        # TODO set contributor_id or custom_name
    payload = {"episode_id": episode_id, "files": production_files}
    request = requests.post(podigee_api_url + "productions", headers=create_podigee_header(), data=json.dumps(payload))
