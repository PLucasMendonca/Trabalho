import speech_recognition as sr  # pip install SpeechRecognition
import openai  # pip install openai
import os
from openai import OpenAI

# Configuração da OpenAI
client = OpenAI(
    api_key="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",
)

def generate_answer(text):
    prompt = f"A informação que estou lhe passando é um código de letras e números: {text}. Quero que interprete ele e me informe o código somente nas letras e dos números."
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content

# reconhecer
r = sr.Recognizer()
mic = sr.Microphone()

print("Reconhecimento de voz ativado com Google Speech Recognition. Fale o código...")

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
        print("Código recebido:", question)
        # Enviar para a OpenAI e obter resposta
        resposta_openai = generate_answer(question)
        print("Interpretação da OpenAI:", resposta_openai)
    else:
        print("Não foi possível entender o áudio ou nenhuma entrada foi fornecida")

    continuar = input("Deseja continuar ouvindo? (s/n): ")
    if continuar.lower() != 's':
        break

print("Programa encerrado")
