def fechar_popup_tour(driver, wait):
    """Função auxiliar para fechar o popup do tour se ele estiver presente"""
    try:
        # Tenta encontrar o botão de finalizar do tour
        tour_button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "a[data-role='end']")))
        if tour_button:
            tour_button.click()
            time.sleep(1)  # Pequena pausa para garantir que o popup fechou
            print("Tour finalizado com sucesso!")
        return True
    except:
        return False

def verificar_aviso(driver, wait):
    """Função para verificar se apareceu o aviso de warning e fechá-lo"""
    try:
        # Verifica se existe o título "Aviso!" e o ícone de warning
        aviso = wait.until(EC.presence_of_element_located((By.CLASS_NAME, "swal2-warning")))
        titulo = wait.until(EC.presence_of_element_located((By.ID, "swal2-title")))
        
        if aviso.is_displayed() and titulo.is_displayed() and titulo.text == "Aviso!":
            print("Aviso detectado! Tentando fechar...")
            # Tenta encontrar e clicar no botão OK
            try:
                ok_button = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "swal2-confirm")))
                ok_button.click()
                print("Aviso fechado com sucesso!")
                time.sleep(1)  # Pequena pausa após fechar o aviso
            except Exception as e:
                print(f"Erro ao fechar aviso: {str(e)}")
            return True
    except:
        pass
    return False