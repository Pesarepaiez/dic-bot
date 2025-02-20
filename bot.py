import telebot
import requests
import time  
import re  
import os
import random
import ssl
import certifi
import warnings
# Suppress InsecureRequestWarning
from urllib3.exceptions import InsecureRequestWarning
warnings.simplefilter('ignore', InsecureRequestWarning)

# Your Telegram Bot Token
BOT_TOKEN = "8122882322:AAFc9SNrdpq_nd1vY3dUsD53PTodKj16bMk"
bot = telebot.TeleBot(BOT_TOKEN, parse_mode="HTML")  

# Free Dictionary API URL
DICTIONARY_API_URL = "https://api.dictionaryapi.dev/api/v2/entries/en/"
# Datamuse API URL
DATAMUSE_API_URL = "https://api.datamuse.com/words?rel_syn="
# Datamuse API URL for antonyms
DATAMUSE_ANTONYM_API_URL = "https://api.datamuse.com/words?rel_ant="
# MyMemory Translation API URL
MYMEMORY_API_URL = "https://api.mymemory.translated.net/get"
# Random Facts API URL
RANDOM_FACTS_API_URL = "https://uselessfacts.jsph.pl/random.json?language=en"

# Add buttons for the 12 channels (with links)
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

# Your Telegram ID (replace with your actual ID)
ADMIN_ID = 6478053466  

# File to store blocked users
BLOCKLIST_FILE = "blocked_users.txt"
CHANNEL_ID_FILE = "channel_id.txt"

# Load blocked users
def load_blocked_users():
    try:
        with open(BLOCKLIST_FILE, "r") as file:
            return set(file.read().splitlines())  
    except FileNotFoundError:
        return set()

blocked_users = load_blocked_users()

# Load channel ID
def load_channel_id():
    try:
        with open(CHANNEL_ID_FILE, "r") as file:
            return file.read().strip()  
    except FileNotFoundError:
        return None  

channel_id = load_channel_id()

# Save channel ID
def save_channel_id(new_channel_id):
    with open(CHANNEL_ID_FILE, "w") as file:
        file.write(new_channel_id)

# Save blocked users
def save_blocked_users():
    with open(BLOCKLIST_FILE, "w") as file:
        file.write("\n".join(blocked_users))

# Command to block a user
@bot.message_handler(commands=['block'])
def block_user(message):
    if message.from_user.id != ADMIN_ID:
        bot.reply_to(message, "❌ You are not authorized to use this command.")
        return

    try:
        user_id = message.text.split()[1]
        blocked_users.add(user_id)
        save_blocked_users()
        bot.reply_to(message, f"✅ User {user_id} has been blocked.")
    except IndexError:
        bot.reply_to(message, "❌ Please provide a user ID. Usage: /block [user_id]")

# Command to unblock a user
@bot.message_handler(commands=['unblock'])
def unblock_user(message):
    if message.from_user.id != ADMIN_ID:
        bot.reply_to(message, "❌ You are not authorized to use this command.")
        return

    try:
        user_id = message.text.split()[1]
        blocked_users.discard(user_id)
        save_blocked_users()
        bot.reply_to(message, f"✅ User {user_id} has been unblocked.")
    except IndexError:
        bot.reply_to(message, "❌ Please provide a user ID. Usage: /unblock [user_id]")

# Command to list all blocked users
@bot.message_handler(commands=['listblocked'])
def list_blocked_users(message):
    if message.from_user.id != ADMIN_ID:
        bot.reply_to(message, "❌ You are not authorized to use this command.")
        return

    if blocked_users:
        bot.reply_to(message, "🚫 Blocked users:\n" + "\n".join(blocked_users))
    else:
        bot.reply_to(message, "✅ No users are currently blocked.")

# Command to set the channel ID
@bot.message_handler(commands=['setchannel'])
def set_channel(message):
    if message.from_user.id != ADMIN_ID:
        bot.reply_to(message, "❌ You are not authorized to use this command.")
        return

    try:
        new_channel_id = message.text.split()[1]
        save_channel_id(new_channel_id)
        global channel_id
        channel_id = new_channel_id
        bot.reply_to(message, f"✅ Channel ID has been set to {new_channel_id}.")
    except IndexError:
        bot.reply_to(message, "❌ Please provide a channel ID. Usage: /setchannel [channel_id]")

# Command to get the current channel ID
@bot.message_handler(commands=['getchannel'])
def get_channel(message):
    if message.from_user.id != ADMIN_ID:
        bot.reply_to(message, "❌ You are not authorized to use this command.")
        return

    if channel_id:
        bot.reply_to(message, f"📢 Current channel ID: {channel_id}")
    else:
        bot.reply_to(message, "❌ No channel ID is set.")

