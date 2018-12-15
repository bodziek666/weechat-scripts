#!/usr/bin/env python2
# -*- coding: utf-8 -*-

import weechat
import json
import socket
import os.path
import os
import fnmatch
import time

def find_mpv_socket():
    base_dir = "/tmp"
    mpv_sock_pattern ='*mpv*.sock'
    matches = []
    for root, dirnames, filenames in os.walk(base_dir):
        for filename in fnmatch.filter(filenames, mpv_sock_pattern):
            matches.append(os.path.join(root, filename))
    if not matches or len(matches) > 1:
        raise Exception
    return matches.pop()

def get_mpv_info():
    mpv_socket = find_mpv_socket()
    client = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
    client.connect(mpv_socket)
    res = {}
    #
    # Length property was deprecated after the mpv 0.9 release, use 'duration' instead
    #
    for i in ['title']: # TODO add more things later
        req = '{{"command": ["get_property", "{}"]}}\n'.format(i)
        client.send(req)
        res[i] = json.loads(client.recv(1024))['data']

    client.close()
    return res

def parse_info():
    try:
        np = get_mpv_info()
    except:
        return ("Unknown")

    title = np['title'].replace('_', ' ').encode('UTF-8')

    return title

def mpv_np(data, buffer, args):
    title = parse_info()
    weechat.command(weechat.current_buffer(),
            "Now playing: {}".format(title))
    return weechat.WEECHAT_RC_OK


weechat.register("weechat-np-mpv", "Bodzioslaw aka pwg", "0.1", "LGPL", "Now playing for mpv", "", "")

hook = weechat.hook_command("mpv", "Now playing mpv", "", "", "", "mpv_np", "")
