import os, shutil, json
import pytest
from lib import indexer

class TestIndexer():
    __indexer = ""
    __cwd = ""

    def __prepare_tests(self):
        self.__cwd = os.path.dirname(os.path.realpath(__file__))
        os.makedirs(self.__cwd + '/test', exist_ok=True)
        
        source = self.__cwd + "/images" 
        target = self.__cwd + "/test"
        self.__indexer = indexer.Indexer(source, target)

    def test_basic_init_indexer(self):
        self.__prepare_tests()

        assert(self.__indexer.sourceDir == self.__cwd + "/images"), "sourceDir should be /images"
        assert(self.__indexer.targetDir == self.__cwd + "/test"), "targetDir should be /test"
        assert len(self.__indexer.files) == 1, "Length of file list should be 1"

    def test_basic_indexing(self):
        self.__prepare_tests()
        self.__indexer.process_images()

        indexed_file = self.__cwd + "/images/a_gallery/testimage.jpg"
        assert(indexed_file in self.__indexer.processedFiles), indexed_file + " should be in list of processed files"

    def test_thumbnails_exist(self):
        self.__prepare_tests()
        self.__indexer.process_images()

        # assert thumbnails created
        assert(os.path.exists(self.__cwd + "/test/max/a_gallery/testimage.jpg"))
        assert(os.path.exists(self.__cwd + "/test/med/a_gallery/testimage.jpg"))
        assert(os.path.exists(self.__cwd + "/test/min/a_gallery/testimage.jpg"))
        assert(os.path.exists(self.__cwd + "/test/original/a_gallery/testimage.jpg"))        

    def test_meta_json_exists(self):
        self.__prepare_tests()
        assert(os.path.exists(self.__cwd + "/meta.json"))

        with open('meta.json') as json_file:
            data = json.load(json_file)
            assert(data['testimage']['iptc']['ObjectName'] == 'in der DEL 2 - EC Bad Nauheim gegen ESV Kaufbeuren')
            assert(data['testimage']['exif']['filename'] == '/app/images/a_gallery/testimage.jpg')

    def __del__(self):
        shutil.rmtree(self.__cwd + '/test/target')

if __name__ == "__main__":
    test = TestIndexer()
    test.test_indexer()
    
