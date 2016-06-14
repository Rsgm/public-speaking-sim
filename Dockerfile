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


# Install npm
# todo: https://github.com/nodejs/docker-node/blob/b2c7f6e357359b7b8f30caada05f1d412d926d7b/5.7/wheezy/Dockerfile
RUN echo Installing npm \
    && apt-get -y install nodejs-legacy npm \
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
    && echo Install python and add python3 link \
    && apt-get -y install python3 python3-pip \
    && pip3 install --upgrade pip \
    \
    \
    && echo npm installs python 2.7, make 3 default \
    && cd /usr/bin \
	&& rm python \
	&& ln -s python3 python \
	\
	\
	&& echo Install packages needed by python packages later \
    && apt-get -y install libjpeg62-turbo-dev zlib1g-dev gcc libffi-dev \
    \
    \
    && apt-get clean


# Install npm dependencies
COPY ./package.json /app/package.json
RUN cd /app \
    && npm install --production


# Install python dependencies
COPY ./requirements /requirements/
RUN pip3 install -r /requirements/production.txt


# Copy the project, up to here should usually be cached
COPY . /app


# Compile sass and run any final commands(keep this layer fast)
RUN cd /app \
    && npm run build \
    && ./fix_permissions.sh # must be in app directory


WORKDIR /app
ENTRYPOINT ["/app/compose/django/entrypoint.sh"]
CMD ["/app/compose/django/gunicorn.sh"]
