from gps import *
import time
from telegram import *
from telegram.ext import * 

running = True

gpsd = gps(mode=WATCH_ENABLE|WATCH_NEWSTYLE)

bot = Bot("YOUR_TOKEN")

updater = Updater("YOUR_TOKEN", use_context=True)
dispatcher = updater.dispatcher

def test_function(update: Update, context: CallbackContext):
    while running:
        nx = gpsd.next()
        if nx['class'] == 'TPV':
            latitude = getattr(nx,'lat', "Unknown")
            longitude = getattr(nx,'lon', "Unknown")
            print("lat = " + str(latitude),"lon = " + str(longitude))
            latlng=str(latitude)+','+str(longitude)
            url="https://www.google.com/maps/place/"+latlng
            print(url)
            bot.send_message(chat_id=update.effective_chat.id,text=url,)
            break
        time.sleep(1.0)
start_value = CommandHandler("location", test_function)
dispatcher.add_handler(start_value)
updater.start_polling()
