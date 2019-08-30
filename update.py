import requests
from urllib.parse import urljoin
from inscrawler import InsCrawler

DOMAIN = 'http://miratcan.pythonanywhere.com'

def get_pending_usernames():
    for record in requests.get(urljoin(DOMAIN, '/api/account_status/')).json():
        yield record['username'], record['latest_post_url']

crawler = InsCrawler()

for username, stop_post in get_pending_usernames():
    print(f'Collecting missing posts for {username}')
    posts = crawler.get_user_posts(username, stop_post)
    requests.post(urljoin(DOMAIN, '/api/account/posts/'))
