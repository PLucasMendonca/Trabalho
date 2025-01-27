import speech_recognition as sr

def capturar_e_transcrever_audio():
    # Configuração do reconhecedor de voz e microfone
    r = sr.Recognizer()
    mic = sr.Microphone()

    with mic as fonte:
        # Ajusta o reconhecedor para o ruído ambiente
        r.adjust_for_ambient_noise(fonte)
        print("Por favor, fale algo...")

        # Captura o áudio
        audio = r.listen(fonte, timeout=15, phrase_time_limit=15)
        print("Processando o áudio...")

        try:
            # Reconhecimento do áudio utilizando o Google Speech Recognition
            texto_reconhecido = r.recognize_google(audio, language="en-US")
            print("Texto reconhecido: " + texto_reconhecido)
            return texto_reconhecido
        except sr.UnknownValueError:
            # Erro caso o reconhecedor não entenda o que foi dito
            print("Google Speech Recognition não entendeu o áudio.")
        except sr.RequestError as e:
            # Erro caso haja problemas com a API do Google
            print(f"Não foi possível solicitar resultados do serviço Google Speech Recognition; {e}")

        return None