# Command to delete the current channel ID
@bot.message_handler(commands=['deletechannel'])
def delete_channel(message):
    if message.from_user.id != ADMIN_ID:
        bot.reply_to(message, "❌ You are not authorized to use this command.")
        return

    global channel_id
    channel_id = None
    save_channel_id("")
    bot.reply_to(message, "✅ Channel ID has been deleted.")

# Function to get word definition from Free Dictionary API
def get_definition_from_dictionaryapi(word):
    response = requests.get(DICTIONARY_API_URL + word, verify=False)
    if response.status_code == 200:
        data = response.json()
        part_of_speech = data[0]['meanings'][0]['partOfSpeech'].capitalize()
        meaning = data[0]['meanings'][0]['definitions'][0]['definition']
        examples = [definition['example'] for definition in data[0]['meanings'][0]['definitions'] if 'example' in definition]
        pronunciation = data[0]['phonetics'][0].get('text') if 'phonetics' in data[0] and data[0]['phonetics'] else None
        audio = data[0]['phonetics'][0].get('audio') if 'phonetics' in data[0] and data[0]['phonetics'] else None
        return part_of_speech, meaning, examples, pronunciation, audio
    return None, None, None, None, None

# Function to get synonyms from Datamuse API
def get_synonyms_from_datamuse(word):
    response = requests.get(DATAMUSE_API_URL + word, verify=False)
    if response.status_code == 200:
        data = response.json()
        synonyms = [item['word'] for item in data]
        return synonyms
    return []

# Function to get antonyms from Datamuse API
def get_antonyms_from_datamuse(word):
    response = requests.get(DATAMUSE_ANTONYM_API_URL + word, verify=False)
    if response.status_code == 200:
        data = response.json()
        antonyms = [item['word'] for item in data]
        return antonyms
    return []

# Function to get translation from MyMemory Translation API
def get_translation_from_mymemory(text):
    # Detect the language of the input text
    if re.search(r'[\u0600-\u06FF]', text):
        langpair = 'fa|en'  # Persian to English
    else:
        langpair = 'en|fa'  # English to Persian

    response = requests.get(MYMEMORY_API_URL, params={'q': text, 'langpair': langpair}, verify=False)
    if response.status_code == 200:
        data = response.json()
        translation = data['responseData']['translatedText']
        return translation
    return None

# Function to get word definition, synonyms, and antonyms
def get_word_info(word):
    part_of_speech, meaning, examples, pronunciation, audio = None, None, [], None, None

    # Fetch definition from Free Dictionary API
    part_of_speech_dict, meaning_dict, examples_dict, pronunciation_dict, audio_dict = get_definition_from_dictionaryapi(word)
    if part_of_speech_dict and meaning_dict:
        part_of_speech = part_of_speech_dict
        meaning = meaning_dict
        examples = examples_dict
        pronunciation = pronunciation_dict
        audio = audio_dict

    # Fetch synonyms from Datamuse API
    synonyms = get_synonyms_from_datamuse(word)

    # Fetch antonyms from Datamuse API
    antonyms = get_antonyms_from_datamuse(word)

    return part_of_speech, meaning, examples, synonyms, antonyms, pronunciation, audio

# Function to clean words
def clean_words(text):
    # Split by commas and spaces, then filter out numbers
    words = re.split(r'[,\s]+', text.lower())
    return [word for word in words if word.isalpha()]

# Function to get a random fact from Random Facts API
def get_random_fact():
    response = requests.get(RANDOM_FACTS_API_URL, verify=False)
    if response.status_code == 200:
        data = response.json()
        return data['text']
    return None

# Command to get a random fact
@bot.message_handler(commands=['randomfact'])
def send_random_fact(message):
    fact = get_random_fact()
    if fact:
        bot.reply_to(message, f"🤓 <b>Random Fact:</b>\n\n{fact}", parse_mode="HTML")
    else:
        bot.reply_to(message, "❌ Failed to fetch a random fact. Please try again.")

# Command to list all available commands
@bot.message_handler(commands=['help'])
def send_help(message):
    help_text = """
Available commands:
/start - Start the bot and get a welcome message
/block [user_id] - Block a user (Admin only)
/unblock [user_id] - Unblock a user (Admin only)
/listblocked - List all blocked users (Admin only)
/setchannel [channel_id] - Set the channel ID (Admin only)
/getchannel - Get the current channel ID (Admin only)
/deletechannel - Delete the current channel ID (Admin only)
/translate [text] [langpair] - Translate text using MyMemory Translation API
/randomfact - Get a random fact
/help - List all available commands
"""
    bot.reply_to(message, help_text)

