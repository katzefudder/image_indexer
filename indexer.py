import os, sys, glob
import click
from lib import library

@click.command()
@click.argument('source', type=click.Path(exists=True))
@click.argument('target', type=click.Path(exists=True))
@click.option('--threads', '-t', type=int)

def main(source, target, threads):
    if threads is None:
        threads = 8
    cwd = os.path.dirname(os.path.realpath(__file__))
    source = cwd + "/" + source
    target = cwd + "/" + target
    indexer = library.Library(source, target)
    indexer.setThreads(threads)
    indexer.process_images()

if __name__ == "__main__":
    main()