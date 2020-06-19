#!/usr/bin/env python
import os, sys, glob, multiprocessing
import click
from lib import library

@click.command()
@click.argument('source', type=click.Path(exists=True))
@click.argument('target', type=click.Path(exists=True))
@click.option('--threads', '-t', type=int, default=0, help='Number of threads')

def main(source, target, threads):
    cwd = os.path.dirname(os.path.realpath(__file__))
    source = cwd + "/" + source
    target = cwd + "/" + target
    indexer = library.Library(source, target)
    indexer.setThreads(threads)
    indexer.process_images()

if __name__ == "__main__":
    main()