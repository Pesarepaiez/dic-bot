import telebot
import requests
import time  
import re  
import os

# Your Telegram Bot Token
BOT_TOKEN = "5909441299:AAEv7WSNh2lrRFTa7gAhH9x8wzOembjmD94"
bot = telebot.TeleBot(BOT_TOKEN, parse_mode="HTML")  

# Your Telegram ID (replace with your actual ID)
ADMIN_ID = 6478053466  

# Define user_ids and channel_id
user_ids = set()  # Change to set
channel_id = None  # Variable to store channel ID

USER_IDS_FILE = "user_ids.txt"

def load_user_ids():
    global user_ids
    if os.path.exists(USER_IDS_FILE):
        with open(USER_IDS_FILE, "r") as file:
            user_ids = set(int(line.strip()) for line in file)  # Change to set

def save_user_ids():
    with open(USER_IDS_FILE, "w") as file:
        for user_id in user_ids:
            file.write(f"{user_id}\n")

# Load user IDs when the bot starts
load_user_ids()

# Free Dictionary API URL
DICTIONARY_API_URL = "https://api.dictionaryapi.dev/api/v2/entries/en/"

# File to store blocked users
BLOCKLIST_FILE = "blocked_users.txt"
CHANNEL_ID_FILE = "channel_id.txt"
USER_IDS_FILE = "user_ids.txt"

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

# Load user IDs
def load_user_ids():
    try:
        with open(USER_IDS_FILE, "r") as file:
            return set(file.read().splitlines())
    except FileNotFoundError:
        return set()

user_ids = list(load_user_ids())  # Convert set to list

# Command to add a channel
@bot.message_handler(commands=['addchannel'])
def add_channel(message):
    global channel_id
    if message.from_user.id == ADMIN_ID:
        channel_id = message.chat.id
        bot.reply_to(message, "📢 Channel added!")
    else:
        bot.reply_to(message, "⚠️ You are not authorized to use this command.")

# Command to show statistics
@bot.message_handler(commands=['stats'])
def show_stats(message):
    if message.from_user.id == ADMIN_ID:
        user_count = len(user_ids)
        channel_count = 1 if channel_id else 0
        group_count = 0  # Assuming no groups are being tracked

        stats_message = f"""
📊 <b>Bot Statistics</b> 📊

👥 <b>Total Users:</b> {user_count}
📢 <b>Total Channels:</b> {channel_count}
👥 <b>Total Groups:</b> {group_count}
"""
        bot.reply_to(message, stats_message, parse_mode="HTML")
    else:
        bot.reply_to(message, "⚠️ You are not authorized to use this command.")

# Command to broadcast a message
@bot.message_handler(commands=['broadcast'])
def broadcast_message(message):
    if message.from_user.id == ADMIN_ID:
        broadcast_text = message.text[len('/broadcast '):]
        for user_id in user_ids:
            bot.send_message(user_id, broadcast_text)
        if channel_id:
            bot.send_message(channel_id, broadcast_text)
        bot.reply_to(message, "📢 Message broadcasted!")
    else:
        bot.reply_to(message, "⚠️ You are not authorized to use this command.")

# Handler to forward messages from the admin to all bot users
@bot.message_handler(func=lambda message: message.from_user.id == ADMIN_ID)
def forward_message(message):
    for user_id in user_ids:
        bot.forward_message(user_id, message.chat.id, message.message_id)
    if channel_id:
        bot.forward_message(channel_id, message.chat.id, message.message_id)

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
    # Send the welcome message with inline buttons and list of commands
    bot.reply_to(
        message, 
        """🚀 𝚆𝚎𝚕𝚌𝚘𝚖𝚎 𝚝𝚘 𝚢𝚘𝚞𝚛 𝚞𝚕𝚝𝚒𝚖𝚊𝚝𝚎 𝙳𝚒𝚌𝚝𝚒𝚘𝚗𝚊𝚛𝚢 𝙱𝚘𝚝! 📚🔍
𝙴𝚡𝚌𝚒𝚝𝚎𝚍 𝚝𝚘 𝚍𝚒𝚟𝚎 𝚒𝚗𝚝𝚘 𝚝𝚑𝚎 𝚎𝚗𝚌𝚑𝚊𝚗𝚝𝚒𝚗𝚐 𝚠𝚘𝚛𝚕𝚍 𝚘𝚏 𝚠𝚘𝚛𝚍𝚜? 🌍✨ 

🏆 𝗧𝗿𝘆 𝘀𝗲𝗮𝗿𝗰𝗵𝗶𝗻𝗴 𝗳𝗼𝗿 𝗮𝗻𝘆 𝘄𝗼𝗿𝗱 𝗻𝗼𝘄!

📌 Available Commands:
- /start: Show this welcome message
- /setchannel: Set the channel ID
- /block: Block a user
- /unblock: Unblock a user
- /categories: Show vocabulary categories

📌 join: <a href="https://t.me/+ojJjzjv3CBEyOWZl">𝑬𝒍𝒊𝒕𝒆 𝑻𝑶𝑬𝑭𝑳 𝑨𝒄𝒂𝒅𝒆𝒎𝒚 | 𝚅𝚘𝚌𝚊𝚋𝚞𝚕𝚊𝚛𝚢</a>""",
        parse_mode="HTML",
        reply_markup=create_inline_button()
    )

