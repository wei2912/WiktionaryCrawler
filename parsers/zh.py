import config

import re
from bs4 import BeautifulSoup, NavigableString

def parse(page, htmldoc):
	soup = BeautifulSoup(htmldoc)
	soup = strip_out_headings(soup, htmldoc, "h2", "Mandarin", 1)
	tags = [
	"a", 
	"b", 
	"i", 
	"span", 
	"strong",
	"table",
	]
	soup = get_tag_content(soup, tags)
	tags = [
	"dd",
	"dl"
	]
	soup = strip_tags(soup, tags)
	soup = strip_out_headings(soup, htmldoc, "h3", "Pronunciation", 0)
	soup = format_headings(soup)
	
	textdoc = [line.strip() for line in soup.get_text().split("\n")]
	textdoc = [line for line in textdoc if line != ""]

	abbrv_regex = r"^[A-Z]+$"
	abbrv_regex = re.compile(abbrv_regex)

	if abbrv_regex.match(page): # abbreviations
		postag = "abbr"
		pinyin = "none"

	pinyin_regex = r"Pinyin (.+?)\)"
	pinyin_regex = re.compile(pinyin_regex)

	word = page
	postag = ""
	pinyin = ""
	english = ""

	spelings = []
	state = 0 # haven't found header
	for line in textdoc:
		if state == 3:
			if not line.startswith("### "):
				continue

		if line.startswith("### "): # found header; overrides everything
			heading = line.strip("### ")
			postag = heading.lower().encode("utf8")

			print("* POS tag: %s" % postag)

			state = 1 # found header
		elif state == 1:
			search = pinyin_regex.search(line)
			if search:
				pinyin = search.groups()[0].encode("utf8")
				print("* Pinyin: %s" % pinyin)

				state = 2 # found pinyin
		elif state == 2:
			english = line.encode("utf8")
			print("* English: %s" % english)
			state = 1

			if word and postag and pinyin and english:
				speling = "%s ; %s ; %s ; %s" % (word, postag, pinyin, english)
				print("** speling: %s" % speling)
				spelings.append(speling)
				print(spelings)
			else:
				raise Exception("Data missing!")
	print(spelings)
	return spelings

def get_tag_content(soup, tags):
	for tag in soup.findAll(True):
		if tag.name in tags:
			tag.replace_with(tag.text)
	return soup

def strip_tags(soup, tags):
	for tag in soup.findAll(True):
		if tag.name in tags:
			tag.replace_with("")
	return soup

def get_heading(soup, headings, matcher):
	for i in range(len(headings)):
		if matcher in headings[i]:
			return (i, headings[i])
	return (-1, None)

"""
Set index to 0 if you wish to obtain everything not between the two headings.
Set index to 1 if you wish to obtain everything between the two headings.
"""
def strip_out_headings(soup, htmldoc, h_level, strip_heading, index):
	if not index == 0 and not index == 1:
		raise Exception("index can only have the following values: 0, 1")

	# obtain current and next heading to strip off unnecessary stuff
	headings = [unicode(heading) for heading in soup.findAll(h_level)]
	tuple = get_heading(soup, headings, strip_heading)
	i = tuple[0]
	cur_head = tuple[1]

	if i+1 < len(headings): # i+1 is not over the max
		next_head = headings[i+1]

	# strip off everything other than what we want
	htmldoc = unicode(soup)
	if not cur_head:
		return soup
	elif not next_head:
		htmldoc = htmldoc.split(cur_head)[index]
	else:
		if index == 0:
			htmldoc = htmldoc.split(cur_head)[0] + htmldoc.split(next_head)[1]
		elif index == 1:
			htmldoc = htmldoc.split(cur_head)[1].split(next_head)[0]

	return BeautifulSoup(htmldoc)

"""
Set index to 0 if you wish to obtain everything before the heading.
Set index to 1 if you wish to obtain everything after the heading.
"""
def strip_headings(soup, htmldoc, h_level, strip_heading, index):
	if not index == 0 and not index == 1:
		raise Exception("index can only have the following values: 0, 1")

	# obtain current heading to strip off unnecessary stuff
	headings = [unicode(heading) for heading in soup.findAll(h_level)]
	tuple = get_heading(soup, headings, strip_heading)
	cur_head = tuple[1]

	htmldoc = unicode(soup)
	if not cur_head:
		return soup
	else:
		htmldoc = htmldoc.split(cur_head)[index]

	return BeautifulSoup(htmldoc)

def format_headings(soup):
	h_levels = range(1, 6)
	for level in h_levels:
		for heading in soup.findAll("h" + str(level)):
			format = "#"
			format *= level 
			heading.replace_with("%s %s" % (format, heading.text))
	return soup