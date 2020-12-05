import os
import dotenv
import json
import requests
from igdb.wrapper import IGDBWrapper

dotenv.load_dotenv()

# make connection to igdb API via wrapper
def GetIGDBWrapper():
    twitch_id = os.environ.get("TWITCH_ID")
    twitch_secret = os.environ.get("TWITCH_SECRET")
    pload = {'client_id':twitch_id,
            'client_secret':twitch_secret,
            'grant_type':'client_credentials'}
    twitch = requests.post('https://id.twitch.tv/oauth2/token', data=pload)

    oAuth = twitch.json()

    wrapper = IGDBWrapper(twitch_id, oAuth['access_token'])
    return wrapper

def RequestIGDB(wrapper, endpoint, query):
    result = wrapper.api_request(endpoint, query)
    return result