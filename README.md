notipy
==========

Very simple XMPP/Jabber notification via HTTP using Flask

Inspired by php-notify (https://github.com/jmara/php-notify)


## Installation

### Clone to your Webserver

    https://github.com/Merenon/notipy.git
    
### Install pip requirements

    pip install -r requirements.txt

### Change the necessary settings and add a *local_settings.py*

    jabber = {
        'id': 'dennis@jabber.example.com',
        'password': 'password',
        'url': 'jabber.example.com',
        'room_prefix': 'conference'
    }

### Run Flask
    
    python notipy.py

## Usage

    curl -F "msg=Test Message" http://notipy.example.com/user/merenon
