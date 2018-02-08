import json
import re
from datetime import datetime

import redis
import requests
import unidecode
from bs4 import BeautifulSoup
from fbmq import Page, Template

from Constants import *

conn = redis.Redis(REDIS_HOST)


def clean_text(raw_text):
    clean_title = raw_text.replace("\n", " ")
    clean_title = re.sub(r" +", " ", clean_title)
    clean_title = unidecode.unidecode(clean_title)
    clean_title = clean_title.strip()
    return clean_title


def download_news(url, news_section):
    """ Download only news if is not on redis cache
        @param url <String> url from news section
        @param news_section <String> news section from newspaper
    """
    redis_key = datetime.today().strftime("%d-%m-%Y") + "-" + news_section
    if conn.llen(redis_key) > 0:
        #We have news of this section from today
        return
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    for item in soup.find_all('a', href=True):
        if NEWSPAPER_PAGE in item["href"] and news_section in item["href"]:
            images = item.findChildren('img')
            titles = item.findChildren("span", {
                "class": "item-titulo-nota-canal"
            })
            subtitles = item.findChildren("span", {"class": "nota-flujo-hora"})
            if not images or not titles or not subtitles:
                continue
            title = clean_text(titles[0].text)
            subtitle = clean_text(subtitles[0].parent.text.split("\n")[2])

            news_dump = json.dumps({
                "url": item["href"],
                "img": images[0]["src"],
                "title": title,
                "subtitle": subtitle
            })
            conn.rpush(redis_key, news_dump)


def build_template(url, image, title, subtitle):
    return Template.GenericElement(
        title,
        subtitle=subtitle,
        image_url=image,
        item_url=url,
        buttons=[
            Template.ButtonWeb("Leer nota", url),
            Template.ButtonPostBack("Recibir mas noticias de  este tipo",
                                    POSTBACK_MORE),
        ])


def send_news(news_section="nacional", recipient_id = "1793673450643455"):
    page = Page(FACEBOOK_TOKEN)
    download_news(NEWSPAPER_PAGE+news_section, news_section)
    redis_key = datetime.today().strftime("%d-%m-%Y") + "-" + news_section
    news = []
    for idx in range(conn.llen(redis_key)):
        item = json.loads(conn.lindex(redis_key, idx))
        template = build_template(item["url"], item["img"], item["title"],
                                  item["subtitle"])
        news.append(template)
    page.send(recipient_id, Template.Generic(news))
