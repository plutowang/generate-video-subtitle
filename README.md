# Generate subtitle for a video

[TOC]



## Requirement

- Adding a subtitle for a video automatically 
  1. Extract sound from video
     1. Input: video
        - Format: any video format allowed by [FFmpge](https://www.easytechguides.com/extract-audio-from-video.htm)
        - Size: no longer than 1min, if it is longer than 1min, we may upload output audio into Google Cloud Storage, and use `gcs_uri` in convert speech step with [Google Cloud Speech-To-Text API](https://cloud.google.com/speech-to-text/docs/languages)
     2. Output: audio
        - Format: 
          - **Ecoding: FLAC**
          - **sample_rate_hertz=16000 or more**
          - Language=Mandarin
  2. Convert speech into text
     1. Input: audio
        - Format: above output audio format
     2. Output: text
        - Format: Plain text and `str` file
  3. Generate subtitle using above source
     - `.str `file is the target subtitle file

## Component

### 1. Extract sound from video using [FFmpeg](https://www.easytechguides.com/extract-audio-from-video.htm)

- Install:

- ```shell
  $ brew install ffmpeg
  ```

- Usage:

  ```shell
  ffmpeg -i video.mp4 -f mp3 -ab 192000 -vn audio.mp3
  ```

  - `-i `input file
  - `-f` convert to format, flac is recommanded by Google Cloud Speech-To-Tex API
  - `-ar ` conver to sampleRateHertz, 16000 is recommanded by Google Cloud Speech-To-Tex API
  - `-vn` output file is not video
  - `-ac` 1 only 1 channel audio would be allowed by Cloud Speech

- Allow format

  ```shell
   ffmpeg -formats
  ```

  ```shell
  D  3dostr          3DO STR
    E 3g2             3GP2 (3GPP2 file format)
    E 3gp             3GP (3GPP file format)
   D  4xm             4X Technologies
    E a64             a64 - video for Commodore 64
   D  aa              Audible AA format files
   D  aac             raw ADTS AAC (Advanced Audio Coding)
   DE ac3             raw AC-3
   D  acm             Interplay ACM
   
  ...
  ```

### 2. Convert audio into text using [Google Cloud Speech-To-Text API](https://cloud.google.com/speech-to-text/docs/languages)

- Install: follow official website [Set up a GCP Console projec, Set the environment variable GOOGLE_APPLICATION_CREDENTIALS](https://cloud.google.com/speech-to-text/docs/quickstart-client-libraries) and [install and initialize Google Cloud SDK](https://cloud.google.com/sdk/docs/)

  Install the client library (for python):

  ```shell
  pip3 install --upgrade google-cloud-speech
  ```

- In this project, our test video is longer than 1 min, we need the asynchronously transcribes and use `gcs_uri` for speech file

- we refer the following code from [official website](https://cloud.google.com/speech-to-text/docs/async-recognize) 

- ```python
  # [START speech_transcribe_async_gcs]
  def transcribe_gcs(gcs_uri):
      """Asynchronously transcribes the audio file specified by the gcs_uri."""
      from google.cloud import speech
      from google.cloud.speech import enums
      from google.cloud.speech import types
      client = speech.SpeechClient()
  
      audio = types.RecognitionAudio(uri=gcs_uri)
      config = types.RecognitionConfig(
          encoding=enums.RecognitionConfig.AudioEncoding.FLAC,
          sample_rate_hertz=16000,
          language_code='en-US')
  
      operation = client.long_running_recognize(config, audio)
  
      print('Waiting for operation to complete...')
      response = operation.result(timeout=90)
  
      # Each result is for a consecutive portion of the audio. Iterate through
      # them to get the transcripts for the entire audio file.
      for result in response.results:
          # The first alternative is the most likely one for this portion.
          print(u'Transcript: {}'.format(result.alternatives[0].transcript))
          print('Confidence: {}'.format(result.alternatives[0].confidence))
  # [END speech_transcribe_async_gcs]
  ```

- In config,

  - We use as following:

    - **sample_rate_hertz=16000**
    - language_code='zh'
    - **encoding='FLAC'**
    - this config would set several phrases for specific vedio "Savvy _June Cut_final.mp4"
    - enable_word_time_offsets=True, which include timestamp used for generate subtitle
    - enable_automatic_punctuation=True, which include punctuation in transcript field

  - ```python
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
    ```

## Usage

### `extract-audio.py`

```shell
python3 extract-audio.py Savvy\ _June\ Cut_final.mp4
```

- This script would recogonize whether the file exists, whether the format allowed by `ffmpeg`

- Furthermore, this script can handle the input name with whitespace and output coutain original file name
- The output audio is obtain each config which needed by [Google Cloud Speech-To-Text API](https://cloud.google.com/speech-to-text/docs/languages)(see: Component2)
- The output file name would be `audio-inputFileName.flac `, which would also be upload into `gs://test-convert-audio/audio-inputFileName.flac`(used in convert step)

### `audio-to-text.py`

For shorter audio (no longer 1 min) using synchronous speech recognition.

```shell
python3 audio-to-text.py localFile.flac
```

For longer audio (longer than 1 min) using asynchronous speech recognition.

```shell
python3 audio-to-text.py "gs://test-convert-audio/audio-Savvy _June Cut_final.flac"
```

Note: if filename with whitespace plase use `""`

#### Step1: convert to text

This script would send a recognize request to [Cloud Speech-to-Text](https://cloud.google.com/speech-to-text/) and obtain the response, and we can also write into a plain text in output folder (` transcript-text.txt`)

```python
operation = client.long_running_recognize(config, audio)
response = operation.result(timeout=90)
```

#### Step2: format text as subtitle file `.srt`

This script add sequence number for each line and timpesamp for each line (e.g `0:00:1.012 —> 0: 00: 3.211`) and the words, which format is need by `.str` file

helper modual `timestr.py` would help us convert the `start_time`or `end_time` as allowed string, `start_time`or `end_time` both are from `response` information

Because the `response.result.alternatives[0].word` only contain word information, so reading output file `transcript-text.txt`, which including punctuation, and add punctuation into subtitle file or leave white space at punctuation position. 

#### Note

- There provide two version audio-to-text.py available 

  - Subtitle with punctuation `audio-to-text-with-punctuation.py`:

    - ```shell
      python3 audio-to-text-with-punctuation.py "gs://test-convert-audio/audio-Savvy _June Cut_final.flac"
      ```

  - Subtitle no punctuation `audio-to-text-no-punctuation.py`

    - ```shell
      python3 audio-to-text-no-punctuation.py "gs://test-convert-audio/audio-Savvy _June Cut_final.flac"
      ```

