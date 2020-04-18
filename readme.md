# Multi-Threaded Indexer for jpg images
[![Build Status](https://travis-ci.org/katzefudder/image_indexer.svg?branch=master)](https://travis-ci.org/katzefudder/image_indexer)

Started as a side project for myself to get my head into image processing and multi-threading in Python.
As a photographer, I tend to shoot lots of photos, especially when shooting ice hockey
Depending on the occasion you shoot your photos, you might end up with Gigabytes of data to process - even on a fast machine, this is going to take at least some time.
I used to have an indexer written in good old PHP, running on a web server. This PHP indexer is then triggered when someone uploads images via SFTP. As PHP is not that good with multi-threading, this indexer will take a while to process all images being uploaded. After uploading and indexing would have finished, all processed images would show up on the website.
As the indexing part was taking more and more time to process the ever-growing file sizes of today's cameras, I decided to re-write the indexing part.

## Use a Docker environment
For not to having to mess up my computer, I decided to "dockerize" the environment to work in.
To build the Docker image use the following
`docker build -t mypy .`

To spin up a Docker container to run my indexer use the following after having built the Docker image
`docker run -v $(pwd):/app mypy indexer.py images target -t 8`

## What it does
I often have to process many photos, resize them, watermark them, do something else about them programmatically. 
Say, you end up with a folder of 74 hi-res images of a hockey game (roughly 260MB) and rely on a structure like this

```
originals
    - hockey_game_1
    - hockey_game_2
    - ...
thumbnails
    - hockey_game_1
        - min_resolution
        - med_resolution
        - max_resolution
    - hockey_game_2
        - min_resolution
        - ...
    - ...
```

Processing 74 images (roughly 3.0 MByte each) takes about 6.2 seconds on my 8-core 2019 MacBook using 8 threads to process data.

```
docker run -v $(pwd):/app mypy indexer.py images target -t 8      
docker
Use 8 threads to index 74 files

Processed Files:
--------------------------------------------
/app/images/20200221_ECBN_Ravnsbrg_130.jpg
/app/images/20200221_ECBN_Ravnsbrg_078.jpg
/app/images/20200221_ECBN_Ravnsbrg_090.jpg
[...]
/app/images/20200221_ECBN_Ravnsbrg_129.jpg

Omitted files:
--------------------------------------------
/app/images/.DS_Store

Indexing took 0:00:06.564612 for 74 files (223.75 MB)
```