# Function to load collocations from file
def load_collocations():
    collocations = []
    try:
        with open("collocations.txt", "r", encoding="utf-8") as file:  # Updated file path
            collocations = file.read().split("\n\n")
    except FileNotFoundError:
        pass
    return collocations

# Load collocations from file
collocations_words = load_collocations()

# Function to load words from file
def load_words_from_file(filename):
    words = []
    try:
        with open(filename, "r", encoding="utf-8") as file:
            words = file.read().splitlines()  # Split lines instead of "\n\n"
        print(f"Loaded {len(words)} words from {filename}")  # Debug print
    except FileNotFoundError:
        print(f"File not found: {filename}")  # Debug print
    return words

# Load words for each category from their respective files
collocations_words = load_words_from_file("collocations.txt")
academic_words = load_words_from_file("academic_words.txt")
speaking_topics = load_words_from_file("speaking_topics.txt")
writing_vocabulary = load_words_from_file("writing_vocabulary.txt")
ielts_academic = load_words_from_file("ielts_academic.txt")
ielts_general = load_words_from_file("ielts_general.txt")
duolingo_essential = load_words_from_file("duolingo_essential.txt")
general_academic_vocabulary = load_words_from_file("general_academic_vocabulary.txt")
extensive_reading = load_words_from_file("extensive_reading.txt")
words_400_toefl = load_words_from_file("400_words_toefl.txt")
words_504_essential = load_words_from_file("504_essential_words.txt")
words_4000_essential = load_words_from_file("4000_essential_words.txt")
neo_vocab = load_words_from_file("neo_vocab.txt")
tpo_vocab = load_words_from_file("tpo_vocab.txt")
vocab_for_speaking = load_words_from_file("vocab_for_speaking.txt")
vocab_writing = load_words_from_file("vocab_writing.txt")
biology_vocabulary = load_words_from_file("biology_vocabulary.txt")
astronomy_vocabulary = load_words_from_file("astronomy_vocabulary.txt")
astrology_vocabulary = load_words_from_file("astrology_vocabulary.txt")
business_english_vocabulary = load_words_from_file("business_english_vocabulary.txt")
additional_vocabulary = load_words_from_file("additional_vocabulary.txt")
conversational_vocabulary = load_words_from_file("conversational_vocabulary.txt")
idioms_expressions = load_words_from_file("idioms_expressions.txt")
phrasal_verbs = load_words_from_file("phrasal_verbs.txt")
listening_vocabulary = load_words_from_file("listening_vocabulary.txt")

# Updated vocabulary categories and their words
CATEGORIES = {
    "Academic_Words": academic_words,
    "Speaking_Topics": speaking_topics,
    "Writing_Vocabulary": writing_vocabulary,
    "IELTS_Academic": ielts_academic,
    "IELTS_General": ielts_general,
    "Duolingo_Essential": duolingo_essential,
    "General_Academic_Vocabulary": general_academic_vocabulary,
    "Extensive_Reading": extensive_reading,
    "400_Words_TOEFL": words_400_toefl,
    "504_Essential_Words": words_504_essential,
    "4000_Essential_Words": words_4000_essential,
    "NEO_Vocab": neo_vocab,
    "TPO_Vocab": tpo_vocab,
    "Vocab for Speaking": vocab_for_speaking,
    "Vocab_Writing": vocab_writing,
    "Biology_Vocabulary": biology_vocabulary,
    "Astronomy_Vocabulary": astronomy_vocabulary,
    "Astrology_Vocabulary": astrology_vocabulary,
    "Business_English_Vocabulary": business_english_vocabulary,
    "Additional_Vocabulary": additional_vocabulary,
    "Conversational_Vocabulary": conversational_vocabulary,
    "Idioms_Expressions": idioms_expressions,
    "Phrasal_Verbs": phrasal_verbs,
    "Collocations": collocations_words,
    "Listening_Vocabulary": listening_vocabulary
}

