from datetime import datetime
import threading
import requests
import os
from dotenv import load_dotenv

### init ###

load_dotenv()

client_id = os.getenv('TWITCH_CLIENT_ID')
client_secret = os.getenv('TWITCH_CLIENT_SECRET')

### functions ###

def get_oauth_token(client_id, client_secret):
    url = 'https://id.twitch.tv/oauth2/token'
    params = {
        'client_id': client_id,
        'client_secret': client_secret,
        'grant_type': 'client_credentials'
    }
    response = requests.post(url, params=params)
    response_data = response.json()
    return response_data['access_token']


def update_time():
    now = datetime.now()

    formatted = now.strftime("%H:%M")
    f = open("time.txt","w")
    f.write(formatted)
    threading.Timer(1.0,update_time).start()


def get_stream_info(client_id, oauth_token, channel_name):
    url = f'https://api.twitch.tv/helix/streams?user_login={channel_name}'
    headers = {
        'Client-ID': client_id,
        'Authorization': f'Bearer {oauth_token}'
    }
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        data = response.json()
        if data['data']:
            stream_info = data['data'][0]
            viewer_count = stream_info['viewer_count']
            return viewer_count
        else:
            return -1
    else:
        return -2


def update_viewers():
    count = get_stream_info(client_id, oauth_token, "toulouselaststock")
    f = open("viewers.txt","w")
    f.write(str(count))
    threading.Timer(10.0,update_viewers).start()


def update_nominees():
    title = input("Titre ?")
    winner = input("Gagnant.e du titre ?")
    gender = input("Genre de la phrase (M/F/N) ?") # mon code est WOKE
    f = open("latest.txt","w",encoding="utf-8")
    if (gender == "F"):
        f.write(f"Derniere nominée : {winner} ({title})")
    elif (gender == "M"):
        f.write(f"Dernier nominé : {winner} ({title})")
    else:
        f.write(f"Dernier.e nominé.e : {winner} ({title})")

    threading.Timer(1.0,update_nominees).start()

### launch ###

def start():
    threading.Timer(1.0,update_time).start()
    threading.Timer(10.0,update_viewers).start()
    threading.Timer(1.0,update_nominees).start()
    

oauth_token = get_oauth_token(client_id, client_secret)

start()