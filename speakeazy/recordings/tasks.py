import subprocess
from datetime import datetime, timedelta
from json import loads
from math import floor
from pathlib import Path

from speakeazy.recordings import models
from speakeazy.recordings.models import Recording, UploadPiece

import base64
import os
from celery.app import shared_task
from django.conf import settings
from django.core.files.base import File


@shared_task
def convert_media(piece_id):
    encoded_video_path = Path('%s/%s.b64' % (settings.RECORDING_PATHS['VIDEO_PIECES'], piece_id)).absolute()
    encoded_audio_path = Path('%s/%s.b64' % (settings.RECORDING_PATHS['AUDIO_PIECES'], piece_id)).absolute()

    video_path = Path('%s/%s.webm' % (settings.RECORDING_PATHS['VIDEO_PIECES'], piece_id)).absolute()
    audio_path = Path('%s/%s.wav' % (settings.RECORDING_PATHS['AUDIO_PIECES'], piece_id)).absolute()

    # decode video data from base64
    try:
        with encoded_video_path.open(mode='rb') as encoded_video:
            with video_path.open(mode='wb') as video:
                base64.decode(encoded_video, video)
    except OSError:
        print('No video data: %s' % encoded_video_path)
        video_path = None

    # decode audio data from base64
    try:
        with encoded_audio_path.open(mode='rb') as encoded_audio:
            with audio_path.open(mode='wb') as audio:
                base64.decode(encoded_audio, audio)
    except OSError:
        print('No audio data: %s' % encoded_audio_path)
        audio_path = None

    combined = False

    if video_path and not audio_path:
        command = 'ffprobe -i %s -v quiet -print_format json -show_streams' % video_path
        output = subprocess.check_output(command.split())
        m = loads(output.decode("utf-8"))  # map

        for stream in m['streams']:
            if stream['codec_type'] == 'audio':
                combined = True
                break

    converted_path = Path('%s/%s.webm' % (settings.RECORDING_PATHS['CONVERTED_PIECES'], piece_id)).absolute()

    # I suppose we will leave these as cpu-used 2, I may downgrade this later if it takes too long
    if combined:
        command = 'ffmpeg -loglevel quiet -i %s ' \
                  '-c:v libvpx -cpu-used 2 -c:a libvorbis -filter:a asetpts=N/SR/TB %s' \
                  % (video_path, converted_path)
    elif video_path and audio_path:
        command = 'ffmpeg -loglevel quiet -i %s -i %s ' \
                  '-map 0 -map 1 -c:v libvpx -cpu-used 2 -c:a libvorbis -filter:a asetpts=N/SR/TB %s' \
                  % (video_path, audio_path, converted_path)
    elif video_path:
        command = 'ffmpeg -loglevel quiet -i %s video_path -c:v libvpx -cpu-used 2' % converted_path
    elif audio_path:
        command = 'ffmpeg -loglevel quiet -i %s -c:a libvorbis -filter:a asetpts=N/SR/TB %s' \
                  % (audio_path, converted_path)
    else:
        command = 'Echo Error - No video or audio'

    # run command
    print(command)
    subprocess.call(command.split())

    # clean up files
    if audio_path:
        os.remove(str(encoded_audio_path))
        os.remove(str(audio_path))
    if video_path:
        os.remove(str(encoded_video_path))
        os.remove(str(video_path))


@shared_task
def concatenate_media(recording_id, piece_list):
    if len(piece_list) < 1:
        return

    list_path = Path('%s/%s.txt' % (settings.RECORDING_PATHS['LISTS'], recording_id)).absolute()
    finished_path = Path('%s/%s.webm' % (settings.RECORDING_PATHS['FINISHED'], recording_id)).absolute()
    thumbnail_video_path = Path('%s/%s.webm' % (settings.RECORDING_PATHS['THUMBNAILS'], recording_id)).absolute()

    # fill list with piece paths
    with list_path.open(mode='w') as list:
        for i in piece_list:
            print('file \'%s/%s.webm\'' % (settings.RECORDING_PATHS['CONVERTED_PIECES'], i), file=list)

    # concat pieces
    command = 'ffmpeg -loglevel quiet -f concat -i %s -c copy %s' % (list_path, finished_path)
    print(command)
    subprocess.call(command.split())

    # create thumbnail image and video
    # find video length
    command = 'ffprobe -i %s -v quiet -print_format json -show_format' % finished_path
    print(command)
    output = subprocess.check_output(command.split())

    # find image offset times
    m = loads(output.decode("utf-8"))  # map
    duration = float(m['format']['duration'])
    offset = floor(duration / 9)  # nine so the first is not at t=0

    # create 8 thumbnails
    thumbnail_image_paths = []
    for i in range(8):
        offset_time = timedelta(seconds=offset * (i + 1))
        path = Path('%s/%s-%s.png' % (settings.RECORDING_PATHS['THUMBNAILS'], recording_id, i)).absolute()
        thumbnail_image_paths.append(path)
        command = 'ffmpeg -v quiet -i %s -vf scale=150:-1 -ss %s -vframes 1 %s' % (finished_path, offset_time, path)
        print(command)
        subprocess.call(command.split())

    # create thumbnail slideshow
    command = 'ffmpeg -v quiet -framerate 2/3 -i %s/%s-%s -c:v libvpx -cpu-used 2 -an %s' \
              % (settings.RECORDING_PATHS['THUMBNAILS'], recording_id, '%1d.png', thumbnail_video_path)
    print(command)
    subprocess.call(command.split())

    # set object finished flags and save media
    recording = Recording.objects.filter(id=recording_id).get()
    recording.finish_time = datetime.now()
    recording.state = models.FINISHED
    recording.duration = duration
    recording.video.save('%s.webm' % recording_id, File(open(str(finished_path), mode='rb')))
    recording.thumbnail_image.save('%s.png' % recording_id, File(open(str(thumbnail_image_paths[0]), mode='rb')))
    recording.thumbnail_video.save('%s.webm' % recording_id, File(open(str(thumbnail_video_path), mode='rb')))
    recording.save()

    # clean up scripts and converted pieces
    os.remove(str(list_path))
    # os.remove(str(finished_path))
    # os.remove(str(thumbnail_video_path))
    # for path in thumbnail_image_paths:
    #     os.remove(str(path))
    for i in piece_list:
        os.remove('%s/%s.webm' % (settings.RECORDING_PATHS['CONVERTED_PIECES'], i))
    UploadPiece.objects.filter(recording=recording).delete()  # clear out database pieces
