#! /usr/bin/env python3

import os
import sys
import csv
path = os.getcwd()


def is_exist(file_path):
    if os.path.isfile(os.path.join(path, file_path)):
        return os.path.join(path, file_path)
    elif os.path.isfile(file_path):
        return file_path
    else:
        return False


def convert_to_audio(file_path):

    # handle filename with whitespace
    [input_name, input_type] = os.path.splitext(file_path)
    output_name = 'audio-' + '"' + input_name + '"'
    file_path = '"' + file_path + '"'

    # conver into flac for Google Cloud Speech-To-Tex API
    #  cmd = 'ffmpeg -i {input} -f flac -ab 192000 -vn {output}.flac'.format(
    #      input=file_path, output=output_name)
    """
        -i input file
        -f convert to format, flac is recommanded by
            Google Cloud Speech-To-Tex API
        -ar conver to sampleRateHertz, 16000 is recommanded
            by Google Cloud Speech-To-Tex API
        -vn output file is not video
        -ac 1 only 1 channel audio would be allowed by Cloud Speech

    """
    cmd = 'ffmpeg -i {input} -f flac -ar 16000 -ac 1 -vn {output}.flac'.format(
        input=file_path, output=output_name)
    try:
        os.system(cmd)
    except BaseException:
        print('error: convert failed!')
        exit(1)


def avaliable_type(file_type):

    # optional 1: common video format
    aval_type = [
        'mp4', 'flv', 'avi', 'mpeg', 'rm', 'mov', 'asf', 'm4v', '3gp', '3g2',
        'mj2'
    ]

    # optional 2: all support format
    all_aval_type = []
    with open('./ffmepeg_all_avaliable_format.csv') as csvfile:
        reader = list(csv.reader(csvfile))
        all_aval_type = [f[0] for f in reader]

    # obtain file format
    [input_name, input_type] = os.path.splitext(file_path)

    # remove '.' and check whether format avaliable for ffmpeg
    if input_type[1:] in all_aval_type:
        return True
    else:
        return False


if __name__ == "__main__":
    file_path = sys.argv[1]
    if is_exist(file_path) and avaliable_type(file_path):
        convert_to_audio(file_path)
        print('Convert Successfully!')
    else:
        print('error: ' + file_path,
              'does not exist or format is not avaliable')
    print("Upload to gcs..")
    [input_name, input_type] = os.path.splitext(file_path)
    output_name = 'audio-' + input_name + '.flac'
    upload_file = '"' + output_name + '"'
    cmd = "gsutil cp " + upload_file + " gs://test-convert-audio"
    try:
        os.system(cmd)
        print("Upload successfully. You can use: " + '"' +
              "gs://test-convert-audio/" + 'audio-' + output_name + '"')
    except BaseException:
        print('error: upload failed!')
        exit(1)
