# AbSync
Simple Python script for a scheduled synchronization between two directories

Keeps the target file and directory structure synchronized with destination directory, by checking for differences using simple MD5 hash
and removing and copying directories and files at given interval in seconds

To run the script use AbSync.py, pass target and destination directory location, interval and logfile location:

---------------------------

> Usage: python AbSync.py "target path" "destination path" interval(seconds) "logfile path"

---------------------------

Requirements: schedule library

---------------------------
