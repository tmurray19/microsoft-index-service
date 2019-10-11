from video_indexer import VideoIndexer
from config import Config
import logging, os, json
from datetime import datetime
import time
import http.client, urllib.request, urllib.parse, urllib.error, base64
from video_status import get_access_token
import requests

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
            logging.debug(json_data['indexer_info']['state'])
            
            # Now, you need to query this video id
            video_id = json_data['index_video_id']

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


def upload_project_to_index(proj_id=None, send_end=None):
    """
    Uploads video at proj_id location to the Azure Indexing service to create 

    """
    success = -1
    logging.debug("Flagging upload session for project id '{}'".format(proj_id))
    proj_loc = os.path.join(Config.BASE_DIR, Config.VIDS_LOCATION, proj_id)

    # We will use this video file later
    video_file = os.path.join(proj_loc, proj_id+"_edited.mp4")

    logging.debug("Checking if item exists before beginning upload instance")
    
    # Check if the file has been uploaded first to avoid any bugs
    if os.path.exists(os.path.join(proj_loc, proj_id + "_index_status.json")):
        try:
            current_status = get_video_status(proj_id)
            if current_status == 'Processed' or current_status == 'Processing':
                logging.debug("Video has already been uploaded")
                success=1
                if send_end is not None:
                    send_end.send(success)
                return success
        except:
            logging.error("Error occured in upload_project_to_index for {}".format(proj_id))
            logging.exception('')
            if send_end is not None:
                send_end.send(success)
            return success
    else:            
        # Attempt to upload video
        try:
            logging.debug("Creating upload instance for {}".format(proj_id))
            print("Creating upload instance for {}".format(proj_id))

            logging.debug("Uploading video '{}'".format(proj_id))
            upload_begin = time.time()      

            video_id = vi.upload_to_video_indexer(
                input_filename=video_file,
                video_name=proj_id+"_edited",  # identifier for video in Video Indexer platform, must be unique during indexing time
                video_language='English'
            )

            logging.debug("Video uploaded to Index Service in {}s".format(time.time() - upload_begin))
            
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
                "requested": datetime.now().strftime("%d-%b-%Y (%H:%M:%S)"),
                "otherInfo": None,
                "indexer_info": info,
                "done": 0
            }
            logging.debug("Writing video status to json file")
            print("Writing video status to json file")
            with open(os.path.join(proj_loc, proj_id + "_index_status.json"), 'w') as outfile:
                json.dump(index_json_data, outfile)
            
            success = 1

            if send_end is not None:
                send_end.send(success)
            return success
        
        except:
            logging.error("An error has occured")
            logging.exception("")
            if send_end is not None:
                send_end.send(success)
            return success


def get_insights(proj_id):
    """
    We need to query the server using the API
        we need to ask for the access token, (write it to the json file just in case)
        we need to query the API, ask for the widget
        return the widget somewhere
    """
    logging.debug("Querying index service for CC widget for {}".format(proj_id))
    # Get access token
    logging.debug("Get index ID")
    video_id = None
    try:        
        # Get location of project
        proj_loc = os.path.join(Config.BASE_DIR, Config.VIDS_LOCATION, proj_id)

        logging.debug("Querying CC status of {}".format(proj_id))
        print("Querying CC status of {}".format(proj_id))

        # Opens JSON data, prints last known status to logging file
        with open(os.path.join(proj_loc, proj_id+"_index_status.json")) as status_json_file:
            # Last known json data 
            json_data = json.load(status_json_file)
            
            # Now, you need to query this video id
            video_id = json_data['index_video_id']
    except:
        logging.error("Error occured during get_widget for '{}'".format(proj_id))
        return -1

    access_token = get_access_token(video_id)

    logging.debug("Access token recieved for '{}'".format(proj_id))
    logging.debug(access_token)

    json_data['accessToken'] = access_token

    logging.debug("Writing access token to json")
    with open(os.path.join(proj_loc, proj_id+"_index_status.json"), 'w') as status_json_file:
        json.dump(json_data, status_json_file)
    
    logging.debug("We are now querying for the widgets")

    cc_src="https://www.videoindexer.ai/embed/insights/{uid}/{vid_id}/?accessToken={token}".format(
        uid=Config.INDEX_ACCOUNT_ID,
        vid_id=video_id,
        token=access_token
    )

    cc_widget = '<iframe width="580" height="780" src="{}" frameborder="1" allowfullscreen></iframe>'.format(cc_src)


    vid_src= "https://www.videoindexer.ai/embed/player/{uid}/{vid_id}/?accessToken={token}".format(
        uid=Config.INDEX_ACCOUNT_ID,
        vid_id=video_id,
        token=access_token
    )

    vid_widget = '<iframe width="800" height="600" src="{}" frameborder="1" allowfullscreen></iframe>'.format(vid_src)

    print(cc_widget)
    print(vid_widget)
    return cc_widget, vid_widget


def api_query_widget(video_id, access_token):    
    #&allowEdit=true&accessToken={token}'
    headers = {
        'Ocp-Apim-Subscription-Key': Config.INDEX_SUBSCRIPTION_KEY,
    }

    params = {
        'allowEdit': 'true',
        'accessToken': access_token
    }

    cc_widget = requests.get(
        'https://api.videoindexer.ai/{loc}/Accounts/{accId}/Videos/{vidId}/InsightsWidget'.format(
            loc=Config.INDEX_ACCOUNT_LOCATION,
            accId=Config.INDEX_ACCOUNT_ID,
            vidId=video_id
        ),
        params=params,
        headers=headers
    )

    print(cc_widget.status_code)

    print(cc_widget.text)
    breakup = cc_widget.text.split("</head>")
    print(breakup)
    print()
    print(breakup[0])
    print()
    print(breakup[1])


def create_queue_instance(proj_id):
    logging.debug("Creating json file for watcher to read for '{}'".format(proj_id))


    try:
        index_watcher_loc = os.path.join(Config.BASE_DIR, Config.INDEX_WATCHER)

        json_data = {
            "project_id": proj_id,
            "seen": False,
            "requested": datetime.now().strftime("%d-%b-%Y (%H:%M:%S)"),
            "otherInfo": None,
            "firstRequested": True
        }

        with open(os.path.join(index_watcher_loc, proj_id+"_index_queue_status.json"), 'w') as write_file:
            json.dump(json_data, write_file)

        return 1
    except:
        logging.error("Error occured during upload initialisation")
        logging.exception("")
        return -1