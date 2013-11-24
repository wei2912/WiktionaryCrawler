# coding=utf8

import re

start_cat = "Category:Mandarin language"
lang = "zh"
zh_s = True # (true) crawl only simplified chinese
zh_t = False # (true) crawl only traditional chinese
crawl_delay = 1 # in seconds

# blacklists
subcats_bl = []
pages_bl = [
"Appendix:.*",
"〜"
]

def init_config():
	for i in range(len(subcats_bl)):
		subcats_bl[i] = re.compile(subcats_bl[i])
	for i in range(len(pages_bl)):
		pages_bl[i] = re.compile(pages_bl[i])

def subcat_bl(subcat):
	return bl(subcats_bl, subcat)

def page_bl(page):
	return bl(pages_bl, page)

def bl(regexes, line):
	for regex in regexes:
		if regex.match(line):
			return True
	return False