import telebot
import requests
import time  # Add a time delay to avoid spam

# Your Telegram Bot Token
BOT_TOKEN = "8058388234:AAEz9jW2tHlcbfyXC8daCC-rEnbxWzy4dLY"
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

# Add buttons for the 9 channels (with links)
def create_inline_button():
    keyboard = telebot.types.InlineKeyboardMarkup()
    
    button_channel_1 = telebot.types.InlineKeyboardButton(
        text="Writing", url="https://t.me/neo_writing"
    )
    button_channel_2 = telebot.types.InlineKeyboardButton(
        text="Listening", url="https://t.me/tpo_listening1"
    )
    button_channel_3 = telebot.types.InlineKeyboardButton(
        text="Speaking", url="https://t.me/+lWir8Hu6css5MGQ1"
    )
    button_channel_4 = telebot.types.InlineKeyboardButton(
        text="Resources", url="https://t.me/+gPhXbnd49yk0NTI1"
    )
    button_channel_5 = telebot.types.InlineKeyboardButton(
        text="YouTube Vocab", url="https://t.me/+oGceYYJCwrZjNDk9"
    )
    button_channel_6 = telebot.types.InlineKeyboardButton(
        text="Ketab", url="https://t.me/ketab_pdfs"
    )
    button_channel_7 = telebot.types.InlineKeyboardButton(
        text="TED Talks", url="https://t.me/moha_ted"
    )
    button_channel_8 = telebot.types.InlineKeyboardButton(
        text="4000 Words", url="https://t.me/+bz-2dmJTxTowZGZl"
    )
    button_channel_9 = telebot.types.InlineKeyboardButton(
        text="Extensive Reading", url="https://t.me/+OCr_ZwPHbCo4ZWM1"
    )

    # Add the buttons to the keyboard, 3 buttons in one row, 3 in the next row
    keyboard.row(button_channel_1, button_channel_2, button_channel_3)
    keyboard.row(button_channel_4, button_channel_5, button_channel_6)
    keyboard.row(button_channel_7, button_channel_8, button_channel_9)
    
    return keyboard


# Start command
@bot.message_handler(commands=['start'])
def send_welcome(message):
    # Send the welcome message with inline buttons
    bot.reply_to(
        message, 
        """🚀 𝚆𝚎𝚕𝚌𝚘𝚖𝚎 𝚝𝚘 𝚢𝚘𝚞𝚛 𝚞𝚕𝚝𝚒𝚖𝚊𝚝𝚎 𝙳𝚒𝚌𝚝𝚒𝚘𝚗𝚊𝚛𝚢 𝙱𝚘𝚝! 📚🔍

        𝙴𝙭𝚌𝚒𝚝𝚎𝚍 𝚝𝚘 𝚍𝚒𝚟𝚎 𝚒𝚗𝚝𝚘 𝚝𝚑𝚎 𝚎𝚗𝚌𝚑𝚊𝚗𝚝𝚒𝚗𝚐 𝚠𝚘𝚛𝚕𝚍 𝚘𝚏 𝚠𝚘𝚛𝚍𝚜? 🌍✨ 𝚂𝚒𝚖𝚙𝚕𝚢 𝚜𝚑𝚊𝚛𝚎 𝚊 𝚠𝚘𝚛𝚍 𝚘𝚛 𝚖𝚞𝚕𝚝𝚒𝚙𝚕𝚎 𝚠𝚘𝚛𝚍𝚜 (𝚜𝚎𝚙𝚊𝚛𝚊𝚝𝚎𝚍 𝚋𝚢 𝚌𝚘𝚖𝚖𝚊𝚜 𝚘𝚛 𝚗𝚎𝚠 𝚕𝚒𝚗𝚎𝚜).

        𝙱𝚎 𝚜𝚞𝚛𝚎 𝚝𝚘 𝚎𝚡𝚙𝚕𝚘𝚛𝚎 𝚝𝚑𝚎 𝚋𝚞𝚝𝚝𝚘𝚗𝚜 𝚋𝚎𝚕𝚘𝚠 𝚏𝚘𝚛 𝚒𝚗𝚌𝚛𝚎𝚍𝚒𝚋𝚕𝚎 𝚌𝚑𝚊𝚗𝚗𝚎𝚕𝚜 𝚊𝚗𝚍 𝚐𝚛𝚘𝚞𝚙𝚜 𝚝𝚘 𝚎𝚗𝚛𝚒𝚌𝚑 𝚢𝚘𝚞𝚛 𝚕𝚎𝚊𝚛𝚗𝚒𝚗𝚐 𝚓𝚘𝚞𝚛𝚗𝚎𝚈! 📘🎓 @dictionaryai_bot""",
        parse_mode="HTML",
        reply_markup=create_inline_button()  # Add the inline keyboard here
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
            # Send to user without inline buttons
            bot.send_message(message.chat.id, reply_text, parse_mode="HTML")
            
            # Send to channel with inline buttons
            channel_message = f"""
📖 <b>Word:</b> <code>{word}</code>
📌 <b>Part of Speech:</b> <i>{part_of_speech}</i>
📝 <b>Meaning:</b> <code>{meaning}</code>
━━━━━━━━━━━━━━━━━━━━━━━
<a href="https://t.me/MomeniTOEFL">Join 𝑬𝒍𝒊𝒕𝒆 𝑻𝑶𝑬𝑭𝑳 𝑨𝒄𝒂𝒅𝒆𝒎𝒚</a>
"""
            bot.send_message(
                "-1002369564811",  # Channel name
                channel_message,
                parse_mode="HTML",
                reply_markup=create_inline_button()  # Inline buttons for the channel
            )
        else:
            bot.send_message(
                message.chat.id, 
                f"❌ <b>Sorry, I couldn't find the meaning of</b> <code>{word}</code>.",
                parse_mode="HTML"
            )
        
        time.sleep(1)  # Add delay to avoid spam

# Start the bot
bot.polling()