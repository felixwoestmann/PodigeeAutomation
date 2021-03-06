import glob
import sys
import os.path
from ApiFunctions import get_latest_episode_number, create_podcast_episode, upload_file, create_production
from UtilFunctions import create_payload_for_episode_creation, create_chapter_marks_from_file

chaptermark_filettype = "chapters.txt"
file_type = "flac"
podcast_id = 9991
print("\n\n")

# Exactly one argument is expected
if len(sys.argv) != 2:
    print("Expected Directory as parameter")
    print("Script will shutdown now")
    exit(-1)


print("Try to create Podigee Podcast Episode for Directory")
user_genereated_episode_title = input("Please enter title for episode:\n")
# Search FLAC Files
directory_path = sys.argv[1]
print("Search all files of type " + file_type + " in given directory")
list_of_flac_files = glob.glob(directory_path + "*." + file_type)
print("\tFiles found: ")
for f in list_of_flac_files:
    print("\t\t" + f)

# Create chapter marks
print("Search for Chaptermarks File " + chaptermark_filettype)
chapter_mark_file = glob.glob(directory_path + "*." + chaptermark_filettype)
if len(chapter_mark_file) > 0:
    print("\tChapter marks found in file " + chapter_mark_file)
    chapter_marks = create_chapter_marks_from_file(chapter_mark_file[0])
else:
        print("Couldn't find Chaptermarks File")
# Function calls are starting
# Obtain Number of latest Episode and increment for new Episode
episode_creation_payload = create_payload_for_episode_creation(9991, get_latest_episode_number(podcast_id) + 1)
episode_creation_payload['title'] = user_genereated_episode_title
if len(chapter_mark_file) > 0:
    episode_creation_payload['chapter_marks'] = chapter_marks
episode_id = create_podcast_episode(episode_creation_payload)
print("Created Episode: " + user_genereated_episode_title)
print("\tID: " + str(episode_id))

# Scan parameter path for FLAC files
print("Upload audio files")
list_of_file_urls = []
for flac_file in list_of_flac_files:
    url = upload_file(flac_file)
    list_of_file_urls.append({"url": url,
                              "name": os.path.basename(flac_file)})
    print("\tUploaded " + str(flac_file))
    print("\t\tURL: " + str(url))
print("All files are uploaded")
print("Create a production for episode")
create_production(episode_id, list_of_file_urls)
print("Script is finished.")
print("Press any key....")
input()
