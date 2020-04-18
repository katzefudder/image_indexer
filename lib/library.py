import os, sys, glob, ntpath, math
from datetime import datetime
from PIL import Image, IptcImagePlugin, ExifTags
from multiprocessing import pool
from multiprocessing.dummy import Pool 
import json

class Library:
    size = {"min":250, "med":450, "max":800}
    threads = 1
    sourceDir = ""
    targetDir = ''
    files = []
    processedFiles = []
    processedFileSize = 0
    omittedFiles = []
    moveOriginalFiles = True
    watermark = "watermark.png"
    
    exifData = []

    def __init__(self, sourceDir, targetDir):
        self.sourceDir = sourceDir
        self.targetDir = targetDir
        self.files = self.walk_directory(self.sourceDir)

    def setMoveOriginalFiles(self, moveOriginalFiles):
        self.moveOriginalFiles = moveOriginalFiles

    def setThreads(self, threads):
        self.threads = threads
    
    def setSourceDir(self, sourceDir):
        self.sourceDir = sourceDir

    def setTargetDir(self, targetDir):
        self.targetDir = targetDir

    def process_images(self):
        begin_time = datetime.now()
        print("\nUse %d threads to index %d files" % (self.threads, len(self.files)))
        self.useThreading(self.threads)
        
        # export all exif data to json file
        self.serializeMetadata()

        print("\nProcessed Files:")
        print("--------------------------------------------")
        print(*self.processedFiles, sep='\n')
        print("\nOmitted files:")
        print("--------------------------------------------")
        print(*self.omittedFiles, sep='\n')
        print("\nIndexing took %s for %d files (%s)" % ((datetime.now() - begin_time), len(self.files), self.convert_size(self.processedFileSize)))

    def serializeMetadata(self):
        with open('data.json', 'w', encoding='utf-8') as file:
            json.dump(self.exifData, file, ensure_ascii=False, indent=4)    

    def useThreading(self, threads):
        pool = Pool(threads)
        pool.map(self.handleImage, self.files)

    def handleImage(self, source, extensionAllowed = '.jpg'):
        pictureName, extension = os.path.splitext(source)
        if extension == extensionAllowed:
            # iterate over different image sizes
            originalPhoto = Image.open(source)
            
            for category, size in self.size.items():
                thumbTarget = self.targetDir + "/" + category
                
                # create thumbnail directory, ignore if existing
                self.createDirectory(thumbTarget)

                photo = Image.open(source)

                photo.thumbnail((size, size), Image.ANTIALIAS)
                thumbnailFilename = thumbTarget + "/" + os.path.basename(source)
                # add image to list

                if size > self.size['med']:
                    photo = self.addWatermark(self.size['max'], photo)

                photo.save(thumbnailFilename, "JPEG")
                
            self.handleProcessedFile(originalPhoto)
        else:
            # all other files should be ommitted
            self.omittedFiles.append(source)

    def convert_size(self, sizeByte):
        if sizeByte == 0:
            return "0B"
        size_name = ("B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB")
        i = int(math.floor(math.log(sizeByte, 1024)))
        p = math.pow(1024, i)
        s = round(sizeByte / p, 2)
        return "%s %s" % (s, size_name[i])

    def handleProcessedFile(self, photo):
        self.extractExif(photo) # extract Exif metadata
        self.processedFileSize += os.path.getsize(photo.filename) # sum up file sizes
        self.processedFiles.append(photo.filename) # add the processed file to the list of processed files
        
        if self.moveOriginalFiles:
            processedImageDir = self.targetDir + "/original" # processed images should go to this folder
            self.createDirectory(processedImageDir) # create directory for original files
            processedImage = processedImageDir + "/" + ntpath.basename(photo.filename)
            os.rename(photo.filename, processedImage) # when processed, move the processed file away

    def createDirectory(self, directory):
        # create thumbnail directory, ignore if existing
        if not os.path.exists(directory):
            try:
                os.mkdir(directory)
            except FileExistsError:
                pass

    def extractExif(self, image):
        exif_data = image._getexif()
        exif = {
            ExifTags.TAGS[k]: str(v)
            for k, v in image._getexif().items()
            if k in ExifTags.TAGS
        }
        exif.update({'filename':image.filename})
        exif.update({'width':image.size[0]})
        exif.update({'height':image.size[1]})
        self.exifData.append(exif)

    def extractIptc(self, image):
        iptc = IptcImagePlugin.getiptcinfo(image)

        if iptc:
            for k, v in iptc.items():
                print("{} {}".format(k, repr(v.decode())))
        else:
            print(" This image has no iptc info")

    def addWatermark(self, basewidth, photo):
        watermark = Image.open(self.watermark)
        wpercent = (basewidth/float(watermark.size[0]))
        hsize = int((float(watermark.size[1])*float(wpercent)))
        watermark = watermark.resize((basewidth,hsize), Image.ANTIALIAS)

        position = ((photo.width - watermark.width), (photo.height - watermark.height))

        # find the centre of an the image to place watermark
        x = int((photo.width/2) - (watermark.width/2))
        y = int((photo.height/2) - (watermark.height/2))

        layer = Image.new('RGBA', photo.size, (0, 0, 0, 0))
        layer.paste(watermark, (x,y))
        return Image.composite(layer, photo, layer)

    def walk_directory(self, path):
        """ walk over files in provided directory and return a list of files """
        files = []
        for dirpath, dirnames, filenames in os.walk(path):
            for filename in filenames:
                files.append(os.path.join(dirpath, filename))
        return files