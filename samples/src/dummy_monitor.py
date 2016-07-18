#!/usr/bin/env python3
# Dummy monitor that connects to a soccerserver and starts a game.
import socket

# soccerserver uses a special connection setup to keep connection state and
# allow dynamic assignment of ports on top of UDP.
#
# The server listens for connection requests on UDP port 6000.
#
# The monitor must bind to some UDP port and send initialization commands to
# 6000. This binded port will be used for the remainder of the session.
#
# The server also allocates an empty port and sends a reply from the newly
# allocated port to the monitor port.
#
# The monitor must save the port from which the server replied and use it for
# communication for the remainder of the session. Now, both the monitor and
# server ports have been assigned.
#
# The server continuously streams the game state to the monitor. The server
# knows that a disconnection happened by watching the status of the send
# operation (UDP does generate errors statuses on send() when sending to
# localhost).

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.bind(('', 0))  # 0 gets an unallocated port on Linux
s.sendto(b'(dispinit version 4)', ('127.0.0.1', 6000))
s.settimeout(0.1)
try:
    while True:
        data, remote_address = s.recvfrom(4096)
        server_port = remote_address[1]
        # Just keep sending dispstart (ignored when game is already started)
        s.sendto(b'(dispstart)', ('127.0.0.1', server_port))
finally:
    s.close()
