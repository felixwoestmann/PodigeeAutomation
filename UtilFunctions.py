import glob
from ApiFunctions import get_latest_episode_number, create_podcast_episode, upload_file, create_production


def create_payload_for_episode_creation(podcast_id, episode_number):
    # Prepare Payload for New Episode Creation
    contributor_id_albert = 186
    contributor_id_felix = 187
    copyright_text = "Felix Wöstmann, Albert Menacher"
    authors = copyright_text
    description = "Albert und Felix reden über "
    episode_cover = "https://podigee.s3-eu-west-1.amazonaws.com/uploads/u5976/b46b3aa7-bdea-4ab4-99ba-7e94af4b1d7c.png"
    show_notes_md = """
###Shownotes

**Kontaktiere uns:**
- Website: [zweimalzwanzig.de](https://zweimalzwanzig.de/)
- Email Adresse: mailto:hallo@zweimalzwanzig.de
- Twitter: [@zwanzigzwanzig](https://twitter.com/zwanzigzwanzig)
"""

    return {"podcast_id": podcast_id,
            "title": "placeholder",
            "slug": "19",
            "description": description,
            "authors": authors,
            "copyright_text": copyright_text,
            "contributor_ids": [contributor_id_felix, contributor_id_albert],
            "show_notes_md": show_notes_md,
            "cover_image": episode_cover,
            "number": episode_number
            }


def create_chapter_marks_from_file(chaptermarkfile):
    chapter_marks_podigee = []
    counter = 1
    opened_file = open(chaptermarkfile, 'r')
    lines = opened_file.readlines()
    for line in lines:
        parts_of_line = line.split(" ")
        chapter_marks_podigee.append({"title": parts_of_line[1],
                                      "start_time": parts_of_line[0],
                                      "id": counter})
        counter += 1
    return chapter_marks_podigee
