import glob
import sys
from ApiFunctions import get_latest_episode_number, create_podcast_episode, upload_file, create_production
from UtilFunctions import create_payload_for_episode_creation

# Exactly one argument is expected
if len(sys.argv) != 2:
    print("Parameter is not as expected.")
    print("Script will shutodwn now")
    exit(-1)

directory_path = sys.argv[1]
file_type = "flac"
print("Search all files of type " + file_type + " in given directory")
list_of_flac_files = glob.glob(directory_path + "*." + file_type)
print("Files found: ")
for f in list_of_flac_files:
    print("\t" + f)
# TODO: Search Chaptermarks
podcast_id = 9991
# Function calls are starting
# Obtain Number of latest Episode and increment for new Episode
episode_id = create_podcast_episode(
    create_payload_for_episode_creation(9991, get_latest_episode_number(podcast_id) + 1))
# Scan parameter path for FLAC files
list_of_file_urls = []
for flac_file in list_of_flac_files:
    list_of_file_urls.append(upload_file(flac_file))
create_production(episode_id, list_of_file_urls)
