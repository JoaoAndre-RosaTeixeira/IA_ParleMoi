import os

import speech_recognition as sr

import pyaudio
import wave


class Mp3Record:

    def __init__(self):
        self.chunk = 1024  # Record in chunks of 1024 samples
        self.sample_format = pyaudio.paInt16  # 16 bits per sample
        self.channels = 2
        self.fs = 44100  # Record at 44100 samples per second
        self.filename = "ressources/output.mp3"
        self.p = pyaudio.PyAudio()  # Create an interface to PortAudio
        self.frames = []  # Initialize array to store frames
        self.stream = None

    def start_record(self):
        self.p = pyaudio.PyAudio()
        self.frames = []
        self.stream = None
        print('Start Recording ...')


        self.stream = self.p.open(format=self.sample_format,
                        channels=self.channels,
                        rate=self.fs,
                        frames_per_buffer=self.chunk,
                        input=True)
    def recordind(self):
        data = self.stream.read(self.chunk)
        self.frames.append(data)



    def stop_record(self):
        # Stop and close the stream
        self.stream.stop_stream()
        self.stream.close()
        # Terminate the PortAudio interface
        self.p.terminate()
        print('... Finished recording')
        # Save the recorded data as a WAV file
        wf = wave.open(self.filename, 'wb')
        wf.setnchannels(self.channels)
        wf.setsampwidth(self.p.get_sample_size(self.sample_format))
        wf.setframerate(self.fs)
        wf.writeframes(b''.join(self.frames))
        wf.close()

    # Suppression du fichier WAV
    # r = sr.Recognizer()
    # with sr.AudioFile(filename) as source:
    #     audio = r.record(source)
    #     try:
    #         data = r.recognize_google(audio, language="fr-FR")
    #         print(data)
    #     except:
    #         print("Please try again")
    #
    #
