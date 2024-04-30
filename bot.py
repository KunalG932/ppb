from pyrogram import Client, filters
import os
import time

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
    photo_path = f"temp_photo_{time.time()}.jpg"
    
    try:
        # Download the photo
        message.download(file_name=photo_path)
        
        # Open the photo file and send it as a photo
        with open(photo_path, "rb") as photo_file:
            client.send_photo(channel_id, photo=photo_file, caption=caption)

        # Wait for 5 seconds
        time.sleep(5)

        # Send the photo as a document to the channel
        client.send_document(channel_id, document=photo_path, caption=caption)
        
    except FileNotFoundError:
        print("Error: Photo file not found")
    finally:
        # Clean up: delete the temporary photo file
        if os.path.exists(photo_path):
            os.remove(photo_path)

# Start the bot
app.run()
