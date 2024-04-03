import argparse
import os
import random
import requests
import telegram
import time
from dotenv import load_dotenv


def publish_comic(url, bot, filename, chat_id):
    response = requests.get(url)
    response.raise_for_status()
    comic = response.json()
    image_url = comic['img']
    comment = comic['alt']
    download_comic(image_url, filename)
    with open(filename, 'rb') as document:
        bot.send_document(
            chat_id=chat_id,
            document=document,
            caption=comment
        )


def download_comic(url, filename):
    response = requests.get(url)
    response.raise_for_status()
    with open(filename, 'wb') as file:
        file.write(response.content)


def main():
    load_dotenv()
    bot = telegram.Bot(token=os.environ['TELEGRAM_BOT_TOKEN'])

    parser = argparse.ArgumentParser(
        description='Публикация комиксов в Telegram чате'
    )
    parser.add_argument(
        "--chat_id",
        required=True,
        help='Cсылка на чат, например, @chatChat'
    )
    parser.add_argument(
        "--interval",
        type=int,
        default=86400,
        help='Частота публикаций'
    )
    args = parser.parse_args()

    current_comic_url = 'https://xkcd.com/info.0.json'
    current_comic_response = requests.get(current_comic_url)
    current_comic_response.raise_for_status()
    current_comic_id = current_comic_response.json()['num']

    while True:
        comic_id = random.randint(1, current_comic_id)
        comic_url = f'https://xkcd.com/{comic_id}/info.0.json'
        filename = 'comic.png'
        try:
            publish_comic(comic_url, bot, filename, args.chat_id)
        finally:
            os.remove(filename)
        time.sleep(args.interval)


if __name__ == '__main__':
    main()
