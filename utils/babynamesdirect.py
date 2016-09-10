# -*- coding: utf-8 -*-

"""
Parse words out of a babynamesdirect.com listing page. Get the pages first
using wget -r -nd -np <url> and run this on the collected files.
"""

import sys
import unicodecsv
from lxml import etree


def parse(fileob):
    out = unicodecsv.writer(sys.stdout)
    htmlparser = etree.HTMLParser()
    tree = etree.parse(fileob, htmlparser)
    headlines = tree.xpath('//*[@id="wrap"]/h1')
    gender = ''
    if headlines:
        headline = headlines[0].text
        if "Boy" in headline:
            gender = 'm'
        elif "Girl" in headline:
            gender = 'f'
    for element in tree.xpath('//table[contains(@class, "bnames")]/tbody/tr[@id]'):
        if not element.xpath('td[2]/b/text()'):
            print >> sys.stderr, etree.tostring(element)
            continue
        word = element.xpath('td[2]/b/text()')[0]
        title = element.xpath('td[2]')[0].attrib.get('title')
        if title and title.startswith('Tag: '):
            prefix, taglist = title.split(':', 1)
            tags = [t.strip() for t in taglist.split(',')]
        else:
            print >> sys.stderr, word
            continue
        meaning_list = element.xpath('td[3]/i/text()')
        if meaning_list:
            meaning = meaning_list[0]
        else:
            meaning = ''
        out.writerow([word, gender, meaning] + tags)


def main(argv):
    if len(argv) < 2:
        print >> sys.stderr, "Syntax: %s file.html ..." % argv[0]
    print "# Name,Gender,Meaning,Tags..."
    for filename in argv[1:]:
        parse(open(filename))

if __name__ == '__main__':
    sys.exit(main(sys.argv))
