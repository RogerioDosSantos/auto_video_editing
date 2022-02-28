import moviepy.editor as mp

import wave
import json

from vosk import Model, KaldiRecognizer, SetLogLevel
from types import SimpleNamespace

import Word as CustomWord
import Command as CustomCommand

def LoadConfiguration(): 
    configurationFile = open("./configuration.json")
    configuration = json.load(configurationFile)
    configurationFile.close()

    data = '{"name": "John Smith", "hometown": {"name": "New York", "id": 123}}'
    # Parse JSON into an object with attributes corresponding to dict keys.
    x = json.loads(data, object_hook=lambda d: SimpleNamespace(**d))
    # print(x.name, x.hometown.name, x.hometown.id)
    print(data)
    print(x)
    print(configuration)



    result = configuration
    return result

def EditVideo(source, destination):
    video = mp.VideoFileClip(source)
    # delete video fragment from 00:30 to 01:00
    segments = [(0, 10), (60, None)]
    clips = []  # list of all video fragments
    for start_seconds, end_seconds in segments:
        # crop a video clip and add it to list
        c = video.subclip(start_seconds, end_seconds)
        clips.append(c)
    final_clip = mp.concatenate_videoclips(clips)
    final_clip.write_videofile(destination)
    final_clip.close()
    return True

def RecogniseWords(source, language):
    model_path = "../models/vosk-model-en-us-0.22"
    # model_path = "../models/vosk-model-small-en-us-0.15"
    # model_path = "../models/vosk-model-en-us-0.22-lgraph"
    if language == "pt-br":
        model_path = "../models/vosk-model-small-pt-0.3"
    # audio_filename = "audio/speech_recognition_systems.wav"
    audio_filename = source
    model = Model(model_path)
    wf = wave.open(audio_filename, "rb")
    rec = KaldiRecognizer(model, wf.getframerate())
    rec.SetWords(True)
    # get the list of JSON dictionaries
    results = []
    # recognize speech using vosk model
    while True:
        data = wf.readframes(4000)
        if len(data) == 0:
            break
        if rec.AcceptWaveform(data):
            part_result = json.loads(rec.Result())
            results.append(part_result)
    part_result = json.loads(rec.FinalResult())
    results.append(part_result)
    # convert list of JSON dictionaries to list of 'Word' objects
    result = []
    for sentence in results:
        if len(sentence) == 1:
            # sometimes there are bugs in recognition 
            # and it returns an empty dictionary
            # {'text': ''}
            continue
        for obj in sentence['result']:
            word = CustomWord.Word(obj)  # create custom Word object
            result.append(word)  # and add it to list
    wf.close()  # close audiofile
    # output to the screen
    # for word in result:
    #     print(word.to_string())
    return result

def ConvertMp4toWav(videoPath, audioOutputPath):
    clip = mp.VideoFileClip(videoPath)
    # convert video to audio
    # ffmpeg_params=["-ac", "1"] parameter convert audio to mono format
    clip.audio.write_audiofile(audioOutputPath, ffmpeg_params=["-ac", "1"])
    return True

def RecognizeCommands(words):
    result = []
    for i in range(len(words)):
        if i < 2:
            continue
        # print("- words[i] = {:1} ; words[i-1] = {:1} ; words[i-2] = {:1}".format(words[i].word, words[i-1].word, words[i-2].word))
        if (words[i].word == words[i-1].word) and (words[i].word == words[i-2].word): 
            command = CustomCommand.Command(words[i].word, words[i-2].start, words[i].end)
            result.append(command)
    for command in result:
        print(command.to_string())
    return result

def AutoEditVideo(inVideoPath, outVideoPath, language):
    configuration = LoadConfiguration()
    # outSoundPath = outVideoPath.replace(".mp4", ".wav")
    # ConvertMp4toWav(inVideoPath, outSoundPath)
    # words = RecogniseWords(outSoundPath, language)
    # commands = RecognizeCommands(words)
    # EditVideo("../qa/videos/video_demo_01.mp4", "../qa/output/video_demo_01_edited.mp4")
    return True

# AutoEditVideo("../qa/videos/video_demo_05.mp4", "../qa/output/video_demo_05.mp4", "pt-br")
AutoEditVideo("../qa/videos/video_demo_07.mp4", "../qa/output/video_demo_07.mp4", "en-us")