# Function to create inline buttons for categories
def create_category_buttons():
    keyboard = telebot.types.InlineKeyboardMarkup()
    for category in CATEGORIES.keys():
        button = telebot.types.InlineKeyboardButton(text=category, callback_data=category)
        keyboard.add(button)
    return keyboard

# Command to show categories
@bot.message_handler(commands=['categories'])
def show_categories(message):
    bot.reply_to(message, "📚 Choose a vocabulary category:", reply_markup=create_category_buttons())

# Dictionary to keep track of user word batches
user_batches = {}

# Function to create inline button for "Continue"
def create_continue_button():
    keyboard = telebot.types.InlineKeyboardMarkup()
    button_continue = telebot.types.InlineKeyboardButton(text="Continue", callback_data="continue")
    keyboard.add(button_continue)
    return keyboard

# Function to send the next word
def send_next_word(chat_id, user_id):
    category, index = user_batches[user_id]
    words = CATEGORIES[category]
    
    if index < len(words):
        word_entry = words[index]
        bot.send_message(chat_id, word_entry, parse_mode="HTML", reply_markup=create_continue_button())
        
        user_batches[user_id] = (category, index + 1)
    else:
        bot.send_message(chat_id, "No more words in this category.", parse_mode="HTML")

# Function to send all content from the category file
def send_category_content(chat_id, category):
    words = CATEGORIES[category]
    message_chunks = []
    current_chunk = ""

    for word in words:
        if len(current_chunk) + len(word) + 1 > 4096:  # Telegram message limit
            message_chunks.append(current_chunk)
            current_chunk = word + "\n"
        else:
            current_chunk += word + "\n"

    if current_chunk:
        message_chunks.append(current_chunk)

    for chunk in message_chunks:
        bot.send_message(chat_id, chunk, parse_mode="HTML")

# Handle category button clicks
@bot.callback_query_handler(func=lambda call: call.data in CATEGORIES)
def send_category_words(call):
    category = call.data
    send_category_content(call.message.chat.id, category)

# Handle "Continue" button clicks
@bot.callback_query_handler(func=lambda call: call.data == "continue")
def handle_continue(call):
    user_id = call.from_user.id
    if user_id in user_batches:
        send_next_word(call.message.chat.id, user_id)

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
        return None, None, None, None  # Add examples to return values
    
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
        pronunciation = data[0].get('phonetic', 'N/A')  # Get pronunciation if available
        examples = data[0]['meanings'][0]['definitions'][0].get('example', 'No example available.')  # Get example sentences
        
        # Handle multiple examples
        example_list = data[0]['meanings'][0]['definitions'][0].get('examples', [])
        if example_list:
            examples = "\n".join([f"{i+1}. {ex}" for i, ex in enumerate(example_list)])
        
        return part_of_speech, meaning, pronunciation, examples
    return None, None, None, None

# Handle words input
@bot.message_handler(func=lambda message: True)
def send_definition(message):
    if str(message.from_user.id) in blocked_users:
        return  

    words = clean_words(message.text)  # Clean the input text

    for word in words:
        part_of_speech, meaning, pronunciation, examples = get_definition(word, message.from_user)
        
        if part_of_speech and meaning:
            reply_text = f"""
📚 <b>{word.capitalize()}</b>    {pronunciation}  
🏷 <i>{part_of_speech}</i>  

📖 <b>Definition:</b>  
🔹 {meaning}  

📖 <b>Example:</b>  
{examples}  
━━━━━━━━━━━━━━━━━━━━━━━
<a href="https://t.me/MomeniTOEFL">Join 𝑬𝒍𝒊𝒕𝒆 𝑻𝑶𝑬𝑭𝑳 𝑨𝒄𝒂𝒅𝒆𝒎𝒚🔗</a>
"""
            bot.reply_to(message, reply_text, parse_mode="HTML")

            # Send to the set channel if available
            if channel_id:
                channel_message = f"""
📚 <b>{word.capitalize()}</b>    {pronunciation}  
🏷 <i>{part_of_speech}</i>  

📖 <b>Definition:</b>  
🔹 {meaning}  

📖 <b>Example:</b>  
{examples}  
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
