#! /usr/bin/env python3
"""
ref: transcribe_file and transcribe_gcs function is reference
    from officaial website, which use asynchronously transcribes,
    because the vedio is longer than 1 min

this script would generate two files: 1. text.txt--plain text for the vedio
                                      2. subtitle.srt--subtitle file

Usage:
        1. longer than 1 min pleause use gcs_uri:
            e.g. python3 audio-to-text.py "gs://test-convert-audio/audio-Savvy _June Cut_final.flac"
            Note: if there exits whitespace in filename, pleause use \"\"
        2. no longer than 1 min we can use local file:
            e.g. python3 audio-to-text.py audio.raw

Note: In this file, the default config:
        1. sample_rate_hertz=16000,
        2. language_code='zh'
        3. encoding='FLAC'
        4. this config would set several phrases
            for specific vedio "Savvy _June Cut_final.mp4"

"""

import sys
import io
import codecs
from timer import TimeStamp
from decimal import Decimal

# Imports the Google Cloud client library
from google.cloud import speech
from google.cloud.speech import enums
from google.cloud.speech import types

#  """
#  encode source_audio_file to dest_audio_file with base64
#
#  """
#  def encode(source_audio_file):
#      [input_name, input_type] = os.path.splitext(source_audio_file)
#      # handle filename with whitespace
#      dest_audio_file = 'base64-' + '"' + input_name + '"'
#      source_audio_file = '"' + source_audio_file + '"'
#      cmd = 'base64 {source} > {dest}'.format(
#          source=source_audio_file, dest=dest_audio_file)
#      try:
#          os.system(cmd)
#      except BaseException:
#          print('error: encoding failed!')
#          exit(1)
#
#
#  def send_recognize_request(file_name):
#      from google.cloud import speech
#      from google.cloud.speech import enums
#      from google.cloud.speech import types
#
#      # Instantiates a client
#      client = speech.SpeechClient()
#
#      # Loads the audio into memory
#      with io.open(file_name, 'rb') as audio_file:
#          content = audio_file.read()
#          audio = types.RecognitionAudio(content=content)
#
#      config = types.RecognitionConfig(
#          encoding=enums.RecognitionConfig.AudioEncoding.FLAC,
#          sample_rate_hertz=16000,
#          language_code='zh')
#      # Detects speech in the audio file
#      response = client.recognize(config, audio)
#
#      for result in response.results:
#          print('Transcript: {}'.format(result.alternatives[0].transcript))
#
#


def transcribe_file(speech_file):
    """Transcribe the given audio file asynchronously."""
    client = speech.SpeechClient()

    # [START speech_python_migration_async_request]
    with io.open(speech_file, 'rb') as audio_file:
        content = audio_file.read()

    audio = types.RecognitionAudio(content=content)
    config = types.RecognitionConfig(
        encoding=enums.RecognitionConfig.AudioEncoding.FLAC,
        sample_rate_hertz=16000,
        language_code='zh',
        phrases=['思睿', '在思睿', '海外教育', '双师', '辅导', '授课', '云台录播'])
    # [START speech_python_migration_async_response]
    operation = client.long_running_recognize(config, audio)
    # [END speech_python_migration_async_request]

    print('Waiting for operation to complete...')
    response = operation.result(timeout=90)

    #  # Each result is for a consecutive portion of the audio. Iterate through
    #  # them to get the transcripts for the entire audio file.
    #  for result in response.results:
    #      # The first alternative is the most likely one for this portion.
    #      print(u'Transcript: {}'.format(result.alternatives[0].transcript))
    #      print('Confidence: {}'.format(result.alternatives[0].confidence))
    #  # [END speech_python_migration_async_response]
    #  # [END speech_transcribe_async]
    return response


def transcribe_gcs(gcs_uri):
    """Transcribe the given audio file asynchronously."""
    client = speech.SpeechClient()

    audio = types.RecognitionAudio(uri=gcs_uri)
    config = types.RecognitionConfig(
        encoding=enums.RecognitionConfig.AudioEncoding.FLAC,
        sample_rate_hertz=16000,
        language_code='zh',
        speech_contexts=[
            speech.types.SpeechContext(phrases=[
                '思睿', '在思睿', '海外教育', '双师', '辅导', '授课', '云台录播', '讲义', '赢取'
            ])
        ],
        enable_word_time_offsets=True,
        enable_automatic_punctuation=True)
    # [START speech_python_migration_async_response]
    operation = client.long_running_recognize(config, audio)
    # [END speech_python_migration_async_request]

    print('Waiting for operation to complete...')
    response = operation.result(timeout=90)

    #  #  Each result is for a consecutive portion of the audio. Iterate
    #  #  through them to get the transcripts for the entire audio file.
    #  for result in response.results:
    #      # The first alternative is the most likely one for this portion.
    #      print(u'Transcript: {}'.format(result.alternatives[0].transcript))
    #      print('Confidence: {}'.format(result.alternatives[0].confidence))
    #  # [END speech_python_migration_async_response]
    #  # [END speech_transcribe_async]
    #  for result in response.results:
    #      alternative = result.alternatives[0]
    #      print(u'Transcript: {}'.format(alternative.transcript))
    #      print('Confidence: {}'.format(alternative.confidence))
    #
    #      for word_info in alternative.words:
    #          word = word_info.word
    #          start_time = word_info.start_time
    #          end_time = word_info.end_time
    #          print('Word: {}, start_time: {}, end_time: {}'.format(
    #              word, start_time.seconds + start_time.nanos * 1e-9,
    #              end_time.seconds + end_time.nanos * 1e-9))
    return response


