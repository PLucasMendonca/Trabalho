import speech_recognition as sr  # pip install SpeechRecognition
import whisper  # pip install whisper-openai
import os

# reconhecer
r = sr.Recognizer()
mic = sr.Microphone()
model = whisper.load_model("base")

path = os.getcwd()
filename = "audio.wav"

print("Reconhecimento de voz ativado")

ajustar_ambiente_noise = True

while True:
    text = ""
    question = ""

    # Capturar áudio
    with mic as fonte:
        if ajustar_ambiente_noise:
            r.adjust_for_ambient_noise(fonte)
            ajustar_ambiente_noise = False
        print("Fale alguma coisa")
        audio = r.listen(fonte)
        print("Enviando para reconhecimento")

        # Escolha entre reconhecimento Google ou Whisper
        escolher_stt = input("Escolha o método de reconhecimento ('google' ou 'whisper'): ")

        if escolher_stt == "google":
            try:
                question = r.recognize_google(audio, language="pt-BR")
            except sr.UnknownValueError:
                print("Google Speech Recognition não entendeu o áudio")
            except sr.RequestError as e:
                print(f"Erro na solicitação ao Google Speech Recognition; {e}")

        elif escolher_stt == "whisper":
            with open(path + filename, "wb") as f:
                f.write(audio.get_wav_data())
            text = model.transcribe(path + filename, language='pt', fp16=False)
            question = text["text"]

    if question:
        print("Você disse:", question)
    else:
        print("Não foi possível entender o áudio ou nenhuma entrada foi fornecida")

    continuar = input("Deseja continuar? (s/n): ")
    if continuar.lower() != 's':
        break

print("Programa encerrado")