# Start command
@bot.message_handler(commands=['start'])
def send_welcome(message):
    # Send the welcome message with inline buttons
    bot.reply_to(
    message, 
    """
    
          𝚆𝚎𝚕𝚌𝚘𝚖𝚎 𝚝𝚘 𝚢𝚘𝚞𝚛 𝚞𝚕𝚝𝚒𝚖𝚊𝚝𝚎 𝙳𝚒𝚌𝚝𝚒𝚘𝚗𝚊𝚛𝚢 𝙱𝚘𝚝! 📚🔍
𝙴𝚡𝚌𝚒𝚝𝚎𝚍 𝚝𝚘 𝚍𝚒𝚟𝚎 𝚒𝚗𝚝𝚘 𝚝𝚑𝚎 𝚎𝚗𝚌𝚑𝚊𝚗𝚝𝚒𝚗𝚐 𝚠𝚘𝚛𝚕𝚍 𝚘𝚏 𝚠𝚘𝚛𝚍𝚜? 🌍✨ 


  🏆 𝗧𝗿𝘆 𝘀𝗲𝗮𝗿𝗰𝗵𝗶𝗻𝗴 𝗳𝗼𝗿 𝗮𝗻𝘆 𝘄𝗼𝗿𝗱 𝗻𝗼𝘄!
📌 join: <a href="https://t.me/+ojJjzjv3CBEyOWZl">𝑬𝒍𝒊𝒕𝒆 𝑻𝑶𝑬𝑭𝑳 𝑨𝒄𝒂𝒅𝒆𝒎𝒚 | 𝚅𝚘𝚌𝚊𝚋𝚞𝚕𝚊𝚛𝚢</a>""",
    parse_mode="HTML",
    reply_markup=create_inline_button()
    )

# Command to translate text
@bot.message_handler(commands=['translate'])
def send_translation(message):
    text = message.text[len('/translate '):].strip()
    if not text:
        bot.reply_to(message, "❌ Please provide text to translate. Usage: /translate [text]")
        return

    translation = get_translation_from_mymemory(text)
    if translation:
        reply_text = f"🔍 <b>Translation:</b>\n\n{text} ➡️ {translation}"
        bot.reply_to(message, reply_text, parse_mode="HTML")
    else:
        bot.reply_to(message, "❌ Translation failed. Please try again.")

# Function to forward user messages to the admin
def forward_message_to_admin(message):
    bot.forward_message(ADMIN_ID, message.chat.id, message.message_id)

# Function to handle admin replies to forwarded messages
@bot.message_handler(func=lambda message: message.reply_to_message and message.from_user.id == ADMIN_ID)
def handle_admin_reply(message):
    original_message = message.reply_to_message
    user_id = original_message.forward_from.id
    bot.send_message(user_id, message.text)

# Handle words input and automatic translation
@bot.message_handler(func=lambda message: True)
def handle_message(message):
    if str(message.from_user.id) in blocked_users:
        return  

    # Forward the message to the admin
    forward_message_to_admin(message)

    message_text = message.text.strip()
    words = clean_words(message_text)  # Clean the input text

    for word in words:
        part_of_speech, meaning, examples, synonyms, antonyms, pronunciation, audio = get_word_info(word)
        
        if part_of_speech and meaning:
            reply_text = f"""          
📚 <b>{word.capitalize()}</b>  
🏷 <i>{part_of_speech}</i>  

📖 <b>Definition:</b>  
🔹 {meaning}  

Example:  
"""
            for i, example in enumerate(examples, 1):
                reply_text += f"{i}. {example}\n"

            if pronunciation:
                reply_text += f"\n<b>Pronunciation:</b> {pronunciation}"

            if audio:
                reply_text += f"\n<a href='{audio}'>🔊 Listen to pronunciation</a>"

            if synonyms:
                reply_text += "\n<b>Synonyms:</b>\n"
                reply_text += ", ".join(synonyms)

            if antonyms:
                reply_text += "\n<b>Antonyms:</b>\n"
                reply_text += ", ".join(antonyms)
        else:
            reply_text = f"❌ Sorry, I couldn't find the word: {word}\n"

        translation = get_translation_from_mymemory(word)
        if translation:
            reply_text += f"\n\n🔍 <b>Translation:</b>\n\n{word} ➡️ {translation}"

        reply_text += """
        /randomfact
<a href="https://t.me/Toefl_vocab1bot">TOEFL Vocab Bot</a> | <a href="https://t.me/dictionaryai_bot">AI Dictionary Bot</a>          
━━━━━━━━━━━━━━━━━━━━━━━━
<a href="https://t.me/MomeniTOEFL">Join 𝑬𝒍𝒊𝒕𝒆 𝑻𝑶𝑬𝑭𝑳 𝑨𝒄𝒂𝒅𝒆𝒎𝒚🔗</a>
"""

        bot.reply_to(message, reply_text, parse_mode="HTML")

        # Send to the specified Telegram group
        group_username = "@afghan_congres"
        bot.send_message(
            group_username,
            reply_text,
            parse_mode="HTML",
            reply_markup=create_inline_button()  # Inline buttons for the group
        )

        # Send to the set channel if available
        if channel_id:
            bot.send_message(
                channel_id,
                reply_text,
                parse_mode="HTML",
                reply_markup=create_inline_button()  # Inline buttons for the channel
            )

# Start the bot
bot.polling()