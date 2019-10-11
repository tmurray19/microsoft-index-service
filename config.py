# Config.py
import os


# Config file
class Config(object):
    BASE_DIR = os.environ.get('BASE_DIR') or "/mnt/csae48d5df47deax41bcxbaa"
    #BASE_DIR = os.environ.get('BASE_DIR') or "N:/project"
    VIDS_LOCATION = os.environ.get('VIDS_LOCATION') or "videos"
    QUEUE_LOCATION = os.environ.get('QUEUE_LOCATION') or 'renderQueue'
    LOGS_LOCATION = os.environ.get('LOGS_LOCATION') or "logs" 
    RESOURCE_PATH = os.environ.get('RESOURCE_PATH') or 'resource'
    WATCHER_LOGS = os.environ.get('WATCHER_LOG') or 'renderWatcher'
    RENDER_LOGS = os.environ.get('RENDER_LOG') or 'renderService'
    FULL_LOGS = os.environ.get('RENDER_LOG') or 'renderServiceFull'
    CHUNK_LOGS = os.environ.get('RENDER_LOG') or 'renderServiceChunk'
    PREVIEW_LOGS = os.environ.get('RENDER_LOG') or 'renderServicePreview'
    FLASK_LOGS = os.environ.get('FLASK_LOG') or 'renderFlask'
    INDEX_WATCHER = os.environ.get('INDEX_WATCHER') or 'indexQueue'
    INDEX_WATCHER_LOGS = os.environ.get('INDEX_WATCHER_LOGS') or 'indexUploader'
    INDEX_FLASk_LOGS = os.environ.get('INDEX_FLASk_LOGS') or 'indexFlask'

    # Defining storage name and key
    STORAGE_ACCOUNT_NAME = os.environ.get('STORAGE_ACCOUNT_NAME') or 'csae48d5df47deax41bcxbaa'
    STORAGE_ACCOUNT_KEY = os.environ.get('STORAGE_ACCOUNT_KEY') or \
        'iUTL5cLSDTObfUliySlqjT4x1dfCQ1U7l7zuaZrPEwhGIHnHPKWfYuFrq16cCjFUS/122mcwJpdseC9JI6mSGA=='
    # TODO: When deploying, remove 'testingazure' for the commented out Share Name
    SHARE_NAME = os.environ.get('SHARE_NAME') or 'cs-william-squarev-media-10037ffe909d3982' #'testingazure'  # 
    # Defining name of json file containing edits
    PROJECT_NAME = os.environ.get('PROJECT_NAME') or 'FinalSubclipJson.json'
    PREVIEW_CHUNK_LENGTH = os.environ.get('PREVIEW_CHUNK_LENGTH') or 10

    # Video Indexer details
    INDEX_ACCOUNT_ID = 'd1c32f1b-2a26-4b44-b6a3-c96e709d0648'
    INDEX_SUBSCRIPTION_KEY = '6b25b9e862fa4af4bab763ceaaf223cd'
    # TODO: CHANGE THIS FROM 'trial'
    INDEX_ACCOUNT_LOCATION = 'trial'
    
    """

        az account list-locations -o table

        will give you a table like:

        DisplayName          Latitude    Longitude    Name
        -------------------  ----------  -----------  ------------------
        East Asia            22.267      114.188      eastasia
        Southeast Asia       1.283       103.833      southeastasia
        Central US           41.5908     -93.6208     centralus
        East US              37.3719     -79.8164     eastus
        East US 2            36.6681     -78.3889     eastus2
        West US              37.783      -122.417     westus
        North Central US     41.8819     -87.6278     northcentralus
        South Central US     29.4167     -98.5        southcentralus
        North Europe         53.3478     -6.2597      northeurope
        West Europe          52.3667     4.9          westeurope
        Japan West           34.6939     135.5022     japanwest
        Japan East           35.68       139.77       japaneast
        Brazil South         -23.55      -46.633      brazilsouth
        Australia East       -33.86      151.2094     australiaeast
        Australia Southeast  -37.8136    144.9631     australiasoutheast
        South India          12.9822     80.1636      southindia
        Central India        18.5822     73.9197      centralindia
        West India           19.088      72.868       westindia
        Canada Central       43.653      -79.383      canadacentral
        Canada East          46.817      -71.217      canadaeast
        UK South             50.941      -0.799       uksouth
        UK West              53.427      -3.084       ukwest
        West Central US      40.890      -110.234     westcentralus
        West US 2            47.233      -119.852     westus2
        Korea Central        37.5665     126.9780     koreacentral
        Korea South          35.1796     129.0756     koreasouth
        France Central       46.3772     2.3730       francecentral
        France South         43.8345     2.1972       francesouth
        Australia Central    -35.3075    149.1244     australiacentral
        Australia Central 2  -35.3075    149.1244     australiacentral2
        South Africa North   -25.731340  28.218370    southafricanorth
        South Africa West    -34.075691  18.843266    southafricawest
    """