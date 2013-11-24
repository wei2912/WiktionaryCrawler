# coding=utf8

start_cat = "Category:Mandarin language"
crawl_delay = 1 # in seconds
lang = "zh"
wiki_lang = "en"

# blacklists
subcats_bl = []
pages_bl = [
"Appendix:.*"
]

## lang-specific config vals ##

## zh - Default
zh_s = True # (true) crawl only simplified chinese
zh_t = False # (true) crawl only traditional chinese

## lang-specific config vals ##

## DO NOT MODIFY ##
import re

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
## DO NOT MODIFY ##