import unittest

from fuzzywuzzy import process, fuzz


class TestFuzzyMatchingMethods(unittest.TestCase):
    def test_methods(self):
        location = "bullshit location that makes searching videos hard"
        hashtags = "#this #isastupidhashtag #cooldude"
        noise = f"{location}\n{hashtags}"
        s = "this is the title of a youtube video and I'm going to add stuff to the front and see which method is best"
        s1 = "this is a completely unrelated string and is bullshit"
        s2 = "this is a yet another completely unrelated string and is bullshit"

        choices = [s, s1, s2]
        s_with_noise = f"{noise} {s}"

        expected_title, score = process.extractOne(
            s_with_noise, choices, scorer=fuzz.partial_token_set_ratio
        )
        print(expected_title)
        print(score)


if __name__ == "__main__":
    unittest.main()
