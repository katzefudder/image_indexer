import os, shutil
import pytest
from lib import library

def prepare_tests():
    os.makedirs('./test/target', exist_ok=True)

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

        assert(self.__indexer.sourceDir == "/app/images"), "sourceDir should be /app/images"
        assert(self.__indexer.targetDir == "/app/test/target"), "targetDir should be /app/test/target"
        assert len(self.__indexer.files) == 1, "Length of file list should be 1"

    def __del__(self):
        shutil.rmtree('./test/target')

if __name__ == "__main__":
    test = TestIndexer()
    test.test_indexer()
    
