def iniciar_processo(self):
        url = "https://minha.effecti.com.br/#/proposta-minhas"
        driver.get(url)
        try:
            # Login mais rápido e direto
            email_field = wait.until(EC.presence_of_element_located((By.NAME, "input-login")))
            password_field = wait.until(EC.presence_of_element_located((By.NAME, "input-password")))
            
            # Preenche email e senha de uma vez
            email_field.send_keys("fernanda@alcantaramendes.com.br")
            password_field.send_keys("Alcantara@2025")
            
            # Clica no botão Entrar imediatamente
            entrar_button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "div.button-submit a.login-btn.l-button")))
            entrar_button.click()
            print("Login realizado com sucesso!")
            
            # Reduz o tempo de espera e já procura o botão Cadastrar Proposta
            print("Aguardando página carregar...")
            time.sleep(3)  # Aguarda a página carregar completamente
            
            # Espera o overlay desaparecer
            try:
                overlay = WebDriverWait(driver, 10).until(
                    EC.invisibility_of_element_located((By.CSS_SELECTOR, "div.overlay.fullscreen"))
                )
            except:
                print("Aviso: Overlay não encontrado ou já invisível")
            
            print("Procurando botão Cadastrar Proposta...")
            try:
                # Primeira tentativa: esperar o botão estar clicável
                cadastrar_proposta_button = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, "button.btn-new-proposal"))
                )
                cadastrar_proposta_button.click()
            except:
                try:
                    # Segunda tentativa: usar JavaScript para remover overlay e clicar
                    driver.execute_script("""
                        // Remove qualquer overlay
                        var overlays = document.querySelectorAll('div.overlay');
                        overlays.forEach(function(overlay) {
                            overlay.remove();
                        });
                        
                        // Encontra e clica no botão
                        var botao = document.querySelector('button.btn-new-proposal');
                        if(botao) {
                            botao.click();
                        }
                    """)
                except:
                    # Terceira tentativa: localizar por XPath e usar Actions
                    from selenium.webdriver.common.action_chains import ActionChains
                    button = driver.find_element(By.XPATH, "//button[contains(@class, 'btn-new-proposal')]")
                    actions = ActionChains(driver)
                    actions.move_to_element(button).click().perform()
            
            print("Iniciando cadastro de proposta...")
            
            # Fecha o popup do tour se aparecer, com tempo reduzido
            if fechar_popup_tour(driver, wait):
                print("Tour inicial fechado!")
            
            # Carrega os dados do JSON
            with open('dados.json', 'r', encoding='utf-8') as arquivo:
                dados = json.load(arquivo)
            
            # Seleciona portal e empresa em sequência rápida
            select_element = wait.until(EC.presence_of_element_located((By.ID, "sel-portal")))
            select = Select(select_element)
            
            # Mapeamento dos IDs dos portais
            portal_mapping = {
                'bll': '24',
                'comprasnet': '1',
                'compraspublicas': '3',
                'bnc': '1362',
                'comprasbr': '898',
                'licitanet': '28'
            }
            
            # Seleciona o portal
            portal_id = portal_mapping.get(dados['portal_id'])
            if portal_id:
                select.select_by_value(portal_id)
                print(f"Portal selecionado: {dados['portal_nome']}")
                
                # Seleciona a empresa Fernanda imediatamente após o portal
                empresa_select = wait.until(EC.presence_of_element_located((By.ID, "branch")))
                Select(empresa_select).select_by_value("1")
                print("Empresa selecionada!")
                
                # Mapeamento dos campos específicos por portal
                field_mapping = {
                    'bll': {
                        'bidding': 'sel-bidding',
                        'organ': 'sel-organ',
                        'quotation': 'sel-quotation'
                    },
                    'comprasnet': {
                        'bidding': 'sel-bidding',
                        'uasg': 'sel-organ',
                        'quotation': 'sel-quotation',
                        'uasg_name': 'sel-uasg-name'
                    },
                    'compraspublicas': {
                        'bidding': 'sel-bidding',
                        'organ': 'sel-organ',
                        'quotation': 'sel-quotation'
                    },
                    'bnc': {
                        'bidding': 'sel-bidding',
                        'organ': 'sel-organ',
                        'quotation': 'sel-quotation'
                    },
                    'comprasbr': {
                        'bidding': 'sel-bidding',
                        'organ': 'sel-organ',
                        'quotation': 'sel-quotation'
                    },
                    'licitanet': {
                        'bidding': 'sel-bidding',
                        'organ': 'sel-organ',
                        'quotation': 'sel-quotation'
                    }
                }
                
                # Pega os IDs corretos para o portal atual
                portal_fields = field_mapping.get(dados['portal_id'])
                
                if portal_fields:
                    fechar_popup_tour(driver, wait)
                    
                    if dados['portal_id'] == 'comprasnet':
                        try:
                            # Campo Licitação (Número da compra)
                            print("Tentando preencher campo Licitação...")
                            bidding_field = wait.until(EC.presence_of_element_located((By.ID, portal_fields['bidding'])))
                            bidding_field.click()
                            
                            # Usar valores padrão se não houver registros
                            if not dados.get('registros'):
                                print("Nenhum registro encontrado, usando valores padrão...")
                                edital_numero = '990012024'
                                uasg = '980425'
                                modalidade = 'Pregão'
                            else:
                                edital_numero = dados['registros'][-1].get('numero_compra', '990012024')
                                uasg = dados['registros'][-1].get('uasg', '980425')
                                modalidade = dados['registros'][-1].get('modalidade', 'Pregão')
                            
                            bidding_field.send_keys(str(edital_numero))
                            print(f"Campo Licitação preenchido: {edital_numero}")
                            
                            # Campo UASG
                            print("Tentando preencher campo UASG...")
                            uasg_field = wait.until(EC.presence_of_element_located((By.ID, portal_fields['uasg'])))
                            uasg_field.click()
                            uasg_field.send_keys(str(uasg))
                            print(f"Campo UASG preenchido: {uasg}")
                            
                            # Modalidade
                            print("\nTentando selecionar modalidade no portal comprasnet...")
                            select_element = wait.until(EC.presence_of_element_located((By.ID, portal_fields['quotation'])))
                            select = Select(select_element)
                            
                            # Obter todas as opções disponíveis
                            available_options = []
                            for option in select.options:
                                value = option.get_attribute('value')
                                text = option.text
                                available_options.append((value, text))
                                print(f"Opção encontrada: valor='{value}', texto='{text}'")
                            
                            # Mapear a modalidade para o valor correto
                            modalidade_id = MODALIDADE_VALUES['comprasnet'].get(modalidade)
                            print(f"Modalidade selecionada: {modalidade} (tentando usar valor: {modalidade_id})")
                            
                            if modalidade_id and any(modalidade_id == opt[0] for opt in available_options):
                                select.select_by_value(modalidade_id)
                                print(f"Modalidade selecionada com sucesso: {modalidade} (valor: {modalidade_id})")
                            else:
                                print(f"AVISO: Valor da modalidade '{modalidade}' ({modalidade_id}) não disponível.")
                                print(f"Valores disponíveis: {available_options}")
                                print("Usando valor padrão '1'")
                                select.select_by_value('1')
                        except Exception as e:
                            print(f"Erro ao preencher campos do ComprasNet: {str(e)}")
                            print("Detalhes do erro:")
                            import traceback
                            print(traceback.format_exc())
                            return
                            
                    else:
                        # Preenchimento padrão para outros portais
                        try:
                            # Campo Licitação/Edital
                            bidding_field = wait.until(EC.presence_of_element_located((By.ID, portal_fields['bidding'])))
                            bidding_field.click()
                            edital_numero = dados['registros'][-1].get('numero_edital', '')
                            bidding_field.send_keys(str(edital_numero))
                            print(f"Campo Licitação preenchido: {edital_numero}")
                            
                            # Campo Órgão
                            organ_field = wait.until(EC.presence_of_element_located((By.ID, portal_fields['organ'])))
                            organ_field.click()
                            orgao = dados['registros'][-1].get('orgao', '')
                            organ_field.send_keys(str(orgao))
                            print(f"Campo Órgão preenchido: {orgao}")
                            
                            # Modalidade
                            print("\nTentando selecionar modalidade no portal...")
                            select_element = wait.until(EC.presence_of_element_located((By.ID, portal_fields['quotation'])))
                            select = Select(select_element)
                            
                            # Obter todas as opções disponíveis
                            available_options = []
                            for option in select.options:
                                value = option.get_attribute('value')
                                text = option.text
                                available_options.append((value, text))
                                print(f"Opção encontrada: valor='{value}', texto='{text}'")
                            
                            # Mapear a modalidade para o valor correto
                            modalidade = dados['registros'][-1].get('modalidade', 'Pregão')
                            modalidade_id = MODALIDADE_VALUES[dados['portal_id']].get(modalidade)
                            print(f"Modalidade selecionada: {modalidade} (tentando usar valor: {modalidade_id})")
                            
                            if modalidade_id and any(modalidade_id == opt[0] for opt in available_options):
                                select.select_by_value(modalidade_id)
                                print(f"Modalidade selecionada com sucesso: {modalidade} (valor: {modalidade_id})")
                            else:
                                print(f"AVISO: Valor da modalidade '{modalidade}' ({modalidade_id}) não disponível.")
                                print(f"Valores disponíveis: {available_options}")
                                print("Usando valor padrão '1'")
                                select.select_by_value('1')
                            
                        except Exception as e:
                            print(f"Erro ao preencher campos: {str(e)}")
                            return
                    
                    # Carregar Itens
                    print("Clicando em Carregar Itens...")
                    carregar_itens_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Carregar Itens')]")))
                    carregar_itens_button.click()
                    print("Botão Carregar Itens clicado!")
                    
                    time.sleep(2)  # Aguarda carregamento
                    
                    # Verificar aviso
                    if verificar_aviso(driver, wait):
                        print("Aviso detectado e fechado. Continuando com a exportação...")
                        time.sleep(1)  # Pequena pausa após fechar o aviso
                    
                    # Scroll e exportação
                    print("Rolando a página...")
                    driver.execute_script("window.scrollBy(0, 300);")
                    time.sleep(1)  # Aguarda o scroll

                    # Após rolar, tenta fechar o span do tour
                    try:
                        print("Procurando botão finalizar do tour...")
                        finalizar_button = driver.find_element(By.CSS_SELECTOR, "div.popover.minha-tour.tour-tour-proposta-cadastro a[data-role='end']")
                        finalizar_button.click()
                        print("Tour fechado com sucesso!")
                        time.sleep(1)  # Aguarda o tour fechar
                    except Exception as e:
                        print(f"Aviso: Tour não encontrado após scroll - {str(e)}")
                    
                    # Exportar planilha
                    try:
                        print("Procurando botão Exportar planilha...")
                        exportar = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'button[title="Exportar planilha"]')))
                        driver.execute_script("arguments[0].click();", exportar)
                        print("Botão Exportar planilha clicado!")
                        
                        time.sleep(2)  # Aguarda modal abrir
                        
                        print("Procurando botão Exportar na modal...")
                        # Tenta diferentes seletores para o botão Exportar
                        try:
                            # Primeira tentativa - botão pela classe
                            confirmar_exportar = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "div.modal-footer button.btn-primary")))
                        except:
                            try:
                                # Segunda tentativa - botão pelo texto
                                confirmar_exportar = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Exportar')]")))
                            except:
                                # Terceira tentativa - botão pela estrutura HTML fornecida
                                confirmar_exportar = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "div[data-v-1d2d804c] button.btn.btn-primary")))
                        
                        # Tenta clicar de diferentes formas
                        try:
                            confirmar_exportar.click()
                        except:
                            try:
                                driver.execute_script("arguments[0].click();", confirmar_exportar)
                            except:
                                # Última tentativa - força o clique via JavaScript
                                driver.execute_script("""
                                    var buttons = document.querySelectorAll('button');
                                    for(var i = 0; i < buttons.length; i++) {
                                        if(buttons[i].textContent.includes('Exportar')) {
                                            buttons[i].click();
                                            break;
                                        }
                                    }
                                """)