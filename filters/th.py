import re

def can_page(page):
	# stage 1: match filter regex
	filter_regex = ".*?:.*"
	filter_regex = re.compile(filter_regex)
	if filter_regex.match(page):
		return False
	return True
def can_subcat(subcat):
	# stage 1: match filter regex
	filter_regex = "Category:(th:.*)"
	filter_regex = re.compile(filter_regex)
	return not filter_regex.match(subcat)