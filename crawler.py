import config, lang, pb, misc

from xml.dom import minidom
import urllib2
import time
import os
import urlnorm
from collections import OrderedDict

def crawl_subcats():
	subcats = get_subcats(config.start_cat)
	subcats = [subcat for subcat in subcats if not config.subcat_bl(subcat)]

	more_subcats = []
	counter = 0
	for subcat in subcats: # crawling down another level
		counter += 1
		pb.update(counter, len(subcats))

		more_subcatslist = get_subcats(subcat)
		more_subcats.extend(more_subcatslist)

	more_subcats = [subcat for subcat in more_subcats if not config.subcat_bl(subcat)]
	subcats.extend(more_subcats)
	subcats = OrderedDict.fromkeys(subcats).keys() # unique
	return subcats

def crawl_pages(subcats):
	pages = get_pages(config.start_cat, subcats)
	pages = [page for page in pages if not config.page_bl(page) and lang.can(page)]
	pages = OrderedDict.fromkeys(pages).keys() # unique
	return pages

def crawl_all_pages(pages):
	dirpath = "data/pages/%s/%s/" % (config.wiki_lang, config.start_cat)
	counter = 0
	for page in pages:
		counter += 1
		pb.update(counter, len(pages))

		if not os.path.exists(dirpath + page + ".html"):
			f = open(dirpath + page + ".html", 'w')
			htmldoc = dl_html(page)
			f.write(htmldoc)
			f.close()

def get_subcats(category):
	dirpath = "data/site/%s/%s/" % (config.wiki_lang, category)
	misc.mkdir_p(dirpath)

	if os.path.exists(dirpath + "subcats.txt"):
		f = open(dirpath + "subcats.txt", 'r')
		subcats = f.read().strip("\n").split("\n")
		f.close()
	else:
		subcats = dl_subcats(category)

		f = open(dirpath + "subcats.txt", 'w')
		for subcat in subcats:
			f.write(subcat + "\n")
		f.close()
	return subcats

def get_pages(category, subcats):
	pages = []
	counter = 0
	for subcat in subcats:
		counter += 1
		pb.update(counter, len(subcats))

		dirpath = "data/site/%s/%s/%s/" % (config.wiki_lang, category, subcat)
		misc.mkdir_p(dirpath)

		if os.path.exists(dirpath + "pages.txt"):
			f = open(dirpath + "pages.txt", 'r')
			subcat_pages = f.read().strip("\n").split("\n")
			f.close()
		else:
			subcat_pages = dl_pages(subcat)

			f = open(dirpath + "pages.txt", 'w')
			for page in subcat_pages:
				f.write(page + "\n")
			f.close()

		pages.extend(subcat_pages)
	return pages

def dl_subcats(category):
	subcats = []
	cmcontinue = True
	cmcontinue_str = ""

	while cmcontinue:
		xml = dl_subcats_xml(category, cmcontinue_str)

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

def dl_subcats_xml(category, cmcontinue):
	if cmcontinue:
		return dl_xml({"action": "query", 
			"list": "categorymembers",
			"cmtitle": category,
			"cmtype": "subcat",
			"cmlimit": "500",
			"cmcontinue": cmcontinue})
	else:
		return dl_xml({"action": "query", 
			"list": "categorymembers",
			"cmtitle": category,
			"cmtype": "subcat",
			"cmlimit": "500"})

def dl_pages(subcat):
	pages = []
	cmcontinue = True
	cmcontinue_str = ""

	while cmcontinue:
		xml = dl_pages_xml(subcat, cmcontinue_str)

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

def dl_pages_xml(subcat, cmcontinue):
	if cmcontinue:
		return dl_xml({"action": "query", 
			"list": "categorymembers",
			"cmtitle": subcat,
			"cmtype": "page",
			"cmlimit": "500",
			"cmcontinue": cmcontinue})
	else:
		return dl_xml({"action": "query", 
			"list": "categorymembers",
			"cmtitle": subcat,
			"cmtype": "page",
			"cmlimit": "500"})

def dl_xml(params):
	url = "http://%s.wiktionary.org/w/api.php?format=xml" % config.wiki_lang
	for key, val in params.iteritems():
		url += "&%s=%s" % (key, val)
	url = urlnorm.norm(url)

	# We're permitted to crawl any page with the API regardless
	# of robots.txt since we're using the API
	response = urllib2.urlopen(url)

	time.sleep(config.crawl_delay)
	return response.read()

def dl_html(page):
	url = "http://%s.wiktionary.org/wiki/%s?action=render" % (config.wiki_lang, page)
	url = urlnorm.norm(url)

	# we should be able to crawl any page from the links we obtained
	# and we're obeying crawling delays here
	response = urllib2.urlopen(url.encode("utf8"))

	time.sleep(config.crawl_delay)
	return response.read()