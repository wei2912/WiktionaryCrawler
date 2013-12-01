import config

if config.lang == "zh":
	from filters import zh as filter
	from parsers import zh as parser
elif config.lang == "th":
	from filters import th as filter
	from parsers import th as parser
## the list goes on

def can_page(page):
	return filter.can_page(page)
def can_subcat(subcat):
	return filter.can_subcat(subcat)
def parse(page, htmldoc):
	return parser.parse(page, htmldoc)