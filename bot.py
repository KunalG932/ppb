from pyrogram import Client, filters
import os
import time

# Initialize your Pyrogram client
api_id = 24496790
api_hash = '95a711fc46d4293b7b419b9b6389b703'
bot_token = '6728814239:AAFlWCe4xs9Yt8BoZjGUMgxRkMBdlZglndc'

app = Client("my_bot", api_id=api_id, api_hash=api_hash, bot_token=bot_token)

# Create a folder to save photos if it doesn't exist
photo_folder = "photos"
if not os.path.exists(photo_folder):
    os.makedirs(photo_folder)

# Define a handler function for processing photos
@app.on_message(filters.photo & filters.private)
def forward_photo_to_channel(client, message):
    # Replace 'YOUR_CHANNEL_ID' with your channel ID
    channel_id = 'NanoSTestingArea'  # Replace with your channel ID

    # Forward the photo to the channel as a photo with a caption
    caption = "Forwarded from user: @" + message.chat.username
    
    # Get the unique file ID of the photo
    photo_id = message.photo.file_id
    
    # Save the photo in the photo folder using the file ID as the filename
    photo_path = os.path.join(photo_folder, f"temp_photo_{photo_id}.jpg")
    message.download(file_name=photo_path)

    # Send the photo to the channel
    with open(photo_path, "rb") as photo_file:
        client.send_photo(channel_id, photo=photo_file, caption=caption)

    # Wait for 5 seconds
    time.sleep(5)

    # Send the photo as a document to the channel
    client.send_document(channel_id, document=photo_path, caption=caption)

    # Clean up: delete the temporary photo file
    os.remove(photo_path)

# Start the bot
app.run()
