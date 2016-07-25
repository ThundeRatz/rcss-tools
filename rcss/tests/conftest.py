#!/usr/bin/env python3
import pytest


@pytest.fixture
def rcssserver_output():
    return '''rcssserver-15.2.2

Copyright (C) 1995, 1996, 1997, 1998, 1999 Electrotechnical Laboratory.
2000 - RoboCup Soccer Simulator Maintenance Group.

Simulator Random Seed: 1469335941
CSVSaver: Ready
STDOutSaver: Ready
Using simulator's random seed as Hetero Player Seed: 1469335941

Hit CTRL-C to exit
Starting "/bin/sh -c left_team.sh"
Waiting for players to connect
A new (v14) player (test_left 1) connected.
Starting "/bin/sh -c right_team.sh"
A new (v14) player (test_right 1) connected.
A new (v14) player (test_left 2) connected.
A new (v14) player (test_left 3) connected.
A new (v14) player (test_left 4) connected.
A new (v14) player (test_left 5) connected.
A new (v14) player (test_left 6) connected.
A new (v14) player (test_left 7) connected.
A new (v14) player (test_left 8) connected.
A new (v14) player (test_left 9) connected.
A new (v14) player (test_right 2) connected.
A new (v14) player (test_left 10) connected.
A new (v14) online coach (test_left) connected.
A new (v14) player (test_left 11) connected.
A new (v14) player (test_right 3) connected.
A new (v14) player (test_right 4) connected.
A new (v14) player (test_right 5) connected.
A new (v14) player (test_right 6) connected.
A new (v14) player (test_right 7) connected.
A new (v14) player (test_right 8) connected.
A new (v14) player (test_right 9) connected.
A new (v14) player (test_right 10) connected.
A new (v14) online coach (test_right) connected.
Waiting to kick off
Kick_off_left
Waiting after end of match
A player disconnected : (test_right 4)
A player disconnected : (test_right 2)
A player disconnected : (test_right 3)
A player disconnected : (test_left 5)
A player disconnected : (test_left 7)
An online coach disconnected : (test_left)
An online coach disconnected : (test)
A player disconnected : (test_left 9)
A player disconnected : (test_right 5)
A player disconnected : (test_right 10)
A player disconnected : (test_left 11)
A player disconnected : (test_right 7)
A player disconnected : (test_left 4)
A player disconnected : (test_right 8)
A player disconnected : (test_left 8)
A player disconnected : (test_left 10)
A player disconnected : (test_right 9)
A player disconnected : (test_left 6)
A player disconnected : (test_left 2)
A player disconnected : (test_left 1)
A player disconnected : (test_right 1)
A player disconnected : (test_right 11)
A player disconnected : (test_left 3)
A player disconnected : (test_right 6)
Killing 19539
Killing 19546

Game Over. Exiting...

Saving Results:
\tCSVSaver: saving...
\tCSVSaver: ...saved
\tSTDOutSaver: saving...

Game Results:
\t2016-07-24 01:52:21
\t'test_left' vs 'test_right'
\tScore: 0 - 2

\tSTDOutSaver: ...saved

Saving Results Complete
'''
