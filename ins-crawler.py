from browser import Browser


class InsCrawler:
    URL = 'https://www.instagram.com/'

    def __init__(self,):
        self.browser = Browser()

    def get_user_profile(self, username):
        browser = self.browser
        browser.get('https://www.instagram.com/%s/' % username)
        name = browser.find_one('._kc4z2').text
        desc = browser.find_one('._tb97a span').text
        statistics = [ele.text for ele in browser.find('._fd86t')]
        post_num, follower_num, following_num = statistics
        print(name, desc, post_num, follower_num, following_num)


if __name__ == '__main__':
    ins_crawler = InsCrawler()
    ins_crawler.get_user_profile('cal_foodie')
