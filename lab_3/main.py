import re
import os

import pandas as pd
import checksum as check


REGULARS ={
    "email": r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$",
    "http_status_message": r"^\d{3} [A-Za-z ]+$",
    "inn": r"",
    "passport": r"^\d{2}\s\d{2}\s\d{6}$",
    "ip_v4": r"^(([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])\.){3}([0-9]|"
             r"[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])$",
    "latitude": r"^\-?(180|1[0-7][0-9]|\d{1,2})\.\d+$",
    "hex_color": r"^#[0-9a-fA-F]{6}$",
    "isbn": r"(\d{3}-)?\d-(\d{5})-(\d{3})-\d",
    "uuid": r"",
    "time": r"^\d{2}:\d{2}:\d{2}\.\d{6}$"
}


def open_csv(path : str) -> pd.DataFrame:
    """
    function open csv file and get out info
    :param path: str
    :return: DataFrame
    """
    data = pd.read_csv(path, encoding="utf-16", sep=";")
    return data


if __name__ == "__main__":