from video_indexer import VideoIndexer
from config import Config
import logging, os, json
from datetime import datetime
import http.client, urllib.request, urllib.parse, urllib.error, base64

# This is the production version

# Define video indexer at top level
vi = VideoIndexer(
    vi_subscription_key=Config.INDEX_SUBSCRIPTION_KEY,
    vi_location=Config.INDEX_ACCOUNT_LOCATION,
    vi_account_id=Config.INDEX_ACCOUNT_ID
)

# Retrieves the video status of a project
def get_video_status(proj_id):
    try:        
        # Get location of project
        proj_loc = os.path.join(Config.BASE_DIR, Config.VIDS_LOCATION, proj_id)

        logging.debug("Querying CC status of {}".format(proj_id))
        print("Querying CC status of {}".format(proj_id))

        # Opens JSON data, prints last known status to logging file
        with open(os.path.join(proj_loc, proj_id+"_index_status.json")) as status_json_file:
            # Last known json data 
            json_data = json.load(status_json_file)
            print(json_data)
            logging.debug("Last known status of video")
            logging.debug(json_data)
            logging.debug("Last known state of '{}': ".format(proj_id))
            logging.debug(json_data['initial_connection_details']['state'])
            
            # Now, you need to query this video id
            video_id = json_data['video_id']

            # TODO: Testing purpoise

            # Now get current state
            info = vi.get_video_info(
                video_id,
                video_language='English'
            )

            print("Current state: {}".format(info['state']))
            logging.debug("Current state: {}".format(info['state']))
            
            logging.debug("Updating JSON status file")
            json_data['lastChecked'] = datetime.now().strftime("%d-%b-%Y (%H:%M:%S)")
            json_data['status'] = info['state']
            json_data['indexer_info'] = info
            json_data['done'] = 1 if info['state'] == 'Processed' else 0
            logging.debug("JSON Data for {}:".format(proj_id))
            logging.debug(json_data)
            with open(os.path.join(proj_loc, proj_id + "_index_status.json"), 'w') as outfile:
                json.dump(json_data, outfile)
        

            return info['state']

    except:
        logging.error("Error occured trying to get video status of {}".format(proj_id))
        logging.exception("")
        return 99


def upload_project_to_index(proj_id=None):
    """
    Uploads video at proj_id location to the Azure Indexing service to create 

    """
    logging.debug("Flagging upload session for project id '{}'".format(proj_id))
    proj_loc = os.path.join(Config.BASE_DIR, Config.VIDS_LOCATION, proj_id)

    # We will use this video file later
    video_file = os.path.join(proj_loc, proj_id+"_edited.mp4")

    logging.debug("Checking if item exists before beginning upload instance")
    
    # Check if the file has been uploaded first to avoid any bugs
    if os.path.exists(os.path.join(proj_loc, proj_id + "_index_status.json")):
        try:
            get_video_status(proj_id)
        except:
            logging.error("Error occured in upload_project_to_index for {}".format(proj_id))
            logging.exception('')
    else:            
        # Attempt to upload video
        try:
            logging.debug("Creating upload instance for {}".format(proj_id))
            print("Creating upload instance for {}".format(proj_id))

            logging.debug("Uploading video '{}'".format(proj_id))

            video_id = vi.upload_to_video_indexer(
                input_filename=video_file,
                video_name=proj_id+"_edited",  # identifier for video in Video Indexer platform, must be unique during indexing time
                video_language='English'
            )

            logging.debug("Video id for project '{}' is '{}'".format(proj_id, video_id))
            print(video_id)

            logging.debug("Video status")
            info = vi.get_video_info(
                video_id,
                video_language='English'
            )

            logging.debug(info)
            print(info)
            
            logging.debug("Writing video status to JSON file")
            index_json_data = {
                "project_id": proj_id,
                "index_video_id": video_id,
                "status": 0,
                "requested": datetime.datetime.now(),
                "otherInfo": None,
                "indexer_info": info,
                "done": 0
            }
            logging.debug("Writing video status to json file")
            print("Writing video status to json file")
            with open(os.path.join(proj_loc, proj_id + "_index_status.json"), 'w') as outfile:
                json.dump(index_json_data, outfile)
        
        except:
            logging.error("An error has occured")
            logging.exception("")
        
get_video_status("2312")