from pyrogram import Client, filters
from pyrogram.types import ReplyKeyboardMarkup, KeyboardButton
import os
import time

api_id = 24496790
api_hash = '95a711fc46d4293b7b419b9b6389b703'
bot_token = '7038639427:AAEPN0kz8qjQklDdSXY-G5UWJqn5uTFzBL8'

app = Client("my_bot", api_id=api_id, api_hash=api_hash, bot_token=bot_token)

photo_folder = "photos"
if not os.path.exists(photo_folder):
    os.makedirs(photo_folder)

# Dictionary to store chat ID and their respective photo captions
photo_captions = {}

# Function to send a message with a custom keyboard
def send_keyboard_message(chat_id):
    keyboard = ReplyKeyboardMarkup(
        [
            [KeyboardButton("Single Photo")],
            [KeyboardButton("Double Photo")],
            [KeyboardButton("Triple Photo")],
            [KeyboardButton("Group Photo")]
        ],
        resize_keyboard=True
    )
    app.send_message(chat_id, "Select an option:", reply_markup=keyboard)

# Handler for /start command to send the keyboard
@app.on_message(filters.command("start") & filters.private)
def start(client, message):
    send_keyboard_message(message.chat.id)

@app.on_message(filters.private)
def handle_private_message(client, message):
    chat_id = message.chat.id
    text = message.text.lower()
    if text == "single photo":
        # Send a message asking for a photo
        app.send_message(chat_id, "Send me a photo.")
    elif text == "double photo":
        forward_photos(client, chat_id, 2)
    elif text == "triple photo":
        forward_photos(client, chat_id, 3)
    elif text == "group photo":
        forward_photos(client, chat_id, 4)
    else:
        send_keyboard_message(chat_id)

# Handler for receiving photo
@app.on_message(filters.photo & filters.private)
def handle_photo(client, message):
    chat_id = message.chat.id
    photo_id = message.photo.file_id

    # Save the photo to a folder
    photo_file_path = os.path.join(photo_folder, f"temp_photo_{photo_id}.jpg")
    message.download(file_name=photo_file_path)

    # Prompt the user for a caption
    app.send_message(chat_id, "Send me a caption for the photo. Please provide two texts separated by '|'.")
    
# Handler for text after sending photo
@app.on_message(filters.text & filters.private)
def handle_caption(client, message):
    chat_id = message.chat.id
    if chat_id in photo_captions:
        if photo_captions[chat_id]['caption'] is None:
            # Split the caption into two parts
            caption_parts = message.text.split('|')
            if len(caption_parts) == 2:
                # Associate the caption with the chat ID
                photo_captions[chat_id]['caption'] = f"💎≻───「ᴘʀᴇᴠɪᴇᴡ」───\n├ ⚝ #{caption_parts[0].strip()}\n├ ⚝ #{caption_parts[1].strip()}\n╰──❯ ❲@Silverwing_Den❳"

                # Forward the photos to the channel with the provided caption
                forward_photos(client, chat_id)

                # Clean up the dictionary entry and delete the photo file
                del photo_captions[chat_id]
                photo_ids = photo_captions[chat_id]['photo_ids']
                for photo_id in photo_ids:
                    photo_file_path = os.path.join(photo_folder, f"temp_photo_{photo_id}.jpg")
                    os.remove(photo_file_path)
                del photo_captions[chat_id]

            else:
                # If the format is incorrect, ask the user to resend the caption
                app.send_message(chat_id, "Please provide the caption in the correct format. Two texts separated by '|'.")

def forward_photos(client, chat_id, photo_count):
    channel_id = 'NanoSTestingArea'
    caption = f"💎≻───「ᴘʀᴇᴠɪᴇᴡ」───\n"

    # Get photo IDs and caption from the dictionary
    photo_ids = photo_captions[chat_id]['photo_ids'][:photo_count]

    # Send photos to channel with the caption
    for photo_id in photo_ids:
        photo_file_path = os.path.join(photo_folder, f"temp_photo_{photo_id}.jpg")
        with open(photo_file_path, "rb") as photo_file:
            client.send_photo(channel_id, photo=photo_file, caption=caption)

    # Clean up: delete the temporary photo files
    for photo_id in photo_ids:
        photo_file_path = os.path.join(photo_folder, f"temp_photo_{photo_id}.jpg")
        os.remove(photo_file_path)

# Start the bot
app.run()
