#!/bin/sh
while inotifywait -r -e modify ./notato; do
    python -m unittest discover -v
done
