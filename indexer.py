#!/usr/bin/env python
import os
import click
from lib import indexer

@click.command()
@click.argument('source', type=click.Path(exists=True))
@click.argument('target', type=click.Path(exists=True))
@click.option('--threads', '-t', type=int, default=0, help='Number of threads')

def index(source, target, threads):
    cwd = os.path.dirname(os.path.realpath(__file__))
    source = cwd + "/" + source
    target = cwd + "/" + target
    indexerJob = indexer.Indexer(source, target)
    indexerJob.setThreads(threads)
    indexerJob.process_images()

if __name__ == "__main__":
    index()