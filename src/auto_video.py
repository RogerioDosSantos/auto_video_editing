import moviepy.editor as mp

import wave
import json

from vosk import Model, KaldiRecognizer, SetLogLevel
import Word as custom_Word

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
            w = custom_Word.Word(obj)  # create custom Word object
            result.append(w)  # and add it to list
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

def AutoEditVideo(inVideoPath, outVideoPath, language):
    # EditVideo("../qa/videos/video_demo_01.mp4", "../qa/output/video_demo_01_edited.mp4")
    outSoundPath = outVideoPath.replace(".mp4", ".wav")
    print(outSoundPath)
    print(outVideoPath)
    ConvertMp4toWav(inVideoPath, outSoundPath)
    words = RecogniseWords(outSoundPath, language)
    frase = []
    for word in words: 
        print(word.to_string())
    #     frase.append("{:} ({:.2f}%)".format(word.word, word.confidence * 100))
    # print(frase)
    return True

# AutoEditVideo("../qa/videos/video_demo_05.mp4", "../qa/output/video_demo_05.mp4", "pt-br")
AutoEditVideo("../qa/videos/video_demo_05.mp4", "../qa/output/video_demo_05.mp4", "en-us")

