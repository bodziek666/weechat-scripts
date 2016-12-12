#!/usr/bin/env python2
# -*- coding: utf-8 -*-

import weechat
import urllib2 
import re 

def get_mpc_hc_info():
   player = urllib2.urlopen("http://pwg.space/mpc.html").read()
   info = re.search('&laquo;\s(.*)\s&bull;\s(.*)\s&bull;\s(.*)\s&bull;', player)
   filename = info.group(2)
   progress = info.group(3)
   version = info.group(1)
   return filename, progress, version

def get_mpc_hc_status():
   player = urllib2.urlopen("http://pwg.space/mpc_status.html").read()
   status = re.search('\("(.*?)",\s"(.*?)",\s(\d*),\s"(.*?)",\s(\d*),\s"(.*?)",', player)
   filename = status.group(1)
   pos = int(status.group(3))
   dur = int(status.group(5))
   pos_str = status.group(4)
   dur_str = status.group(6)
   percent = int((pos/dur) * 100)
   bar_prog = int(round((pos/dur)*15, 1))
   bar = '['+'>'*bar_prog+'-'*(15-bar_prog)+']'
   return filename, pos_str, dur_str, percent, bar 


def mpc_hc_np(data, buffer, args):
   filename, pos_str, dur_str, percent, bar = get_mpc_hc_status()
   weechat.command(weechat.current_buffer(),
      "/me is watching \x02{} {}/{} {} ({}%)".format(filename, pos_str, dur_str, bar, percent))
   return weechat.WEECHAT_RC_OK

def mpc_hc_info(data, buffer, args):
   filename, progress, version = get_mpc_hc_info()
   weechat.command(weechat.current_buffer(),
      "/me is watching \x02{} \x0Fat \x02{} \x0Fvia \x02{}".format(filename, progress, version))
   return weechat.WEECHAT_RC_OK
   
weechat.register("weechat-np-mpv", "Bodzioslaw aka pwg", "0.1", "LGPL", "Simple mow playing for mpc_hc", "", "")

hook = weechat.hook_command("mpc", "Now playing mpc-hc", "", "", "", "mpc_hc_np", "")

hook = weechat.hook_command("mpc-info", "mpc-hc info", "", "", "", "mpc_hc_info", "")
