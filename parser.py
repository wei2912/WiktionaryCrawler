import config, lang
import pb

import urllib2
import urlnorm
import os
import time

def parse(pages):
	parse_again = False
	spelings = []

	pages_dirpath = "data/pages/%s/%s/" % (config.wiki_lang, config.start_cat)
	speling_dirpath = "data/speling/%s/%s/" % (config.wiki_lang, config.start_cat)
	counter = 0
	for page in pages:
		counter += 1
		pb.update(counter, len(pages))

		if os.path.exists(speling_dirpath + page + ".txt"):
			f = open(speling_dirpath + page + ".txt", 'r')
			speling_list = f.read().strip("\n").split("\n")
			f.close()
		else:
			f = open(pages_dirpath + page + ".html", 'r')
			htmldoc = f.read()
			f.close()

			try:
				speling_list = lang.parse(page, htmldoc)

				f = open(speling_dirpath + page + ".txt", 'w')
				for speling in speling_list:
					f.write(speling + "\n")
				f.close()
			except:
				e = sys.exc_info()[0]
				print(e)
				parse_again = True
				continue
				# skip for now, we'll do another round of parsing later
		spelings.extend(speling_list)
	
	if parse_again:
		spelings = parse(pages)
	spelings = [speling for speling in spelings if not speling == ""]
	return spelings

