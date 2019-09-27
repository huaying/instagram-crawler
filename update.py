import requests
from urllib.parse import urljoin
from inscrawler import InsCrawler

DOMAIN = 'http://miratcan.pythonanywhere.com'

def get_pending_usernames():
    import ipdb; ipdb.set_trace()
    for record in requests.get(urljoin(DOMAIN,
        '/api/account_status/')).json()['accounts']:
        yield record['username'], record['last_post_url']

crawler = InsCrawler()

for username, stop_post in get_pending_usernames():
    if username != 'rterdogan':
        continue
    print(f'Collecting missing posts for {username}')
    # import json
    # posts = json.load(open('/tmp/posts.json', 'r'))
    posts = crawler.get_user_posts(username, stop_post)
    for post in posts:
        post['post_url'] = post.pop('key')
        post['owner_id'] = username
    import ipdb; ipdb.set_trace()
    response = requests.post(urljoin(DOMAIN, '/api/update_posts/'),
            json={'posts': posts})
    print(response.content)
