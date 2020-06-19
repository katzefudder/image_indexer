# Multi-Threaded Indexer for jpg images
[![Build Status](https://travis-ci.org/katzefudder/image_indexer.svg?branch=master)](https://travis-ci.org/katzefudder/image_indexer)
![Testing Indexer](https://github.com/katzefudder/image_indexer/workflows/Testing%20Indexer/badge.svg)

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
`docker run -v $(pwd):/app mypy ./indexer.py images target -t 8`

## What it does

### Workflow
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

### Meta tags: Exif, IPTC
Dealing with enclosed meta tags is also an issue I have to deal with.
Pictures are enriched with a vast amount of information, so any indexing script should scrape that information.
Currently, the indexer exports a `meta.json` file, with a list of objects according to the indexed files:

```
{
    "testimage": {
        "exif": {
            "ExifVersion": "b'0231'",
            "ShutterSpeedValue": "(9965784, 1000000)",
            "ApertureValue": "(2275007, 1000000)",
            "DateTimeOriginal": "2020:03:01 20:19:20",
            "DateTimeDigitized": "2020:03:01 20:19:20",
            "ExposureBiasValue": "(0, 6)",
            "MaxApertureValue": "(20, 10)",
            "MeteringMode": "2",
            "LightSource": "0",
            "Flash": "0",
            "FocalLength": "(2000, 10)",
            "ColorSpace": "1",
            "WhiteBalance": "0",
            "FocalLengthIn35mmFilm": "200",
            "SceneCaptureType": "0",
            "GainControl": "1",
            "SubsecTimeOriginal": "80",
            "SubsecTimeDigitized": "80",
            "SubjectDistanceRange": "0",
            "Model": "NIKON D850",
            "SensingMethod": "2",
            "Make": "NIKON CORPORATION",
            "FileSource": "b'\\x03'",
            "ExposureTime": "(1, 1000)",
            "XResolution": "(300, 1)",
            "YResolution": "(300, 1)",
            "FNumber": "(22, 10)",
            "SceneType": "b'\\x01'",
            "ExposureProgram": "1",
            "CFAPattern": "b'\\x02\\x00\\x02\\x00\\x00\\x01\\x01\\x02'",
            "CustomRendered": "0",
            "ISOSpeedRatings": "2500",
            "ResolutionUnit": "2",
            "ExposureMode": "1",
            "BodySerialNumber": "6022867",
            "LensSpecification": "((2000, 10), (2000, 10), (20, 10), (20, 10))",
            "LensModel": "200.0 mm f/2.0",
            "Software": "Adobe Photoshop Lightroom Classic 9.2 (Macintosh)",
            "DateTime": "2020:03:02 08:19:20",
            "Artist": "A. Chuc",
            "Contrast": "0",
            "Saturation": "0",
            "ImageDescription": "-71- Sami Blomqvist (ESV Kaufbeuren) versucht einen Schuss abzufÃ¤lschen, -31- Felix Bick (EC Bad Nauheim) ist auf dem Posten, in der DEL 2 - EC Bad Nauheim gegen ESV Kaufbeuren, Bad Nauheim, Colonel-Knight-Stadion, 01.03.20",
            "Sharpness": "0",
            "ExifOffset": "484",
            "filename": "/app/images/a_gallery/testimage.jpg",
            "width": 4000,
            "height": 2667
        },
        "iptc": {
            "CodedCharacterSet": "\u001b%G",
            "Whatever": "\u0000\u0004",
            "ObjectName": "in der DEL 2 - EC Bad Nauheim gegen ESV Kaufbeuren",
            "Urgency": "1",
            "Category": "Spo",
            "Keywords": [
                "19/20",
                "2019/20",
                "Buron Jokers",
                "CKS",
                "Colonel-Knight-Stadion",
                "DEL 2",
                "DEL2",
                "EC Bad Nauheim",
                "ESV Kaufbeuren",
                "Eishockey",
                "Eissport",
                "Icehockey",
                "Kurstadt",
                "Mannschaft",
                "Rote Teufel",
                "Sason 2019/2020",
                "Stadion",
                "Team",
                "Wetterau",
                "Winter",
                "Wintersport",
                "hockey"
            ],
            "CreationDate": "20200301",
            "CreationTime": "201920",
            "DigitizationDate": "20200301",
            "(2, 63)": "201920+0100",
            "AuthorByline": "A. Chuc",
            "City": "Bad Nauheim",
            "SubLocation": "Colonel-Knight-Stadion",
            "State": "Hessen",
            "CountryCode": "DEU",
            "Country": "Deutschland",
            "Headline": "in der DEL 2 - EC Bad Nauheim gegen ESV Kaufbeuren",
            "Caption": "-71- Sami Blomqvist (ESV Kaufbeuren) versucht einen Schuss abzufälschen, -31- Felix Bick (EC Bad Nauheim) ist auf dem Posten, in der DEL 2 - EC Bad Nauheim gegen ESV Kaufbeuren, Bad Nauheim, Colonel-Knight-Stadion, 01.03.20",
            "CaptionWriter": "A. Chuc"
        }
    },
    ...
}
```
