from pyrogram import Client, filters

# Initialize your Pyrogram client
api_id = 24496790
api_hash = '95a711fc46d4293b7b419b9b6389b703'
bot_token = '6728814239:AAFlWCe4xs9Yt8BoZjGUMgxRkMBdlZglndc'

app = Client("my_bot", api_id=api_id, api_hash=api_hash, bot_token=bot_token)

# Define a handler function for processing photos
@app.on_message(filters.photo & filters.private)
def forward_photo_to_channel(client, message):
    # Replace 'YOUR_CHANNEL_ID' with your channel ID
    channel_id = '-1001905486162'

    # Forward the photo to the channel as a photo with a caption
    caption = "Forwarded from user: @" + message.chat.username
    client.send_photo(channel_id, photo=message.photo.file_id, caption=caption)

# Start the bot
app.run()
