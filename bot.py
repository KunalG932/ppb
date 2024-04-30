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
    # Save the chat ID to associate with the photo caption
    photo_captions[message.chat.id] = {}

    # Send a message asking for a caption
    client.send_message(message.chat.id, "Send me a caption for the photo and document.")

    # Save the photo ID
    photo_id = message.photo.file_id
    photo_captions[message.chat.id]['photo_id'] = photo_id

@app.on_message(filters.text & filters.private)
def handle_caption(client, message):
    chat_id = message.chat.id
    if chat_id in photo_captions:
        if 'photo_id' in photo_captions[chat_id]:
            # Associate the caption with the photo ID
            photo_captions[chat_id]['caption'] = message.text

            # Forward the photo and document to the channel with the provided caption
            forward_photo_and_document(client, chat_id)

            # Clean up the dictionary entry
            del photo_captions[chat_id]

def forward_photo_and_document(client, chat_id):
    channel_id = 'NanoSTestingArea'
    caption = f"{photo_captions[chat_id]['caption']}"

    # Get photo ID and caption from the dictionary
    photo_id = photo_captions[chat_id]['photo_id']

    # Download photo to a temporary file
    photo_path = os.path.join(photo_folder, f"temp_photo_{photo_id}.jpg")
    app.download_media(photo_id, file_name=photo_path)

    # Send photo to channel
    with open(photo_path, "rb") as photo_file:
        client.send_photo(channel_id, photo=photo_file, caption=caption)

    time.sleep(5)

    # Send document to channel
    with open(photo_path, "rb") as document_file:
        client.send_document(channel_id, document=document_file, caption=caption)

    # Clean up: delete the temporary photo file
    os.remove(photo_path)

# Start the bot
app.run()
