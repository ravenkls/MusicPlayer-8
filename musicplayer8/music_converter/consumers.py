import json
from channels.generic.websocket import WebsocketConsumer
from django.conf import settings
import os

from asgiref.sync import async_to_sync
from pydub import AudioSegment
import youtube_dl

import uuid


class ConvertConsumer(WebsocketConsumer):
    def connect(self):
        self.accept()
        self.generated_files = []
    
    def disconnect(self, close_code):
        for f in self.generated_files:
            os.remove(f)

    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        url = text_data_json['url']

        file_path, file = self.convert(url)
        file_url = os.path.join(settings.MEDIA_URL, "songs", file)
        self.generated_files.append(file_path)

        self.send(text_data=json.dumps({
            "progress": 100,
            "src": file_url,
        }))

    def download_hook(self, data):
        if data['status'] == 'finished':
            percent = 50
        else:
            percent = int(float(data["_percent_str"][:-1].strip())*.5)
        
        self.send(text_data=json.dumps({
            "progress": percent
        }))

    def convert(self, url, *, delay=150):
        ytdl = youtube_dl.YoutubeDL({
            'format': 'm4a',
            'noplaylist': True,
            'nocheckcertificate': True,
            'ignoreerrors': False,
            'logtostderr': False,
            'quiet': True,
            'no_warnings': True,
            'outtmpl': os.path.join(settings.MEDIA_ROOT, 'downloaded_songs', '%(id)s.%(ext)s'),
            'progress_hooks': [self.download_hook]
        })

        data = ytdl.extract_info(url)
        file_path = os.path.join(settings.MEDIA_ROOT, 'downloaded_songs', f'{data.get("id")}.m4a')

        path, ext = os.path.splitext(file_path)
        origin_dir = os.path.dirname(path)
        origin_filename = os.path.basename(path)

        a = AudioSegment.from_file(file_path, format="m4a")

        b = AudioSegment.from_file(file_path, format="m4a")

        silent = AudioSegment.silent(duration=delay)
        b = silent.append(b)

        self.send(text_data=json.dumps({
            "progress": 60
        }))

        left = a.pan(-1)
        right = b.pan(+1)
        
        self.send(text_data=json.dumps({
            "progress": 70
        }))

        remixed = left.overlay(right)

        self.send(text_data=json.dumps({
            "progress": 80
        }))
        
        compressed = remixed.set_frame_rate(int(remixed.frame_rate // 2))

        filename = uuid.uuid4().hex + ".mp3"
        os.makedirs(os.path.join(settings.MEDIA_ROOT, 'songs'), exist_ok=True)
    
        path = os.path.join(settings.MEDIA_ROOT, 'songs', filename)
        compressed.export(path)

        os.remove(file_path)

        return path, filename