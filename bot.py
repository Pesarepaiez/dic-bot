import telebot

API_TOKEN = '8122882322:AAFc9SNrdpq_nd1vY3dUsD53PTodKj16bMk'

bot = telebot.TeleBot(API_TOKEN)

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, "Hello, World!")

if __name__ == "__main__":
    bot.polling()
