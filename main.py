import os
from glob import glob
import argparse

import webvtt
import ffmpeg

SUPPORT_VOICE_FORMAT = ['.wav']
SUPPORT_SUBTITLE_FORMAT = ['.vtt']


def audio_cutter(args):
    for file in glob(os.path.join(args.input, '*' + args.subtitle_format)):
        filename = os.path.basename(file).replace(args.subtitle_format, '')
        vtt_file = os.path.join(args.input, filename + args.subtitle_format)
        wav_file = os.path.join(args.input, filename + args.voice_format)

        for i, subtitle in enumerate(webvtt.read(vtt_file)):
            print(subtitle.raw_text)
            print(subtitle.start_in_seconds)
            print(subtitle.end_in_seconds)
            print(subtitle.raw_text)

            (
                ffmpeg
                    .input(wav_file)
                    .filter('atrim', start=subtitle.start_in_seconds, end=subtitle.end_in_seconds)
                    .output(os.path.join(args.output, filename + ".%04d" % i + args.voice_format))
                    .run()
            )


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Cut the voice file corresponding to the subtitles into sections.')
    parser.add_argument('-i', '--input', help='Path where the input voice and subtitle files', default='./src')
    parser.add_argument('-o', '--output', help='Path where the output file will be generated', default='./dst')
    parser.add_argument('--voice_format', default='.wav')
    parser.add_argument('--subtitle_format', default='.vtt')

    args = parser.parse_args()

    if args.voice_format not in SUPPORT_VOICE_FORMAT:
        raise TypeError('Error: %s is not support' % args.voice_format)

    if args.subtitle_format not in SUPPORT_SUBTITLE_FORMAT:
        raise TypeError('Error: %s is not support' % args.subtitle_format)

    try:
        if not os.path.exists(args.output):
            os.makedirs(args.output)
    except OSError:
        print('Error: Creating directory. ' + args.output)

    audio_cutter(args)
