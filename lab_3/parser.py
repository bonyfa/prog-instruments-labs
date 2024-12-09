import logging
import os
import random
from time import sleep

import argparse
import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
from typing import List


URL = "https://akbotadoya.ru/akkumulyatory?page="

def parse_arguments() -> argparse:
    """
            Получаем ссылку путь директории и количество страниц

    """
    parser = argparse.ArgumentParser(description="Скрипт для парсинга рецензий с сайта и сортировка их на хорошии и плохие")
    parser.add_argument("--out_dir", type=str, default="dataset", help="Путь к директории для сохранения датасета")
    parser.add_argument("--urls", type=str, default="https://akbotadoya.ru/akkumulyatory?page=", help="Базовый URL для сбора данных")
    parser.add_argument("--pages", type=int, default=3, help="Количество страниц для обхода")
    return parser.parse_args()

def get_html_code(page: int , url: str) -> BeautifulSoup:
    """
               Получаем html код страницы.

    """

    try:
        tmp_url = url+str(page)
        sleep_time = random.uniform(1, 3)
        sleep(sleep_time)
        headers = {
            "User-Agent": random_user_agent()
        }
        tmp_res = requests.get(tmp_url, headers=headers)
        tmp_res.raise_for_status()
        soup = BeautifulSoup(tmp_res.content, "html.parser")
        return soup
    except requests.exceptions.RequestException as e:
        logging.exception(f"Ошибка при получении html кода")
        return None

def random_user_agent() -> str:
    u = UserAgent()
    return u.random

if __name__ == "__main__":
    args = parse_arguments()
    string = get_html_code(1, URL)
    print(string)
    print("sdad")

