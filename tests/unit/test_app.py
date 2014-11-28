# -*- coding: utf-8 -*-
# (C) Copyright Connected Digital Economy Catapult Limited 2014
import facebook

import pytest
import datetime

def test_zero_division():
    with pytest.raises(ZeroDivisionError):
        1 / 0


def test_write_csv_file():
    today = datetime.date.today()

    write_string = "27-11-2014 11:03:12,,The drawer is open, Facebook\n"

    with open('/tmp/testCsvOutput.csv', 'a') as the_file:
        the_file.write("27-11-2014 11:03:12,,The drawer is open, Facebook\n")
        the_file.write("27-11-2014 11:03:12,27-11-2014 11:04:12,The drawer is closing, Facebook\n")
        the_file.write("27-11-2014 11:30:15,,The drawer is open, Facebook\n")
        the_file.write("27-11-2014 11:30:15,27-11-2014 11:31:00,The drawer is closing, Facebook\n")
        the_file.write("27-11-2014 11:34:02,,The drawer is open, Facebook\n")
        the_file.write("27-11-2014 11:34:02,27-11-2014 11:36:13,The drawer has closed, Facebook\n")
    assert(1 == 1)


def test_post_to_facebook():
    graph = facebook.GraphAPI("CAALZA3vgt0TYBAHghbwefK9lK3qB2kCFSwHZBxRON8wVcUYA19jpyIFLsW9qiSj7QcnlxMllxNck88AGpYjRZBmTSqB3ZAto0TvXHprwEGwgtHJJluqXTbf9Jynph8ZA52k6g3bakCZBYFxzvmnLsWkCXvSRsXnzwIj10P2vmsMoqVq0lPb1sOlfqZCflWLCp6gzYvSZBzD1aGZA51xV25IbL")
    profile = graph.get_object("me")
    friends = graph.get_connections("me", "friends")
    graph.put_object("me", "feed", message="I am writing on my wall!")
