import json
import requests
import re

from collections import OrderedDict
from bs4 import BeautifulSoup


table = {
    "১": "1",
    "২": "2",
    "৩": "3",
    "৪": "4",
    "৫": "5",
    "৬": "6",
    "৭": "7",
    "৮": "8",
    "৯": "9",
    "০": "0",
}

table = {ord(k): ord(v) for k, v in table.items()}


def scrape(biodata_number):
    url = f"https://ordhekdeen.com/biodatas/{biodata_number}/"

    info_dict = OrderedDict()

    def parse(value):
        for match in soup.find_all(**{"class": value}):
            key = match.label.string
            value = " ".join(p.string for p in match.find_all('p') if p.string)
            info_dict[key] = value.translate(table)

    r = requests.get(url)

    if r.status_code == 200:
        info_dict["_id"] = biodata_number

        soup = BeautifulSoup(r.text, "html.parser")

        for value in ["profile-info-item", "each-pii selectbox", "each-pii textarea", "each-pii textbox"]:
            parse(value)

        for name in re.findall("bp-field-name bp-field-id-[0-9]+", r.text):
            key = soup.find(**{'class': name}).string
            value = soup.find(**{'class': name.replace("name", "value")}).p.string
            info_dict[key] = value.translate(table)

        return json.dumps(info_dict)
