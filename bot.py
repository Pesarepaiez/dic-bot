import telebot
import requests
import time  # Add a time delay to avoid spam

# Your Telegram Bot Token
BOT_TOKEN = "5909441299:AAEv7WSNh2lrRFTa7gAhH9x8wzOembjmD94"
bot = telebot.TeleBot(BOT_TOKEN, parse_mode="HTML")  # Ensure HTML formatting works

# Free Dictionary API URL
DICTIONARY_API_URL = "https://api.dictionaryapi.dev/api/v2/entries/en/"

# Function to get word definition
def get_definition(word):
    response = requests.get(DICTIONARY_API_URL + word)
    if response.status_code == 200:
        data = response.json()
        
        # Extract meaning and part of speech
        part_of_speech = data[0]['meanings'][0]['partOfSpeech'].capitalize()
        meaning = data[0]['meanings'][0]['definitions'][0]['definition']
        
        return part_of_speech, meaning
    return None, None

# Create an inline button that redirects to your channel and group
def create_inline_button():
    keyboard = telebot.types.InlineKeyboardMarkup()
    
    # Add buttons for Channel and Group
    button_channel = telebot.types.InlineKeyboardButton(
        text="Channel", url="https://t.me/paieznsher"
    )
    button_group = telebot.types.InlineKeyboardButton(
        text="Group", url="https://t.me/afghan_congres"
    )
    
    keyboard.add(button_channel, button_group)  # Add buttons to keyboard
    return keyboard

# Start command
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(
        message, 
        "📚 <b>Welcome to the Dictionary Bot!</b> 🔍\n\n"
        "Send a word or multiple words (separated by commas or new lines) to get their meanings.",
        reply_markup=create_inline_button(),  # Inline button to redirect to channel and group
        parse_mode="HTML"
    )

# Handle multiple words (comma or newline separated)
@bot.message_handler(func=lambda message: True)
def handle_word(message):
    words = message.text.replace("\n", ",").split(",")  # Handle both comma and newline separation
    words = [word.strip().lower() for word in words if word.strip()]  # Clean up words
    
    if not words:
        bot.reply_to(message, "❌ <b>Please enter at least one valid word.</b>", parse_mode="HTML")
        return

    for word in words:
        part_of_speech, meaning = get_definition(word)
        
        if meaning:
            reply_text = f"""

📖 <b>Word:</b> <code>{word}</code>
📌 <b>Part of Speech:</b> <i>{part_of_speech}</i>
📝 <b>Meaning:</b> <code>{meaning}</code>
━━━━━━━━━━━━━━━━━━━━━━━
 <a href="https://t.me/MomeniTOEFL/725">𝑬𝒍𝒊𝒕𝒆 𝑻𝑶𝑬𝑭𝑳 𝑨𝒄𝒂𝒅𝒆𝒎𝒚</a>
"""
            bot.send_message(message.chat.id, reply_text, parse_mode="HTML")
        else:
            bot.send_message(
                message.chat.id, 
                f"❌ <b>Sorry, I couldn't find the meaning of</b> <code>{word}</code>.",
                parse_mode="HTML"
            )
        
        time.sleep(1)  # Add delay to avoid spam

# Start the bot
bot.polling()