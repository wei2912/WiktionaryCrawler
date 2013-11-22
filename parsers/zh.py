import config

import re
from bs4 import BeautifulSoup, NavigableString

def parse(page, htmldoc):
	print("* Crawling %s.html" % page)

	spelings = []

	word = page
	postag = ""
	pinyin = ""
	english = ""

	abbrv_regex = r"^[A-Z]+$"
	abbrv_regex = re.compile(abbrv_regex)

	pinyin_regex = r"(?P<ts>traditional|simplified|traditional and simplified), Pinyin (?P<pinyin>.+?)(?:, (?:simplified|traditional) .+?)?\)"
	pinyin_regex = re.compile(pinyin_regex)

	pinyin_regex2 = r"\((?P<pinyin>\S+? or \S+?)\)"
	pinyin_regex2 = re.compile(pinyin_regex2)

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
	"dl",
	"ul"
	]
	soup = strip_tags(soup, tags)
	
	soup = strip_out_headings(soup, htmldoc, "h3", "Pronunciation", 0)
	soup = strip_out_headings(soup, htmldoc, "h3", "Hanzi", 0)
	soup = strip_out_headings(soup, htmldoc, "h3", "Affix", 0)
	soup = strip_out_headings(soup, htmldoc, "h3", "Prefix", 0)
	soup = strip_out_headings(soup, htmldoc, "h3", "References", 0)

	if abbrv_regex.match(page): # abbreviations
		soup = strip_out_headings(soup, htmldoc, "h3", "Initialism", 1)
		postag = "abbrv"
		pinyin = "none"

	soup = format_headings(soup)
	soup = format_ol(soup)

	textdoc = [line.strip() for line in soup.get_text().split("\n")]
	textdoc = [line for line in textdoc if line != ""]
	textdoc = [line.replace("####", "###") for line in textdoc] # h4 to h3

	for line in textdoc:
		search = pinyin_regex.search(line)
		search2 = pinyin_regex2.search(line)

		if line.startswith("### "): # found header; overrides everything
			heading = line[4:].lower().encode("utf8")
			postag = shortify(heading)
			print("* POS tag: %s" % postag)
		elif search or search2: # found pinyin
			if search:
				groupdict = search.groupdict()
				if groupdict["ts"] == "traditional" and config.zh_s:
					print("* Is traditional, returning.")
					return []
				if groupdict["ts"] == "simplified" and config.zh_t:
					print("* Is simplified, returning.")
					return []
				pinyin = groupdict["pinyin"].encode("utf8")
			elif search2:
				groupdict = search2.groupdict()
				pinyin = groupdict["pinyin"].encode("utf8")
			print("* Pinyin: %s" % pinyin)
		elif line.startswith("* "): # found english
			english = line[2:].encode("utf8")
			print("* English: %s" % english)

			if word and postag and pinyin and english:
				speling = "%s ; %s ; %s ; %s" % (word, postag, pinyin, english)
				print("** speling: %s" % speling)
				print("")
				spelings.append(speling)
			else:
				raise Exception("Data missing!")
	return spelings

def shortify(postag):
	shortify_tags = {
	"adjective": "adj",
	"adverb": "adv",
	"conjunction": "conj",
	"interjection": "interj",
	"measure word": "mw",
	}
	if postag in shortify_tags:
		return shortify_tags[postag]
	return postag

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
	else:
		next_head = None

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

def format_ol(soup):
	for ol in soup.findAll("ol"):
		for li in ol.findAll("li"):
			li.replace_with("* %s" % li.text)
	return soup