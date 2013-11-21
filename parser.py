import config

import urllib2
import urlnorm
import os
import time

if config.lang == "zh":
	from parsers import zh as parser
## the list goes on

def parse(pages):
	if not os.path.exists("data/pages/"):
		os.mkdir("data/pages/")

	spelings = []

	dirpath = "data/pages/"
	counter = 1
	for page in pages:
		print("Progress: %d/%d" % (counter, len(pages)))
		counter += 1

		if "appendix" in page.lower():
			print("* Page is appendix, skipping.")
			continue

		if os.path.exists(dirpath + page + ".txt"):
			f = open(dirpath + page + ".txt", 'r')
			speling_list = f.read().strip("\n").split("\n")
			f.close()
		else:
			htmldoc = get_html(page)
			speling_list = parser.parse(page, htmldoc)

			if len(speling_list) == 0:
				print("* No speling info could be derived.")
				print("")

			f = open(dirpath + page + ".txt", 'w')
			for speling in speling_list:
				f.write(speling + "\n")
			f.close()
		spelings.extend(speling_list)

def get_html(page):
	url = "http://en.wiktionary.org/wiki/%s?action=render" % page
	url = urlnorm.norm(url)

	print("Crawling %s" % url)
	response = urllib2.urlopen(url.encode("utf8"))

	time.sleep(config.crawl_delay)
	return response.read()