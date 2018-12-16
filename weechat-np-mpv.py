#!/usr/bin/env python2
# -*- coding: utf-8 -*-

import weechat
import json
import socket
import os.path
import os
import fnmatch
import urllib2

from HTMLParser import HTMLParser


class FirstYoutubeURLFetcher(HTMLParser):

    def __init__(self, title):
        self.yt_base_url = "https://www.youtube.com"
        self.yt_url = ""
        self.title=title
        self.__first_url_tag = ""
        HTMLParser.__init__(self)


    def make_request(self):
        yt_search_query_str = "/results?search_query={}"
        search_query = self.title.strip().replace(" ", "+")
        res = urllib2.urlopen(self.yt_base_url +
                              yt_search_query_str.format(search_query))
        return res

    def find_youtube_url(self):
        res = self.make_request()
        if res.code == 200:
            print(res)
            self.feed(res.read())
        return self.yt_url

    def handle_starttag(self, tag, attrs):
        if tag == "h3":
            for attr in attrs:
                if "yt-lockup-title " in attr:
                    self.__first_url_tag = tag
                    return

        elif tag == "a" and self.__first_url_tag:
            for attribs in attrs:
                attr, link_part = attribs
                if "href" in attr:
                    self.yt_url = self.yt_base_url + link_part
                    return


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
    f = FirstYoutubeURLFetcher(title)
    res = f.make_request()
    f.feed(res.read())
    return f.yt_url


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
