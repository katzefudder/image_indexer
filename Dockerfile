FROM frolvlad/alpine-python3

COPY ./requirements.txt /app/requirements.txt

RUN apk add build-base jpeg-dev zlib-dev python3-dev
ENV LIBRARY_PATH=/lib:/usr/lib
RUN apk add --no-cache --virtual .build-deps build-base linux-headers g++ jpeg-dev zlib-dev freetype-dev lcms2-dev openjpeg-dev \
    && pip3 install pip --upgrade \
    && apk del .build-deps

WORKDIR /app

RUN pip3 install -r /app/requirements.txt

ENTRYPOINT ["python"]