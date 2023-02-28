import threading
from utils.create_mp3 import Mp3Record
from utils.Open_Ai import OpenAi
from flask import Flask, request, jsonify
from flask_restful import Resource, Api
from flask_cors import CORS
from gtts import gTTS
from io import BytesIO
from pygame import mixer
import pyttsx3




api_key = "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"
my_model = "text-davinci-003"
mp3recorder = Mp3Record()
openai_instance = OpenAi(my_model, api_key)




app = Flask(__name__)
cors = CORS(app, resources={r"/api/*": {"origins": "*"}})
api = Api(app)

# Variable de drapeau pour contrôler la boucle
recording_manage = False

# Fonction à exécuter en arrière-plan
def boucle_recording():
    print(recording_manage)
    while recording_manage == True:
        # Changer la variable en fonction de la logique de votre application
        mp3recorder.recordind()
    print(recording_manage)


class stop_record_f(Resource):
    def post(self):
        global recording_manage
        # Modifier la variable de drapeau pour arrêter la boucle
        recording_manage = False

        mp3recorder.stop_record()

        audio_path = "ressources/output.mp3"

        response = openai_instance.get_response(audio_path)
        self.pyttsx(response)

        # Retourner une réponse
        return jsonify({'success': 'Enregistrement arrêté avec succès',
                        'record': False,
                        'response': response
                        })


    def pyttsx(self, text_res):

        # Initialiser le moteur de synthèse vocale
        engine = pyttsx3.init()

        # Définir la voix
        voices = engine.getProperty('voices')
        engine.setProperty('voice', voices[0].id)

        # Définir la vitesse
        engine.setProperty('rate', 150)

        # Définir la hauteur
        engine.setProperty('pitch', 0)

        # Synthétiser le texte
        engine.say(text_res)

        # Attendre que la synthèse vocale soit terminée
        engine.runAndWait()
        return True

    def text_te_speech(self, text_res):
        # On crée un objet gTTS avec notre texte
        tts = gTTS(text=text_res, lang='fr')

        # On crée un objet BytesIO pour stocker le fichier audio généré
        fichier_audio = BytesIO()

        # On enregistre l'audio dans le fichier BytesIO
        tts.write_to_fp(fichier_audio)

        # On "rewind" le curseur pour lire le fichier audio à partir du début
        fichier_audio.seek(0)

        # On initialise Pygame mixer
        mixer.init()

        # On charge le fichier audio
        mixer.music.load(fichier_audio)

        # On joue le fichier audio
        mixer.music.play()

        # On attend que le fichier audio soit joué en entier
        while mixer.music.get_busy():
            pass

        # On arrête Pygame mixer
        mixer.quit()

class start_record_f(Resource):
    def post(self):
        global recording_manage
        if recording_manage == False:
            mp3recorder.start_record()
            # Modifier la variable de drapeau pour démarrer la boucle
            recording_manage = True
            # Lancer la boucle en arrière-plan
            thread = threading.Thread(target=boucle_recording)
            thread.start()
            # Retourner une réponse
            return jsonify({'success': 'Enregistrement démarré avec succès',
                            'record': True
                            })

api.add_resource(stop_record_f, '/api/stop_record')
api.add_resource(start_record_f, '/api/start_record')

if __name__ == '__main__':
    app.run(debug=True)