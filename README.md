Weechat scripts written for daily use and learning purposes.
 
Enable socket on mpv startup - add this line to mpv.conf
`input-unix-socket=/tmp/mpvsocket` or `input-ipc-server=/tmp/mpvsocket` 
It depends on mpv version. 

Tunnel mpv socket over ssh:
`ssh -R/tmp/mpvsocket:/tmp/mpvsocket -p ssh_port user@host`
 
Delete tunneled socket after logout (add these lines to ~/.bash_logout):
```
if [ -S /tmp/mpvsocket ]; then
   rm /tmp/mpvsocket
fi
```
