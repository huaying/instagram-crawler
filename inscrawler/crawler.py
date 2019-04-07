from __future__ import unicode_literals
from builtins import open
from selenium.webdriver.common.keys import Keys
import traceback

from .exceptions import RetryException
from .browser import Browser
from .utils import instagram_int
from .utils import retry
from .utils import randmized_sleep
from .utils import get_parsed_mentions
from .utils import get_parsed_hashtags
from . import secret
import json
import time
from time import sleep
from tqdm import tqdm
import os
import glob
import sys


class Logging(object):
    PREFIX = 'instagram-crawler'

    def __init__(self):
        try:
            timestamp  = int(time.time())
            self.cleanup(timestamp)
            self.logger = open('/tmp/%s-%s.log' % (Logging.PREFIX, timestamp), 'w')
            self.log_disable = False
        except:
            self.log_disable = True

    def cleanup(self, timestamp):
        days = 86400 * 7
        days_ago_log = '/tmp/%s-%s.log' % (Logging.PREFIX, timestamp - days)
        for log in glob.glob("/tmp/instagram-crawler-*.log"):
            if log < days_ago_log:
                os.remove(log)

    def log(self, msg):
        if self.log_disable: return

        self.logger.write(msg + '\n')
        self.logger.flush()

    def __del__(self):
        if self.log_disable: return
        self.logger.close()


