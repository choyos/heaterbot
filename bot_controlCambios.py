import RPi.GPIO as GPIO
import time, telebot, select
from telebot import types
from wireless import Wireless

# Definimos pineage
GPIO.setmode(GPIO.BCM)

# Definimos objeto rele
class rele:

    # En inicializacion
    def __init__(self, pin):
        # Asignamos el pin y lo configuramos como salida
        self.rele = pin
        GPIO.setup(self.rele, GPIO.OUT)
        # Ponemos la salida a nivel bajo (empieza apagado)
        GPIO.output(self.rele, False)

        self.status = "Off"

    # Definimos funcion de encendido del enchufe
    def on(self):
        GPIO.output(self.rele, True)
        self.status = "On"
        print "Encender"
        return
    # Definimos funcion de apagado del enchufe
    def off(self):
        GPIO.output(self.rele, False)
        self.status = "Off"
        print "Apagar"
        return

# Hacemos las asignaciones de los pines fisicos
pin_rele = 25

# Establecemos el valor del TOKEN facilitado por The BotFather
TOKEN = "289317488:AAEpHlZCmDrndtD_zxbFp1YVkQXuDgZ9zFc"

# Creamos una instancia tipo rele para el enchufe
plug = rele(pin_rele)

# Creamos objeto para manejar estado de la conexion
wifi = Wireless()

# Creamos conexion con bot de telegram
bot = telebot.TeleBot(TOKEN)

# Definimos identificadores de usuarios
cesar_id = 9519882
marta_id = 3453463

# Definimos funcion para comprobar la identidad de los usuarios
def check_security(message):
    print message.chat.username
    print message.from_user.id
    print message.chat.id
    if message.chat.type == "group":
        return True
    elif message.chat.id == cesar_id:
        return True
    elif message.chat.id == marta_id:
        return True
    else:
        return False

# Definimos teclado para facilitar uso
keyboard = types.ReplyKeyboardMarkup(row_width=1)
btn_on = types.KeyboardButton('Encender')
btn_off = types.KeyboardButton('Apagar')
keyboard.add(btn_on, btn_off)

def send_changes(message):
    if message.chat.id == marta_id:
        bot.send_message(cesar_id, "Aviso: enchufe " + plug.status)
    elif message.chat.id == cesar_id:
        bot.send_message(marta_id, "Aviso: enchufe " + plug.status)

def broadcast(message_str):
    bot.send_message(cesar_id, message_str)
    bot.send_message(marta_id, message_str)

# Definimos mensaje con instrucciones de uso
# Este mensaje tambien sera el recurrente
# usandose como respuesta automatica ante cualquier mensaje
@bot.message_handler(commands = ['start', 'help'])
def send_instructions(message):
    bot.send_message(message.chat.id, "Enchufe: " + plug.status + ".\n"+
                         "Que quieres hacer?", reply_markup = keyboard)


# Definimos mensajes para comandos
@bot.message_handler(commands = ['status'])
def send_status(message):
    send_instructions(message)

# Definimos commando de encendido
@bot.message_handler(commands = ['turn_on'])
def turn_on(message):
    if check_security(message):
        plug.on()
        send_changes(message)

# Definimos commando de apagado
@bot.message_handler(commands = ['turn_off'])
def turn_off(message):
    if check_security(message):
        plug.off()
        send_changes(message)

# Definimos como actuar en caso de llegar un mensaje
@bot.message_handler(func=lambda message: True)
def echo_all(message):
    # Si el mensaje es encender
    if message.text == "Encender":
        turn_on(message)
    # Si el mensaje es apagar
    elif message.text == "Apagar":
        turn_off(message)
    # En otro caso
    else:
        bot.send_message(message.chat.id, "No reconocido")
    send_instructions(message)

# Iniciamos el bot
try:
    while 1:
        try:
            print "Entra en try"
            bot.polling()
        except:
            while not wifi.current():
                time.sleep(2)
            else:
                time.sleep(15)
            # Abrimos nueva conexion con bot de telegram
            bot = telebot.TeleBot(TOKEN)
            print "Sistema reiniciado"
            bot.send_message(cesar_id, "Reiniciado. Enchufe: "+ plug.status)
            bot.send_message(marta_id, "Reiniciado. Enchufe: "+ plug.status)
 
finally:
    # Cerramos socket servidor
    # ss.close()
    GPIO.cleanup()
    print "Cerrando conexion y liberando pines"
