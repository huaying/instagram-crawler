from selenium.webdriver.common.keys import Keys
from .browser import Browser
from .utils import instagram_int
from .utils import retry
from .utils import randmized_sleep
from . import secret
from time import sleep


class InsCrawler:
    URL = 'https://www.instagram.com'
    RETRY_LIMIT = 10

    def __init__(self, has_screen=False):
        self.browser = Browser(has_screen)
        self.page_height = 0

    def login(self):
        browser = self.browser
        url = '%s/accounts/login/' % (InsCrawler.URL)
        browser.get(url)

        u_input = browser.find_one('input[name="username"]')
        u_input.send_keys(secret.username)
        p_input = browser.find_one('input[name="password"]')
        p_input.send_keys(secret.password)
        p_input.send_keys(Keys.RETURN)

        @retry()
        def check_login():
            if browser.find_one('input[name="username"]'):
                raise Exception()

        check_login()

    def get_user_profile(self, username):
        browser = self.browser
        url = '%s/%s/' % (InsCrawler.URL, username)
        browser.get(url)
        name = browser.find_one('._kc4z2')
        desc = browser.find_one('._tb97a span')
        photo = browser.find_one('._rewi8')
        statistics = [ele.text for ele in browser.find('._fd86t')]
        post_num, follower_num, following_num = statistics
        return {
            'name': name.text,
            'desc': desc.text if desc else None,
            'photo_url': photo.get_attribute('src'),
            'post_num': post_num,
            'follower_num': follower_num,
            'following_num': following_num
        }

    def get_user_posts(self, username, number=None):
        user_profile = self.get_user_profile(username)
        if not number:
            number = instagram_int(user_profile['post_num'])
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
        ele_posts = browser.find_one('._mck9w a')
        ele_posts.click()

        for _ in range(maximum):
            heart = browser.find_one('._8scx2.coreSpriteHeartOpen')
            if heart:
                heart.click()
                randmized_sleep(2)

            left_arrow = browser.find_one('.coreSpriteRightPaginationArrow')
            if left_arrow:
                left_arrow.click()
                randmized_sleep(2)
            else:
                break

    def _get_posts(self, num):
        '''
            To get posts, we have to click on the load more
            button and make the browser call post api.
        '''
        TIMEOUT = 600
        browser = self.browser
        dict_posts = {}
        pre_post_num = 0
        wait_time = 1

        def start_fetching(pre_post_num, wait_time):
            ele_posts = browser.find('._mck9w a')
            for ele in ele_posts:
                key = ele.get_attribute('href')
                if key not in dict_posts:
                    ele_img = browser.find_one('._2di5p', ele)
                    content = ele_img.get_attribute('alt')
                    img_url = ele_img.get_attribute('src')
                    dict_posts[key] = {
                        'content': content,
                        'img_url': img_url
                    }

            if pre_post_num == len(dict_posts):
                print('Number of fetched posts: %s' % pre_post_num)
                print('Wait for %s sec...' % (wait_time))
                sleep(wait_time)
                wait_time *= 2
                browser.scroll_up(300)
            else:
                wait_time = 1

            pre_post_num = len(dict_posts)
            browser.scroll_down()

            return pre_post_num, wait_time

        print('Strating fetching...')
        while len(dict_posts) < num and wait_time < TIMEOUT:
            pre_post_num, wait_time = start_fetching(pre_post_num, wait_time)

            loading = browser.find_one('._anzsd._o5uzb')
            if (not loading and wait_time > TIMEOUT/2):
                break

        posts = list(dict_posts.values())
        print('Done. Fetched %s posts.' % (min(len(posts), num)))
        return posts[:num]


