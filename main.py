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
	if not os.path.exists("data/site/%s/" % config.start_cat):
		os.mkdir("data/site/%s/" % config.start_cat)
	if not os.path.exists("data/pages/"):
		os.mkdir("data/pages/")
	if not os.path.exists("data/pages/%s/" % config.start_cat):
		os.mkdir("data/pages/%s/" % config.start_cat)
	if not os.path.exists("data/speling/"):
		os.mkdir("data/speling/")
	if not os.path.exists("data/speling/%s/" % config.start_cat):
		os.mkdir("data/speling/%s/" % config.start_cat)

	config.init_config()

	# stage 1 - obtaining list of words to crawl
	print("** Stage 1: Obtaining list of pages to crawl. **")
	pages = OrderedDict.fromkeys(crawler.crawl()).keys() # unique

	# stage 2 - crawling all pages
	print("** Stage 2: Crawling all pages in list. **")
	crawler.crawl_all_pages(pages)

	# stage 3 - parsing (scraping) all pages
	print("** Stage 3: Parsing all pages in list. **")
	spelings = parser.parse(pages)

	# stage 4 - write to file
	print("** Stage 4: Writing final results to file. **")
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