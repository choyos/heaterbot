import commands, os, time, telebot

# Se define el token para usarlo en caso de errores
TOKEN = "289317488:AAEpHlZCmDrndtD_zxbFp1YVkQXuDgZ9zFc"

# Definimos identificadores de usuarios
cesar_id = 9519882

# Ejecutamos bucle infinito
while 1:
    # Se ejecuta el programa de control
    try:
        os.system("python bot_control.py")
    # En caso de excepcion
    except:
        # Se espera 60 segundos
        time.sleep(60)
        # Se inicia el bot
        bot = telebot.TeleBot(TOKEN)
        message_str = "Error del sistema. Volvera a iniciarse en un minuto"
        # Se manda un mensaje de difusion a los usuarios para avisar del error
        bot.send_message(cesar_id, message_str)       
