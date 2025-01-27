@echo off
echo Instalando dependencias...
pip install -r requirements.txt
pip install pyinstaller

echo Criando executavel...
pyinstaller automacao.spec --clean

echo Copiando executavel para a pasta principal...
copy /Y "dist\Automacao_Certidoes.exe" "Automacao_Certidoes.exe"

echo Processo concluido!
pause
