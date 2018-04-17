# -*- coding: utf-8 -*-
import unittest
import format
from nltk.corpus import words as english_words

class FormatTestCase(unittest.TestCase):

    def test_generate_spam_list(self):
        spam_list = ['spam', 'ham']
        expected_result = ['spam', 'ham',' spam ', 'spam ', 'spam.',
                           '#spam', ' ham ', 'ham ', 'ham.', '#ham']
        actual_result = format.generate_spam_list(spam_list)
        self.assertEqual(expected_result, actual_result)

    def test_remove_url(self):
        sample_tweet = "iluv bitcoin https/clickhere.com"
        expected_result = "iluv bitcoin "
        actual_result = format.remove_url(sample_tweet)
        self.assertEqual(expected_result, actual_result)

    def test_remove_excess_whitespace(self):
        sample_tweet = "iluv  spaces   "
        expected_result = "iluv spaces"
        actual_result = format.remove_excess_whitespace(sample_tweet)
        self.assertEqual(expected_result, actual_result)

    def test_convert_to_lowercase(self):
        sample_tweet = "ILUV This"
        expected_result = "iluv this"
        actual_result = format.convert_to_lowercase(sample_tweet)
        self.assertEqual(expected_result, actual_result)

    def rest_remove_non_alpha_chars(self):
        sample_tweet = "what 34 £$£$"
        expected_result = "what 34 "
        actual_result = format.remove_non_alpha_chars(sample_tweet)
        self.assertEqual(expected_result, actual_result)

    def test_remove_non_english_words(self):
        english = set(w.lower() for w in english_words.words())
        sample_tweet = "what 34 £$£$"
        expected_result = "what"
        actual_result = format.remove_non_english_words(sample_tweet, english)
        self.assertEqual(expected_result, actual_result)

    def test_remove_non_english_words(self):
        english = set(w.lower() for w in english_words.words())
        sample_tweet = "what 34 £$£$"
        expected_result = "what"
        actual_result = format.remove_non_english_words(sample_tweet, english)
        self.assertEqual(expected_result, actual_result)







