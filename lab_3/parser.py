import logging
import os
import random
from time import sleep

import argparse
import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
from typing import List


def parse_arguments() -> argparse:
    """
            Получаем ссылку путь директории и количество страниц

    """
    parser = argparse.ArgumentParser(description="Скрипт для парсинга рецензий с сайта и сортировка их на хорошии и плохие")
    parser.add_argument("--out_dir", type=str, default="dataset", help="Путь к директории для сохранения датасета")
    parser.add_argument("--urls", type=str, default="https://akbotadoya.ru/akkumulyatory?page=", help="Базовый URL для сбора данных")
    parser.add_argument("--pages", type=int, default=3, help="Количество страниц для обхода")
    return parser.parse_args()