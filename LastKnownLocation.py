import pyrebase
from telegram import *
from telegram.ext import *

firebaseConfig = {
    "apiKey": "xxx",
    "authDomain": "xxx",
    "databaseURL": "xxx",
    "projectId": "xxx",
    "storageBucket": "xxx",
    "messagingSenderId": "xxx",
    "appId": "xxx",
    "measurementId": "xxx"}

firebase = pyrebase.initialize_app(firebaseConfig)
db = firebase.database()

bot = Bot("[YOUR_BOT_TOKEN]s")

updater = Updater("[YOUR_BOT_TOKEN]", use_context=True)
dispatcher = updater.dispatcher


def test_function(update: Update, context: CallbackContext):
    res = db.child("Thief").get()
    len_db = len(res.val())
    print(len_db)
    loc = "Location" + str(len_db)
    latlng = res.val()[loc]
    url = "This was the last known location of your car.....\n\nhttps://www.google.com/maps/place/" + latlng
    bot.send_message(
        chat_id=update.effective_chat.id,
        text=url,
    )


start_value = CommandHandler("lastknownlocation", test_function)
dispatcher.add_handler(start_value)
updater.start_polling()
