#SleepWake Alert

O projeto SleepWake Alert é um sistema inteligente que utiliza visão computacional e processamento de imagem para detectar quando uma pessoa está dormindo e emitir um alerta sonoro para acordá-la. O sistema é capaz de detectar a taxa de piscadas e o fechamento prolongado dos olhos, indicando quando uma pessoa está sonolenta ou dormindo.

Requisitos
Python 3.x
Bibliotecas Python: numpy, dlib, opencv-python, pygame
Instalação
Clone o repositório do projeto:

git clone https://github.com/seu-usuario/sleepwake-alert.git
Instale as bibliotecas Python necessárias:

pip install numpy dlib opencv-python pygame

**Uso**
Para executar o algoritmo, execute o seguinte comando no diretório raiz do projeto:

python sleepwake_alert.py

O programa será iniciado e a webcam será ativada automaticamente. O sistema monitorará o rosto de todas as pessoas na imagem e emitirá um alerta sonoro caso detecte que uma pessoa está dormindo.

O programa pode ser interrompido pressionando a tecla 'q' no teclado.
