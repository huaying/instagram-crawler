from inscrawler import InsCrawler
import argparse


def usage():
    return '''
        python crawler.py [tag]
    '''


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Instagram Liker',
                                     usage=usage())
    parser.add_argument('tag',
                        help='tag name')
    args = parser.parse_args()
    ins_crawler = InsCrawler(has_screen=True)
    ins_crawler.auto_like(tag=args.tag)
