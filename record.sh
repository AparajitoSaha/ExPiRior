#!/bin/bash
sudo arecord --format=S16_LE --rate=44100 -D hw:1,0 --file-type=wav hi.wav