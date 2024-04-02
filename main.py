import argparse
import os
import random
import requests
import telegram
import time
from dotenv import load_dotenv


def download_comics(url, filename):
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

    current_comics_url = 'https://xkcd.com/info.0.json'
    current_comics_response = requests.get(current_comics_url)
    current_comics_response.raise_for_status()
    current_comics_id = current_comics_response.json()['num']

    while True:
        comics_id = random.randint(1, current_comics_id)
        comics_url = f'https://xkcd.com/{comics_id}/info.0.json'
        comics_response = requests.get(comics_url)
        comics_response.raise_for_status()
        image_url = comics_response.json()['img']
        comment = comics_response.json()['alt']
        filename = 'comics.png'
        download_comics(image_url, filename)
        with open(filename, 'rb') as document:
            bot.send_document(
                chat_id=args.chat_id,
                document=document,
                caption=comment
            )
        os.remove(filename)
        time.sleep(args.interval)


if __name__ == '__main__':
    main()
