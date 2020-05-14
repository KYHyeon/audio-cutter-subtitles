import os
from glob import glob

import webvtt
import ffmpeg

SRC_PATH = './src/'
DST_PATH = './dst/'


def audio_cutter():
    for file in glob('./src/*.vtt'):
        filename = os.path.basename(file).replace('.vtt', '')
        vtt_file = SRC_PATH + filename + '.vtt'
        wav_file = SRC_PATH + filename + '.wav'

        for i, caption in enumerate(webvtt.read(vtt_file)):
            print(caption.raw_text)
            print(caption.start_in_seconds)
            print(caption.end_in_seconds)
            print(caption.raw_text)

            (
                ffmpeg
                    .input(wav_file)
                    .filter('atrim', start=caption.start_in_seconds, end=caption.end_in_seconds)
                    .output(DST_PATH + filename + ".%04d" % i + '.wav')
                    .run()
            )


audio_cutter()
