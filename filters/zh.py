# coding=utf8

import config

from mafan import simplify, tradify
import re

def can_page(page):
	# stage 1: match filter regex
	filter_regex = ".*?:.*"
	filter_regex = re.compile(filter_regex)
	if filter_regex.match(page):
		return False

	# stage 2: simplified or traditional
	if not can_st(page):
		return False

	# stage 3: pinyin
	if is_pinyin(page):
		return False

	return True

def can_subcat(subcat):
	# stage 1: match filter regex
	filter_regex = "Category:(cmn:.*|Mandarin pinyin)"
	filter_regex = re.compile(filter_regex)
	return not filter_regex.match(subcat)

def can_st(page):
	simplified = simplify(page) == page.decode("utf8")
	traditional = tradify(page) == page.decode("utf8")
	# only simplified
	if simplified and not traditional and not config.zh_s:
		return False
	# only traditional
	elif traditional and not simplified and not config.zh_t:
		return False
	else:
		return config.zh_t or config.zh_s

def is_pinyin(page):
	regex = "([a-z]+[0-9])+"
	regex = re.compile(regex)

	if regex.match(page):
		return True

	tones = [
	"ā", "á", "ǎ", "à",
	"ē", "é", "ě", "è",
	"ī", "í", "ǐ", "ì",
	"ō", "ó", "ǒ", "ò",
	"ū", "ú", "ǔ", "ù",
	"ǖ", "ǘ", "ǚ", "ǜ", "ü" 
	]

	for letter in tones:
		if letter.decode("utf8") in page.decode("utf8"):
			return True
	return False