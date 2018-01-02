from .browser import Browser
from .utils import instagram_int
from time import sleep


class InsCrawler:
    URL = 'https://www.instagram.com'
    RETRY_LIMIT = 10

    def __init__(self):
        self.browser = Browser()
        self.page_height = 0

    def get_user_profile(self, username):
        browser = self.browser
        url = '%s/%s/' % (InsCrawler.URL, username)
        browser.get(url)
        name = browser.find_one('._kc4z2')
        desc = browser.find_one('._tb97a span')
        photo = browser.find_one('._9bt3u ')
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

    def _has_more(self):
        height = self.browser.page_height
        has_more = self.page_height != height
        self.page_height = height
        return has_more

    def _load_more(self):
        browser = self.browser

        if self._has_more():
            self._reset_find_limit()
        self._inc_find_limit()

        while True:
            before_height = browser.page_height
            browser.scroll_down()
            after_height = browser.page_height
            if before_height >= after_height:
                break

    def _reset_find_limit(self):
        self.num_find = 0

    def _inc_find_limit(self):
        '''
            Monitor if encountering rate limit.
            Then sleep 3 mins
        '''
        self.num_find += 1
        if self.num_find > self.RETRY_LIMIT:
            self.num_find = 0
            sleep(300)
            retry_btn = self.browser.find_one('._rke62')
            if retry_btn:
                retry_btn.click()
            self.browser.scroll_up()

    def _get_posts(self, num):
        '''
            To get posts, we have to click on the load more
            button and make the browser call post api.
        '''
        browser = self.browser

        signin_x_btn = browser.find_one('._5gt5u')
        if signin_x_btn:
            signin_x_btn.click()

        signin_x_btn = browser.find_one('._lilm5')
        if signin_x_btn:
            browser.scroll_down()
            browser.js_click(signin_x_btn)

        more_btn = browser.find_one('._1cr2e._epyes')
        if not more_btn:
            return []
        more_btn.click()

        ele_posts = []

        while len(ele_posts) < num:
            self._load_more()
            ele_posts = browser.find('._cmdpi ._mck9w')

        posts = []
        for idx, ele in enumerate(ele_posts):
            if idx == num:
                break

            ele_img = browser.find_one('._2di5p', ele)
            content = ele_img.get_attribute('alt')
            img_url = ele_img.get_attribute('src')
            posts.append({
                'content': content,
                'img_url': img_url
            })

        return posts

    def get_user_posts(self, username, number=None):
        user_profile = self.get_user_profile(username)
        if not number:
            number = instagram_int(user_profile['post_num'])
        return self._get_posts(number)

    def get_latest_posts_by_tag(self, tag, num):
        url = '%s/explore/tags/%s/' % (InsCrawler.URL, tag)
        self.browser.get(url)
        return self._get_posts(num)
