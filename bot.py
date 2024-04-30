from pyrogram import Client, filters
from pyrogram.types import InputMediaPhoto, InputMediaDocument

# Initialize your Pyrogram client
api_id = 24496790
api_hash = '95a711fc46d4293b7b419b9b6389b703'
bot_token = '6728814239:AAFlWCe4xs9Yt8BoZjGUMgxRkMBdlZglndc'

app = Client("my_bot", api_id=api_id, api_hash=api_hash, bot_token=bot_token)

# Define a handler function for processing photos
@app.on_message(filters.photo)
def forward_photo_to_channel(client, message):
    # Replace 'YOUR_CHANNEL_ID' with your channel ID
    channel_id = '-1001905486162'

    # Forward the photo to the channel as a photo with a caption
    caption = "Forwarded from user: @" + message.chat.username
    client.forward_messages(channel_id, message.chat.id, message.message_id, caption=caption)

    # Also, send the photo as a document to the channel
    document = InputMediaDocument(message.photo.file_id, caption=caption)
    client.send_media_group(channel_id, [document])

# Start the bot
app.run()
