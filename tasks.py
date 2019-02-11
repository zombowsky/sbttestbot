from celery import Celery
from telegram import Bot
import requests
import settings
import json
from watson_developer_cloud import SpeechToTextV1

app = Celery('tasks', backend='amqp', broker='amqp://')


@app.task()
def find_artist_info(artist):
    result = requests.get(
        settings.lfm_api + "?method=artist.getinfo&artist={}&api_key={}&format=json".format(
            artist, settings.lfm_api_key
        )).text
    text = json.loads(result)["artist"]["bio"]["summary"].split('<a')[0]
    return text


@app.task()
def send_message(msg, token, chat_id):
    Bot(token).send_message(chat_id=chat_id, text=msg)


@app.task()
def download_voice(token, file_id):
    Bot(token).get_file(file_id).download(file_id+'.ogg')
    return file_id+'.ogg'


@app.task()
def recognize_speech(filename):
    print(filename)
    speech_to_text = SpeechToTextV1(iam_apikey=settings.ibm_api_key, url=settings.ibm_api)
    result = speech_to_text.recognize(audio=open(filename, 'rb'), content_type='audio/ogg').get_result()
    return result["results"][0]["alternatives"][0]["transcript"].strip()