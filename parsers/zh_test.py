# coding=utf8

import zh
import unittest

class TestSequenceFunctions(unittest.TestCase):
    def test_parse(self):
        page = "啊"
        htmldoc = open("zh_tests/啊.html", "r").read()

        spelings = zh.parse(page, htmldoc)
        correct_spelings = open("zh_tests/啊.txt", "r").read().strip("\n").split("\n")
        self.assertEqual(spelings, correct_spelings)

        page = "好"
        htmldoc = open("zh_tests/好.html", "r").read()

        spelings = zh.parse(page, htmldoc)
        correct_spelings = open("zh_tests/好.txt", "r").read().strip("\n").split("\n")
        self.assertEqual(spelings, correct_spelings)

if __name__ == '__main__':
    unittest.main()