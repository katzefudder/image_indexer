import os, shutil
import pytest
from lib import library

def prepare_tests():
    os.makedirs('./test/target', exist_ok=True)
    shutil.rmtree('./test/target')

class TestIndexer():
    __indexer = ""

    def __prepare_tests(self):
        os.makedirs('./test/target', exist_ok=True)
        shutil.rmtree('./test/target')
        
        cwd = os.path.dirname(os.path.realpath(__file__))
        source = cwd + "/test" 
        target = cwd + "/test/target"
        self.__indexer = library.Library(source, target)

    def test_indexer(self):
        self.__prepare_tests

        assert len(self.__indexer.files) == 1, "Length of file list should be 1"
        assert(self.__indexer.sourceDir == "/app/test"), "sourceDir should be /app/test"
        assert(self.__indexer.targetDir == "/app/test/target"), "targetDir should be /app/test/target"

if __name__ == "__main__":
    test = TestIndexer()
    test.test_indexer()
    