class InsCrawler(Logging):
    URL = 'https://www.instagram.com'
    RETRY_LIMIT = 10

    def __init__(self, has_screen=False):
        super(InsCrawler, self).__init__()
        self.browser = Browser(has_screen)
        self.page_height = 0

    def _dismiss_login_prompt(self):
        ele_login = self.browser.find_one('.Ls00D .Szr5J')
        if ele_login:
            ele_login.click()

    def login(self):
        browser = self.browser
        url = '%s/accounts/login/' % (InsCrawler.URL)
        browser.get(url)
        u_input = browser.find_one('input[name="username"]')
        u_input.send_keys(secret.username)
        p_input = browser.find_one('input[name="password"]')
        p_input.send_keys(secret.password)

        login_btn = browser.find_one('.L3NKy')
        login_btn.click()

        @retry()
        def check_login():
            if browser.find_one('input[name="username"]'):
                raise RetryException()

        check_login()

    def get_user_profile(self, username):
        browser = self.browser
        url = '%s/%s/' % (InsCrawler.URL, username)
        browser.get(url)
        name = browser.find_one('.rhpdm')
        desc = browser.find_one('.-vDIg span')
        photo = browser.find_one('._6q-tv')
        statistics = [ele.text for ele in browser.find('.g47SY')]
        post_num, follower_num, following_num = statistics
        return {
            'name': name.text,
            'desc': desc.text if desc else None,
            'photo_url': photo.get_attribute('src'),
            'post_num': post_num,
            'follower_num': follower_num,
            'following_num': following_num
        }

    def get_user_posts(self, username, number=None, detail=False):
        user_profile = self.get_user_profile(username)
        if not number:
            number = instagram_int(user_profile['post_num'])

        self._dismiss_login_prompt()

        if detail:
            return self._get_posts_full(number)
        else:
            return self._get_posts(number)

    def get_latest_posts_by_tag(self, tag, num):
        url = '%s/explore/tags/%s/' % (InsCrawler.URL, tag)
        self.browser.get(url)
        return self._get_posts(num)

    def auto_like(self, tag='', maximum=1000):
        self.login()
        browser = self.browser
        if tag:
            url = '%s/explore/tags/%s/' % (InsCrawler.URL, tag)
        else:
            url = '%s/explore/' % (InsCrawler.URL)
        self.browser.get(url)

        ele_post = browser.find_one('.v1Nh3 a')
        ele_post.click()

        for _ in range(maximum):
            heart = browser.find_one(
                '.dCJp8 .glyphsSpriteHeart__outline__24__grey_9')
            if heart:
                heart.click()
                randmized_sleep(2)

            left_arrow = browser.find_one('.HBoOv')
            if left_arrow:
                left_arrow.click()
                randmized_sleep(2)
            else:
                break

    def _fetch_post_with_key(self, key, dict_post):
        browser = self.browser
        dict_post['key'] = key

        ele_datetime = browser.find_one('.eo2As .c-Yi7 ._1o9PC')
        datetime = ele_datetime.get_attribute('datetime')
        dict_post['datetime'] = datetime

        # Fetching all img
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

        # Fetching number of likes and plays
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

        # Fetching comments
        ele_comments = browser.find('.eo2As .gElp9')

        comment = ''
        if len(ele_comments) > 0:
            dict_post['caption'] = browser.find_one(
                'span', ele_comments[0]).text
            hashtags = get_parsed_hashtags(dict_post['caption'])
            mentions = get_parsed_mentions(dict_post['caption'])

            if hashtags:
                dict_post['hashtags'] = hashtags
            if mentions:
                dict_post['mentions'] = mentions

        comments = []
        for els_comment in ele_comments[1:]:
            author = browser.find_one('.FPmhX', els_comment).text
            comment = browser.find_one('span', els_comment).text
            comment_obj = {
                'author': author,
                'comment': comment,
            }

            hashtags = get_parsed_hashtags(comment)
            mentions = get_parsed_mentions(comment)
            if hashtags:
                comment_obj['hashtags'] = hashtags
            if mentions:
                comment_obj['mentions'] = mentions

            comments.append(comment_obj)

        if comments:
            dict_post['comments'] = comments


    def _get_posts_full(self, num):
        @retry()
        def check_next_post(cur_key):
            ele_a_datetime = browser.find_one('.eo2As .c-Yi7')

            # It takes time to load the post for some users with slow network
            if ele_a_datetime is None:
                raise RetryException()

            next_key = ele_a_datetime.get_attribute('href')
            if cur_key == next_key:
                raise RetryException()

        browser = self.browser
        browser.implicitly_wait(1)
        ele_post = browser.find_one('.v1Nh3 a')
        ele_post.click()
        dict_posts = {}

        pbar = tqdm(total=num)
        pbar.set_description('fetching')
        cur_key = None

        # Fetching all posts
        for _ in range(num):
            dict_post = {}

            # Fetching post detail
            try:
                check_next_post(cur_key)

                # Fetching datetime and url as key
                ele_a_datetime = browser.find_one('.eo2As .c-Yi7')
                cur_key = ele_a_datetime.get_attribute('href')
                self._fetch_post_with_key(cur_key, dict_post)

            except RetryException:
                sys.stderr.write(
                    '\x1b[1;31m' + 'Failed to fetch the post: ' + cur_key + '\x1b[0m' + '\n')
                break

            except Exception:
                sys.stderr.write(
                    '\x1b[1;31m' + 'Failed to fetch the post: ' + cur_key + '\x1b[0m' + '\n')
                traceback.print_exc()

            self.log(json.dumps(dict_post, ensure_ascii=False))
            dict_posts[browser.current_url] = dict_post

            pbar.update(1)
            left_arrow = browser.find_one('.HBoOv')
            if left_arrow:
                left_arrow.click()

        pbar.close()
        posts = list(dict_posts.values())
        if posts:
            posts.sort(key=lambda post: post['datetime'], reverse=True)
        return posts

    def _get_posts(self, num):
        '''
            To get posts, we have to click on the load more
            button and make the browser call post api.
        '''
        TIMEOUT = 600
        browser = self.browser
        key_set = set()
        posts = []
        pre_post_num = 0
        wait_time = 1

        pbar = tqdm(total=num)

        def start_fetching(pre_post_num, wait_time):
            ele_posts = browser.find('.v1Nh3 a')
            for ele in ele_posts:
                key = ele.get_attribute('href')
                if key not in key_set:
                    ele_img = browser.find_one('.KL4Bh img', ele)
                    caption = ele_img.get_attribute('alt')
                    img_url = ele_img.get_attribute('src')
                    key_set.add(key)
                    posts.append({
                        'key': key,
                        'caption': caption,
                        'img_url': img_url
                    })
            if pre_post_num == len(posts):
                pbar.set_description('Wait for %s sec' % (wait_time))
                sleep(wait_time)
                pbar.set_description('fetching')

                wait_time *= 2
                browser.scroll_up(300)
            else:
                wait_time = 1

            pre_post_num = len(posts)
            browser.scroll_down()

            return pre_post_num, wait_time

        pbar.set_description('fetching')
        while len(posts) < num and wait_time < TIMEOUT:
            post_num, wait_time = start_fetching(pre_post_num, wait_time)
            pbar.update(post_num - pre_post_num)
            pre_post_num = post_num

            loading = browser.find_one('.W1Bne')
            if (not loading and wait_time > TIMEOUT/2):
                break

        pbar.close()
        print('Done. Fetched %s posts.' % (min(len(posts), num)))
        return posts[:num]


