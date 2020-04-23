import re


def find_items_starting_with(string, items):
    return [i for i, line in enumerate(items) if line.startswith(string)]


def hms_to_seconds(h, m, s):
    if h == "":
        h = 0
    if m == "":
        m = 0
    if s == "":
        s = 0
    return int(h) * 3600 + int(m) * 60 + int(s)


def extract_two_timestamp_seconds(text):
    regex = re.compile(r"(?:(?:(\d+):)?(\d+):)(\d+)")
    timestamps = [hms_to_seconds(h, m, s) for h, m, s in regex.findall(text)]

    if len(timestamps) >= 2:
        return timestamps[0], timestamps[1]
    elif len(timestamps) == 1:
        return timestamps[0], None
    else:
        return None, None


def first_url(string):
    regex = re.compile(
        r"(?:(?:https?|ftp):\/\/)?[\w/\-?=%.]+\.[\w/\-?=%.]+", re.IGNORECASE,
    )

    urls = regex.findall(string)

    if len(urls) < 1:
        return None
    else:
        return urls[0]


def consecutive(nums):
    return sorted(nums) == list(range(min(nums), max(nums) + 1))


def cheat_youtube_url_lookup(title):
    """Cached YouTube URL lookup from title with a couple of titles that I use for testing"""
    return {
        "Cloud Run QuickStart - Docker to Serverless": "https://www.youtube.com/watch?v=3OP-q55hOUI",
        "White Screen 10 Hours": "https://www.youtube.com/watch?v=J3pF2jkQ4vc",
    }.get(title)
