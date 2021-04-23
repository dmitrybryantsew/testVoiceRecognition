#!/usr/bin/env python3

from vosk import Model, KaldiRecognizer
import os
import json
import pyaudio
import locale

class Recognizer:
    def __init__(self, pathToModel):
        self.answer = "None"
        self.modelFlag = False
        self.pyAudioFlag = False
        self.pathToModel = pathToModel

    def setupModel(self):
        if not os.path.exists(self.pathToModel):
            print("Please download the model from https://github.com/alphacep/vosk-api/blob/master/doc/models.md and unpack as 'model' in the current folder.")
            exit(1)
        self.model = Model(self.pathToModel)
        self.rec = KaldiRecognizer(self.model, 16000)
        self.modelFlag = True
        self.startPyaudio()

    def startPyaudio(self):
        self.p = pyaudio.PyAudio()
        self.stream = self.p.open(
            format=pyaudio.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=8000)
        self.stream.start_stream()
        self.pyAudioFlag = True

    def stopPyaudio(self):
        self.stream.stop_stream()
        self.pyAudioFlag = False

    def runTimedRecognition(self):
        n = 1000
        while True:
            data = self.stream.read(4000)
            if len(data) == 0:
                break
            if self.rec.AcceptWaveform(data):
                result = self.rec.Result()
                print(result)
                d = json.loads(str(result))
                myStr = d["text"]
                print(myStr)
                self.answer = myStr
                return myStr
            else:
                print(self.rec.PartialResult())
            if n == 0:
                break
            print(n)
            n -= 1