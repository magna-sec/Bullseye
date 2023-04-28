#!/bin/bash

cvlc -vvv --no-audio /home/vlc-user/stream.mp4 --sout "#transcode{vcodec=theo,vb=800,acodec=none}:http{mux=ogg,dst=:8081/}" --loop
