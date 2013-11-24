import config

import re
from bs4 import BeautifulSoup, NavigableString
from collections import OrderedDict
from mafan import text

def parse(page, htmldoc):
	spelings = []

	word = page
	postag = ""
	pinyin = ""
	english = ""

	if text.contains_latin(page): # contains latin; no pinyin
		pinyin = "none"

	abbrv_regex = r"^[A-Z]+$"
	abbrv_regex = re.compile(abbrv_regex)

	pinyin_regex = r".+?, pinyin:? (?P<pinyin>.+?)(?:,|\))"
	pinyin_regex = re.compile(pinyin_regex, re.IGNORECASE)
	
	pinyin_regex1 = r"pinyin:? (.+?) (?:\(.+?\))?(?:, (.+?) (?:\(.+?\))?)?"
	pinyin_regex1 = re.compile(pinyin_regex1, re.IGNORECASE)

	pinyin_regex2 = r"\((?P<pinyin>\S+? or \S+?)\)"
	pinyin_regex2 = re.compile(pinyin_regex2)

	pinyin_regex3 = r"\(.+?\) \((.+?)\)"
	pinyin_regex3 = re.compile(pinyin_regex3)

	pinyin_regex4 = r"\((.+?)\)"
	pinyin_regex4 = re.compile(pinyin_regex4)

	soup = BeautifulSoup(htmldoc)
	soup = take_out_edit(soup)

	soup = strip_out_section(soup, htmldoc, "h2", "Mandarin", 1)
	soup = strip_out_section(soup, htmldoc, "h3", "Romanization", 0)

	soup = format_headings(soup) # marks out sections
	soup = format_ol(soup) # marks out english

	if abbrv_regex.match(page):
		soup = BeautifulSoup(unicode(soup).replace("### Initialism", "### Abbreviation"))

	textdoc = [line.strip() for line in soup.get_text().split("\n")]
	textdoc = [line for line in textdoc if line != ""]
	textdoc = [line.replace("####", "###") for line in textdoc] # h4 to h3

	for line in textdoc:
		if line.startswith("### "): # found header; overrides everything
			heading = line[4:].lower().encode("utf8")
			postag = shortify(heading)
		elif line.startswith(page.decode("utf8")): # found pinyin
			search = pinyin_regex.search(line)
			search1 = pinyin_regex1.search(line)
			search2 = pinyin_regex2.search(line)
			search3 = pinyin_regex3.search(line)
			search4 = pinyin_regex4.search(line)

			if search:
				groupdict = search.groupdict()
				pinyin = groupdict["pinyin"].encode("utf8")
			elif search1:
				groups = search1.groups()
				groups = [group for group in groups if not group is None]
				pinyin = ', '.join(groups).encode("utf8")
			elif search2:
				groupdict = search2.groupdict()
				pinyin = groupdict["pinyin"].encode("utf8")
			elif search3:
				pinyin = search3.groups()[0].encode("utf8")
			elif search4:
				pinyin = search4.groups()[0].encode("utf8")
			pinyin.replace(" or ", ", ")
		elif line.startswith("* "): # found english
			english = line[2:].encode("utf8")

			if not pinyin:
				pinyin = "not found"

			if word and postag and pinyin and english:
				speling = "%s ; %s ; %s ; %s" % (word, postag, pinyin, english)
				spelings.append(speling)
			else:
				print("Word: %s" % word)
				print("POS tag: %s" % postag)
				print("Pinyin: %s" % pinyin)
				print("English: %s" % english)
				raise Exception("Data missing!")
	return spelings

def shortify(postag):
	shortify_tags = {
	"adjective": "adj",
	"adverb": "adv",
	"conjunction": "conj",
	"interjection": "interj",
	"measure word": "mw",
	"abbreviation": "abbrv"
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