def write_into_doc(source):
    #  from google.protobuf.json_format import MessageToJson
    #  with open('./test-json.txt', 'w', encoding='utf-8') as writer:
    #      json.dump(MessageToJson(source), writer, ensure_ascii=False)

    print('Waiting for writing doc to complete...')

    with codecs.open('./text.txt', 'w', 'utf-8') as writer:
        for result in source.results:
            alternative = result.alternatives[0].transcript
            writer.write(alternative)


def write_into_subtitle(source):

    print('Waiting for writing subtitle to complete...')

    with codecs.open('./subtitle.srt', 'w', 'utf-8') as writer:
        i = 1  # setting the sequence number for srt
        init = True  # init flag
        for result in response.results:
            alternative = result.alternatives[0]
            line = ""  # each line contain 10 words
            counter = 0  # word counter in a line
            # how many words remaining in this result
            num_woeds = len(alternative.words)
            start_next_para = True
            # loop the word in the result
            for word_info in alternative.words:
                num_woeds -= 1
                counter += 1
                word = word_info.word
                if init:
                    start_time = word_info.start_time
                    time = TimeStamp(start_time.seconds +
                                     start_time.nanos * 1e-9)
                    str_start = time.toString()
                    init = False
                if start_next_para:
                    start_time = (word_info.start_time.seconds +
                                  word_info.start_time.nanos * 1e-9)
                    str_start = TimeStamp(
                        Decimal(start_time).quantize(
                            Decimal("0.000000000"))).toString()
                    #  str_start = time.toString()
                    start_next_para = False

                # acccumulate the time
                time.addSeconds(
                    Decimal((word_info.end_time.seconds +
                             word_info.end_time.nanos * 1e-9
                             )).quantize(Decimal("0.000000000")) -
                    Decimal((word_info.start_time.seconds +
                             word_info.start_time.nanos * 1e-9
                             )).quantize(Decimal("0.000000000")))

                if counter < 8:
                    # when the num of word in this line less than
                    # 10 word, we only add this word in this line
                    line += word
                else:
                    # the line is enouge 10 words, we inster seq num,
                    # time and line into the srt file
                    counter = 0  # clear the counter for nex iteration
                    str_end = time.toString()
                    #  print(1)
                    #  end_time = (word_info.end_time.seconds +
                    #              word_info.end_time.nanos * 1e-9)
                    #  str_end = TimeStamp(end_time).toString()
                    writer.write(str(i))  # write the seq num into file,
                    # and then add 1
                    i += 1
                    line += word
                    writer.write('\n')
                    writer.write(str_start)  # write start time
                    writer.write(' --> ')
                    writer.write(str_end)  # write end time
                    writer.write('\n')
                    writer.write(line)  # write the word
                    line = ""  # clear the line for next iteration
                    writer.write('\n\n')
                    str_start = time.toString()
                    #  start_time = (word_info.start_time.seconds +
                    #                word_info.start_time.nanos * 1e-9)
                    #  str_start = TimeStamp(start_time).toString()
                # avoid miss any word, because counter < 0,
                # but this iteration has no word remain
                if counter < 8 and num_woeds == 0:
                    str_end = time.toString()
                    #  end_time = (word_info.end_time.seconds +
                    #              word_info.end_time.nanos * 1e-9)
                    #  str_end = TimeStamp(end_time).toString()
                    writer.write(str(i))
                    i += 1
                    writer.write('\n')
                    writer.write(str_start)  # write start time
                    writer.write(' --> ')
                    writer.write(str_end)  # write end time
                    writer.write('\n')
                    writer.write(line)  # write the word
                    line = ""
                    writer.write('\n\n')
                    str_start = time.toString()


if __name__ == "__main__":
    arg = sys.argv[1]
    if arg.startswith('gs://'):
        try:
            response = transcribe_gcs(arg)
            print("Transcribe successfully!")
        except BaseException:
            print('error: transcribe failed!')
            exit(1)
    else:
        try:
            response = transcribe_file(arg)
            print("Transcribe successfully!")
        except BaseException:
            print('error: transcribe failed!')
            exit(1)
    # write into doc
    try:
        write_into_doc(response)
        print("Write into doc successfully!")
    except BaseException:
        print('error: Write into doc failed!')
        exit(1)
    # write into doc
    try:
        write_into_subtitle(response)
        print("Write into subtitle successfully!")
    except BaseException:
        print('error: Write into subtitle failed!')
        exit(1)
