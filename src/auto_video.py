import moviepy.editor as mp

import wave
import json

from vosk import Model, KaldiRecognizer, SetLogLevel
from types import SimpleNamespace

import Word as CustomWord
import Command as CustomCommand

def LoadConfiguration(): 
    configurationFile = open("./configuration.json")
    result = json.loads(configurationFile.read(), object_hook=lambda d: SimpleNamespace(**d))
    configurationFile.close()
    # print(result.commandWords.startSegment[1])
    return result

def GetCommandsByWord(configuration): 
    commandsByWord = {}
    for word in configuration.commandWords.startSegment:
        commandsByWord[word] = "startSegment"
    for word in configuration.commandWords.deleteSegment:
        commandsByWord[word] = "deleteSegment"
    for word in configuration.commandWords.endSegment:
        commandsByWord[word] = "endSegment"
    # print(commandsByWord)
    return commandsByWord

def RecognizeCommands(words):
    configuration = LoadConfiguration()
    commandsByWord = GetCommandsByWord(configuration)
    result = []
    for i in range(len(words)):
        if i < 2:
            continue
        if (words[i].word == words[i-1].word) and (words[i].word == words[i-2].word): 
            if words[i].word in commandsByWord:
                command = CustomCommand.Command(commandsByWord[words[i].word], words[i-2].start, words[i].end)
                result.append(command)
            else:
                print("Warning: The word '{:1}' was received as a command but there is not a command configured for this word!".format(words[i].word))
    return result

def EditVideo(source, destination, segments):
    video = mp.VideoFileClip(source)
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
    # model_path = "../models/vosk-model-en-us-0.22"
    model_path = "../models/vosk-model-small-en-us-0.15"
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
    return result

def ConvertMp4toWav(videoPath, audioOutputPath):
    clip = mp.VideoFileClip(videoPath)
    # convert video to audio
    # ffmpeg_params=["-ac", "1"] parameter convert audio to mono format
    clip.audio.write_audiofile(audioOutputPath, ffmpeg_params=["-ac", "1"])
    return True

def GetSegments(commands): 
    # segments = [(0, 10), (60, None)]
    segments = []
    for i in range(len(commands)):
        if i < 1:
            continue
        if commands[i].command == "startSegment": 
            continue
        elif commands[i].command == "deleteSegment":
            continue 
        elif commands[i].command == "endSegment":
            if commands[i-1].command == "startSegment":
                segments.append((commands[i-1].end, commands[i].start))
            else: 
                print("Warning: Found 'endSegment' command without 'startSegment' command. Ignoring command 'endSegment' from {:.2f} sec to {:.2f} sec".format(commands[i].start, commands[i].end))
        else:
            print("Error: Command '{:1}' not implemented!".format(commands[i].command))
    return segments

def AutoEditVideo(inVideoPath, outVideoPath, language):
    outSoundPath = outVideoPath.replace(".mp4", ".wav")
    ConvertMp4toWav(inVideoPath, outSoundPath)
    words = RecogniseWords(outSoundPath, language)
    print("Words:")
    for word in words:
        print(word.to_string())
    commands = RecognizeCommands(words)
    print("Commands:")
    for command in commands:
        print(command.to_string())

    segments = GetSegments(commands)
    print("Segments:")
    print(segments)

    EditVideo(inVideoPath, outVideoPath, segments)
    return True

# AutoEditVideo("../qa/videos/video_demo_05.mp4", "../qa/output/video_demo_05.mp4", "pt-br")
# AutoEditVideo("../qa/videos/video_demo_07.mp4", "../qa/output/video_demo_07.mp4", "en-us")
AutoEditVideo("../qa/videos/hackathon_autovideo_editor.mp4", "../qa/output/hackathon_autovideo_editor.mp4", "en-us")

