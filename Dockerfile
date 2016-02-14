FROM debian:jessie

ENV PYTHONUNBUFFERED 1
ENV LANG C.UTF-8

#todo: fix public key issue here
#todo: maybe replace with compiling from source to remove unneeded x11 and playback libraries
# Install ffmpeg
RUN echo deb http://www.deb-multimedia.org jessie main non-free >> /etc/apt/sources.list \
    && echo deb-src http://www.deb-multimedia.org jessie main non-free >> /etc/apt/sources.list \
    && apt-key adv --keyserver keyserver.ubuntu.com --recv-keys 5C808C2B65558117 \
    && apt-get -y --force-yes update \
    && apt-get -y --force-yes install deb-multimedia-keyring \
    && apt-get -y --force-yes update \
    && apt-get -y --force-yes install ffmpeg


# Install npm
# This tries to install python 2.7, do this after installing python
RUN apt-get -y --force-yes update \
    && apt-get -y --force-yes install nodejs-legacy \
    && apt-get -y --force-yes install npm \
    && npm install -g grunt-cli


# Install python and add python3 link
RUN apt-get -y --force-yes update \
    && apt-get -y --force-yes install python3 python3-pip \
    && pip3 install --upgrade pip \
    \
    && cd /usr/bin \
	&& rm python \
	&& ln -s python3 python


# Install packages needed by python packages later
RUN apt-get -y --force-yes update \
    && apt-get -y --force-yes install libjpeg62-turbo-dev zlib1g-dev gcc libffi-dev


# Requirements have to be pulled and installed here, otherwise caching won't work
COPY ./requirements /requirements
RUN pip3 install -r /requirements/production.txt


RUN groupadd -r django && useradd -r -g django django
COPY . /app


# install npm dependencies and fix file permissions
RUN cd /app \
    && npm install \
    && grunt build \
    \
    && echo fixing file permissions \
    && chown -R django /app \
    && chmod -R 777 /app # todo: is this a security issue?


COPY ./compose/django/gunicorn.sh /gunicorn.sh
COPY ./compose/django/entrypoint.sh /entrypoint.sh


RUN chown django /entrypoint.sh && chmod +x /entrypoint.sh \
    && chown django /gunicorn.sh && chmod +x /gunicorn.sh


WORKDIR /app
ENTRYPOINT ["/entrypoint.sh"]
