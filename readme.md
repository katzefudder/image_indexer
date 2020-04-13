# Multi-Threaded Indexer for jpg images
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

Processing 74 images (roughly 3.5 MByte each) takes about 6.2 seconds on my 8-core 2019 MacBook using 8 threads to process data.

```
docker run -v $(pwd):/app mypy indexer.py images target -t 8      
docker
Use 8 threads to index 74 files

Processed Files:
--------------------------------------------
/app/images/20200221_ECBN_Ravnsbrg_130.jpg
/app/images/20200221_ECBN_Ravnsbrg_078.jpg
/app/images/20200221_ECBN_Ravnsbrg_090.jpg
/app/images/20200221_ECBN_Ravnsbrg_081.jpg
/app/images/20200221_ECBN_Ravnsbrg_133.jpg
/app/images/20200221_ECBN_Ravnsbrg_119.jpg
/app/images/20200221_ECBN_Ravnsbrg_092.jpg
/app/images/20200221_ECBN_Ravnsbrg_085.jpg
/app/images/20200221_ECBN_Ravnsbrg_124.jpg
/app/images/20200221_ECBN_Ravnsbrg_132.jpg
/app/images/20200221_ECBN_Ravnsbrg_084.jpg
/app/images/20200221_ECBN_Ravnsbrg_087.jpg
/app/images/20200221_ECBN_Ravnsbrg_122.jpg
/app/images/20200221_ECBN_Ravnsbrg_086.jpg
/app/images/20200221_ECBN_Ravnsbrg_091.jpg
/app/images/20200221_ECBN_Ravnsbrg_125.jpg
/app/images/20200221_ECBN_Ravnsbrg_118.jpg
/app/images/20200221_ECBN_Ravnsbrg_127.jpg
/app/images/20200221_ECBN_Ravnsbrg_126.jpg
/app/images/20200221_ECBN_Ravnsbrg_093.jpg
/app/images/20200221_ECBN_Ravnsbrg_136.jpg
/app/images/20200221_ECBN_Ravnsbrg_131.jpg
/app/images/20200221_ECBN_Ravnsbrg_079.jpg
/app/images/20200221_ECBN_Ravnsbrg_095.jpg
/app/images/20200221_ECBN_Ravnsbrg_137.jpg
/app/images/20200221_ECBN_Ravnsbrg_145.jpg
/app/images/20200221_ECBN_Ravnsbrg_147.jpg
/app/images/20200221_ECBN_Ravnsbrg_080.jpg
/app/images/20200221_ECBN_Ravnsbrg_142.jpg
/app/images/20200221_ECBN_Ravnsbrg_096.jpg
/app/images/20200221_ECBN_Ravnsbrg_108.jpg
/app/images/20200221_ECBN_Ravnsbrg_121.jpg
/app/images/20200221_ECBN_Ravnsbrg_146.jpg
/app/images/20200221_ECBN_Ravnsbrg_141.jpg
/app/images/20200221_ECBN_Ravnsbrg_123.jpg
/app/images/20200221_ECBN_Ravnsbrg_094.jpg
/app/images/20200221_ECBN_Ravnsbrg_097.jpg
/app/images/20200221_ECBN_Ravnsbrg_143.jpg
/app/images/20200221_ECBN_Ravnsbrg_109.jpg
/app/images/20200221_ECBN_Ravnsbrg_120.jpg
/app/images/20200221_ECBN_Ravnsbrg_144.jpg
/app/images/20200221_ECBN_Ravnsbrg_140.jpg
/app/images/20200221_ECBN_Ravnsbrg_083.jpg
/app/images/20200221_ECBN_Ravnsbrg_148.jpg
/app/images/20200221_ECBN_Ravnsbrg_082.jpg
/app/images/20200221_ECBN_Ravnsbrg_135.jpg
/app/images/20200221_ECBN_Ravnsbrg_149.jpg
/app/images/20200221_ECBN_Ravnsbrg_134.jpg
/app/images/20200221_ECBN_Ravnsbrg_139.jpg
/app/images/20200221_ECBN_Ravnsbrg_098.jpg
/app/images/20200221_ECBN_Ravnsbrg_110.jpg
/app/images/20200221_ECBN_Ravnsbrg_112.jpg
/app/images/20200221_ECBN_Ravnsbrg_102.jpg
/app/images/20200221_ECBN_Ravnsbrg_103.jpg
/app/images/20200221_ECBN_Ravnsbrg_111.jpg
/app/images/20200221_ECBN_Ravnsbrg_114.jpg
/app/images/20200221_ECBN_Ravnsbrg_077.jpg
/app/images/20200221_ECBN_Ravnsbrg_138.jpg
/app/images/20200221_ECBN_Ravnsbrg_099.jpg
/app/images/20200221_ECBN_Ravnsbrg_113.jpg
/app/images/20200221_ECBN_Ravnsbrg_117.jpg
/app/images/20200221_ECBN_Ravnsbrg_089.jpg
/app/images/20200221_ECBN_Ravnsbrg_105.jpg
/app/images/20200221_ECBN_Ravnsbrg_100.jpg
/app/images/20200221_ECBN_Ravnsbrg_088.jpg
/app/images/20200221_ECBN_Ravnsbrg_104.jpg
/app/images/20200221_ECBN_Ravnsbrg_106.jpg
/app/images/20200221_ECBN_Ravnsbrg_116.jpg
/app/images/20200221_ECBN_Ravnsbrg_107.jpg
/app/images/20200221_ECBN_Ravnsbrg_128.jpg
/app/images/20200221_ECBN_Ravnsbrg_115.jpg
/app/images/20200221_ECBN_Ravnsbrg_101.jpg
/app/images/20200221_ECBN_Ravnsbrg_129.jpg

Omitted files:
--------------------------------------------
/app/images/.DS_Store

Indexing took 0:00:06.207444 for 74 files
```
