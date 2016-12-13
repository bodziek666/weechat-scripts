#!/usr/bin/env python2
# -*- coding: utf-8 -*-

import weechat
import urllib2 
import re 

def get_mpc_hc_info():
   player = urllib2.urlopen("http://127.0.0.1:13579/info.html").read()
   info = re.search('&laquo;\s(.*)\s&bull;\s(.*)\s&bull;\s(.*)\s&bull;', player)
   version, filename, progress = info.groups()
   filename = filename.replace('_', ' ').encode('UTF-8')
   return filename, progress, version

def get_mpc_hc_status():
   player = urllib2.urlopen("http://127.0.0.1:13579/status.html").read()
   status = re.search('\("(.*?)",\s"(.*?)",\s(\d*),\s"(.*?)",\s(\d*),\s"(.*?)",', player)
   filename, _, pos, pos_str, dur, dur_str = status.groups()
   filename = filename.replace('_', ' ').encode('UTF-8')
   return filename, pos, pos_str, dur, dur_str

def parse_mpc_hc_status():
    filename, pos, pos_str, dur, dur_str = get_mpc_hc_status()
    pos = float(pos)
    dur = float(dur)
    percent = int((pos/dur) * 100)
    bar_prog = int(round((pos/dur)*15, 1))
    bar = '['+'>'*bar_prog+'-'*(15-bar_prog)+']'
    return filename, pos_str, dur_str, percent, bar 

def mpc_hc_np(data, buffer, args):
   filename, pos_str, dur_str, percent, bar = parse_mpc_hc_status()
   weechat.command(weechat.current_buffer(),
      "/me is watching \x02{} {}/{} {} ({}%)".format(filename, pos_str, dur_str, bar, percent))
   return weechat.WEECHAT_RC_OK

def mpc_hc_info(data, buffer, args):
   filename, progress, version = get_mpc_hc_info()
   weechat.command(weechat.current_buffer(),
      "/me is watching \x02{} \x0Fat \x02{} \x0Fvia \x02{}".format(filename, progress, version))
   return weechat.WEECHAT_RC_OK
   
weechat.register("weechat-np-mpc-hc", "Bodzioslaw aka pwg", "0.2", "LGPL", "Simple mow playing for mpc_hc", "", "")

hook = weechat.hook_command("mpc", "Now playing mpc-hc", "", "", "", "mpc_hc_np", "")

hook = weechat.hook_command("mpc-info", "mpc-hc info", "", "", "", "mpc_hc_info", "")
