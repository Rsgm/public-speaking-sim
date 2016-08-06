import logging
import os
import shutil
import subprocess
from datetime import datetime, timedelta
from ftplib import FTP
from json import loads
from math import floor
from pathlib import Path

from celery.app import shared_task
from django.conf import settings
from django.core.files.base import File, ContentFile

from speakeazy.recordings import models
from speakeazy.recordings.models import Recording, UploadPiece

LOG_LEVEL = settings.FFMPEG_LOG_LEVEL

logger = logging.getLogger(__name__)


@shared_task
def combine_media(host, piece_id, video, audio):
    video_path = Path('%s/%s.webm' % (settings.RECORDING_PATHS['VIDEO_PIECES'], piece_id))
    audio_path = Path('%s/%s.wav' % (settings.RECORDING_PATHS['AUDIO_PIECES'], piece_id))
    combined_path = Path('%s/%s.combined.webm' % (settings.RECORDING_PATHS['VIDEO_PIECES'], piece_id)).absolute()

    ftp = FTP()
    ftp.connect(host, 22)
    ftp.login()

    if video:
        ftp.cwd('/recordings/video_pieces')
        remote_fie = '%s.webm' % piece_id

        with video_path.open(mode='wb') as video_file:
            ftp.retrbinary('RETR %s' % remote_fie, video_file.write)

        ftp.delete(remote_fie)

    if audio:
        ftp.cwd('/recordings/audio_pieces')
        remote_fie = '%s.webm' % piece_id

        with audio_path.open(mode='wb') as audio_file:
            ftp.retrbinary('RETR %s' % remote_fie, audio_file.write)

        ftp.delete(remote_fie)

    ftp.close()

    status = None

    if audio and video:
        command = 'ffmpeg -v %s -i %s -i %s -c copy %s' % (LOG_LEVEL, video_path, audio_path, combined_path)

        logger.info('Running: %s' % command)
        status = subprocess.call(command.split())

        os.remove(video_path.absolute())
        os.remove(audio_path.absolute())

        shutil.move(combined_path, video_path.absolute())

    elif audio and not video:
        command = 'ffmpeg -v %s -i %s %s' % (LOG_LEVEL, audio_path, combined_path)

        logger.warn('No video, piece_id: %s' % piece_id)
        logger.info('Running: %s' % command)
        status = subprocess.call(command.split())

        os.remove(video_path.absolute())
        os.remove(audio_path.absolute())

        shutil.move(combined_path, video_path.absolute())

    elif not (audio or video):
        logger.error('No audio or video, piece id: %s' % piece_id)

    if status > 0:
        logger.error('command exited with status code %s' % status)


@shared_task
def concatenate_media(recording_id, piece_list):
    if len(piece_list) < 1:
        return

    list_path = Path('%s/%s.txt' % (settings.RECORDING_PATHS['LISTS'], recording_id)).absolute()
    finished_path = Path('%s/%s.webm' % (settings.RECORDING_PATHS['FINISHED'], recording_id)).absolute()

    # fill list with piece paths
    with list_path.open(mode='w') as list_file:
        for i in piece_list:
            print('file \'%s/%s.webm\'' % (settings.RECORDING_PATHS['VIDEO_PIECES'], i), file=list_file)

    # concat pieces, safe 0 since all paths are absolute, I don't trust relative paths to work
    command = 'ffmpeg -v %s -f concat -safe 0 -i %s -c copy %s' % (LOG_LEVEL, list_path, finished_path.absolute())
    logger.info('Running concat: %s' % command)
    status = subprocess.call(command.split())

    if status > 0:
        logger.error('Command exited with status %s' % status)
        return

    # set object finished flags and save media
    recording = Recording.objects.get(pk=recording_id)
    recording.finish_time = datetime.now()
    recording.state = models.RECORDING_FINISHED
    recording.thumbnail_image.save('%s-temp.png' % recording_id, ContentFile(''))
    recording.thumbnail_video.save('%s-temp.png' % recording_id, ContentFile(''))
    recording.save()

    with finished_path.open(mode='rb') as finished:
        recording.video.save('%s.webm' % recording_id, File(finished))

    # create thumbnails in separate task
    create_thumbnails.delay(recording_id)

    # clean up scripts and converted pieces
    os.remove(list_path)
    for i in piece_list:
        os.remove('%s/%s.webm' % (settings.RECORDING_PATHS['VIDEO_PIECES'], i))
    UploadPiece.objects.filter(recording=recording).delete()  # clear out database pieces


@shared_task
def create_thumbnails(recording_id):
    finished_path = Path('%s/%s.webm' % (settings.RECORDING_PATHS['FINISHED'], recording_id)).absolute()
    thumbnail_video_path = Path('%s/%s.webm' % (settings.RECORDING_PATHS['THUMBNAILS'], recording_id)).absolute()

    recording = Recording.objects.get(id=recording_id)

    # find video length
    command = 'ffprobe -v %s -i %s -print_format json -show_format' % (LOG_LEVEL, finished_path)
    print(command)
    output = subprocess.check_output(command.split())

    # find image offset times
    m = loads(output.decode("utf-8"))  # map
    duration = float(m['format']['duration'])
    offset = floor(duration / 9)  # nine so the first is not at t=0

    # set recording duration
    recording.duration = duration
    recording.save()

    # create 8 thumbnails
    thumbnail_image_paths = []
    for i in range(8):
        offset_time = timedelta(seconds=offset * (i + 1))
        path = Path('%s/%s-%s.png' % (settings.RECORDING_PATHS['THUMBNAILS'], recording_id, i)).absolute()
        thumbnail_image_paths.append(path)
        command = 'ffmpeg -v %s -i %s -vf scale=150:-1 -ss %s -vframes 1 %s' \
                  % (LOG_LEVEL, finished_path, offset_time, path)
        print(command)
        subprocess.call(command.split())

        # save first image when possible
        if i == 0:
            recording.thumbnail_image.save('%s.png' % recording_id,
                                           File(open(str(thumbnail_image_paths[0]), mode='rb')))

    # create thumbnail slideshow
    command = 'ffmpeg -v %s -framerate 2/3 -i %s/%s-%s -c:v libvpx -cpu-used 2 -an %s' \
              % (LOG_LEVEL, settings.RECORDING_PATHS['THUMBNAILS'], recording_id, '%1d.png', thumbnail_video_path)
    print(command)
    subprocess.call(command.split())

    recording.thumbnail_video.save('%s.webm' % recording_id, File(open(str(thumbnail_video_path), mode='rb')))

    # clean up thumbnails and finished video files
    os.remove(str(finished_path))
    os.remove(str(thumbnail_video_path))
    for path in thumbnail_image_paths:
        os.remove(str(path))
