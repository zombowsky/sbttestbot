from celery import Celery
import requests
import settings
import json


app = Celery('tasks', backend='amqp', broker='amqp://')


@app.task()
def find_artist_info(artist):
    result = requests.get(
        settings.lfm_api + "?method=artist.getinfo&artist={}&api_key={}&format=json".format(
            artist, settings.lfm_api_key
        )).text
    text = json.loads(result)["artist"]["bio"]["summary"].split('<a')[0]
    return text
