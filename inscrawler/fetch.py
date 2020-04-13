import re
from time import sleep

from .settings import settings


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
        dict_obj["mentions"] = mentions

def fetch_hashtags(raw_test, dict_obj):
    if not settings.fetch_hashtags:
        return

    hashtags = get_parsed_hashtags(raw_test)
    if hashtags:
        dict_obj["hashtags"] = hashtags


def fetch_datetime(browser, dict_post):
    ele_datetime = browser.find_one(".eo2As .c-Yi7 ._1o9PC")
    datetime = ele_datetime.get_attribute("datetime")
    dict_post["datetime"] = datetime


def fetch_imgs(browser, dict_post):
    img_urls = set()
    while True:
        ele_imgs = browser.find("._97aPb img", waittime=10)

        if isinstance(ele_imgs, list):
            for ele_img in ele_imgs:
                img_urls.add(ele_img.get_attribute("src"))
        else:
            break

        next_photo_btn = browser.find_one("._6CZji .coreSpriteRightChevron")

        if next_photo_btn:
            next_photo_btn.click()
            sleep(0.3)
        else:
            break

    dict_post["img_urls"] = list(img_urls)

def fetch_likes_plays(browser, dict_post):
    if not settings.fetch_likes_plays:
        return

    likes = None
    el_likes = browser.find_one(".Nm9Fw > * > span")
    el_see_likes = browser.find_one(".vcOH2")

    if el_see_likes is not None:
        el_plays = browser.find_one(".vcOH2 > span")
        dict_post["views"] = int(el_plays.text.replace(",", "").replace(".", ""))
        el_see_likes.click()
        el_likes = browser.find_one(".vJRqr > span")
        likes = el_likes.text
        browser.find_one(".QhbhU").click()

    elif el_likes is not None:
        likes = el_likes.text

    dict_post["likes"] = (
        int(likes.replace(",", "").replace(".", "")) if likes is not None else 0
    )


def fetch_likers(browser, dict_post):
    if not settings.fetch_likers:
        return
    like_info_btn = browser.find_one(".EDfFK ._0mzm-.sqdOP")
    like_info_btn.click()

    likers = {}
    liker_elems_css_selector = ".Igw0E ._7UhW9.xLCgt a"
    likers_elems = list(browser.find(liker_elems_css_selector))
    last_liker = None
    while likers_elems:
        for ele in likers_elems:
            likers[ele.get_attribute("href")] = ele.get_attribute("title")

        if last_liker == likers_elems[-1]:
            break

        last_liker = likers_elems[-1]
        last_liker.location_once_scrolled_into_view
        sleep(0.6)
        likers_elems = list(browser.find(liker_elems_css_selector))

    dict_post["likers"] = list(likers.values())
    close_btn = browser.find_one(".WaOAr button")
    close_btn.click()


def fetch_caption(browser, dict_post):
    ele_comments = browser.find(".eo2As .gElp9")

    if len(ele_comments) > 0:

        temp_element = browser.find("span",ele_comments[0])

        for element in temp_element:

            if element.text not in ['Verified',''] and 'caption' not in dict_post:
                dict_post["caption"] = element.text

        fetch_mentions(dict_post.get("caption",""), dict_post)
        fetch_hashtags(dict_post.get("caption",""), dict_post)


def fetch_comments(browser, dict_post):
    if not settings.fetch_comments:
        return

    show_more_selector = "button .glyphsSpriteCircle_add__outline__24__grey_9"
    show_more = browser.find_one(show_more_selector)
    while show_more:
        show_more.location_once_scrolled_into_view
        show_more.click()
        sleep(0.3)
        show_more = browser.find_one(show_more_selector)

    show_comment_btns = browser.find(".EizgU")
    for show_comment_btn in show_comment_btns:
        show_comment_btn.location_once_scrolled_into_view
        show_comment_btn.click()
        sleep(0.3)

    ele_comments = browser.find(".eo2As .gElp9")
    comments = []
    for els_comment in ele_comments[1:]:
        author = browser.find_one(".FPmhX", els_comment).text

        temp_element = browser.find("span", els_comment)

        for element in temp_element:

            if element.text not in ['Verified','']:
                comment = element.text

        comment_obj = {"author": author, "comment": comment}

        fetch_mentions(comment, comment_obj)
        fetch_hashtags(comment, comment_obj)

        comments.append(comment_obj)

    if comments:
        dict_post["comments"] = comments


def fetch_initial_comment(browser, dict_post):
    comments_elem = browser.find_one("ul.XQXOT")
    first_post_elem = browser.find_one(".ZyFrc", comments_elem)
    caption = browser.find_one("span", first_post_elem)

    if caption:
        dict_post["description"] = caption.text


def fetch_details(browser, dict_post):
    if not settings.fetch_details:
        return

    browser.open_new_tab(dict_post["key"])

    username = browser.find_one("a.ZIAjV")
    location = browser.find_one("a.O4GlU")

    if username:
        dict_post["username"] = username.text
    if location:
        dict_post["location"] = location.text

    fetch_initial_comment(browser, dict_post)

    browser.close_current_tab()
