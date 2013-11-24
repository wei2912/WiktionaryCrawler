# coding=utf8

import zh
import unittest

class TestSequenceFunctions(unittest.TestCase):
    def test_parse(self):
        self.parse_word("啊")
        self.parse_word("好")
        self.parse_word("LKK")
        self.parse_word("便当")
        self.parse_word("几个")
        self.parse_word("a1")
        self.parse_word("阿")
        self.parse_word("兩者")
        self.parse_word("巴扎")
        self.parse_word("の")

    def parse_word(self, word):
        htmldoc = open("zh_tests/%s.html" % word, "r").read()

        spelings = zh.parse(word, htmldoc)
        correct_spelings = open("zh_tests/%s.txt" % word, "r").read().strip("\n").split("\n")
        correct_spelings = [speling.strip() for speling in correct_spelings]
        correct_spelings = [speling for speling in correct_spelings if speling != ""]
        
        self.assertEqual(spelings, correct_spelings)

if __name__ == '__main__':
    unittest.main()