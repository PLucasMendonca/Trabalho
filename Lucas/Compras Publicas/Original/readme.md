# Portal de Compras Públicas

Uma aplicação desktop em Python para automatizar e facilitar o acesso ao Portal de Compras Públicas.

## 📋 Descrição

Este projeto é uma interface gráfica que automatiza o acesso e operações no Portal de Compras Públicas, permitindo gerenciar múltiplos perfis de usuário e realizar operações comuns de forma eficiente.

## 🚀 Funcionalidades

- 👤 **Gerenciamento de Perfis**
  - Salvar múltiplos perfis de usuário
  - Suporte a perfis MEI
  - Interface intuitiva para gerenciamento de credenciais

- 🔍 **Pesquisa Avançada**
  - Interface dedicada para pesquisas
  - Histórico de pesquisas
  - Filtros personalizados

- 🌐 **Automação Web**
  - Navegação automática no portal
  - Preenchimento automático de formulários
  - Validações de segurança

- 🎨 **Interface Moderna**
  - Design responsivo
  - Suporte a temas claro/escuro
  - Feedback visual das operações

## 🗂️ Estrutura do Projeto

```
portal-compras-publicas/
├── config/                 # Configurações do projeto
│   └── settings.py        # Configurações gerais
├── core/                  # Núcleo da aplicação
│   ├── credentials.py     # Gerenciamento de credenciais
│   ├── data_manager.py    # Gerenciamento de dados
│   └── webdriver.py       # Controle do navegador
├── json/                  # Armazenamento de dados
│   ├── credentials.json   # Credenciais dos usuários
│   └── search_history.json# Histórico de pesquisas
├── UI/                    # Interfaces gráficas
│   ├── login_gui.py       # Interface de login
│   ├── portal_gui.py      # Interface principal
│   ├── pesquisa_gui.py    # Interface de pesquisa
│   └── acao_especifica_gui.py # Ações específicas
├── utils/                 # Utilitários
│   ├── logging_config.py  # Configuração de logs
│   ├── portal_validation.py # Validações do portal
│   ├── validation.py      # Validações gerais
│   └── exceptions.py      # Exceções personalizadas
└── main.py               # Ponto de entrada da aplicação
```

## 💻 Requisitos

- Python 3.8+
- customtkinter
- Selenium WebDriver
- Chrome/Firefox instalado

## 🛠️ Instalação

1. Clone o repositório:
```bash
git clone [URL_DO_REPOSITORIO]
```

2. Instale as dependências:
```bash
pip install -r requirements.txt
```

3. Execute a aplicação:
```bash
python main.py
```

## 🔧 Configuração

1. **Configurações Gerais**
   - Edite `config/settings.py` para personalizar:
     - Tema padrão
     - Atalhos de teclado
     - Configurações do WebDriver

2. **Credenciais**
   - As credenciais são salvas em `json/credentials.json`
   - Formato seguro e criptografado
   - Backup automático

## 🔐 Segurança

- Credenciais armazenadas localmente
- Validações de segurança implementadas
- Logs para auditoria
- Tratamento seguro de exceções

## 📝 Logs

O sistema mantém logs detalhados em `logs/`:
- Informações de execução
- Erros e exceções
- Ações do usuário
- Performance e métricas

## 🤝 Contribuição

