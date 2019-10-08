########### Python 3.2 #############
import http.client, urllib.request, urllib.parse, urllib.error, base64

headers = {
    # Request headers
    'x-ms-client-request-id': '',
    'Ocp-Apim-Subscription-Key': '6b25b9e862fa4af4bab763ceaaf223cd',
}

params = {
    # Request parameters
    #'allowEdit': 'True',
    'location': 'trial',   
    'accountId': 'd1c32f1b-2a26-4b44-b6a3-c96e709d0648',
    'videoId': '8e2e2ef6e4'
}

p_url = "/auth/{}/Accounts/{}/Videos/{}/AccessToken".format(params['location'], params['accountId'], params['videoId'])

params = urllib.parse.urlencode(params)

try:
    conn = http.client.HTTPSConnection('api.videoindexer.ai')
    conn.request("GET", p_url, headers=headers)
    response = conn.getresponse()
    data = response.read()
    print(data)
    conn.close()
except Exception as e:
    print(e)

