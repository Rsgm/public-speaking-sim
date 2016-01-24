FROM debian:jessie

ENV PYTHONUNBUFFERED 1
ENV LANG C.UTF-8

#todo: fix public key issue here
#todo: maybe replace with compiling from source to remove unneeded x11 and playback libraries
# Install ffmpeg
RUN echo deb http://www.deb-multimedia.org jessie main non-free >> /etc/apt/sources.list \
    && echo deb-src http://www.deb-multimedia.org jessie main non-free >> /etc/apt/sources.list \
    && apt-get -y --force-yes update \
    && apt-get -y --force-yes install deb-multimedia-keyring \
    && apt-get -y --force-yes update \
    && apt-get -y --force-yes install ffmpeg


# Install python and add python3 link
RUN apt-get -y --force-yes update \
    && apt-get -y --force-yes install python3 python3-pip \
    \
    && cd /usr/bin \
	&& ln -s python3 python


# Install packages needed by python packages later
RUN apt-get -y --force-yes update \
    && apt-get -y --force-yes install libjpeg62-turbo-dev zlib1g-dev gcc libffi-dev


# Requirements have to be pulled and installed here, otherwise caching won't work
COPY ./requirements /requirements
RUN pip3 install -r /requirements/production.txt


RUN groupadd -r django && useradd -r -g django django
COPY . /app
RUN chown -R django /app && chmod -R 777 /app # is this a security issue?


#ARG FFMPEG_VERSION=n2.8.5
#
## Install ffmpeg, https://github.com/FFmpeg/FFmpeg/releases
## This takes 20 minutes, todo: make a celery repo that adds ffmpeg
#RUN apt-get -y --force-yes update \
#    && apt-get -y --force-yes install autoconf automake build-essential libass-dev libfreetype6-dev libtheora-dev \
#    libtool libvorbis-dev pkg-config texinfo zlib1g-dev \
#    \
#    \
#    && apt-get -y --force-yes install yasm \
#    && apt-get -y --force-yes install libx264-dev \
#    && apt-get -y --force-yes install libopus-dev \
#    && apt-get -y --force-yes autoremove \
#    \
#    \
#    && mkdir ~/ffmpeg_sources \
#    && cd ~/ffmpeg_sources \
#    && wget https://storage.googleapis.com/downloads.webmproject.org/releases/webm/libvpx-1.5.0.tar.bz2 \
#    && tar xjvf libvpx-1.5.0.tar.bz2 \
#    && cd libvpx-1.5.0 \
#    && PATH="$HOME/bin:$PATH" ./configure --prefix="$HOME/ffmpeg_build" --disable-examples --disable-unit-tests \
#    && PATH="$HOME/bin:$PATH" make \
#    && make install \
#    && make clean \
#    \
#    \
#    #&& cd / \
#    #&& tar -xvf $FFMPEG_VERSION.tar.gz \
#    #&& cd /FFmpeg-$FFMPEG_VERSION \
#    #&& ./configure \
#    #    --enable-libvorbis \
#    #    --enable-libvpx \
#    #    --enable-nonfree \
#    #&& make \
#    #&& make install \
#    #&& cd \
#    #&& rm /$FFMPEG_VERSION.tar.gz \
#    \
#    \
#    && cd ~/ffmpeg_sources \
#    && wget https://github.com/FFmpeg/FFmpeg/archive/$FFMPEG_VERSION.tar.gz \
#    && tar -xvf $FFMPEG_VERSION.tar.gz \
#    && cd FFmpeg-$FFMPEG_VERSION \
#    #&& tar xjvf ffmpeg-snapshot.tar.bz2 \
#    #&& cd ffmpeg \
#    && PATH="$HOME/bin:$PATH" PKG_CONFIG_PATH="$HOME/ffmpeg_build/lib/pkgconfig" ./configure \
#         --prefix="$HOME/ffmpeg_build" \
#         --pkg-config-flags="--static" \
#         --extra-cflags="-I$HOME/ffmpeg_build/include" \
#         --extra-ldflags="-L$HOME/ffmpeg_build/lib" \
#         --bindir="$HOME/bin" \
#         --enable-gpl \
#         --enable-libass \
#         --enable-libfreetype \
#         --enable-libopus \
#         --enable-libtheora \
#         --enable-libvorbis \
#         --enable-libvpx \
#         --enable-libx264 \
#         --enable-nonfree \
#    && PATH="$HOME/bin:$PATH" make \
#    && make install \
#    && make distclean \
#    && hash -r \
#    \
#    && ln -s ~/bin/* /bin
#    && rm -rf /FFmpeg-$FFMPEG_VERSION


COPY ./compose/django/gunicorn.sh /gunicorn.sh
COPY ./compose/django/entrypoint.sh /entrypoint.sh

RUN chown django /entrypoint.sh && chmod +x /entrypoint.sh
RUN chown django /gunicorn.sh && chmod +x /gunicorn.sh

WORKDIR /app

ENTRYPOINT ["/entrypoint.sh"]
