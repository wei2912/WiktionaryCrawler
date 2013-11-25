import config, lang, pb, misc

from xml.dom import minidom
import urllib2
import time
import os
import urlnorm


def crawl():
	subcats = crawl_subcats(config.start_cat)
	subcats = [subcat for subcat in subcats if not config.subcat_bl(subcat)]
	pages = crawl_pages(config.start_cat, subcats)
	pages = [page for page in pages if not config.page_bl(page) and lang.can(page)]
	return pages

def crawl_subcats(category):
	dirpath = "data/site/%s/%s/" % (config.wiki_lang, category)
	misc.mkdir_p(dirpath)

	if os.path.exists(dirpath + "subcats.txt"):
		f = open(dirpath + "subcats.txt", 'r')
		subcats = f.read().strip("\n").split("\n")
		f.close()
	else:
		subcats = get_subcats(category)

		f = open(dirpath + "subcats.txt", 'w')
		for subcat in subcats:
			f.write(subcat + "\n")
		f.close()
	return subcats

def crawl_pages(category, subcats):
	pages = []
	counter = 0
	for subcat in subcats:
		counter += 1
		pb.update(counter*100/len(subcats))

		dirpath = "data/site/%s/%s/%s/" % (config.wiki_lang, category, subcat)
		misc.mkdir_p(dirpath)

		if os.path.exists(dirpath + "pages.txt"):
			f = open(dirpath + "pages.txt", 'r')
			subcat_pages = f.read().strip("\n").split("\n")
			f.close()
		else:
			subcat_pages = get_pages(subcat)

			f = open(dirpath + "pages.txt", 'w')
			for page in subcat_pages:
				f.write(page + "\n")
			f.close()

		pages.extend(subcat_pages)
	return pages

def crawl_all_pages(pages):
	dirpath = "data/pages/%s/%s/" % (config.wiki_lang, config.start_cat)
	counter = 0
	for page in pages:
		counter += 1
		pb.update(counter*100/len(pages))

		if "appendix" in page.lower():
			continue

		if not os.path.exists(dirpath + page + ".html"):
			f = open(dirpath + page + ".html", 'w')
			htmldoc = get_html(page)
			f.write(htmldoc)
			f.close()

def get_subcats(category):
	subcats = []
	cmcontinue = True
	cmcontinue_str = ""

	while cmcontinue:
		xml = get_subcats_xml(category, cmcontinue_str)

		xmldoc = minidom.parseString(xml)
		subcatlist = xmldoc.getElementsByTagName('cm')
		subcatlist = [subcat.attributes['title'].value.encode("utf8") for subcat in subcatlist]
		subcats.extend(subcatlist)

		list = xmldoc.getElementsByTagName('query-continue')
		if list:
			categorymembers = list[0].getElementsByTagName('categorymembers')[0]
			cmcontinue_str = categorymembers.attributes["cmcontinue"].value
		else:
			cmcontinue = False

	return subcats

def get_subcats_xml(category, cmcontinue):
	if cmcontinue:
		return get_xml({"action": "query", 
			"list": "categorymembers",
			"cmtitle": category,
			"cmtype": "subcat",
			"cmlimit": "500",
			"cmcontinue": cmcontinue})
	else:
		return get_xml({"action": "query", 
			"list": "categorymembers",
			"cmtitle": category,
			"cmtype": "subcat",
			"cmlimit": "500"})

def get_pages(subcat):
	pages = []
	cmcontinue = True
	cmcontinue_str = ""

	while cmcontinue:
		xml = get_pages_xml(subcat, cmcontinue_str)

		xmldoc = minidom.parseString(xml)
		pagelist = xmldoc.getElementsByTagName('cm')
		pagelist = [page.attributes['title'].value.encode("utf8") for page in pagelist]
		pages.extend(pagelist)

		list = xmldoc.getElementsByTagName('query-continue')
		if list:
			categorymembers = list[0].getElementsByTagName('categorymembers')[0]
			cmcontinue_str = categorymembers.attributes["cmcontinue"].value
		else:
			cmcontinue = False

	return pages

def get_pages_xml(subcat, cmcontinue):
	if cmcontinue:
		return get_xml({"action": "query", 
			"list": "categorymembers",
			"cmtitle": subcat,
			"cmtype": "page",
			"cmlimit": "500",
			"cmcontinue": cmcontinue})
	else:
		return get_xml({"action": "query", 
			"list": "categorymembers",
			"cmtitle": subcat,
			"cmtype": "page",
			"cmlimit": "500"})

def get_xml(params):
	url = "http://%s.wiktionary.org/w/api.php?format=xml" % config.wiki_lang
	for key, val in params.iteritems():
		url += "&%s=%s" % (key, val)
	url = urlnorm.norm(url)

	# We're permitted to crawl any page with the API regardless
	# of robots.txt since we're using the API
	response = urllib2.urlopen(url)

	time.sleep(config.crawl_delay)
	return response.read()

def get_html(page):
	url = "http://%s.wiktionary.org/wiki/%s?action=render" % (config.wiki_lang, page)
	url = urlnorm.norm(url)

	# we should be able to crawl any page from the links we obtained
	# and we're obeying crawling delays here
	response = urllib2.urlopen(url.encode("utf8"))

	time.sleep(config.crawl_delay)
	return response.read()