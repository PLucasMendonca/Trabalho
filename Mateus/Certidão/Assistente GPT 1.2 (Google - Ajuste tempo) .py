import speech_recognition as sr

# reconhecer
r = sr.Recognizer()
mic = sr.Microphone()

print("Reconhecimento de voz ativado com Google Speech Recognition. Fale alguma coisa...")

# Duração do ajuste para o ruído ambiente (em segundos)
ajuste_ruido_duracao = 5  # Pode aumentar se necessário

while True:
    with mic as fonte:
        # Ajustar para ruído ambiente
        if ajuste_ruido_duracao:
            r.adjust_for_ambient_noise(fonte, duration=ajuste_ruido_duracao)
            ajuste_ruido_duracao = 0  # Ajuste feito, não precisa repetir

        # Escutar o áudio
        try:
            audio = r.listen(fonte, timeout=15, phrase_time_limit=15)  # Aumente os limites conforme necessário
            print("Processando o áudio...")
            question = r.recognize_google(audio, language="pt-BR")
            print("Você disse:", question)
        except sr.UnknownValueError:
            print("Google Speech Recognition não entendeu o áudio")
        except sr.RequestError as e:
            print(f"Erro na solicitação ao Google Speech Recognition; {e}")
        except sr.WaitTimeoutError:
            print("Tempo de espera excedido, nenhum áudio detectado")

    continuar = input("Deseja continuar ouvindo? (s/n): ")
    if continuar.lower() != 's':
        break

print("Programa encerrado")
