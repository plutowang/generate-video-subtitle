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
import os
import codecs
import timestr
import string
# Imports the Google Cloud client library
from google.cloud import speech
from google.cloud.speech import enums
from google.cloud.speech import types


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
        phrases=[
            '思睿', '在思睿', '海外教育', '双师', '贴心的辅导', '授课', '云台录播', '讲义', '赢取', '引起',
            '只为', '相结合', '坚持而努力', '越来越近', '思睿用爱'
        ])
    # [START speech_python_migration_async_response]
    operation = client.long_running_recognize(config, audio)
    # [END speech_python_migration_async_request]

    print('Waiting for operation to complete...')
    response = operation.result(timeout=90)
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
                '思睿', '在思睿', '海外教育', '双师', '贴心的辅导', '授课', '云台录播', '讲义', '赢取',
                '引起', '只为', '相结合', '坚持而努力', '越来越近', '思睿用爱'
            ])
        ],
        enable_word_time_offsets=True,
        enable_automatic_punctuation=True)
    # [START speech_python_migration_async_response]
    operation = client.long_running_recognize(config, audio)
    # [END speech_python_migration_async_request]

    print('Waiting for operation to complete...')
    response = operation.result(timeout=90)
    return response


def write_into_doc(source, output_path):
    #  from google.protobuf.json_format import MessageToJson
    #  with open('./test-json.txt', 'w', encoding='utf-8') as writer:
    #      json.dump(MessageToJson(source), writer, ensure_ascii=False)

    print('Waiting for writing doc to complete...')

    with codecs.open(output_path + 'transcript-text.txt', 'w',
                     'utf-8') as writer:
        for result in source.results:
            alternative = result.alternatives[0].transcript
            writer.write(alternative)


def write_into_subtitle(response, output_path):

    print('Waiting for writing subtitle to complete...')

    # read the chinese punctuation
    with codecs.open(output_path + 'transcript-text.txt', 'r',
                     'utf-8') as reader:
        words = reader.read()
        punc_index_list = []
        punc_index = 0
        for w in words:
            if not w.isalpha() and w not in string.whitespace:
                punc_index_list.append(punc_index)
                punc_index += 1
            elif w.isalpha():
                punc_index += 1

    with codecs.open(output_path + 'subtitle-no-punctuation.srt', 'w',
                     'utf-8') as writer:
        i = 1  # setting the sequence number for srt
        init = True  # init flag
        word_index = 0
        curr = 0  # current punctuation number
        for result in response.results:
            alternative = result.alternatives[0]
            line = ""  # each line contain 10 words
            counter = 0  # word counter in a line
            # how many words remaining in this result
            num_woeds = len(alternative.words)
            start_next_para = True
            # loop the word in the result
            for word_info in alternative.words:
                word_index += 1
                num_woeds -= 1
                counter += 1
                word = word_info.word
                if init:
                    start_time = word_info.start_time
                    str_start = timestr.timefm(start_time.seconds +
                                               start_time.nanos * 1e-9)
                    init = False
                if start_next_para:
                    start_time = word_info.start_time
                    str_start = timestr.timefm(start_time.seconds +
                                               start_time.nanos * 1e-9)
                    start_next_para = False

                if counter < 10:
                    # when the num of word in this line less than
                    # 10 word, we only add this word in this line
                    line += word
                    if word_index == (punc_index_list[curr]):
                        curr += 1
                        line += ' '
                        word_index += 1
                else:
                    # the line is enouge 10 words, we inster seq num,
                    # time and line into the srt file
                    counter = 0  # clear the counter for nex iteration
                    end_time = word_info.end_time
                    str_end = timestr.timefm(end_time.seconds +
                                             end_time.nanos * 1e-9)
                    writer.write(str(i))  # write the seq num into file,
                    # and then add 1
                    i += 1
                    line += word
                    if word_index == (punc_index_list[curr]):
                        curr += 1
                        line += ' '
                        word_index += 1
                    writer.write('\n')
                    writer.write(str_start)  # write start time
                    writer.write(' --> ')
                    writer.write(str_end)  # write end time
                    writer.write('\n')
                    writer.write(line)  # write the word
                    line = ""  # clear the line for next iteration
                    writer.write('\n\n')
                    start_time = word_info.start_time
                    str_start = timestr.timefm(start_time.seconds +
                                               start_time.nanos * 1e-9)

                # avoid miss any word, because counter < 0,
                # but this iteration has no word remain
                if counter < 10 and num_woeds == 0:
                    end_time = word_info.end_time
                    str_end = timestr.timefm(end_time.seconds +
                                             end_time.nanos * 1e-9)

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


def main():
    arg = sys.argv[1]
    output_path = './output/'
    if not os.path.exists(output_path):
        os.mkdir(output_path)

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
        write_into_doc(response, output_path)
        print("Write into doc successfully!")
    except BaseException:
        print('error: Write into doc failed!')
        exit(1)
    # write into doc
    try:
        write_into_subtitle(response, output_path)
        print("Write into subtitle successfully!")
    except BaseException:
        print('error: Write into subtitle failed!')
        exit(1)


if __name__ == "__main__":
    main()
