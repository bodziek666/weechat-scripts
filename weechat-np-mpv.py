#!/usr/bin/env python2
# -*- coding: utf-8 -*-

import weechat
import json
import socket
import os.path
import os
import fnmatch
import time
import urllib2
from BeautifulSoup import BeautifulSoup

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
        return "Unknown"

    title = np['title'].replace('_', ' ').encode('UTF-8')

    return title

def grab_youtube_url(title):
    yt_base_url = "https://www.youtube.com"
    yt_search_query_str = "/results?search_query={}"

    search_query = title.strip().replace(" ", "+")

    res = urllib2.urlopen(yt_base_url +
                          yt_search_query_str.format(search_query))

    yt_url = ""

    if res.code == 200:
        soup = BeautifulSoup(res.read())
        query = soup.find(attrs={"class": "yt-lockup-title "})
        if query:
            link_part = query.first()["href"]
            yt_url = yt_base_url + link_part

    return yt_url


def mpv_np(data, buffer, args):
    yt_url = ""

    title = parse_info()

    if title != "Unknown":
        yt_url = grab_youtube_url(title)

    np_str = (
        "Now playing: {}"
        " - Link: {}" if yt_url else "{}"
    ).format(title, yt_url)

    weechat.command(weechat.current_buffer(), np_str)
    return weechat.WEECHAT_RC_OK


weechat.register("weechat-np-mpv", "Bodzioslaw aka pwg", "0.1", "LGPL", "Now playing for mpv", "", "")

hook = weechat.hook_command("mpv", "Now playing mpv", "", "", "", "mpv_np", "")
