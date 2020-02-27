import requests
import json

api_token = ""

with open("config.json") as json_file:
    data = json.load(json_file)
    api_token = data["token"]

podcast_id = 9991
contributor_id_albert = 186
contributor_id_felix = 187
copyright_text = "Felix Wöstmann, Albert Menacher"
authors = copyright_text
description = "Albert und Felix reden über "
show_notes_md = """
###Shownotes

**Kontaktiere uns:**
- Website: [zweimalzwanzig.de](https://zweimalzwanzig.de/)
- Email Adresse: mailto:hallo@zweimalzwanzig.de
- Twitter: [@zwanzigzwanzig](https://twitter.com/zwanzigzwanzig)
"""
episode_cover = "https://images.podigee.com/800x,sx4dMZWhfErFlJffZaCMoqL2NUL6uRwbhM0dc8lImQEk=/https://cdn.podigee.com/uploads/u5976/6ec42bfe-d3b0-4d8c-b354-da0d2fceb2c4.png"
#
headers = {"Token": api_token, "Accept": "application/json", "Content-Type": "application/json"}
payload = {"podcast_id": podcast_id, "title": "placeholder", "slug": "19", "description": description,
           "authors": authors, "copyright_text": copyright_text,
           "contributor_ids": [contributor_id_felix, contributor_id_albert], "show_notes_md": show_notes_md,
           "episode_cover": episode_cover}

request = requests.post("https://app.podigee.com/api/v1/episodes", headers=headers, data=json.dumps(payload))

print(request.status_code)
