from video_indexer import VideoIndexer
import logging, os, json

from datetime import datetime
from config import Config

# Config to be moved to separate file
# Can sit here for now though
# TODO: Move this
CONFIG = {
    'SUBSCRIPTION_KEY': '6b25b9e862fa4af4bab763ceaaf223cd',
    'LOCATION': 'trial',
    'ACCOUNT_ID': 'd1c32f1b-2a26-4b44-b6a3-c96e709d0648',
    'BASE_DIR':'/Users/taidghmurray',
    'VIDS_LOCATION' : 'Downloads'
}

# Create video index instance using account details
vi = VideoIndexer(
    vi_subscription_key=CONFIG['SUBSCRIPTION_KEY'],
    vi_location=CONFIG['LOCATION'],
    vi_account_id=CONFIG['ACCOUNT_ID']
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
            json_data['dateCompleted'] = datetime.now().strftime("%d-%b-%Y (%H:%M:%S)")
            json_data['status'] = True
            json_data['correctlyRendered'] = render_status
            json_data['otherInfo'] = info
            logging.debug("JSON Data for {}:".format(proj_id))
            logging.debug(json_data)
            with open(event.src_path, "w") as json_write:
                json.dump(json_data, json_write)   


            return info['state']

    except:
        logging.error("Error occured trying to get video status of {}".format(proj_id))
        logging.exception("")
        return 99



def upload_video(proj_id):        
    # Define locations
    proj_loc = os.path.join(Config.BASE_DIR, Config.VIDS_LOCATION, proj_id)
    video_file = os.path.join(proj_loc, proj_id+"_edited.mp4")
    logging.debug("Checking if item exists before beginning upload instance")
    
    # Check if the file has been uploaded first to avoid any bugs
    try:
        get_video_status(proj_id)
    except:
        logging.debug("Error occured during video status")
        logging.exception("")
    
    # Attempt to upload video
    try:
        logging.debug("Creating upload instance for {}".format(proj_id))
        print("Creating upload instance for {}".format(proj_id))

        # Crrate instance of video upload to account with name of file
        video_id = vi.upload_to_video_indexer(
            input_filename=video_file,
            video_name=proj_id + '_edited', 
            video_language='English'
        )

        # Check initial video info
        info = vi.get_video_info(
            video_id,
            video_language='English'
        )

        logging.debug("Initial video info")
        logging.debug(info)

        print("Initial video info")
        print(info)

        logging.debug("Video successfully uploaded, writing video ID to project folder")
        logging.debug("Poll the video_id if you want the status of the videp")
        
        print("Video successfully uploaded, writing video ID to project folder")
        print("Poll the video_id if you want the status of the video")

        index_json = {
            'project_id': proj_id,
            'video_id': video_id,
            'requested': datetime.now().strftime("%d-%b-%Y (%H:%M:%S)"),
            'done': 0,
            'status': 0,
            'initial_connection_details': info,
        }

        logging.debug("Writing video status to json file")
        print("Writing video status to json file")
        with open(os.path.join(proj_loc, proj_id+"_index_status.json"), 'w') as outfile:
            json.dump(index_json, outfile)
    except:
        logging.error("An error has occured")
        logging.exception("")
        index_json = {
            'project_id': proj_id,
            'video_id': video_id,
            'requested': datetime.now().strftime("%d-%b-%Y (%H:%M:%S)"),
            'done': 0,
            'status': 0,
            'initial_connection_details': info,
        }

        logging.debug("Writing video status to json file")
        print("Writing video status to json file")
        with open(os.path.join(proj_loc, proj_id+"_index_status.json"), 'w') as outfile:
            json.dump(index_json, outfile)



#upload_video("2312")
get_video_status("2312")