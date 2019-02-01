import RPi.GPIO as GPIO
import time, telebot, select
from time import sleep
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
        aux_bool = GPIO.input(self.rele)
        # Ponemos la salida al mismo nivel que se encontraba
        GPIO.output(self.rele, aux_bool)
        self.status = "Off"
        if(aux_bool):
            self.status = "On"
        

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

# Definimos funcion para comprobar la identidad de los usuarios
def check_security(message):
    print message.chat.username
    print message.from_user.id
    print message.chat.id
    if message.chat.type == "group":
        return True
    elif message.chat.id == cesar_id:
        return True
    else:
        return False

# Definimos teclado para facilitar uso
keyboard = types.ReplyKeyboardMarkup(row_width=1)
btn_on = types.KeyboardButton('Encender')
btn_off = types.KeyboardButton('Apagar')
keyboard.add(btn_on, btn_off)

def send_changes(message):
    bot.send_message(message.chat.id, "Aviso: enchufe " + plug.status)

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
	user_status = "On"
	current_time = time.time()
    # Si el mensaje es apagar
    elif message.text == "Apagar":
        turn_off(message)
	user_status = "Off"
	current_time = time.time()
    # En otro caso
    else:
        bot.send_message(message.chat.id, "No reconocido")
    send_instructions(message)

# Definimos tiempos para apagado/encendido
time_min = 10.0
time_sec = 60.0 * time_min
current_time = time.time()

# Definimos indice de los mensajes
msgs_index = 0

#Definimos variable para saber estado en el que el usuario ha dicho que se encuentre
user_status = "On"

# Definimos funcion para hacer el cambio
def switch_plug():
	if user_status == "On":
		if plug.status == "On":
			plug.off()
		else:
			plug.on()

# Iniciamos el bot
try:
    print "Entra en try"
    while 1:
	# Recibimos los ultimos mensajes
	updates = bot.get_updates()
	# Si se acaba de iniciar el bot
	if msgs_index == 0:
		# Se establece el indice del bot en funcion del anterior mensaje
		msgs_index = updates[-1].message.message_id
	# En caso contrario, se procesa el ultimo mensaje
	elif updates[-1].message.message_id > msgs_index:
		echo_all(updates[-1].message)
		msgs_index = updates[-1].message.message_id

	if (time.clock()-current_time) >= time_sec:
		current_time = time.time()
		switch_plug()
    
finally:
    # Cerramos socket servidor
    # ss.close()
    # GPIO.cleanup()
    print "Cerrando conexion y liberando pines"
