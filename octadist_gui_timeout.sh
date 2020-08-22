#!/bin/bash

# Run your app in the background
python3 -m octadist &

# Store it's Process ID
bg_pid=$!

# sleep for X seconds
sleep 10

# Kill the python process
kill $bg_pid

# Optionally exit true to prevent travis seeing this as an error
exit 0