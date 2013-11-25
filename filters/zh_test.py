# coding=utf8

import config
import zh
import unittest

class TestSequenceFunctions(unittest.TestCase):
    def test_can_st(self):
        results = {
            # word: (simplified, traditional)
            "啊": (True, True),
            "好": (True, True),
            "LKK": (True, True),
            "兩者": (False, True),
            "巴扎": (True, False),
            "危險": (False, True),
            "脸": (True, False)
        }

        for key in results.keys():
            self.assert_st(key, results)

    def assert_st(self, word, results):
        # only simplified
        config.zh_s = True
        config.zh_t = False

        self.assertEqual(zh.can_st(word), results[word][0])

        # only traditional
        config.zh_s = False
        config.zh_t = True

        self.assertEqual(zh.can_st(word), results[word][1])

        # both
        config.zh_s = True
        config.zh_t = True

        self.assertEqual(zh.can_st(word), True)

        # none
        config.zh_s = False
        config.zh_t = False

        self.assertEqual(zh.can_st(word), False)

    def test_is_pinyin(self):
        results = {
            "啊": False,
            "a1": True,
            "hǎo": True
        }

        for key in results.keys():
            self.assertEqual(zh.is_pinyin(key), results[key])

if __name__ == '__main__':
    unittest.main()