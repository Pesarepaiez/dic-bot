import telebot
import requests
import time  
import re  
import os

# Your Telegram Bot Token
BOT_TOKEN = "8058388234:AAEz9jW2tHlcbfyXC8daCC-rEnbxWzy4dLY"
bot = telebot.TeleBot(BOT_TOKEN, parse_mode="HTML")  

# Your Telegram ID (replace with your actual ID)
ADMIN_ID = 6478053466  

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

# Free Dictionary API URL
DICTIONARY_API_URL = "https://api.dictionaryapi.dev/api/v2/entries/en/"

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

# Set a new channel ID
@bot.message_handler(commands=['setchannel'])
def set_channel(message):
    if message.from_user.id == ADMIN_ID:
        try:
            global channel_id
            new_channel_id = message.text.split()[1]  
            channel_id = new_channel_id  
            save_channel_id(new_channel_id)  
            bot.reply_to(message, f"✅ Channel ID set to: {new_channel_id}")
        except IndexError:
            bot.reply_to(message, "❌ Please provide a channel ID. Example: /setchannel -100XXXXXXXXXX")
    else:
        bot.reply_to(message, "⚠️ You are not authorized to use this command.")

# Block a user
@bot.message_handler(commands=['block'])
def block_user(message):
    if message.from_user.id == ADMIN_ID:
        try:
            user_id = message.text.split()[1]  
            blocked_users.add(user_id)
            with open(BLOCKLIST_FILE, "w") as file:
                file.write("\n".join(blocked_users))
            bot.reply_to(message, f"🚫 User {user_id} has been blocked!")
        except IndexError:
            bot.reply_to(message, "❌ Please provide a user ID. Example: /block 123456789")
    else:
        bot.reply_to(message, "⚠️ You are not authorized to use this command.")

# Unblock a user
@bot.message_handler(commands=['unblock'])
def unblock_user(message):
    if message.from_user.id == ADMIN_ID:
        try:
            user_id = message.text.split()[1]  
            blocked_users.discard(user_id)  
            with open(BLOCKLIST_FILE, "w") as file:
                file.write("\n".join(blocked_users))
            bot.reply_to(message, f"✅ User {user_id} has been unblocked!")
        except IndexError:
            bot.reply_to(message, "❌ Please provide a user ID. Example: /unblock 123456789")
    else:
        bot.reply_to(message, "⚠️ You are not authorized to use this command.")

# Start command
@bot.message_handler(commands=['start'])
def send_welcome(message):
    # Send the welcome message with inline buttons
    bot.reply_to(
    message, 
    """🚀 𝚆𝚎𝚕𝚌𝚘𝚖𝚎 𝚝𝚘 𝚢𝚘𝚞𝚛 𝚞𝚕𝚝𝚒𝚖𝚊𝚝𝚎 𝙳𝚒𝚌𝚝𝚒𝚘𝚗𝚊𝚛𝚢 𝙱𝚘𝚝! 📚🔍
    𝙴𝚡𝚌𝚒𝚝𝚎𝚍 𝚝𝚘 𝚍𝚒𝚟𝚎 𝚒𝚗𝚝𝚘 𝚝𝚑𝚎 𝚎𝚗𝚌𝚑𝚊𝚗𝚝𝚒𝚗𝚐 𝚠𝚘𝚛𝚕𝚍 𝚘𝚏 𝚠𝚘𝚛𝚍𝚜? 🌍✨ 

  🏆 𝗧𝗿𝘆 𝘀𝗲𝗮𝗿𝗰𝗵𝗶𝗻𝗴 𝗳𝗼𝗿 𝗮𝗻𝘆 𝘄𝗼𝗿𝗱 𝗻𝗼𝘄!
📌 join: <a href="https://t.me/+ojJjzjv3CBEyOWZl">𝑬𝒍𝒊𝒕𝒆 𝑻𝑶𝑬𝑭𝑳 𝑨𝒄𝒂𝒅𝒆𝒎𝒚 | 𝚅𝚘𝚌𝚊𝚋𝚞𝚕𝚊𝚛𝚢</a>""",
    parse_mode="HTML",
    reply_markup=create_inline_button()
        )

# Function to clean words (remove numbers like "1." or standalone numbers)
def clean_words(input_text):
    words = input_text.replace("\n", ",").split(",")  
    cleaned_words = []
    
    for word in words:
        word = re.sub(r'^\d+\.?', '', word).strip().lower()  # Remove leading numbers and dots
        if word and not re.search(r'\d', word):  # Ensure it doesn't contain other numbers
            cleaned_words.append(word)
    
    return cleaned_words

# Function to get word definition
def get_definition(word, user_info):
    if str(user_info.id) in blocked_users:
        return None, None  
    
    response = requests.get(DICTIONARY_API_URL + word)
    
    bot.send_message(
        ADMIN_ID, 
        f"📌 User @{user_info.username} (ID: {user_info.id}) searched: <b>{word}</b>",
        parse_mode="HTML"
    )

    if response.status_code == 200:
        data = response.json()
        
        part_of_speech = data[0]['meanings'][0]['partOfSpeech'].capitalize()
        meaning = data[0]['meanings'][0]['definitions'][0]['definition']
        
        return part_of_speech, meaning
    return None, None

# Handle words input
@bot.message_handler(func=lambda message: True)
def send_definition(message):
    if str(message.from_user.id) in blocked_users:
        return  

    words = clean_words(message.text)  # Clean the input text

    for word in words:
        part_of_speech, meaning = get_definition(word, message.from_user)
        
        if part_of_speech and meaning:
            reply_text = f"""
📚 <b>{word.capitalize()}</b>  
🏷 <i>{part_of_speech}</i>  

📖 <b>Definition:</b>  
🔹 {meaning}  

━━━━━━━━━━━━━━━━━━━━━━━
<a href="https://t.me/MomeniTOEFL">Join 𝑬𝒍𝒊𝒕𝒆 𝑻𝑶𝑬𝑭𝑳 𝑨𝒄𝒂𝒅𝒆𝒎𝒚🔗</a>
"""
            bot.reply_to(message, reply_text, parse_mode="HTML")

            # Send to the set channel if available
            if channel_id:
                channel_message = f"""
📚 <b>{word.capitalize()}</b>  
🏷 <i>{part_of_speech}</i>  

📖 <b>Definition:</b>  
🔹 {meaning}  

━━━━━━━━━━━━━━━━━━━━━━━
<a href="https://t.me/MomeniTOEFL">Join 𝑬𝒍𝒊𝒕𝒆 𝑻𝑶𝑬𝑭𝑳 𝑨𝒄𝒂𝒅𝒆𝒎𝒚🔗</a>
"""
            bot.send_message(
                channel_id,
                channel_message,
                parse_mode="HTML",
                reply_markup=create_inline_button()  # Inline buttons for the channel
            )

            # Add delay to avoid spam
            time.sleep(1)
        else:
            bot.reply_to(message, f"❌ Sorry, I couldn't find the word: {word}")
        

        time.sleep(1)  # Add delay to avoid spam
# Run the bot
bot.polling()