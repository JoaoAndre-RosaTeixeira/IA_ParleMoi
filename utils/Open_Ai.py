import openai
import speech_recognition as sr



class OpenAi:

    def __init__(self, model_name, api_key):
        openai.api_key = api_key
        self.model_engine = model_name

    def transcribe_audio(self, audio_path):
        r = sr.Recognizer()
        with sr.AudioFile(audio_path) as source:
            audio_data = r.record(source)
        try:
            transcription = r.recognize_google(audio_data, language='fr-FR')
            return transcription
        except:
            return False

    def get_response(self, audio_path):
        prompt = self.transcribe_audio(audio_path)
        if prompt != False:
            print(prompt)
            # Set the maximum number of tokens to generate in the response
            max_tokens = 500

            completion = openai.Completion.create(
                engine=self.model_engine,
                prompt=prompt,
                max_tokens=max_tokens,
                temperature=0.3,
                top_p=1,
                frequency_penalty=0,
                presence_penalty=0
            )
            response = completion.choices[0].text.strip()
            print(response)
            return response
        else:
            return "Erreur : le fichier audio est vide ou corrompu"