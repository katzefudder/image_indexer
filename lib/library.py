import os, shutil, sys, glob, ntpath, math, multiprocessing
from datetime import datetime
from PIL import Image, IptcImagePlugin, ExifTags
from multiprocessing import pool
from multiprocessing.dummy import Pool 
import json

class MyEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, (bytes, bytearray)):
            return obj.decode("UTF-8") # <- or any other encoding of your choice
        # Let the base class default method raise the TypeError
        return json.JSONEncoder.default(self, obj)

class Library:
    thumbnail_sizes = {"min":250, "med":450, "max":800}
    threads = 1
    sourceDir = ""
    targetDir = ''
    files = []
    processedFiles = []
    processedFileSize = 0
    omittedFiles = []
    removeOriginalFiles = False
    watermark = "watermark.png"
    
    exifData = []
    iptcData = []

    __debugMode = True

    def __init__(self, sourceDir, targetDir):
        self.sourceDir = sourceDir
        self.targetDir = targetDir
        self.files = self.walk_directory(self.sourceDir)

    def _getCpuCount(self):
        return multiprocessing.cpu_count()

    def setDebugMode(self, debug):
        self.__debugMode = debug

    def setRemoveOriginalFiles(self, removeOriginalFiles):
        self.removeOriginalFiles = removeOriginalFiles

    def setThreads(self, threads):
        self.threads = threads
    
    def setSourceDir(self, sourceDir):
        self.sourceDir = sourceDir

    def setTargetDir(self, targetDir):
        self.targetDir = targetDir

    def process_images(self):
        begin_time = datetime.now()
        if self.threads <= 0:
            self.threads = self._getCpuCount()

        self.useThreading(self.threads)
        
        # export all exif data to json file
        self.serializeMetadata()

        if self.__debugMode:
            print("\nUse %d threads to index %d files" % (self.threads, len(self.files)))
            print("\nProcessed Files:")
            print("--------------------------------------------")
            print(*self.processedFiles, sep='\n')
            print("\nOmitted files:")
            print("--------------------------------------------")
            print(*self.omittedFiles, sep='\n')
            print("\nIndexing took %s for %d files (%s)" % ((datetime.now() - begin_time), len(self.files), self.convert_size(self.processedFileSize)))

    def serializeMetadata(self):
        with open('exif.json', 'w', encoding='utf-8') as file:
            json.dump(self.exifData, file, ensure_ascii=False, indent=4)
        with open('iptc.json', 'w', encoding='utf-8') as file:
            iptc = json.dumps( self.iptcData, cls=MyEncoder )
            json.dump(iptc, file, ensure_ascii=False, indent=4)

    def useThreading(self, threads):
        pool = Pool(threads)
        pool.map(self.handleImage, self.files)

    def handleImage(self, source, extensionAllowed = '.jpg'):
        pictureName, extension = os.path.splitext(source)
        if extension == extensionAllowed:
            # iterate over different image sizes
            originalPhoto = Image.open(source)
            # get the folder containing the image to process
            originalFolder = os.path.dirname(source).split('/')[-1]
            
            for size, dimension in self.thumbnail_sizes.items():
                thumbTarget = self.targetDir + "/" + size + "/" + originalFolder
                
                # create thumbnail directory, ignore if existing
                self.createDirectory(thumbTarget)

                photo = Image.open(source)

                photo.thumbnail((dimension, dimension), Image.ANTIALIAS)
                thumbnailFilename = thumbTarget + "/" + os.path.basename(source)
                # add image to list

                # add a watermark to all images larger than medium sized thumbnails
                if dimension > self.thumbnail_sizes['med']:
                    photo = self.addWatermark(self.thumbnail_sizes['max'], photo)

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
        self.extractIptc(photo)
        self.processedFileSize += os.path.getsize(photo.filename) # sum up file sizes
        self.processedFiles.append(photo.filename) # add the processed file to the list of processed files

        originalFolder = os.path.dirname(photo.filename).split('/')[-1]
        
        processedImageDir = self.targetDir + "/original/" + originalFolder # processed images should go to this folder
        self.createDirectory(processedImageDir) # create directory for original files
        processedImage = processedImageDir + "/" + ntpath.basename(photo.filename)
        shutil.copyfile(photo.filename, processedImage) # when processed, move the processed file away

        if self.removeOriginalFiles:
            os.remove(photo.filename)

    def createDirectory(self, directory):
        # create thumbnail directory, ignore if existing
        if not os.path.exists(directory):
            try:
                os.makedirs(directory, exist_ok=True)
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
        iptc = {}

        iptc_tags = {
            (1, 90): 'CodedCharacterSet',
            (2, 0): 'Whatever',
            (2, 5): 'ObjectName',
            (2, 10): 'Urgency',
            (2, 15): 'Category',
            (2, 20): 'Subcategories',
            (2, 25): 'Keywords',
            (2, 40): 'SecialInstructions',
            (2, 55): 'CreationDate',
            (2, 60): 'CreationTime',
            (2, 62): 'DigitizationDate',
            (2, 80): 'AuthorByline',
            (2, 85): 'AuthorTitle',
            (2, 90): 'City',
            (2, 92): 'SubLocation',
            (2, 95): 'State',
            (2, 100): 'CountryCode',
            (2, 101): 'Country',
            (2, 103): 'OTR',
            (2, 105): 'Headline',
            (2, 110): 'Source',
            (2, 115): 'PhotoSource',
            (2, 116): 'Copyright',
            (2, 120): 'Caption',
            (2, 122): 'CaptionWriter',
        }

        iptc_info = IptcImagePlugin.getiptcinfo(image) or {}
        for tag, value in iptc_info.items():
            decoded = iptc_tags.get(tag, str(tag))
            iptc[decoded] = value
        print(type(iptc))
        self.iptcData.append(iptc)
        
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