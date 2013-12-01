# coding=utf8

import config

import re
from bs4 import BeautifulSoup
from collections import OrderedDict

def parse(page, htmldoc):
	spelings = []

	word = page
	postag = ""
	romanised = ""
	english = ""

	romanised_regex = r"\((.+?)\)"
	romanised_regex = re.compile(romanised_regex)

	citation_regex = r"\[\d\]"
	citation_regex = re.compile(citation_regex)

	soup = BeautifulSoup(htmldoc)
	soup = take_out_edit(soup)

	strip_tags = [
	"dd",
	"dl"
	]
	for tag in strip_tags:
		for e in soup.findAll(tag):
			e.extract()

	soup = strip_out_section(soup, htmldoc, "h2", "Lao", 1)
	soup = strip_out_section(soup, htmldoc, "h3", "References", 0)
	soup = strip_out_section(soup, htmldoc, "h3", "Usage notes", 0)

	soup = format_headings(soup) # marks out sections
	soup = format_ol(soup) # marks out english

	textdoc = [line.strip() for line in soup.get_text().split("\n")]
	textdoc = [line for line in textdoc if line != ""]
	textdoc = [line.replace("####", "###") for line in textdoc] # h4 to h3

	for line in textdoc:
		if line.startswith("### "): # found header; overrides everything
			heading = line[4:].lower().encode("utf8")
			postag = shortify(heading)
		elif line.startswith(page.decode("utf8")): # found romanised
			search = romanised_regex.search(line)

			if search:
				groups = search.groups()
				romanised = groups[0].encode("utf8")
		elif line.startswith("* "): # found english
			english = line[2:].encode("utf8")
			english = citation_regex.sub("", english)

			if not romanised:
				romanised = "none"

			if word and postag and romanised and english:
				speling = "%s ; %s ; %s ; %s" % (word, postag, romanised, english)
				spelings.append(speling)
			else:
				print("Word: %s" % word)
				print("POS tag: %s" % postag)
				print("Romanised: %s" % romanised)
				print("English: %s" % english)
				raise Exception("Data missing!")
	return spelings

def shortify(postag):
	shortify_tags = {
	"abbreviation": "abbrv",
	"adjective": "adj",
	"adverb": "adv",
	"conjunction": "cnj",
	"determiner": "det",
	"interjection": "ij",
	"interrogative": "itg",
	"noun": "n",
	"preposition": "pre",
	"pronoun": "prn",
	"proper noun": "np",
	"verb": "vblex"
	}
	if postag in shortify_tags:
		return shortify_tags[postag]
	return postag

def take_out_edit(soup):
	h_levels = range(1, 6)
	for level in h_levels:
		for heading in soup.findAll("h" + str(level)):
			if heading.span:
				new_string = heading.span.text.replace("[edit]", "")
				for span in heading.findAll("span"):
					span.extract()
				heading.append(new_string)
			else:
				new_string = heading.text.replace("[edit]", "")
				heading.string.replace_with(new_string)
	return soup

"""
Set index to 0 if you wish to obtain everything not in the section
Set index to 1 if you wish to obtain everything in the section
"""
def strip_out_section(soup, htmldoc, h_level, strip_heading, index):
	if not index == 0 and not index == 1:
		raise Exception("index can only have the following values: 0, 1")

	headings = OrderedDict()
	# obtain current and next heading to strip off unnecessary stuff
	for heading in soup.findAll(h_level):
		headings.update({unicode(heading.text): unicode(heading)})

	cur_head = ""
	next_head = ""
	found_cur_head = False
	for key in headings.keys():
		if found_cur_head:
			next_head = headings.get(key)
			break
		if key == strip_heading:
			cur_head = headings.get(key)
			found_cur_head = True

	# strip off everything other than what we want
	htmldoc = unicode(soup)
	if not cur_head:
		return soup
	elif not next_head:
		htmldoc = htmldoc.split(cur_head)[index]
	else:
		if index == 0:
			htmldoc = htmldoc.split(cur_head)[0] + next_head + htmldoc.split(next_head)[1]
		elif index == 1:
			htmldoc = cur_head + htmldoc.split(cur_head)[1].split(next_head)[0]

	return BeautifulSoup(htmldoc)

def format_headings(soup):
	h_levels = range(1, 6)
	for level in h_levels:
		for heading in soup.findAll("h" + str(level)):
			format = "#"
			format *= level 
			heading.replace_with("%s %s" % (format, heading.text))
	return soup

def format_ol(soup):
	for ol in soup.findAll("ol"):
		for li in ol.findAll("li"):
			li.replace_with("* %s" % li.text)
	return soup