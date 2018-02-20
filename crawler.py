from inscrawler import InsCrawler
import sys
import argparse
import json
from io import open


def usage():
    return '''
        python crawler.py posts -u cal_foodie -n 100 -o ./output
        python crawler.py profile -u cal_foodie -o ./output
        python crawler.py hashtag -t taiwan -o ./output

        The default number for fetching posts via hashtag is 100.
    '''


def get_posts_by_user(username, number):
    ins_crawler = InsCrawler()
    return ins_crawler.get_user_posts(username, number)


def get_profile(username):
    ins_crawler = InsCrawler()
    return ins_crawler.get_user_profile(username)


def get_posts_by_hashtag(tag, number):
    ins_crawler = InsCrawler()
    return ins_crawler.get_latest_posts_by_tag(tag, number)


def arg_required(args, fields=[]):
    for field in fields:
        if not getattr(args, field):
            parser.print_help()
            sys.exit()


def output(data, filepath):
    out = json.dumps(data, ensure_ascii=False)
    if filepath:
        with open(filepath, 'w') as f:
            f.write(out)
    else:
        print(out)


if __name__ == '__main__':
    ins_crawler = InsCrawler()
    ins_crawler.auto_like()
    
    parser = argparse.ArgumentParser(description='Instagram Crawler',
                                     usage=usage())
    parser.add_argument('mode',
                        help='options: [posts, profile, hashtag]')
    parser.add_argument('-n', '--number',
                        type=int,
                        help='number of returned posts')
    parser.add_argument('-u', '--username',
                        help='instagram\'s username')
    parser.add_argument('-t', '--tag',
                        help='instagram\'s tag name')
    parser.add_argument('-o', '--output', help='output file name(json format)')
    args = parser.parse_args()

    if args.mode == 'posts':
        arg_required('username')
        output(get_posts_by_user(args.username, args.number), args.output)
    elif args.mode == 'profile':
        arg_required('username')
        output(get_profile(args.username), args.output)
    elif args.mode == 'hashtag':
        arg_required('tag')
        output(
            get_posts_by_hashtag(args.tag, args.number or 100), args.output)
    else:
        usage()
