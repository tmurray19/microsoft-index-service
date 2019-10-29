########### Python 3.2 #############
import http.client, urllib.request, urllib.parse, urllib.error, base64
import logging
from config import Config

def get_access_token(index_video_id):
    # The id here MUST be the index video id, not the videosherpa ID 
    logging.debug("This is for getting access token for a given private video private videos on account")

    headers = {
        # Request headers
        'x-ms-client-request-id': '',
        'Ocp-Apim-Subscription-Key': Config.INDEX_SUBSCRIPTION_KEY,
    }

    params = {
        # Request parameters
        #'allowEdit': 'True',
        'location': Config.INDEX_ACCOUNT_LOCATION,   
        'accountId': Config.INDEX_ACCOUNT_ID,
        'videoId': index_video_id
    }

    p_url = "/auth/{}/Accounts/{}/Videos/{}/AccessToken".format(params['location'], params['accountId'], params['videoId'])

    params = urllib.parse.urlencode(params)

    try:
        logging.debug("Attempting to get access token for videos on account")
        conn = http.client.HTTPSConnection('api.videoindexer.ai')
        conn.request("GET", p_url, headers=headers)
        response = conn.getresponse()
        logging.debug("Access token for '{}' recieved".format(index_video_id))
        data = response.read()
        print(data[1:-1].decode("utf-8"))
        conn.close()
        return data[1:-1].decode("utf-8")
    except:
        logging.error("Error occured during access token of {}".format(index_video_id))
        logging.exception("")
        return None