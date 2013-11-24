import config

if config.lang == "zh":
	from filters import zh as filter
	from parsers import zh as parser
## the list goes on

def can(page):
	return filter.can(page)

def parse(page, htmldoc):
	return parser.parse(page, htmldoc)