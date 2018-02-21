from inscrawler import InsCrawler
import argparse


def usage():
    return '''
        python crawler.py [tag]
    '''


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Instagram Liker',
                                     usage=usage())
    parser.add_argument('hashtag',
                        help='hashtag name')
    parser.add_argument('-n', '--number',
                        type=int,
                        default=1000,
                        help='number of posts to like')
    args = parser.parse_args()
    ins_crawler = InsCrawler(has_screen=True)
    ins_crawler.auto_like(tag=args.hashtag, maximum=args.number)
