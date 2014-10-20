############################################
#                  _   _                   #
#      _ __   ___ | |_(_)_ __  _   _       #
#     | '_ \ / _ \| __| | '_ \| | | |      #
#     | | | | (_) | |_| | |_) | |_| |_     #
#     |_| |_|\___/ \__|_| .__/ \__, (_)    #
#                       |_|    |___/       #
#                                          #
#      @author Dennis Detering             #
#      @email <yo@dety.eu>                 #
#      @version 1.1                        #
#                                          #
############################################

from netaddr import IPAddress, IPNetwork
from jabberbot import JabberBot
from flask import Flask, request, jsonify, abort

# Load config object from local_settings.py
try:
    from local_settings import *
except ImportError:
    print "[!] Error: no 'local_settings.py' config found!"
    exit(1)

# Connect JabberBot
try:
    bot = JabberBot(jabber['id'], jabber['password'], debug=False)
    bot.connect()
    if bot.conn:
        print '[+] JabberBot connected!'
except:
    raise

app = Flask(__name__)


# Check for allowed IPs
@app.before_request
def limit_remote_addr():
    IP = IPAddress(request.remote_addr)
    if not any(IP in IPNetwork(x) for x in allowed_ips):
        abort(403)


@app.route('/')
def home():
    return 'Hi, I\'m your notipy bot.'


# Send message to user
@app.route('/user/<username>', methods=['POST', 'GET'])
def user(username):
    message = None

    if request.method == 'POST':
        message = request.form.get('msg', '')
    elif request.method == 'GET':
        message = request.args.get('msg', '')

    if not message:
        return jsonify({'success': False, 'message': 'No message set'})

    try:
        bot.send("%s@%s" % (username, jabber['url']), message, None, "chat")

        if app.debug:
            print '[+] Message send to user %s' % username
    except:
        return jsonify({'success': False})

    return jsonify({'success': True})


# Send message to room
@app.route('/room/<roomname>', methods=['POST', 'GET'])
def room(roomname):
    message = None

    if request.method == 'POST':
        message = request.form.get('msg', '')
    elif request.method == 'GET':
        message = request.args.get('msg', '')

    if not message:
        return jsonify({'success': False, 'message': 'No message set'})

    try:
        bot.join_room('%s@%s.%s' % (roomname, jabber['room_prefix'], jabber['url']))
        bot.send('%s@%s.%s' % (roomname, jabber['room_prefix'], jabber['url']), message, None, "groupchat")

        if app.debug:
            print '[+] Message send to room %s' % roomname
    except:
        return jsonify({'success': False})

    return jsonify({'success': True})


if __name__ == "__main__":
    app.debug = True
    app.run()
