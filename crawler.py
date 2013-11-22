import config

from xml.dom import minidom
import urllib2
import time
import os
import urlnorm

def crawl():
	subcats = crawl_subcats(config.start_cat)
	pages = crawl_pages(config.start_cat, subcats)
	return pages

def crawl_subcats(category):
	dirpath = "data/site/%s/" % category

	if os.path.exists(dirpath + "subcats.txt"):
		f = open(dirpath + "subcats.txt", 'r')
		subcats = f.read().strip("\n").split("\n")
		f.close()
	else:
		subcats = get_subcats(category)

		os.mkdir(dirpath)
		f = open(dirpath + "subcats.txt", 'w')
		for subcat in subcats:
			f.write(subcat + "\n")
		f.close()
	return subcats

def crawl_pages(category, subcats):
	pages = []
	counter = 1
	for subcat in subcats:
		print("Progress: %d/%d" % (counter, len(subcats)))
		counter += 1

		dirpath = "data/site/%s/%s/" % (category, subcat)

		if os.path.exists(dirpath + "pages.txt"):
			f = open(dirpath + "pages.txt", 'r')
			subcat_pages = f.read().strip("\n").split("\n")
			f.close()
		else:
			subcat_pages = get_pages(subcat)

			os.mkdir(dirpath)
			f = open(dirpath + "pages.txt", 'w')
			for page in subcat_pages:
				f.write(page + "\n")
			f.close()

		pages.extend(subcat_pages)
	return pages

def crawl_all_pages(pages):
	dirpath = "data/pages/"
	counter = 1
	for page in pages:
		print("Progress: %d/%d" % (counter, len(pages)))
		counter += 1

		if "appendix" in page.lower():
			continue

		if not os.path.exists(dirpath + page + ".html"):
			f = open(dirpath + page + ".html", 'w')
			htmldoc = get_html(page)
			f.write(htmldoc)
			f.close()


def get_subcats(category):
	xml = get_xml({"action": "query", 
		"list": "categorymembers",
		"cmtitle": category,
		"cmtype": "subcat",
		"cmlimit": "500"})

	xmldoc = minidom.parseString(xml)
	subcatlist = xmldoc.getElementsByTagName('cm')
	subcats = [subcat.attributes['title'].value.encode("utf8") for subcat in subcatlist]

	return subcats

def get_pages(subcat):
	xml = get_xml({"action": "query", 
		"list": "categorymembers",
		"cmtitle": subcat,
		"cmtype": "page",
		"cmlimit": "500"})

	xmldoc = minidom.parseString(xml)
	pagelist = xmldoc.getElementsByTagName('cm')
	pages = [page.attributes['title'].value.encode("utf8") for page in pagelist]

	return pages

def get_xml(params):
	url = "http://en.wiktionary.org/w/api.php?format=xml"
	for key, val in params.iteritems():
		url += "&%s=%s" % (key, val)
	url = urlnorm.norm(url)

	# We're permitted to crawl any page with the API regardless
	# of robots.txt since we're using the API
	response = urllib2.urlopen(url)

	time.sleep(config.crawl_delay)
	return response.read()

def get_html(page):
	url = "http://en.wiktionary.org/wiki/%s?action=render" % page
	url = urlnorm.norm(url)

	# we should be able to crawl any page from the links we obtained
	# and we're obeying crawling delays here
	response = urllib2.urlopen(url.encode("utf8"))

	time.sleep(config.crawl_delay)
	return response.read()