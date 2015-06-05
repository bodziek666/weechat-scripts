Weechat scripts written for daily use and learning purposes.
 
Enable socket on mpv startup - add this line to mpv.conf
`input-unix-socket=/tmp/mpvsocket`
 
Tunnel mpv socket over ssh:
`ssh -R/tmp/mpvsocket:/tmp/mpvsocket -p ssh_port user@host`
 
Delete tunneled socket after logout (~/.bash_logout):
`if [ -S /tmp/mpvsocket ]; then`
`   rm /tmp/mpvsocket`
`fi`