1. Faça um Fork do projeto
2. Crie uma Branch para sua Feature (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. Push para a Branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request

## 📄 Licença

Este projeto está sob a licença MIT. Veja o arquivo `LICENSE` para mais detalhes.

## 👥 Autores

- **Welder** - *Desenvolvimento inicial* - [GitHub](https://github.com/welderc)

## 📞 Suporte

Para suporte, envie um email para [EMAIL] ou abra uma issue no GitHub.



Automação:

Agora e a parte do dowlond e capcha aonde vc vai ter que utilizar uma biblioteca do Buster - Captcha Solver para resolver o captcha do site da compra publica. vc vai clciar em 

BAixar edital: //*[@id="mainContent"]/div[1]/div[2]/div[2]/div[1]/div/div[2]/a

Captcha: //*[@id="rc-anchor-container"] 

campo para clicar no captcha: //*[@id="recaptcha-anchor"]/div[1]

e no final faz o download do edital: //*[@id="btGravar"]

e fecha: /html/body/div[3]/div[2]/div/div/div/div[2]/div[3]/a

. Primeiro vai analisar o código para depois implementar isso pq provavelmente vai mexer no driver de uma forma que fique 100% certo.
Faça testes

## Configuração do Buster Captcha Solver

Para que o download de editais funcione corretamente, você precisa configurar a extensão Buster Captcha Solver:

### 1. Instalar a extensão

1. Abra o Google Chrome
2. Acesse a [Chrome Web Store](https://chrome.google.com/webstore/detail/buster-captcha-solver-for/mpbjkejclgfgadiemmefgebjfooflfhl)
3. Clique em "Adicionar ao Chrome"
4. Confirme a instalação

### 2. Exportar a extensão

1. Abra uma nova aba no Chrome
2. Digite `chrome://extensions/` na barra de endereços e pressione Enter
3. No canto superior direito, ative o "Modo do desenvolvedor"
4. Localize o Buster na lista de extensões
5. Anote o ID da extensão (algo como "mpbjkejclgfgadiemmefgebjfooflfhl")
6. Vá até a pasta onde o Chrome armazena as extensões:
   - Windows: `%LOCALAPPDATA%\Google\Chrome\User Data\Default\Extensions\[ID_DA_EXTENSAO]`
7. Copie a pasta com a versão mais recente (ex: "1.2.3")
8. Clique em "Pack extension" no Chrome
9. Em "Extension root directory", selecione a pasta que você copiou
10. Clique em "Pack Extension"
11. Será gerado um arquivo .crx

### 3. Configurar no projeto

1. Renomeie o arquivo .crx gerado para `buster.crx`
2. Copie o arquivo para a pasta `extensions` do projeto
3. Verifique se o arquivo está em: `portal-compras-publicas/extensions/buster.crx`

### Notas importantes:

- O arquivo DEVE se chamar `buster.crx`
- O arquivo DEVE estar na pasta `extensions`
- Se o arquivo não estiver presente, o sistema exibirá um erro
- Em caso de problemas, verifique os logs em `logs/portal.log`

2025-01-19 16:21:34 | INFO     | core.webdriver | WebDriver iniciado com sucesso
2025-01-19 16:21:37 | INFO     | core.automation_rules | Navegando para página de login
2025-01-19 16:21:40 | INFO     | core.automation_rules | Cookies aceitos com sucesso
2025-01-19 16:21:41 | INFO     | core.automation_rules | Campo usuário preenchido com sucesso
2025-01-19 16:21:41 | INFO     | core.automation_rules | Campo senha preenchido com sucesso
2025-01-19 16:21:43 | INFO     | core.automation_rules | Botão de login clicado com sucesso
2025-01-19 16:21:44 | INFO     | core.automation_rules | Login realizado com sucesso
2025-01-19 16:21:44 | INFO     | core.automation_rules | Iniciando pesquisa do pregão 001/2024
2025-01-19 16:21:44 | INFO     | core.automation_rules | Navegando para página de pregões
2025-01-19 16:21:53 | INFO     | core.automation_rules | Total de resultados encontrados: 1
2025-01-19 16:21:53 | INFO     | core.automation_rules | Um resultado encontrado, clicando no link...
2025-01-19 16:21:55 | INFO     | core.automation_rules | Link clicado com sucesso
2025-01-19 16:22:10 | INFO     | utils.validation | Operação iniciar_automacao completada em 38.10s
2025-01-19 16:22:10 | INFO     | utils.validation | Ação iniciar_automacao completada em 39.31s ate aki foi tudo bem com a pesquisa. Agora quero que clique e faça o processo que te falei do capcha e depois baixe o edital. 

baicar edital: //*[@id="mainContent"]/div[1]/div[2]/div[2]/div[1]/div/div[2]/a

Captcha: <div id="rc-anchor-container" class="rc-anchor rc-anchor-normal rc-anchor-light"><div id="recaptcha-accessible-status" class="rc-anchor-aria-status" aria-hidden="true">reCAPTCHA requer verificação. </div><div class="rc-anchor-error-msg-container" style="display:none"><span class="rc-anchor-error-msg" aria-hidden="true"></span></div><div class="rc-anchor-content"><div class="rc-inline-block"><div class="rc-anchor-center-container"><div class="rc-anchor-center-item rc-anchor-checkbox-holder"><span class="recaptcha-checkbox goog-inline-block recaptcha-checkbox-unchecked rc-anchor-checkbox" role="checkbox" aria-checked="false" id="recaptcha-anchor" tabindex="0" dir="ltr" aria-labelledby="recaptcha-anchor-label"><div class="recaptcha-checkbox-border" role="presentation"></div><div class="recaptcha-checkbox-borderAnimation" role="presentation"></div><div class="recaptcha-checkbox-spinner" role="presentation"><div class="recaptcha-checkbox-spinner-overlay"></div></div><div class="recaptcha-checkbox-checkmark" role="presentation"></div></span></div></div></div><div class="rc-inline-block"><div class="rc-anchor-center-container"><label class="rc-anchor-center-item rc-anchor-checkbox-label" aria-hidden="true" role="presentation" id="recaptcha-anchor-label"><span aria-live="polite" aria-labelledby="recaptcha-accessible-status"></span>Não sou um robô</label></div></div></div><div class="rc-anchor-normal-footer"><div class="rc-anchor-logo-portrait" aria-hidden="true" role="presentation"><div class="rc-anchor-logo-img rc-anchor-logo-img-portrait"></div><div class="rc-anchor-logo-text">reCAPTCHA</div></div><div class="rc-anchor-pt"><a href="https://www.google.com/intl/pt-BR/policies/privacy/" target="_blank">Privacidade</a><span aria-hidden="true" role="presentation"> - </span><a href="https://www.google.com/intl/pt-BR/policies/terms/" target="_blank">Termos</a></div></div></div>

campo para clicar no captcha: //*[@id="recaptcha-anchor"]/div[1]

e no final faz o download do edital: //*[@id="btGravar"]

e fecha: /html/body/div[3]/div[2]/div/div/div/div[2]/div[3]/a


Nessa parte: 2025-01-19 16:58:49 | INFO     | core.automation_rules | Clicando no botão de baixar edital
2025-01-19 16:58:50 | INFO     | core.automation_rules | Aguardando iframe do captcha  vc vai clicar aki: //*[@id="recaptcha-anchor"]/div[1]
se preferir esse:<div class="recaptcha-checkbox-border" role="presentation"></div>
ou esse: /html/body/div[2]/div[3]/div[1]/div/div/span/div[2]. o hmllt está assim: <span class="recaptcha-checkbox goog-inline-block recaptcha-checkbox-unchecked rc-anchor-checkbox" role="checkbox" aria-checked="false" id="recaptcha-anchor" tabindex="0" dir="ltr" aria-labelledby="recaptcha-anchor-label"><div class="recaptcha-checkbox-border" role="presentation"></div><div class="recaptcha-checkbox-borderAnimation" role="presentation"></div><div class="recaptcha-checkbox-spinner" role="presentation"><div class="recaptcha-checkbox-spinner-overlay"></div></div><div class="recaptcha-checkbox-checkmark" role="presentation"></div></span>


5-01-19 17:05:19 | INFO     | core.automation_rules | Iniciando download do edital
2025-01-19 17:05:19 | INFO     | core.automation_rules | Localizando botão de baixar edital
2025-01-19 17:05:19 | INFO     | core.automation_rules | Clicando no botão de baixar edital
2025-01-19 17:05:20 | INFO     | core.automation_rules | Aguardando iframe do captcha
2025-01-19 17:05:31 | ERROR    | core.automation_rules | Erro ao baixar edital: Message: 
Stacktrace:
        GetHandleVerifier [0x007E0A13+25091]
        (No symbol) [0x0076A584]
        (No symbol) [0x0064B3B3]
        (No symbol) [0x0068F4A0]
        (No symbol) [0x0068F61B]
        (No symbol) [0x006CD882]
        (No symbol) [0x006B1EF4]
        (No symbol) [0x006CB43E]
        (No symbol) [0x006B1C46]
        (No symbol) [0x00683175]
        (No symbol) [0x006842FD]
        GetHandleVerifier [0x00AD6493+3128451]
        GetHandleVerifier [0x00AE994B+3207483]
        GetHandleVerifier [0x00AE45F2+3186146]
        GetHandleVerifier [0x008770C0+641200]
        (No symbol) [0x007736BD]
        (No symbol) [0x00770738]
        (No symbol) [0x007708D6]
        (No symbol) [0x00763040]
        BaseThreadInitThunk [0x77A5FCC9+25]
        RtlGetAppContainerNamedObjectPath [0x77E7809E+286]
        RtlGetAppContainerNamedObjectPath [0x77E7806E+238]

2025-01-19 17:05:31 | ERROR    | core.automation_rules | Erro ao baixar edital

o html completo: <div class="pp_pic_holder pp_default" style="top: 910px; left: 547.5px; display: block; width: 792px;"> 						<div class="pp_top"> 							<div class="pp_left"></div> 							<div class="pp_middle"></div> 							<div class="pp_right"></div> 						</div> 						<div class="pp_content_container"> 							<div class="pp_left"> 							<div class="pp_right"> 								<div class="pp_content" style="height: 535px; width: 752px;"> 									<div class="pp_loaderIcon" style="display: none;"></div> 									<div class="pp_fade" style="display: block;"> 										<a href="#" class="pp_expand" title="Expand the image" style="display: none;">Expand</a> 										<div class="pp_hoverContainer" style="height: 415px; width: 752px; display: none;"> 											<a class="pp_next" href="#">next</a> 											<a class="pp_previous" href="#">previous</a> 										</div> 										<div id="pp_full_res"><iframe src="/4/Pregoes/Download/Arquivo/?ttCD_CHAVE=1532&amp;slCD_ORIGEM=357875&amp;ttVoltar=0" width="752" height="500" frameborder="no" data-lf-form-tracking-inspected-jmvz8gzal6ma2pod="true" data-lf-yt-playback-inspected-jmvz8gzal6ma2pod="true" data-lf-vimeo-playback-inspected-jmvz8gzal6ma2pod="true"></iframe></div> 										<div class="pp_details clearfix" style="width: 752px;"> 											<div class="ppt" style="opacity: 1; display: block; width: 752px;">&nbsp;</div> 											<p class="pp_description" style="display: block;">Baixar Edital</p> 											<a class="pp_close" href="#">Close</a> 											<div class="pp_nav" style="display: none;"> 												<a href="#" class="pp_arrow_previous">Previous</a> 												<p class="currentTextHolder">1/1</p> 												<a href="#" class="pp_arrow_next">Next</a> 											</div> 										</div> 									</div> 								</div> 							</div> 							</div> 						</div> 						<div class="pp_bottom"> 							<div class="pp_left"></div> 							<div class="pp_middle"></div> 							<div class="pp_right"></div> 						</div> 					</div>



2025-01-19 17:36:52 | INFO     | core.automation_rules | Cookies aceitos com sucesso
2025-01-19 17:36:53 | INFO     | core.automation_rules | Campo usuário preenchido com sucesso
2025-01-19 17:36:53 | INFO     | core.automation_rules | Campo senha preenchido com sucesso
2025-01-19 17:36:55 | INFO     | core.automation_rules | Botão de login clicado com sucesso
2025-01-19 17:36:56 | INFO     | core.automation_rules | Login realizado com sucesso
2025-01-19 17:36:56 | INFO     | core.automation_rules | Iniciando pesquisa do pregão 001/2024
2025-01-19 17:36:56 | INFO     | core.automation_rules | Navegando para página de pregões
2025-01-19 17:36:59 | INFO     | core.automation_rules | Aguardando carregamento da página...
2025-01-19 17:37:29 | ERROR    | core.automation_rules | Erro ao pesquisar pregão: Message: 
Stacktrace:
        GetHandleVerifier [0x00390A13+25091]
        (No symbol) [0x0031A584]
        (No symbol) [0x001FB3B3]
        (No symbol) [0x0023F4A0]
        (No symbol) [0x0023F61B]
        (No symbol) [0x0027D882]
        (No symbol) [0x00261EF4]
        (No symbol) [0x0027B43E]
        (No symbol) [0x00261C46]
        (No symbol) [0x00233175]
        (No symbol) [0x002342FD]
        GetHandleVerifier [0x00686493+3128451]
        GetHandleVerifier [0x0069994B+3207483]
        GetHandleVerifier [0x006945F2+3186146]
        GetHandleVerifier [0x004270C0+641200]
        (No symbol) [0x003236BD]
        (No symbol) [0x00320738]
        (No symbol) [0x003208D6]
        (No symbol) [0x00313040]
        BaseThreadInitThunk [0x77A5FCC9+25]
        RtlGetAppContainerNamedObjectPath [0x77E7809E+286]
        RtlGetAppContainerNamedObjectPath [0x77E7806E+238]

2025-01-19 17:37:29 | ERROR    | UI.portal_gui | Erro ao iniciar automação: Erro ao pesquisar pregão. Cara antes vc passava nisso dboa deve ter tirado algo que agora não funciona mais vou mostra aonde ta cada campo dnvovo. 

Processo: //*[@id="ttBusca"]
Abertura: //*[@id="ttAbertura"]
UF que é um option: <select name="slCD_UF" id="slCD_UF" class="selectDefault width220">
										<option value=""></option>
										<option value="100112">AC</option>
										<option value="100127">AL</option>
										<option value="100113">AM</option>
										<option value="100116">AP</option>
										<option value="100129">BA</option>
										<option value="100123">CE</option>
										<option value="100153">DF</option>
										<option value="100132">ES</option>
										<option value="100152">GO</option>
										<option value="100121">MA</option>
										<option value="100131">MG</option>
										<option value="100150">MS</option>
										<option value="100151">MT</option>
										<option value="100115">PA</option>
										<option value="100125">PB</option>
										<option value="100126">PE</option>
										<option value="100122">PI</option>
										<option value="100141">PR</option>
										<option value="100133">RJ</option>
										<option value="100124">RN</option>
										<option value="100111">RO</option>
										<option value="100114">RR</option>
										<option value="100143">RS</option>
										<option value="100142">SC</option>
										<option value="100128">SE</option>
										<option value="100135">SP</option>
										<option value="100117">TO</option>
									</select>


Orgão: //*[@id="ttOrgao"]

botão de busca: //*[@id="defaultForm2"]/div[15]/input

total de registro: <p class="resultCounter">| Total de Registros: <b>265.938</b></p>

Visualizar registro(pregão): //*[@id="searchTableSorter"]/tbody/tr[1]/td[7]/a

em abertura deu isso: o hmtl "<input class="inputData width220  hasDatepicker" type="text" id="ttAbertura" name="ttAbertura" value="" maxlength="10">" o js é esse: document.querySelector("#ttAbertura")


o de registrar proposta é esse: //*[@id="mainContent"]/div[1]/div[2]/div[3]/a[1]

Erro: 2025-01-19 17:50:08 | INFO     | core.automation_rules | Localizando botão de registrar proposta
2025-01-19 17:50:08 | INFO     | core.automation_rules | Clicando no botão de registrar proposta
2025-01-19 17:50:09 | ERROR    | core.automation_rules | Erro ao registrar proposta: Message: stale element reference: stale element not found
  (Session info: chrome=132.0.6834.83); For documentation on this error, please visit: https://www.selenium.dev/documentation/webdriver/troubleshooting/errors#stale-element-reference-exception
Stacktrace:
        GetHandleVerifier [0x01120A13+25091]
        (No symbol) [0x010AA584]
        (No symbol) [0x00F8B3B3]
        (No symbol) [0x00F9ACA9]
        (No symbol) [0x00F99D75]
        (No symbol) [0x00F91723]
        (No symbol) [0x00F91803]
        (No symbol) [0x00F8FAD6]
        (No symbol) [0x00F92F64]
        (No symbol) [0x0100C1A7]
        (No symbol) [0x00FF1EAC]
        (No symbol) [0x0100B43E]
        (No symbol) [0x00FF1C46]
        (No symbol) [0x00FC3175]
        (No symbol) [0x00FC42FD]
        GetHandleVerifier [0x01416493+3128451]
        GetHandleVerifier [0x0142994B+3207483]
        GetHandleVerifier [0x014245F2+3186146]
        GetHandleVerifier [0x011B70C0+641200]
        (No symbol) [0x010B36BD]
        (No symbol) [0x010B0738]
        (No symbol) [0x010B08D6]
        (No symbol) [0x010A3040]
        BaseThreadInitThunk [0x77A5FCC9+25]
        RtlGetAppContainerNamedObjectPath [0x77E7809E+286]
        RtlGetAppContainerNamedObjectPath [0x77E7806E+238]

2025-01-19 17:50:09 | ERROR    | core.automation_rules | Erro ao registrar proposta
2025-01-19 17:50:09 | ERROR    | UI.portal_gui | Erro ao iniciar automação: Erro ao pesquisar pregão
2025-01-19 17:50:19 | INFO     | utils.validation | Operação iniciar_automacao completada em 49.73s
2025-01-19 17:50:19 | INFO     | utils.validation | Ação iniciar_automacao completada em 50.94s


Agora nessa parte de registrar proposta vc vai: clicar aki: //*[@id="GrupoDeclaracoes"]/a Padão tem em todas.

ai vai ter as checkbox aonde vai selecionar todas: //*[@id="defaultForm"]/div[1]
ou HTML: <div class="FB100">
								<div class="formLeftBlock FB100">
									<div class="checkField">
										<fieldset class="checkBoxIMG">
											<input type="checkbox" name="ckDeclaracao1368" id="checkIt1368">
											<label for="checkIt"></label>
										</fieldset>
										<p class="formText"><b>Declaro que estou ciente e concordo com as condições contidas no edital e seus anexos, bem como de que cumpro plenamente os requisitos de habilitação definidos no edital.</b></p>
									</div>
									<div class="clearBlock"></div>
								</div>
								<div class="formLeftBlock FB100">
									<div class="checkField">
										<fieldset class="checkBoxIMG">
											<input type="checkbox" name="ckDeclaracao1369" id="checkIt1369">
											<label for="checkIt"></label>
										</fieldset>
										<p class="formText"><b>Declaro cumprir as exigências de reserva de cargos para pessoa com deficiência e para reabilitado da Previdência Social, previstas em lei e em outras normas específicas.</b></p>
									</div>
									<div class="clearBlock"></div>
								</div>
								<div class="formLeftBlock FB100">
									<div class="checkField">
										<fieldset class="checkBoxIMG">
											<input type="checkbox" name="ckDeclaracao1370" id="checkIt1370">
											<label for="checkIt"></label>
										</fieldset>
										<p class="formText"><b>Sob pena de desclassificação, declaro que minhas propostas econômicas compreendem a integralidade dos custos para atendimento dos direitos trabalhistas assegurados na Constituição Federal, nas leis trabalhistas, nas normas infralegais, nas convenções coletivas de trabalho e nos termos de ajustamento de conduta vigentes na data de entrega das propostas.</b></p>
									</div>
									<div class="clearBlock"></div>
								</div>
								<div class="formLeftBlock FB100">
									<div class="checkField">
										<fieldset class="checkBoxIMG">
											<input type="checkbox" name="ckDeclaracao1371" id="checkIt1371">
											<label for="checkIt"></label>
										</fieldset>
										<p class="formText"><b>Declaro para fins do inciso XXXIII do artigo 7° da Constituição Federal, com redação dada pela Emenda Constitucional, nº 20/98, que não emprega menores de dezoito anos em trabalho noturno, perigoso ou insalubre e de que qualquer trabalho a menores de 16 anos.</b></p>
									</div>
									<div class="clearBlock"></div>
								</div>
								<div class="formLeftBlock FB100">
									<div class="checkField">
										<fieldset class="checkBoxIMG">
											<input type="checkbox" name="ckDeclaracao1372" id="checkIt1372">
											<label for="checkIt"></label>
										</fieldset>
										<p class="formText"><b>Declaro não possuir em sua cadeia produtiva, empregados executando trabalho degradante ou forçado, nos termos do inciso III e IV do art.1º e no inciso III do art.5º da Constituição Federal.</b></p>
									</div>
									<div class="clearBlock"></div>
								</div>
								<div class="formLeftBlock FB100">
									<div class="checkField">
										<fieldset class="checkBoxIMG">
											<input type="checkbox" name="ckDeclaracao1373" id="checkIt1373">
											<label for="checkIt"></label>
										</fieldset>
										<p class="formText"><b>Declaro que, conforme disposto no art. 93 da Lei nº 8.213, de 24 de julho de 1991, estou ciente do cumprimento da reserva de cargos prevista em lei para pessoa com deficiência ou para reabilitado da Previdência Social e que, se aplicado ao número de funcionários da minha empresa, atendo às regras de acessibilidade previstas na legislação.</b></p>
									</div>
									<div class="clearBlock"></div>
								</div>
								<div class="formLeftBlock FB100">
									<div class="checkField">
										<fieldset class="checkBoxIMG">
											<input type="checkbox" name="ckDeclaracao1374" id="checkIt1374">
											<label for="checkIt"></label>
										</fieldset>
										<p class="formText"><b>Declaro sob as penas da lei, que até a presente data inexistem fatos impeditivos para sua habilitação no presente processo licitatório, ciente da obrigatoriedade de declarar ocorrências posteriores.</b></p>
									</div>
									<div class="clearBlock"></div>
								</div>
									</div>

ou js: document.querySelector("#defaultForm > div:nth-child(4)")

dps vai Faalr se e mei ou não caso mei sim. caso não mei não aonde o arquivo ta localidado em @credentials.json. Ex: "usuario_mei": "não" marca o radio como não. Ex: "usuario_mei": "sim" marca o radio como sim.

e dps como padrão validade da proposta coloca 120: //*[@id="ttPRAZO_VALIDADE"]

por Vai salar Declarações: //*[@id="defaultForm"]/div[5]/input


2025-01-19 18:09:00 | INFO     | core.automation_rules | Marcando todas as declarações...
2025-01-19 18:09:03 | INFO     | core.automation_rules | Carregando configurações do usuário...
2025-01-19 18:09:03 | INFO     | core.automation_rules | Selecionando opção MEI: Não
2025-01-19 18:09:14 | ERROR    | core.automation_rules | Erro ao configurar MEI: Message: 
Stacktrace:
        GetHandleVerifier [0x00CC0A13+25091]
        (No symbol) [0x00C4A584]
        (No symbol) [0x00B2B3B3]
        (No symbol) [0x00B6F4A0]
        (No symbol) [0x00B6F61B]
        (No symbol) [0x00BAD882]
        (No symbol) [0x00B91EF4]
        (No symbol) [0x00BAB43E]
        (No symbol) [0x00B91C46]
        (No symbol) [0x00B63175]
        (No symbol) [0x00B642FD]
        GetHandleVerifier [0x00FB6493+3128451]
        GetHandleVerifier [0x00FC994B+3207483]
        GetHandleVerifier [0x00FC45F2+3186146]
        GetHandleVerifier [0x00D570C0+641200]
        (No symbol) [0x00C536BD]
        (No symbol) [0x00C50738]
        (No symbol) [0x00C508D6]
        (No symbol) [0x00C43040]
        BaseThreadInitThunk [0x77A5FCC9+25]
        RtlGetAppContainerNamedObjectPath [0x77E7809E+286]
        RtlGetAppContainerNamedObjectPath [0x77E7806E+238]

        o radio tá aki <div class="FB100 radioGroup">
								<p class="formText"><b>Declaro, sob as penas da Lei, que não ultrapassei o limite de faturamento e cumpro os requisitos estabelecidos no Art. 3º da Lei Complementar nº 123, de 14 de dezembro de 2006, sendo apto a usufruir do tratamento favorecido estabelecido nos artigos 42 ao 49 da referida Lei Complementar.</b></p>
								<div class="formLeftBlock FB25">
									<div class="radioField">
										<fieldset class="radioButtonIMG">
											<input type="radio" name="ttCD_BOLEANO_D_EPP" value="1" id="radioIt1">
											<label for="radioIt1"></label>
										</fieldset>
										<span class="formLabel">Sim</span>
									</div>
									<div class="clearBlock"></div>
								</div>
								<div class="formLeftBlock FB25">
									<div class="radioField">
										<fieldset class="radioButtonIMG">
											<input type="radio" name="ttCD_BOLEANO_D_EPP" value="2" id="radioIt2">
											<label for="radioIt2"></label>
										</fieldset>
										<span class="formLabel">Não</span>
									</div>
									<div class="clearBlock"></div>
								</div>
							</div>


2025-01-19 18:13:34 | INFO     | core.automation_rules | Carregando configurações do usuário...
2025-01-19 18:13:34 | INFO     | core.automation_rules | Selecionando opção MEI: Não
2025-01-19 18:13:34 | INFO     | core.automation_rules | Clicando no radio button Não
2025-01-19 18:13:35 | INFO     | core.automation_rules | Preenchendo validade da proposta...
2025-01-19 18:13:35 | ERROR    | core.automation_rules | Erro ao registrar proposta: Message: element not interactable
  (Session info: chrome=132.0.6834.83)
Stacktrace:
        GetHandleVerifier [0x006F0A13+25091]
        (No symbol) [0x0067A584]
        (No symbol) [0x0055B229]
        (No symbol) [0x00596D43]
        (No symbol) [0x005C1EAC]
        (No symbol) [0x00594DE4]
        (No symbol) [0x005C2144]
        (No symbol) [0x005DB43E]
        (No symbol) [0x005C1C46]
        (No symbol) [0x00593175]
        (No symbol) [0x005942FD]
        GetHandleVerifier [0x009E6493+3128451]
        GetHandleVerifier [0x009F994B+3207483]
        GetHandleVerifier [0x009F45F2+3186146]
        GetHandleVerifier [0x007870C0+641200]
        (No symbol) [0x006836BD]
        (No symbol) [0x00680738]
        (No symbol) [0x006808D6]
        (No symbol) [0x00673040]
        BaseThreadInitThunk [0x77A5FCC9+25]
        RtlGetAppContainerNamedObjectPath [0x77E7809E+286]
        RtlGetAppContainerNamedObjectPath [0x77E7806E+238]

2025-01-19 18:13:35 | ERROR    | core.automation_rules | Erro ao registrar proposta

o da validade vai ser: //*[@id="ttPRAZO_VALIDADE"]
NÃO FOI TENA ESSE: <input class="inputDefault width140 required" type="text" id="ttPRAZO_VALIDADE" name="ttPRAZO_VALIDADE" value="0" maxlength="3">

ACHO QUE JA SEI O PQ  ELE TEM QEU CLICAR NMA GUIA DE DECLARAÇÕES DNOVO PARA PODER COLOCAR NO CAMPO : //*[@id="GrupoDeclaracoes"]/a  AI VAI APARECER O CAMPO PARA PREECHER faz isso com as demais qeu irei falar futuramente.

agora vai ter o Informações complementares que tem como padrão essas duas. o restante e o acaso que vou te explicar dps mas por padrão todso tem o Declarações e informações complementares.

//*[@id="GrupoComplementar"]/a nele vc não precisa clicar e só para vc ficar cinte ele abre sozinho dentro vc vai marcar todso os radios como sim  emacar em salvat informações.

//*[@id="GrupoComplementar"]/div/form/div[7]/input

<form method="POST" action="/4/Pregoes/RegistroProposta/CriteriosDesempate/" name="defaultForm" class="formSubscribe">
							<input type="hidden" id="ttCD_CHAVE" name="ttCD_CHAVE" value="357875">
<p class="formText"><b>Em igualdade de condições, se não houver desempate, será assegurada preferência, sucessivamente, aos bens e serviços produzidos ou prestados em decorrência das declarações abaixo. Assinale as que se adequem à sua empresa:</b></p>
<h3 class="h3TitleBlue divisor"></h3>
							<div class="FB100 radioGroup formLeftBlock">
								<p class="formText">Declaro para os devidos fins legais, realizar ações de equidade entre homens e mulheres.</p>
								<div class="formLeftBlock FB25">
									<div class="radioField">
										<fieldset class="radioButtonIMG">
											<input type="radio" name="rd-desempate-2" value="1" id="checkIt2-1">
											<label for="radioIt1"></label>
										</fieldset>
										<span class="formLabel">Sim</span>
									</div>
									<div class="clearBlock"></div>
								</div>
								<div class="formLeftBlock FB25" style="margin-right: 0px;">
									<div class="radioField">
										<fieldset class="radioButtonIMG">
											<input type="radio" name="rd-desempate-2" value="2" id="checkIt2-2">
											<label for="radioIt2"></label>
										</fieldset>
										<span class="formLabel">Não</span>
									</div>
									<div class="clearBlock"></div>
								</div>
							</div>
							<div class="FB100 radioGroup formLeftBlock">
								<p class="formText">Declaro para os devidos fins legais, realizar ações de integridade, conforme orientações dos órgãos de controle.</p>
								<div class="formLeftBlock FB25">
									<div class="radioField">
										<fieldset class="radioButtonIMG">
											<input type="radio" name="rd-desempate-3" value="1" id="checkIt3-1">
											<label for="radioIt1"></label>
										</fieldset>
										<span class="formLabel">Sim</span>
									</div>
									<div class="clearBlock"></div>
								</div>
								<div class="formLeftBlock FB25">
									<div class="radioField">
										<fieldset class="radioButtonIMG">
											<input type="radio" name="rd-desempate-3" value="2" id="checkIt3-2">
											<label for="radioIt2"></label>
										</fieldset>
										<span class="formLabel">Não</span>
									</div>
									<div class="clearBlock"></div>
								</div>
							</div>
							<div class="FB100 radioGroup formLeftBlock">
								<p class="formText">Empresa estabelecida no território do Estado ou do Distrito Federal do órgão ou entidade da Administração Pública estadual ou distrital licitante ou, no caso de licitação realizada por órgão ou entidade de Município, no território do Estado em que este se localize.</p>
								<div class="formLeftBlock FB25">
									<div class="radioField">
										<fieldset class="radioButtonIMG">
											<input type="radio" name="rd-desempate-4" value="1" id="checkIt4-1">
											<label for="radioIt1"></label>
										</fieldset>
										<span class="formLabel">Sim</span>
									</div>
									<div class="clearBlock"></div>
								</div>
								<div class="formLeftBlock FB25" style="margin-right: 0px;">
									<div class="radioField">
										<fieldset class="radioButtonIMG">
											<input type="radio" name="rd-desempate-4" value="2" id="checkIt4-2">
											<label for="radioIt2"></label>
										</fieldset>
										<span class="formLabel">Não</span>
									</div>
									<div class="clearBlock"></div>
								</div>
							</div>
							<div class="FB100 radioGroup formLeftBlock">
								<p class="formText">Empresa brasileira.</p>
								<div class="formLeftBlock FB25">
									<div class="radioField">
										<fieldset class="radioButtonIMG">
											<input type="radio" name="rd-desempate-5" value="1" id="checkIt5-1">
											<label for="radioIt1"></label>
										</fieldset>
										<span class="formLabel">Sim</span>
									</div>
									<div class="clearBlock"></div>
								</div>
								<div class="formLeftBlock FB25">
									<div class="radioField">
										<fieldset class="radioButtonIMG">
											<input type="radio" name="rd-desempate-5" value="2" id="checkIt5-2">
											<label for="radioIt2"></label>
										</fieldset>
										<span class="formLabel">Não</span>
									</div>
									<div class="clearBlock"></div>
								</div>
							</div>
							<div class="FB100 radioGroup formLeftBlock">
								<p class="formText">Empresa que investe em pesquisa e no desenvolvimento de tecnologia no País.</p>
								<div class="formLeftBlock FB25">
									<div class="radioField">
										<fieldset class="radioButtonIMG">
											<input type="radio" name="rd-desempate-6" value="1" id="checkIt6-1">
											<label for="radioIt1"></label>
										</fieldset>
										<span class="formLabel">Sim</span>
									</div>
									<div class="clearBlock"></div>
								</div>
								<div class="formLeftBlock FB25" style="margin-right: 0px;">
									<div class="radioField">
										<fieldset class="radioButtonIMG">
											<input type="radio" name="rd-desempate-6" value="2" id="checkIt6-2">
											<label for="radioIt2"></label>
										</fieldset>
										<span class="formLabel">Não</span>
									</div>
									<div class="clearBlock"></div>
								</div>
							</div>
							<div class="FB100 radioGroup formLeftBlock">
								<p class="formText">Empresa capaz de comprovar a prática de mitigação, nos termos da Lei nº 12.187, de 29 de dezembro de 2009.</p>
								<div class="formLeftBlock FB25">
									<div class="radioField">
										<fieldset class="radioButtonIMG">
											<input type="radio" name="rd-desempate-7" value="1" id="checkIt7-1">
											<label for="radioIt1"></label>
										</fieldset>
										<span class="formLabel">Sim</span>
									</div>
									<div class="clearBlock"></div>
								</div>
								<div class="formLeftBlock FB25">
									<div class="radioField">
										<fieldset class="radioButtonIMG">
											<input type="radio" name="rd-desempate-7" value="2" id="checkIt7-2">
											<label for="radioIt2"></label>
										</fieldset>
										<span class="formLabel">Não</span>
									</div>
									<div class="clearBlock"></div>
								</div>
							</div>
								<div class="formLeftBlock FB100">
									<input type="submit" value="Salvar Informações" name="btGravar" class="buttonDefault btnGravar">
								</div>
							</form>


              2025-01-19 18:41:45 | INFO     | core.automation_rules | Carregando configurações do usuário...
2025-01-19 18:41:45 | INFO     | core.automation_rules | Selecionando opção MEI: Não
2025-01-19 18:41:45 | INFO     | core.automation_rules | Preenchendo validade da proposta...
2025-01-19 18:41:45 | INFO     | core.automation_rules | Clicando na guia de declarações...
2025-01-19 18:41:47 | WARNING  | core.automation_rules | Erro ao preencher com JavaScript: Message: element not interactable
  (Session info: chrome=132.0.6834.83)
Stacktrace:
        GetHandleVerifier [0x00610A13+25091]
        (No symbol) [0x0059A584]
        (No symbol) [0x0047B229]
        (No symbol) [0x004B6D43]
        (No symbol) [0x004E1EAC]
        (No symbol) [0x004B4DE4]
        (No symbol) [0x004E2144]
        (No symbol) [0x004FB43E]
        (No symbol) [0x004E1C46]
        (No symbol) [0x004B3175]
        (No symbol) [0x004B42FD]
        GetHandleVerifier [0x00906493+3128451]
        GetHandleVerifier [0x0091994B+3207483]
        GetHandleVerifier [0x009145F2+3186146]
        GetHandleVerifier [0x006A70C0+641200]
        (No symbol) [0x005A36BD]
        (No symbol) [0x005A0738]
        (No symbol) [0x005A08D6]
        (No symbol) [0x00593040]
        BaseThreadInitThunk [0x77A5FCC9+25]
        RtlGetAppContainerNamedObjectPath [0x77E7809E+286]
        RtlGetAppContainerNamedObjectPath [0x77E7806E+238]

2025-01-19 18:41:47 | ERROR    | core.automation_rules | Erro ao preencher com send_keys: Message: element not interactable
  (Session info: chrome=132.0.6834.83)
Stacktrace:
        GetHandleVerifier [0x00610A13+25091]
        (No symbol) [0x0059A584]
        (No symbol) [0x0047B229]
        (No symbol) [0x004BA159]
        (No symbol) [0x004B8876]
        (No symbol) [0x004E1EAC]
        (No symbol) [0x004B4DE4]
        (No symbol) [0x004E2144]
        (No symbol) [0x004FB43E]
        (No symbol) [0x004E1C46]
        (No symbol) [0x004B3175]
        (No symbol) [0x004B42FD]
        GetHandleVerifier [0x00906493+3128451]
        GetHandleVerifier [0x0091994B+3207483]
        GetHandleVerifier [0x009145F2+3186146]
        GetHandleVerifier [0x006A70C0+641200]
        (No symbol) [0x005A36BD]
        (No symbol) [0x005A0738]
        (No symbol) [0x005A08D6]
        (No symbol) [0x00593040]
        BaseThreadInitThunk [0x77A5FCC9+25]
        RtlGetAppContainerNamedObjectPath [0x77E7809E+286]
        RtlGetAppContainerNamedObjectPath [0x77E7806E+238]

2025-01-19 18:41:47 | ERROR    | core.automation_rules | Erro ao preencher validade da proposta: Message: element not interactable
  (Session info: chrome=132.0.6834.83)
Stacktrace:
        GetHandleVerifier [0x00610A13+25091]
        (No symbol) [0x0059A584]
        (No symbol) [0x0047B229]
        (No symbol) [0x004BA159]
        (No symbol) [0x004B8876]
        (No symbol) [0x004E1EAC]
        (No symbol) [0x004B4DE4]
        (No symbol) [0x004E2144]
        (No symbol) [0x004FB43E]
        (No symbol) [0x004E1C46]
        (No symbol) [0x004B3175]
        (No symbol) [0x004B42FD]
        GetHandleVerifier [0x00906493+3128451]
        GetHandleVerifier [0x0091994B+3207483]
        GetHandleVerifier [0x009145F2+3186146]
        GetHandleVerifier [0x006A70C0+641200]
        (No symbol) [0x005A36BD]
        (No symbol) [0x005A0738]
        (No symbol) [0x005A08D6]
        (No symbol) [0x00593040]
        BaseThreadInitThunk [0x77A5FCC9+25]
        RtlGetAppContainerNamedObjectPath [0x77E7809E+286]
        RtlGetAppContainerNamedObjectPath [0x77E7806E+238]

2025-01-19 18:41:47 | ERROR    | core.automation_rules | Erro ao registrar proposta
2025-01-19 18:41:47 | ERROR    | UI.portal_gui | Erro ao iniciar automação: Erro ao pesquisar pregão
2025-01-19 18:41:52 | INFO     | utils.validation | Operação iniciar_automacao completada em 55.02s
2025-01-19 18:41:52 | INFO     | utils.validation | Ação iniciar_automacao completada em 56.20s


acho que deu erro pq ja tinha tudo marcado e preechido ele deu erro mas caso isso ocorra faça a fereficação nesse e nos procimos se já está preechido os campos.


Ficou perfeito! apenas fala clicar em salvar para da tudo certo. 2025-01-19 18:45:50 | INFO     | core.automation_rules | Preenchendo validade da proposta...
2025-01-19 18:45:50 | INFO     | core.automation_rules | Clicando na guia de declarações...
2025-01-19 18:45:51 | INFO     | core.automation_rules | Campo de validade já está preenchido com 120
2025-01-19 18:45:51 | INFO     | core.automation_rules | Preenchendo informações complementares...
2025-01-19 18:45:51 | INFO     | core.automation_rules | Marcando radio button checkIt2-1
2025-01-19 18:45:52 | INFO     | core.automation_rules | Marcando radio button checkIt3-1
2025-01-19 18:45:52 | INFO     | core.automation_rules | Marcando radio button checkIt4-1
2025-01-19 18:45:53 | INFO     | core.automation_rules | Marcando radio button checkIt5-1
2025-01-19 18:45:53 | INFO     | core.automation_rules | Marcando radio button checkIt6-1
2025-01-19 18:45:54 | INFO     | core.automation_rules | Marcando radio button checkIt7-1
2025-01-19 18:45:55 | INFO     | core.automation_rules | Todos os radio buttons já estão marcados como 'Sim', não é necessário salvar
2025-01-19 18:45:55 | INFO     | core.automation_rules | Salvando declarações...
2025-01-19 18:46:05 | ERROR    | core.automation_rules | Erro ao registrar proposta: Message: 

//*[@id="GrupoComplementar"]/div/form/div[7]/input


Em declarações: //*[@id="GrupoDeclaracoes"]/a so clica nele se não paracer os checkbox ai clica nele. mas caso apareça já os checkbox Esse é o html que tem que tem que ter: <form id="defaultForm" action="/4/Pregoes/RegistroProposta/" method="post" name="defaultForm" class="formSubscribe">
							<input type="hidden" id="ttCD_CHAVE" name="ttCD_CHAVE" value="348094">
							<input type="hidden" id="ttPASSO" name="ttPASSO" value="2">
							<input type="hidden" id="slCD_TIPO_PARTICIPACAO" name="slCD_TIPO_PARTICIPACAO" value="">
									<div class="FB100">
								<div class="formLeftBlock FB100">
									<div class="checkField">
										<fieldset class="checkBoxIMG">
											<input type="checkbox" name="ckDeclaracao1368" id="checkIt1368">
											<label for="checkIt"></label>
										</fieldset>
										<p class="formText"><b>Declaro que estou ciente e concordo com as condições contidas no edital e seus anexos, bem como de que cumpro plenamente os requisitos de habilitação definidos no edital.</b></p>
									</div>
									<div class="clearBlock"></div>
								</div>
								<div class="formLeftBlock FB100">
									<div class="checkField">
										<fieldset class="checkBoxIMG">
											<input type="checkbox" name="ckDeclaracao1369" id="checkIt1369">
											<label for="checkIt"></label>
										</fieldset>
										<p class="formText"><b>Declaro cumprir as exigências de reserva de cargos para pessoa com deficiência e para reabilitado da Previdência Social, previstas em lei e em outras normas específicas.</b></p>
									</div>
									<div class="clearBlock"></div>
								</div>
								<div class="formLeftBlock FB100">
									<div class="checkField">
										<fieldset class="checkBoxIMG">
											<input type="checkbox" name="ckDeclaracao1370" id="checkIt1370">
											<label for="checkIt"></label>
										</fieldset>
										<p class="formText"><b>Sob pena de desclassificação, declaro que minhas propostas econômicas compreendem a integralidade dos custos para atendimento dos direitos trabalhistas assegurados na Constituição Federal, nas leis trabalhistas, nas normas infralegais, nas convenções coletivas de trabalho e nos termos de ajustamento de conduta vigentes na data de entrega das propostas.</b></p>
									</div>
									<div class="clearBlock"></div>
								</div>
								<div class="formLeftBlock FB100">
									<div class="checkField">
										<fieldset class="checkBoxIMG">
											<input type="checkbox" name="ckDeclaracao1371" id="checkIt1371">
											<label for="checkIt"></label>
										</fieldset>
										<p class="formText"><b>Declaro para fins do inciso XXXIII do artigo 7° da Constituição Federal, com redação dada pela Emenda Constitucional, nº 20/98, que não emprega menores de dezoito anos em trabalho noturno, perigoso ou insalubre e de que qualquer trabalho a menores de 16 anos.</b></p>
									</div>
									<div class="clearBlock"></div>
								</div>
								<div class="formLeftBlock FB100">
									<div class="checkField">
										<fieldset class="checkBoxIMG">
											<input type="checkbox" name="ckDeclaracao1372" id="checkIt1372">
											<label for="checkIt"></label>
										</fieldset>
										<p class="formText"><b>Declaro não possuir em sua cadeia produtiva, empregados executando trabalho degradante ou forçado, nos termos do inciso III e IV do art.1º e no inciso III do art.5º da Constituição Federal.</b></p>
									</div>
									<div class="clearBlock"></div>
								</div>
								<div class="formLeftBlock FB100">
									<div class="checkField">
										<fieldset class="checkBoxIMG">
											<input type="checkbox" name="ckDeclaracao1373" id="checkIt1373">
											<label for="checkIt"></label>
										</fieldset>
										<p class="formText"><b>Declaro que, conforme disposto no art. 93 da Lei nº 8.213, de 24 de julho de 1991, estou ciente do cumprimento da reserva de cargos prevista em lei para pessoa com deficiência ou para reabilitado da Previdência Social e que, se aplicado ao número de funcionários da minha empresa, atendo às regras de acessibilidade previstas na legislação.</b></p>
									</div>
									<div class="clearBlock"></div>
								</div>
								<div class="formLeftBlock FB100">
									<div class="checkField">
										<fieldset class="checkBoxIMG">
											<input type="checkbox" name="ckDeclaracao1374" id="checkIt1374">
											<label for="checkIt"></label>
										</fieldset>
										<p class="formText"><b>Declaro sob as penas da lei, que até a presente data inexistem fatos impeditivos para sua habilitação no presente processo licitatório, ciente da obrigatoriedade de declarar ocorrências posteriores.</b></p>
									</div>
									<div class="clearBlock"></div>
								</div>
									</div>
						<div class="dataInfoBlock6">
<p><b>ATENÇÃO: </b>Esse processo exige garantia, <b><a href="https://finiscorretora.com.br/" class="portalMenuLink" target="_blank" title="">clique aqui para realizar uma cotação online!</a></b></p>						</div>
<h3 class="h3TitleBlue divisor">DECLARAÇÃO  DE  ENQUADRAMENTO  DE  MICROEMPRESA  OU  EMPRESA  DE  PEQUENO PORTE</h3>							<div class="FB100 radioGroup">
								<p class="formText"><b>Declaro, sob as penas da Lei, que não ultrapassei o limite de faturamento e cumpro os requisitos estabelecidos no Art. 3º da Lei Complementar nº 123, de 14 de dezembro de 2006, sendo apto a usufruir do tratamento favorecido estabelecido nos artigos 42 ao 49 da referida Lei Complementar.</b></p>
								<div class="formLeftBlock FB25">
									<div class="radioField">
										<fieldset class="radioButtonIMG">
											<input type="radio" name="ttCD_BOLEANO_D_EPP" value="1" id="radioIt1">
											<label for="radioIt1"></label>
										</fieldset>
										<span class="formLabel">Sim</span>
									</div>
									<div class="clearBlock"></div>
								</div>
								<div class="formLeftBlock FB25">
									<div class="radioField">
										<fieldset class="radioButtonIMG">
											<input type="radio" name="ttCD_BOLEANO_D_EPP" value="2" id="radioIt2">
											<label for="radioIt2"></label>
										</fieldset>
										<span class="formLabel">Não</span>
									</div>
									<div class="clearBlock"></div>
								</div>
							</div>
							<input type="hidden" id="slCD_MOEDA" name="slCD_MOEDA" value="1">
<div class="clearBlock"></div>
							<div class="formLeftBlock FB50">
								<label class="formLabel" for="ttPRAZO_VALIDADE">Validade da Proposta - em dias, conforme edital <img src="/imgMaster/imgRequired.png" alt="Obrigatório"></label>
								<div class="formInputBlock">
									<input class="inputDefault width140 required" type="text" id="ttPRAZO_VALIDADE" name="ttPRAZO_VALIDADE" value="0" maxlength="3">
								</div>
							</div>
							<div class="formLeftBlock FB100">
								<input type="submit" value="Salvar Declarações" name="btGravar" class="buttonDefault btnGravar">
							</div>
							<div class="clearBlock"></div>
						</form> Faz o mesmo processo se for mei coloca sim caos não coloca não, e validade da proposta coloca 120. e clica em salvar declarações.


Agora vai ser diferente é outra etapa. Depois "2-" que é "2 - INFORMAÇÕES COMPLEMENTARES" vc verifica se o arquivo tem que anexar algo se tiver vc vai anexar o seguinte arquivo: D:\trabalho\AlcantaraMendes\PROJETO OPERACIONAL\portal-compras-publicas\portal-compras-publicas\core\docs\teste.pdf. Vc vai clicar no seguinte se tiver 3- 4- 5- ... e tiver um locao para anexar que seria o //*[@id="searchTableSorter"]/tbody/tr/td[3]/a  ele vai abrir um campo como esse: <div class="pp_pic_holder pp_default" style="top: 219.5px; left: 557.5px; display: block; width: 772px;"> 						<div class="pp_top"> 							<div class="pp_left"></div> 							<div class="pp_middle"></div> 							<div class="pp_right"></div> 						</div> 						<div class="pp_content_container"> 							<div class="pp_left"> 							<div class="pp_right"> 								<div class="pp_content" style="height: 486px; width: 732px;"> 									<div class="pp_loaderIcon" style="display: none;"></div> 									<div class="pp_fade" style="display: block;"> 										<a href="#" class="pp_expand" title="Expand the image" style="display: none;">Expand</a> 										<div class="pp_hoverContainer" style="height: 450px; width: 732px; display: none;"> 											<a class="pp_next" href="#">next</a> 											<a class="pp_previous" href="#">previous</a> 										</div> 										<div id="pp_full_res"><iframe src="/4/Pregoes/RegistroProposta/DocumentoGarantia/?slA=New&amp;slCD_ORIGEM=348094" width="732" height="450" frameborder="no"></iframe></div> 										<div class="pp_details clearfix" style="width: 732px;"> 											<div class="ppt" style="opacity: 1; display: block; width: 732px;">Editar Registro</div> 											<p class="pp_description" style="display: block;">Inserir Documento</p> 											<a class="pp_close" href="#">Close</a> 											<div class="pp_nav" style="display: none;"> 												<a href="#" class="pp_arrow_previous">Previous</a> 												<p class="currentTextHolder">1/1</p> 												<a href="#" class="pp_arrow_next">Next</a> 											</div> 										</div> 									</div> 								</div> 							</div> 							</div> 						</div> 						<div class="pp_bottom"> 							<div class="pp_left"></div> 							<div class="pp_middle"></div> 							<div class="pp_right"></div> 						</div> 					</div>



92/2024
12/02/2025

108/2024
10/02/2025

176/2024
24/02/2025



o que tiver verdinho: <img src="/4/img/icoOk.png" alt="Item Gravado"> item gravado e que esse já foi cadastrado ai vc vai no de baixo indo percorrendo o html aate não ter nenhum item para cadastrarmais.. analisa a logia da priemra para desenvolver