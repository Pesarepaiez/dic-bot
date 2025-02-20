import telebot
<<<<<<< HEAD

API_TOKEN = '8122882322:AAFc9SNrdpq_nd1vY3dUsD53PTodKj16bMk'

bot = telebot.TeleBot(API_TOKEN)

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, "Hello, World!")

if __name__ == "__main__":
    bot.polling()
=======
import requests
import time  
import re  
import os
from dictionary_api import get_word_definition  # Import the function from dictionary_api.py

# Your Telegram Bot Token
BOT_TOKEN = "8122882322:AAFc9SNrdpq_nd1vY3dUsD53PTodKj16bMk"
bot = telebot.TeleBot(BOT_TOKEN, parse_mode="HTML")  

# Your Telegram ID (replace with your actual ID)
ADMIN_ID = YOUR_ADMIN_ID_HERE  

# Add buttons for the 12 channels (with links)
def create_inline_button():
    keyboard = telebot.types.InlineKeyboardMarkup()
    # ...existing code...
    return keyboard

# File to store blocked users
BLOCKLIST_FILE = "blocked_users.txt"
CHANNEL_ID_FILE = "channel_id.txt"

# Load blocked users
def load_blocked_users():
    # ...existing code...

blocked_users = load_blocked_users()

# Load channel ID
def load_channel_id():
    # ...existing code...

channel_id = load_channel_id()

# Save channel ID
def save_channel_id(new_channel_id):
    # ...existing code...

# Set a new channel ID
@bot.message_handler(commands=['setchannel'])
def set_channel(message):
    # ...existing code...

# Block a user
@bot.message_handler(commands=['block'])
def block_user(message):
    # ...existing code...

# Unblock a user
@bot.message_handler(commands=['unblock'])
def unblock_user(message):
    # ...existing code...

# Start command
@bot.message_handler(commands=['start'])
def send_welcome(message):
    # ...existing code...

# Function to clean words (remove numbers like "1." or standalone numbers)
def clean_words(input_text):
    # ...existing code...

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
>>>>>>> d318d65a185e11015c8d02529a07cb8b00a028ba
