import requests
from urllib.parse import urljoin
from inscrawler import InsCrawler

DOMAIN = 'http://miratcan.pythonanywhere.com'

def get_pending_usernames():
    for record in requests.get(urljoin(DOMAIN,
        '/api/account_status/')).json()['accounts']:
        yield record['username'], record['last_post_url']


def chunks(l, n):
    """Yield successive n-sized chunks from l."""
    t = range(0, len(l), n)
    for i in t:
        yield i, len(t), l[i:i + n]

crawler = InsCrawler()
for username, stop_post in get_pending_usernames():
    print(f'Collecting missing posts for {username}')
    if not stop_post:
        continue
    posts = crawler.get_user_posts(username)

    for post in posts:
        post['post_url'] = post.pop('key')
        post['owner_id'] = username
        post['thmb_srcset'] = ''
 
    for counter, total, chunk in chunks(posts, 10):
        print(f'Updating {counter + 1}/{total}')
        response = requests.post(urljoin(DOMAIN, '/api/update_posts/'),
                                 json={'posts': chunk}, timeout=60000)
        print(response.content)
        import time
        time.sleep(1)
