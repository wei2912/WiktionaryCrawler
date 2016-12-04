# WiktionaryCrawler

This crawler was written to parse Wiktionary pages (which tend to be a mess, sadly) into the [speling format](http://wiki.apertium.org/wiki/Speling_format), which can be used by programs which require these wordlists.

# Dependencies

	$ sudo pip install urlnorm

Depending on your language, you may need to install more dependencies.

Here are the list of language specific dependencies:

* **zh** (Chinese, simplified and traditional): `sudo pip install mafan BeautifulSoup4`
* **th** (Thai): `sudo pip install BeautifulSoup4`
* **lo** (Lao): `sudo pip install BeautifulSoup4`

# Running the crawler

	$ python main.py

That's all you have to do. All configuration is done in `config.py`.

# General config

Refer to [General config](https://github.com/wei2912/WiktionaryCrawler/wiki/General-config) for more details.

# How it works

Refer to [How it works](https://github.com/wei2912/WiktionaryCrawler/wiki/How-it-Works) for more details.
