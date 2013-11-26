import config, lang
import pb

import urllib2
import urlnorm
import os
import time

def parse(pages):
	spelings = []

	speling_dirpath = "data/speling/%s/%s/" % (config.wiki_lang, config.start_cat)
	pages_dirpath = "data/pages/%s/%s/" % (config.wiki_lang, config.start_cat)
	counter = 0

	for page in pages:
		counter += 1
		pb.update(counter, len(pages))

		if os.path.exists(speling_dirpath + page + ".txt"):
			f = open(speling_dirpath + page + ".txt", 'r')
			speling_list = f.read().strip("\n").split("\n")
			f.close()

			spelings.extend(speling_list)
			continue

		speling_list = parse_page(page)
		f = open(speling_dirpath + page + ".txt", 'w')
		for speling in speling_list:
			f.write(speling + "\n")
		f.close()

		spelings.extend(speling_list)
	
	spelings = [speling for speling in spelings if not speling == ""]
	return spelings

def parse_page(page):
	f = open(dirpath + page + ".html", 'r')
	htmldoc = f.read()
	f.close()

	while True:
		try:
			speling_list = lang.parse(page, htmldoc)
			break
		except:
			e = sys.exc_info()[0]
			print(e)
	return speling_list