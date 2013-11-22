# coding=utf8

import config

from collections import OrderedDict
import crawler, parser
import os

def main():
	if not os.path.exists("data/"):
		os.mkdir("data/")
	if not os.path.exists("data/site/"):
		os.mkdir("data/site/")
	if not os.path.exists("data/pages/"):
		os.mkdir("data/pages/")
	if not os.path.exists("data/speling/"):
		os.mkdir("data/speling/")

	# stage 1 - obtaining list of words to crawl
	pages = OrderedDict.fromkeys(crawler.crawl()).keys() # unique

	# stage 2 - crawling all pages
	crawler.crawl_all_pages(pages)

	# stage 3 - parsing (scraping) all pages
	spelings = parser.parse(pages)

	# stage 4 - write to file
	f = open("data/speling.txt", "w")
	for speling in spelings:
		f.write(speling + "\n")
	f.close()

	print("")
	print("")
	print("=== STATS ===")
	print("Crawled %d pages" % len(pages))
	print("Obtained %d spelings" % len(spelings))
	print("=============")

main()