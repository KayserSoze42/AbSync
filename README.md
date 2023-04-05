# AbSync

*Simple Python script for a scheduled synchronization*


## Usage:

**_Unix / macOS:_**

    python3 -m AbSync <target/path> <destination/path> <interval in seconds> <logfile/path>

**_Windows:_**

    py -m AbSync <target/path> <destination/path> <interval in seconds> <logfile/path>


*example : python3 -m AbSync project/original project/copy 360 project/logs*

Running the script starts initial sync, creates directories if not found and schedules sync with given delay

--------------------

## Installation:

- Download and then install the latest release using:

        pip install AbSync-<Version Number>.tar.gz

- Build your own with *python -m build*

--------------------

## Requirements:

    schedule

--------------------

## Description:

It's really just a basic script, not great, but done with great hope.

Basically, it makes a backup of a directory with a delay in seconds.

First it performs os.walk() for the target and destination directories. It stores the results and then compares the lists.

By comparing target list to the destination, it gets files and directories not present in the destination.
If a file is present in both target and destination, it compares the files by checking file sizes and comparing MD5 hashes.

By comparing destination list to the target, it gets files and directories not present in the target.

The results are saved in copyList and cleanList

It iterates over both lists, first removing files and directories from destination(going last to first) and then
creating directories and copying files from target to destination.

The whole process is found in *AbSync.sync()* function

By calling the main function, it schedules the *AbSync.sync()* job using *AbSync.scheduleSync()* with **schedule** library

--------------------

## Planned Changes:

- Improve comparison:
  
  * Find solutions for cases: 
    
    + File/directory renamed
    
    + File/directory moved  
      
    + ~~IndexError - find another way to unpack and manipulate lists~~
    
  * Add different methods to avoid hashing if not needed

- Improve scheduling

- Threading / Multiprocessing (?)

  * Computing hashes
  
  * Copying
  
- General Code Improvements:
  
  * Exception/Error Handling
    
  * Logging
  
  * Tests 

  * Packaging names and structure
  


