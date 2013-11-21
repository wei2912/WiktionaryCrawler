# coding=utf8

import config

from collections import OrderedDict
import crawler, parser
import os

def main():
	if not os.path.exists("data/"):
		os.mkdir("data/")

	# stage 1 - obtaining list of words to crawl
	if os.path.exists("data/pages.txt"):
		f = open("data/pages.txt", 'r')
		pages = f.read().strip("\n").split("\n")
		f.close()
	else:
		pages = OrderedDict.fromkeys(crawler.crawl()).keys() # unique
		f = open("data/pages.txt", 'w')
		for page in pages:
			f.write(page + "\n")
		f.close()

	# stage 2 - crawling and parsing all pages
	spelings = parser.parse(pages)

	# stage 3 - write to file
	f = open("data/speling.txt", "w")
	for speling in spelings:
		f.write(speling + "\n")
	f.close()

main()