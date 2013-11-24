import config
import pb

import urllib2
import urlnorm
import os
import time

if config.lang == "zh":
	from parsers import zh as parser
## the list goes on

def parse(pages):
	spelings = []

	pages_dirpath = "data/pages/%s/" % config.start_cat
	speling_dirpath = "data/speling/%s/" % config.start_cat
	counter = 0
	for page in pages:
		counter += 1
		pb.update(counter*100/len(pages))

		if os.path.exists(speling_dirpath + page + ".txt"):
			f = open(speling_dirpath + page + ".txt", 'r')
			speling_list = f.read().strip("\n").split("\n")
			f.close()
		else:
			f = open(pages_dirpath + page + ".html", 'r')
			htmldoc = f.read()
			f.close()

			speling_list = parser.parse(page, htmldoc)

			f = open(speling_dirpath + page + ".txt", 'w')
			for speling in speling_list:
				f.write(speling + "\n")
			f.close()
		spelings.extend(speling_list)
	return spelings

