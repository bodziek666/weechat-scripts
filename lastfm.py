#           DO WHAT THE FUCK YOU WANT TO PUBLIC LICENSE
#                   Version 2, December 2004
# 
# Copyright (C) 2019 pwg96 (bodzioslaw aka pwg)
#
# Everyone is permitted to copy and distribute verbatim or modified
# copies of this license document, and changing it is allowed as long
# as the name is changed.
# 
#           DO WHAT THE FUCK YOU WANT TO PUBLIC LICENSE
#  TERMS AND CONDITIONS FOR COPYING, DISTRIBUTION AND MODIFICATION
#
# 0. You just DO WHAT THE FUCK YOU WANT TO.
#
# HOW TO USE:
# Set your lastfm username before using this script like this: 
#
# /set plugins.var.python.lastfm.username yourusername
#
# You can also change lastfm_url, api_key and timeout by using:
#
# /set plugins.var.python.lastfm.api_key your_api_key
# /set plugins.var.python.lastfm.api_url api_url
# /set plugins.var.python.lastfm.timeout 20000 (default: 30000)
#
# That's all!

SCRIPT_NAME = "lastfm"
SCRIPT_AUTHOR = "pwg96 (bodzioslaw aka pwg)"
SCRIPT_VERSION = "0.1"
SCRIPT_LICENSE = "WTFPL"

SCRIPT_DESC = "Sends your latest last.fm track to the current buffer"
SCRIPT_COMMAND = "lastfm"

try:
    import weechat
except:
    print("This script must be run under WeeChat.")
    print("Get WeeChat now at: https://weechat.org/")
    quit()

import json

def lastfm_get_track(data, command, rc, stdout, stderr):

    try:
        lastfm_response = json.loads(stdout)

        if "error" in lastfm_response:
            weechat.prnt('', 
                "last.fm api error: '{}'".format(lastfm_response['message']))
        else:
            
            artist = lastfm_response['recenttracks']['track'][0]['artist']['#text']
            track = lastfm_response['recenttracks']['track'][0]['name']
            album = lastfm_response['recenttracks']['track'][0]['album']['#text']

            if album:
                weechat.command(weechat.current_buffer(), 
                    "/me np: \x02{}\x02 – \x02{}\x02 from album: \x02{}\x02".format(artist, track, album))
            else:
                weechat.command(weechat.current_buffer(), 
                    "/me np: \x02{}\x02 – \x02{}\x02".format(artist, track))

    except Exception as e:
        weechat.prnt('', "Error parsing last.fm response: " + str(e))

    return weechat.WEECHAT_RC_OK

def lastfm_np(data, buffer, args):

    lastfm_username = weechat.config_get_plugin('username').lower()
    lastfm_api_key = weechat.config_get_plugin('api_key')
    lastfm_api_url = weechat.config_get_plugin('api_url')
    timeout = int(weechat.config_get_plugin('timeout'))

    lastfm_url = 'url:' + lastfm_api_url.format(username=lastfm_username,
        api_key=lastfm_api_key)

    if lastfm_username:
        lastfm_hook_process = weechat.hook_process(lastfm_url,
            timeout, "lastfm_get_track", "")
    else:
        weechat.prnt('',
            "lastfm: please set your last.fm username: /set plugins.var.python.lastfm.username yourusername")

    return weechat.WEECHAT_RC_OK

weechat.register(SCRIPT_NAME, SCRIPT_AUTHOR, SCRIPT_VERSION, 
    SCRIPT_LICENSE, SCRIPT_DESC, "", "")

lastfm_config = {
    "username": "",
    "api_key": "618f9ef38b3d0fed172a88c45ae67f33",
    "api_url": "https://ws.audioscrobbler.com/2.0/?method=user.getrecenttracks&user={username}&api_key={api_key}&format=json&limit=1&extended=0",
    "timeout": "30000"
} 

# set defaults
for option, default_value in lastfm_config.items():
    if not weechat.config_is_set_plugin(option):
        weechat.config_set_plugin(option, default_value)

hook = weechat.hook_command(SCRIPT_COMMAND, SCRIPT_DESC, "", "", "",
    "lastfm_np", "")