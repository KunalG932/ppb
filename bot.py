from pyrogram import Client, filters
import os
import time

api_id = 24496790
api_hash = '95a711fc46d4293b7b419b9b6389b703'
bot_token = '6728814239:AAFlWCe4xs9Yt8BoZjGUMgxRkMBdlZglndc'

app = Client("my_bot", api_id=api_id, api_hash=api_hash, bot_token=bot_token)

photo_folder = "photos"
if not os.path.exists(photo_folder):
    os.makedirs(photo_folder)

# Dictionary to store chat ID and their respective photo captions
photo_captions = {}

@app.on_message(filters.photo & filters.private)
def ask_for_caption(client, message):
    # Save the chat ID to associate with the photo captions
    photo_captions[message.chat.id] = {'photo_ids': [], 'caption': None}

    # Save the photo IDs
    for photo in message.photo:
        photo_id = photo.file_id
        photo_captions[message.chat.id]['photo_ids'].append(photo_id)

    # Send a message asking for a caption
    client.send_message(message.chat.id, "Send me a caption for the photos.")

@app.on_message(filters.text & filters.private)
def handle_caption(client, message):
    chat_id = message.chat.id
    if chat_id in photo_captions:
        if photo_captions[chat_id]['caption'] is None:
            # Associate the caption with the chat ID
            photo_captions[chat_id]['caption'] = message.text

            # Forward the photos and documents to the channel with the provided caption
            forward_photos_and_documents(client, chat_id)

            # Clean up the dictionary entry
            del photo_captions[chat_id]

def forward_photos_and_documents(client, chat_id):
    channel_id = 'NanoSTestingArea'
    caption = f"Forwarded from user: @{app.get_me().username}\n\n{photo_captions[chat_id]['caption']}"

    # Get photo IDs and caption from the dictionary
    photo_ids = photo_captions[chat_id]['photo_ids']

    # Download photos to temporary files
    photo_paths = []
    for photo_id in photo_ids:
        photo_path = os.path.join(photo_folder, f"temp_photo_{photo_id}.jpg")
        app.download_media(message=photo_id, file_name=photo_path)
        photo_paths.append(photo_path)

    # Send group media to channel
    media_group = []
    for photo_path in photo_paths:
        with open(photo_path, "rb") as photo_file:
            media_group.append({"type": "photo", "media": photo_file})
    client.send_media_group(channel_id, media=media_group, caption=caption)

    # Wait for a short time to avoid rate limits
    time.sleep(2)

    # Send documents to channel one by one
    for photo_path in photo_paths:
        with open(photo_path, "rb") as document_file:
            client.send_document(channel_id, document=document_file, caption=caption)

    # Clean up: delete the temporary photo files
    for photo_path in photo_paths:
        os.remove(photo_path)

# Start the bot
app.run()
