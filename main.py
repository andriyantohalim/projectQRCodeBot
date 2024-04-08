import os
import asyncio

from dotenv import load_dotenv, find_dotenv
import qrcode.constants
from telebot.async_telebot import AsyncTeleBot
import qrcode

load_dotenv(find_dotenv())

TELEGRAM_PROJECT_QR_BOT_TOKEN = os.environ.get("TELEGRAM_PROJECT_QR_BOT_TOKEN")

bot = AsyncTeleBot(TELEGRAM_PROJECT_QR_BOT_TOKEN)


# Start Handler and Help Handler
@bot.message_handler(commands=['start'])
async def start_cmd_handler(message):
    bot_reply = f"""
                Hello {message.chat.first_name}. 
                Use /qr followed by URL or text to generate the QR. 
                """

    splitted_reply = bot_reply.split(". ")

    for sentence in splitted_reply:
        await bot.send_message(message.chat.id, sentence)


# QR Code generator
@bot.message_handler(commands=['qr'])
async def main_chat_handler(message):
    qr_data = message.text.strip("/qr")

    # Creating a new QR code
    qr = qrcode.QRCode( 
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=8,
        border=4,
        )
    
    qr.add_data(f"{qr_data}")

    # Generating the QR code
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    img.save("qr.png")
    qr_photo = open('qr.png', 'rb')
    
    # Generating the QR code caption
    qr_caption_text = f"QR Code for {qr_data}. \nGenerated by @HalimQR_bot"

    await bot.send_photo(message.chat.id, photo=qr_photo, caption=qr_caption_text)


if __name__ == "__main__":
    print("Starting bot")
    asyncio.run(bot.polling())
