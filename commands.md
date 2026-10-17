cd hardware

py -3.14 -m mpremote connect COM5 fs cp sh1106.py :sh1106.py
py -3.14 -m mpremote connect COM5 fs cp ssd1306.py :ssd1306.py
py -3.14 -m mpremote connect COM5 fs mkdir src

py -3.14 -m mpremote connect COM5 fs cp src/display.py :src/display.py
py -3.14 -m mpremote connect COM5 fs cp src/buttons.py :src/buttons.py
py -3.14 -m mpremote connect COM5 fs cp src/screens.py :src/screens.py
py -3.14 -m mpremote connect COM5 fs cp src/serialClient.py :src/serialClient.py
py -3.14 -m mpremote connect COM5 fs cp src/spotifyService.py :src/spotifyService.py
py -3.14 -m mpremote connect COM5 fs cp src/microphone.py :src/microphone.py
py -3.14 -m mpremote connect COM5 fs cp src/qr.py :src/qr.py

py -3.14 -m mpremote connect COM5 fs cp main.py :main.py
py -3.14 -m mpremote connect COM5 reset
py -3.14 -m mpremote connect COM5 repl

# debug

py -3.14 -m mpremote connect COM5 fs ls
py -3.14 -m mpremote connect COM5 fs ls :src

py -3.14 -m mpremote connect COM5 repl
