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

@app.on_message(filters.photo & filters.private)
def forward_photo_to_channel(client, message):
    channel_id = 'NanoSTestingArea'

    caption = "Forwarded from user: @" + message.chat.username
    
    photo_id = message.photo.file_id
    
    photo_path = os.path.join(photo_folder, f"temp_photo_{photo_id}.jpg")
    message.download(file_name=photo_path)

    with open(photo_path, "rb") as photo_file:
        client.send_photo(channel_id, photo=photo_file, caption=caption)

    time.sleep(5)

    with open(photo_path, "rb") as document_file:
        client.send_document(channel_id, document=document_file, caption=caption)

    os.remove(photo_path)

app.run()
