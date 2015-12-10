import os
import subprocess
from json import loads
from pathlib import Path
import base64
from celery.app import shared_task
from django.conf import settings
from speakeazy.speakeazy import models
from speakeazy.speakeazy.models import Recording


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
            with audio_path.open(mode='wb')as audio:
                base64.decode(encoded_audio, audio)
    except OSError:
        print('No audio data: %s' % encoded_audio_path)
        audio_path = None

    combined = False

    if video_path and not audio_path:
        command = 'ffprobe -i %s -v quiet -print_format json -show_format -show_streams' % video_path
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

    # fill list with piece paths
    with list_path.open(mode='w') as list:
        for i in piece_list:
            print('file \'%s/%s.webm\'' % (settings.RECORDING_PATHS['CONVERTED_PIECES'], i), file=list)

    # concat pieces
    command = 'ffmpeg -loglevel quiet -f concat -i %s -c copy %s' % (str(list_path), str(finished_path))
    print(command)
    subprocess.call(command.split())

    # create thumbnail
    # todo: make video and image
    # the video should have 1/5 the frames and low bitrate,
    # http://superuser.com/questions/573747/drop-every-even-or-odd-frames-using-ffmpeg

    # upload video and thumbnails to aws bucket
    # todo: setup aws

    # set object finished flags
    recording = Recording.objects.filter(id=recording_id).get()
    recording.state = models.FINISHED
    recording.save()  # if this does not work, move it to the recording finish post

    # clean up scripts and converted pieces
    os.remove(str(list_path))
    # os.remove(str(finished_path))
    for i in piece_list:
        os.remove('%s/%s.webm' % (settings.RECORDING_PATHS['CONVERTED_PIECES'], i))
