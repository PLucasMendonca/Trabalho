import speech_recognition as sr  # pip install SpeechRecognition
from openai import OpenAI  # pip install openai
import os

# Configuração da OpenAI
api_key = "SUA_CHAVE_API_AQUI"
client = OpenAI(api_key=api_key)

def generate_answer(text):
    response = client.chat.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": text}]
    )
    return response.choices[0].message.content

# reconhecer
r = sr.Recognizer()
mic = sr.Microphone()

print("Reconhecimento de voz ativado com Google Speech Recognition. Fale alguma coisa...")

ajustar_ambiente_noise = True

while True:
    question = ""

    # Capturar áudio
    with mic as fonte:
        if ajustar_ambiente_noise:
            r.adjust_for_ambient_noise(fonte)
            ajustar_ambiente_noise = False
        audio = r.listen(fonte)
        print("Processando o áudio...")

        # Reconhecimento de voz com Google
        try:
            question = r.recognize_google(audio, language="pt-BR")
        except sr.UnknownValueError:
            print("Google Speech Recognition não entendeu o áudio")
        except sr.RequestError as e:
            print(f"Erro na solicitação ao Google Speech Recognition; {e}")

    if question:
        print("Você disse:", question)
        # Enviar para a OpenAI e obter resposta
        resposta_openai = generate_answer(question)
        print("Resposta da OpenAI:", resposta_openai)
    else:
        print("Não foi possível entender o áudio ou nenhuma entrada foi fornecida")

    continuar = input("Deseja continuar ouvindo? (s/n): ")
    if continuar.lower() != 's':
        break

print("Programa encerrado")
