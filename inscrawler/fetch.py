from time import sleep
from .settings import settings
import re


def get_parsed_mentions(raw_text):
    regex = re.compile(r"@([\w\.]+)")
    regex.findall(raw_text)
    return regex.findall(raw_text)


def get_parsed_hashtags(raw_text):
    regex = re.compile(r"#(\w+)")
    regex.findall(raw_text)
    return regex.findall(raw_text)


def fetch_mentions(raw_test, dict_obj):
    if not settings.fetch_mentions:
        return

    mentions = get_parsed_mentions(raw_test)
    if mentions:
        dict_obj['mentions'] = mentions


def fetch_hashtags(raw_test, dict_obj):
    if not settings.fetch_hashtags:
        return

    hashtags = get_parsed_hashtags(raw_test)
    if hashtags:
        dict_obj['hashtags'] = hashtags


def fetch_datetime(browser, dict_post):
    ele_datetime = browser.find_one('.eo2As .c-Yi7 ._1o9PC')
    datetime = ele_datetime.get_attribute('datetime')
    dict_post['datetime'] = datetime


def fetch_imgs(browser, dict_post):
    img_urls = set()
    while True:
        ele_imgs = browser.find('._97aPb img', waittime=10)
        for ele_img in ele_imgs:
            img_urls.add(ele_img.get_attribute('src'))

        next_photo_btn = browser.find_one(
            '._6CZji .coreSpriteRightChevron')

        if next_photo_btn:
            next_photo_btn.click()
            sleep(0.3)
        else:
            break

    dict_post['img_urls'] = list(img_urls)


def fetch_likes_plays(browser, dict_post):
    if not settings.fetch_likes_plays:
        return

    likes = None
    el_likes = browser.find_one('.Nm9Fw > * > span')
    el_see_likes = browser.find_one('.vcOH2')

    if el_see_likes is not None:
        el_plays = browser.find_one('.vcOH2 > span')
        dict_post['views'] = int(
            el_plays.text.replace(',', '').replace('.', ''))
        el_see_likes.click()
        el_likes = browser.find_one('.vJRqr > span')
        likes = el_likes.text
        browser.find_one('.QhbhU').click()

    elif el_likes is not None:
        likes = el_likes.text

    dict_post['likes'] = int(likes.replace(',', '').replace(
        '.', '')) if likes is not None else 0


def fetch_caption(browser, dict_post):
    ele_comments = browser.find('.eo2As .gElp9')
    if len(ele_comments) > 0:
        dict_post['caption'] = browser.find_one(
            'span', ele_comments[0]).text

        fetch_mentions(dict_post['caption'], dict_post)
        fetch_hashtags(dict_post['caption'], dict_post)


def fetch_comments(browser, dict_post):
    if not settings.fetch_comments:
        return

    ele_comments = browser.find('.eo2As .gElp9')
    comments = []
    for els_comment in ele_comments[1:]:
        author = browser.find_one('.FPmhX', els_comment).text
        comment = browser.find_one('span', els_comment).text
        comment_obj = {
            'author': author,
            'comment': comment,
        }

        fetch_mentions(comment, comment_obj)
        fetch_hashtags(comment, comment_obj)

        comments.append(comment_obj)

    if comments:
        dict_post['comments'] = comments
