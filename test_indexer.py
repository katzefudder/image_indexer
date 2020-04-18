import os, shutil
import pytest
from lib import library

class TestIndexer():
    __indexer = ""

    def __prepare_tests(self):
        cwd = os.path.dirname(os.path.realpath(__file__))
        os.makedirs(cwd + '/test/target', exist_ok=True)
        
        source = cwd + "/images" 
        target = cwd + "/test/target"
        self.__indexer = library.Library(source, target)

    def test_indexer(self):
        self.__prepare_tests()

        cwd = os.path.dirname(os.path.realpath(__file__))
        assert(self.__indexer.sourceDir == cwd + "/images"), "sourceDir should be /images"
        assert(self.__indexer.targetDir == cwd + "/test/target"), "targetDir should be /test/target"
        assert len(self.__indexer.files) == 1, "Length of file list should be 1"

if __name__ == "__main__":
    test = TestIndexer()
    test.test_indexer()
    
