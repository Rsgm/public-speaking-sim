import os
import subprocess
from json import load
from pathlib import Path
import base64
from celery.app import shared_task
from django.conf import settings


@shared_task
def convert_media(id):
    encoded_video_path = Path('%s/%s.b64' % (settings.RECORDING_PATHS['VIDEO_PIECES'], id))
    encoded_audio_path = Path('%s/%s.b64' % (settings.RECORDING_PATHS['AUDIO_PIECES'], id))

    video_path = Path('%s/%s.webm' % (settings.RECORDING_PATHS['VIDEO_PIECES'], id))
    audio_path = Path('%s/%s.webm' % (settings.RECORDING_PATHS['AUDIO_PIECES'], id))

    # decode video data from base64
    try:
        with (encoded_video_path.open(), video_path.open()) as (encoded_video, video):
            base64.decode(encoded_video, video)
    except OSError:
        print('No video data: %s' % encoded_video_path)
        video_path = None

    # decode audio data from base64
    try:
        with (encoded_audio_path.open(), audio_path.open())as (encoded_audio, audio):
            base64.decode(encoded_audio, audio)
    except OSError:
        print('No audio data: %s' % encoded_audio_path)
        audio_path = None

    combined = False

    if video_path and not video_path:
        output = subprocess.check_output(
            'ffprobe -i %s -v quiet -print_format json -show_format -show_streams' % video_path)
        map = load(output)

        for stream in map['streams']:
            if stream['codec_type'] == 'audio':
                combined = True
                break

    converted_path = Path('%s/%s.webm' % (settings.RECORDING_PATHS['CONVERTED_PIECES'], id))

    # I suppose we will leave these as cpu-used 2, I may downgrade this later if it takes too long
    if combined:
        command = 'ffmpeg -i %s -c:v libvpx -cpu-used 2 -c:a libvorbis -filter:a \"asetpts=N/SR/TB\" %s' % (
            video_path, converted_path)
    elif video_path and audio_path:
        command = 'ffmpeg -i %s -i %s -map 0 -map 1 -c:v libvpx -cpu-used 2 -c:a libvorbis -filter:a \"asetpts=N/SR/TB\" %s' % (
            video_path, audio_path, converted_path)
    elif video_path:
        command = 'ffmpeg -i %s -c:v libvpx -cpu-used 2  %s' % (video_path, converted_path)
    elif audio_path:
        command = 'ffmpeg -i %s -c:a libvorbis -filter:a \"asetpts=N/SR/TB\" %s' % (audio_path, converted_path)
    else:
        command = 'Echo Error - No video or audio'

    print(command)
    subprocess.call(command)

    # clean up files
    if audio_path:
        os.remove(encoded_audio_path)
        os.remove(audio_path)
    if video_path:
        os.remove(encoded_video_path)
        os.remove(video_path)


@shared_task
def concatenate_media(project_id, piece_list):
    if len(piece_list) < 1:
        return

    script_path = Path('%s/%s.sh' % (settings.RECORDING_PATHS['SCRIPTS'], project_id))
    finished_path = Path()

    for i in piece_list:
        with script_path.open(mode='a') as script:
            script.write('%s/%s.webm' % (settings.RECORDING_PATHS['CONVERTED_PIECES'], i))
