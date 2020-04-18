import os, shutil
import pytest
from lib import library

class TestIndexer():
    __indexer = ""
    __cwd = ""

    def __prepare_tests(self):
        self.__cwd = os.path.dirname(os.path.realpath(__file__))
        os.makedirs(self.__cwd + '/test/target', exist_ok=True)
        
        source = self.__cwd + "/images" 
        target = self.__cwd + "/test/target"
        self.__indexer = library.Library(source, target)

    def test_basic_init_indexer(self):
        self.__prepare_tests()

        assert(self.__indexer.sourceDir == self.__cwd + "/images"), "sourceDir should be /images"
        assert(self.__indexer.targetDir == self.__cwd + "/test/target"), "targetDir should be /test/target"
        assert len(self.__indexer.files) == 1, "Length of file list should be 1"

    def test_basic_indexing(self):
        self.__prepare_tests()
        self.__indexer.process_images()

        indexed_file = self.__cwd + "/images/testimage.jpg"
        assert(indexed_file in self.__indexer.processedFiles), indexed_file + " should be in list of processed files"

        # assert thumbnails created
        assert(os.path.exists(self.__cwd + "/test/target/max/testimage.jpg"))
        assert(os.path.exists(self.__cwd + "/test/target/med/testimage.jpg"))
        assert(os.path.exists(self.__cwd + "/test/target/min/testimage.jpg"))
        assert(os.path.exists(self.__cwd + "/test/target/original/testimage.jpg"))

    def __del__(self):
        
        shutil.rmtree(self.__cwd + '/test/target')

if __name__ == "__main__":
    test = TestIndexer()
    test.test_indexer()
    
