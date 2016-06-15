FROM debian:jessie

ENV PYTHONUNBUFFERED 1
ENV LANG C.UTF-8

# Install ffmpeg
RUN echo deb http://www.deb-multimedia.org jessie main non-free >> /etc/apt/sources.list \
    && echo deb-src http://www.deb-multimedia.org jessie main non-free >> /etc/apt/sources.list \
    && apt-key adv --keyserver keyserver.ubuntu.com --recv-keys 5C808C2B65558117 \
    && apt-get -y update \
    && apt-get -y install deb-multimedia-keyring \
    && apt-get -y update \
    && apt-get -y install ffmpeg

# 4.4.5 is current node LTS
ENV NODE_VERSION 4.4.5
ENV NPM_CONFIG_LOGLEVEL info

RUN apt-get -y install curl xz-utils \
    \
    && echo 'install npm, gpg keys listed at https://github.com/nodejs/node' \
    && gpg --keyserver ha.pool.sks-keyservers.net --recv-keys \
        9554F04D7259F04124DE6B476D5A82AC7E37093B \
        94AE36675C464D64BAFA68DD7434390BDBE9B9C5 \
        0034A06D9D9B0064CE8ADF6BF1747F4AD2306D93 \
        FD3A5288F042B6850C66B31F09FE44734EB7990E \
        71DCFD284A79C3B38668286BC97EC7A07EDE3FC1 \
        DD8F2338BAE7501E3DD5AC78C273792F7D83545D \
        C4F0DFFF4E8C1A8236409D08E73BC641CC11F4C8 \
    \
    && curl -SLO "https://nodejs.org/dist/v$NODE_VERSION/node-v$NODE_VERSION-linux-x64.tar.xz" \
    && curl -SLO "https://nodejs.org/dist/v$NODE_VERSION/SHASUMS256.txt.asc" \
    && gpg --batch --decrypt --output SHASUMS256.txt SHASUMS256.txt.asc \
    && grep " node-v$NODE_VERSION-linux-x64.tar.xz\$" SHASUMS256.txt | sha256sum -c - \
    && tar -xJf "node-v$NODE_VERSION-linux-x64.tar.xz" -C /usr/local --strip-components=1 \
    && rm "node-v$NODE_VERSION-linux-x64.tar.xz" SHASUMS256.txt.asc SHASUMS256.txt \
    && apt-get -y remove curl xz-utils \
    \
    \
    && echo create non-root user \
    && groupadd -r django \
    && useradd -r -g django django \
    \
    && mkdir /app \
    && chmod 777 /app \
    && chown django /app \
    \
    \
    && echo Install python and python dependencies for later \
    && apt-get -y install python3 python3-pip libjpeg62-turbo-dev zlib1g-dev gcc libffi-dev \
    && pip3 install --upgrade pip \
    && ln -s /usr/bin/python3 /usr/local/bin/python \
    \
    \
    && apt-get clean


# Install npm dependencies
COPY ./package.json /app/package.json
RUN cd /app \
    && npm install --production


# Install python dependencies
COPY ./requirements /app/requirements/
RUN pip3 install -r /app/requirements/production.txt


# Copy the project, up to here should usually be cached
COPY . /app


# Compile sass and run any final commands(keep this layer fast)
RUN cd /app \
    && npm run build \
    && chmod 755 ./fix_permissions.sh \
    && ./fix_permissions.sh


WORKDIR /app
ENTRYPOINT ["/app/compose/django/entrypoint.sh"]
CMD ["/app/compose/django/gunicorn.sh"]
