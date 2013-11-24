# coding=utf8

import config
import zh
import unittest

class TestSequenceFunctions(unittest.TestCase):
    def test_filter(self):
        results = {
            # word: (simplified, traditional)
            "啊": (True, True),
            "好": (True, True),
            "LKK": (True, True),
            "兩者": (False, True),
            "巴扎": (True, False),
            "危險": (False, True)
        }

        for key in results.keys():
            self.filter_assert(key, results)

    def filter_assert(self, word, results):
        # only simplified
        config.zh_s = True
        config.zh_t = False

        self.assertEqual(zh.can(word), results[word][0])

        # only traditional
        config.zh_s = False
        config.zh_t = True

        self.assertEqual(zh.can(word), results[word][1])

        # both
        config.zh_s = True
        config.zh_t = True

        self.assertEqual(zh.can(word), True)

        # none
        config.zh_s = False
        config.zh_t = False

        self.assertEqual(zh.can(word), False)

if __name__ == '__main__':
    unittest.main()