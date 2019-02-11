import validators
from lxml import html
import requests
import argparse
import re

TINY_URL = 'https://tinyurl.com/create.php?url={}'
FAIL = 0
SUCCESS = 1

parser = argparse.ArgumentParser()
# TODO: implement argparse -u (optional) for Custom alias
parser.add_argument("link", type=str,
                    help="Paste the link to shorten (use quotes('link'))")
parser.add_argument("-p", "--http", action="store_true",
                    help="Changes the default prefix from https to http")
parser.add_argument("-u", "--unique", action="store",
                    help="spesific your own unique link suffix")
args = parser.parse_args()


def shorter_link(args):
    try:
        if not re.match(r'https?://', args.link):
            prefix = 'http://' if args.http else 'https://'
            args.link = prefix + args.link

        if validators.url(args.link):
            page = requests.get(TINY_URL.format(args.link))
            tree = html.fromstring(page.content)
            shorter_url = tree.xpath('//html/body/div[1]/div[2]/'
                                     'div[2]/div[2]/div[2]/div[2]/b/text()')
            return (SUCCESS, shorter_url[0])

        else:
            return (FAIL, 'Not a valid URL: {}'.format(args.link))
    except Exception as e:
        return (FAIL, str(e))


if __name__ == '__main__':
    print(shorter_link(args))
