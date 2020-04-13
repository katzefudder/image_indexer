# Multi-Threaded Indexer for jpg images
Started as a side project for myself to get my head into image processing and multi-threading in Python.

## Use a Docker environment
For not to having to mess up my computer, I decided to "dockerize" the environment to work in.
To build the Docker image use the following
`docker build -t mypy .`

To spin up a Docker container to run my indexer use the following after having built the Docker image
`docker run -v $(pwd):/app mypy indexer.py images target -t 8`