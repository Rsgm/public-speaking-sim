import subprocess
from pathlib import Path

from speakeazy.groups.models import Audience
import os
from celery.app import shared_task
from django.conf import settings
from django.core.files.base import File

LOG_LEVEL = settings.FFMPEG_LOG_LEVEL


@shared_task
def transcode_audience(id):
    """
    Transcodes an audience video file to a webm file and an mp4 file.

    The mp4 file is for legacy browsers and safari.

    :param id:
    :return:
    """
    audience_path = Path('%s/%s' % (settings.RECORDING_PATHS['AUDIENCE'], id)).absolute()
    webm_path = Path('%s/%s.webm' % (settings.RECORDING_PATHS['AUDIENCE'], id)).absolute()
    mp4_path = Path('%s/%s.mp4' % (settings.RECORDING_PATHS['AUDIENCE'], id)).absolute()

    # Analyze video
    # command = 'ffprobe -i %s -v quiet -print_format json -show_streams' % video_path
    # output = subprocess.check_output(command.split())
    # m = loads(output.decode("utf-8"))  # map
    #
    # for stream in m['streams']:
    #     if stream['codec_type'] == 'audio':
    #         combined = True
    #         break

    # webm pass 1
    command = 'ffmpeg -v %s -y -i %s -c:v libvpx -cpu-used 1 -c:a libvorbis -vb 800K -maxrate 1m -pass 1 -f webm /dev/null' \
              % (LOG_LEVEL, audience_path)
    print(command)
    subprocess.call(command.split())
    # webm pass 2
    command = 'ffmpeg -v %s -y -i %s -c:v libvpx -cpu-used 1 -c:a libvorbis -vb 800K -maxrate 1m -pass 2 %s' \
              % (LOG_LEVEL, audience_path, webm_path)
    print(command)
    subprocess.call(command.split())

    # mp4 pass 1
    command = 'ffmpeg -v %s -y -i %s -c:v libx264 -preset veryslow -crf 5 -b:v 800k -maxrate 1m -pass 1 -profile:v baseline -level 3.0 -c:a copy -f mp4 /dev/null' \
              % (LOG_LEVEL, audience_path)
    print(command)
    subprocess.call(command.split())
    # mp4 pass 2
    command = 'ffmpeg -v %s -y -i %s -c:v libx264 -preset veryslow -crf 5 -b:v 800k -maxrate 1m -pass 2 -profile:v baseline -level 3.0 -c:a copy %s' \
              % (LOG_LEVEL, audience_path, mp4_path)
    print(command)
    subprocess.call(command.split())

    # upload video files
    audience = Audience.objects.get(pk=id)
    with webm_path.open(mode='rb') as video:
        audience.file_webm.save('%s.webm' % id, File(video))
    with mp4_path.open(mode='rb') as video:
        audience.file_mp4.save('%s.mp4' % id, File(video))

    # clean up files
    os.remove(str(audience_path))
    os.remove(str(webm_path))
    os.remove(str(mp4_path))
