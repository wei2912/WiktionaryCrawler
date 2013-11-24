import config

from mafan import simplify, tradify

def can(page):
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