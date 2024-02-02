import requests
import logging
from telegram.ext import *
from telegram.ext import Updater, CommandHandler
import responses


def send_message_to_telegram_bot(bot_token, chat_id, message):
    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    params = {
        "chat_id": chat_id,
        "text": message
    }
    response = requests.post(url, params=params)
    updates_data = response.json()
    if response.status_code == 200:
        print("Message sent successfully!")
    else:
        print("Failed to send message.")
bot_token = "6923769393:AAE4JNy4bTkBvchtDE5AJAZjTpd4O1F5JmA"
chat_id = "5158199727"
# Replace with your scraped data
url = 'https://addismercato.com/'





response = requests.get(url)
content = response.content
from bs4 import BeautifulSoup
soup = BeautifulSoup(content, 'html.parser')

category = soup.find_all('h5', class_="product-name")
catli = [h5.text for h5 in category[:11]]  # Limit to the first 5 elements


price = soup.find_all('span', class_="product-price")
pricloop = [span.text for span in price[:11]]  # Limit to the first 5 elements





# Concatenate all categories into a single string
scraped_data = '\n'.join(catli) 



logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logging.info('starting bot...')
# Send the concatenated data as one message to the Telegram bot

def command1(update, context):
 messages = []
 for product_name, product_price in zip(catli, pricloop):
    message = f"Product: {product_name}\nPrice: {product_price}\n\n"
    messages.append(message)  # Add the message to the list    
    
 final_message = ''.join(messages)
 send_message_to_telegram_bot(bot_token, chat_id, final_message.strip())


def mess_handl(update, context):
   text = str(update.message.text).lower()
   logging.info(f'user ({update.message.chat.id}) sayes: {text}')

   update.message.reply_text(text)


def error(update, context):
   logging.error(f'update {update} cused error {context.error}')



if __name__ == '__main__':
    updater = Updater(bot_token, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler('command1', command1))

    dp.add_handler(MessageHandler(Filters.text, mess_handl))
    dp.add_error_handler(error)

    updater.start_polling(1.0)
    updater.idel()
