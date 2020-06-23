<div style="text-align: center">
    <img src="https://i.imgur.com/z0Ltyxq.png">
    <p style="font-size: 1.5em; margin-top: 0; margin-bottom: 2em;">Listen to your favourite music from a unique perspective</p>
</div>

A simple web app that converts songs from YouTube or soundcloud (anything that YouTubeDL supports) into a '3D'
rendition. This is done by delaying the left channel by approximately 100 miliseconds, this of course means that the
effect only works using headphones with a left and right channel.

## Screenshots
<img src="https://i.imgur.com/XuGJdHK.png">

## Installation

### Requirements
 - Docker & Docker Compose

### Steps

1. Clone the repository
```bash
git clone https://github.com/ravenkls/MusicPlayer-8.git && cd MusicPlayer-8
```

2. Spin up the docker containers
```bash
docker-compose up -d
```

3. View the web app on http://localhost:8000