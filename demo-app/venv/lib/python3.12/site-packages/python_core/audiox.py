
import os
import pyttsx3
import sounddevice
from gtts import gTTS
from core.system import *
from pydub import AudioSegment
from playsound import playsound
import speech_recognition as sr
from core.pathx import *
from scipy.io.wavfile import write
from core.aesthetix import *

def playaudio(source_path):
    if type(source_path) != str:
        raise TypeError("param @absolute_path should be str.")
    
    if not is_file(source_path):
        raise ValueError("param @absolute_path is not an absolute path.")
    
    if not source_path.endswith(".wav") and not source_path.endswith(".mp3"):
        raise ValueError("param @absolute_path should end with .wav or .mp3")
    
    playsound(source_path)
    
def SaveTextToSpeech(destination, text, lang, slowmotion=False):
    if type(destination) != str:
        raise TypeError("param @destination should be type str.")
    if not destination.endswith(".mp3"):
        raise ValueError("param @destination should end with .mp3")
    
    if not os.path.isabs(destination):
        raise ValueError("param @destination should be an absolute path.")
    
    if type(text) != str:
        raise TypeError("param @text should be type str.")
    if text == "":
        raise ValueError("param @text is void-string.")
    
    if type(lang) != str:
        raise TypeError("param @lang should be type str.")
    if type(slowmotion) != bool:
        raise TypeError("param @slowmotion should be type bool.")
    
    texttospeech = gTTS(text, lang=lang, slow=slowmotion)
    texttospeech.save(destination)
    
def SaveRecodedMicrophone(destination, duration):
    if type(destination) != str:
        raise TypeError("param @destination should be type str.")
    if type(duration) != int:
        raise TypeError("param @duration should be type int.")
    
    if not os.path.isabs(destination):
        raise ValueError("param @destination should be absolute path.")
    
    if not destination.endswith(".wav"):
        raise ValueError("param @destination should end with .wav extension.")
    
    if duration <= 0:
        raise ValueError("param @duration should be bigger than 0.")
    
    try:
        sample_rate = 44100
        print("you have {} seconds to speak:".format(duration))
        print("recording...")
        
        myrecording = sounddevice.rec(int(duration * sample_rate), samplerate=sample_rate, channels=2)
        sounddevice.wait()
        
        write(destination, sample_rate, myrecording)
        
        print("recording saved to path: {}.".format(destination))
        
    except OSError as error:
        print(type(error))
        print(error)
        print("turn OFF your anti-virus application.")
        
def SpeechToText():
    """ listens to voice, if understands: return speech to text else return None."""
    
    recognizer = sr.Recognizer()
    microphone = sr.Microphone()
    
    # just in case you need micrphone list
    # microphone_list = microphone.list_microphone_names()
    # print(microphone_list)
    
    print("listening...")
    with microphone as audio:
        recognizer.adjust_for_ambient_noise(audio)
        recorded_audio = recognizer.listen(audio)
    try:
        speechtotext = recognizer.recognize_google(recorded_audio)
    except sr.UnknownValueError:
        print("your speech was incomprehensible. None was returned.")
        return None
    return speechtotext
    
def SpeakThisPYTTSX3(message, speech_speed=150):
    if type(message) != str:
        raise TypeError("param @message should be type str.")
    if message == "":
        raise ValueError("param @message shouldn't be void-string.")
    
    engine = pyttsx3.init("sapi5")
    engine.setProperty("rate", speech_speed)
    engine.setProperty("volume", 0.8)
    voices = engine.getProperty("voices")
    engine.setProperty("voice", voices[1].id)
    engine.say(message)
    engine.runAndWait()
    
def ModifyVolume(source, destination_folder, quantity=15):
    """ applicable only to .wav and .mp3 files. """
    
    if type(source) != str:
        message = ConsoleColored("param @absolute_path should be type str.", "red", bold=1)
        raise TypeError(message)
        del message
    if type(quantity) != int:
        message = ConsoleColored("param @quantity should be type int.", "red", bold=1)
        raise TypeError(message)
        del message
    
    import os
    if not os.path.isfile(source):
        message = ConsoleColored("param @absolute_path is not an absolut path.", "red", bold=1)
        raise ValueError(message)
        del message
        
    if not source.endswith(".wav") and not source.endswith("mp3"):
        message = ConsoleColored("param @absolute_path should end with .wav or .mp3.", "red", bold=1)
        raise ValueError(message)
        del message
    
    extension = get_file_extension(source)
    # print(ConsoleColored(source, "green", bold=1))
    if extension == "wav":
        audio_file = AudioSegment.from_wav(source)
    elif extension == "mp3":
        audio_file = AudioSegment.from_mp3(source)
        
    filename = get_file_name(source)
    audio_file += quantity
    if quantity < 0:
        destination = destination_folder + "\\{}_minus_{}.{}".format(filename, -quantity, extension)
    else:
        destination = destination_folder + "\\{}_plus_{}.{}".format(filename, quantity, extension)
        
    audio_file.export(destination, extension)
    return destination