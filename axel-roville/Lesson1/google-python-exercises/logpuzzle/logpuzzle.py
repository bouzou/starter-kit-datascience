#!/usr/bin/python
# Copyright 2010 Google Inc.
# Licensed under the Apache License, Version 2.0
# http://www.apache.org/licenses/LICENSE-2.0

# Google's Python Class
# http://code.google.com/edu/languages/google-python-class/

import os
import re
import sys
import urllib.request

"""Logpuzzle exercise
Given an apache logfile, find the puzzle urls and download the images.

Here's what a puzzle url looks like:
10.254.254.28 - - [06/Aug/2007:00:13:48 -0700] "GET /~foo/puzzle-bar-aaab.jpg HTTP/1.0" 302 528 "-" "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.1.6) Gecko/20070725 Firefox/2.0.0.6"
"""

# Match any string like the one above
reg = '\d+\.\d+\.\d+\.\d+ \- \- \[.+\] \"GET (.+puzzle.+) HTTP\/1\.0\".+'
regex_url = re.compile(reg)

# Find the last '/' delimited part, typically the name of the file
reg_filename = '.*[\/](.+)'
regex_filename = re.compile(reg_filename)


def read_urls(filename):
    """Returns a list of the puzzle urls from the given log file,
    extracting the hostname from the filename itself.
    Screens out duplicate urls and returns the urls sorted into
    increasing order."""

    urls = []

    # Read the file line by line
    for line in open(filename, 'r'):
        # Compare the line to our computed regex
        url_search_result = regex_url.search(line)

        # If we found a match, add the corresponding URL
        if url_search_result:
            urls.append('http://code.google.com/' + url_search_result.group(1))

    return urls

def filename_from_url(url):
    return regex_filename.search(url).group(1)


def download_images(img_urls, dest_dir):
    """Given the urls already in the correct order, downloads
    each image into the given directory.
    Gives the images local filenames img0, img1, and so on.
    Creates an index.html in the directory
    with an img tag to show each local image file.
    Creates the directory if necessary.
    """

    # If the folder doesn't exist, create it
    if not os.path.exists(dest_dir):
        os.makedirs(dest_dir)

    # Make sure that we include the folder name in the path,
    # and not the name of the files
    if dest_dir[-1] != '/':
        dest_dir += '/'

    # Download and save the images in the folder
    for url in img_urls:
        urllib.request.urlretrieve(url, dest_dir + filename_from_url(url))


def main():
    args = sys.argv[1:]

    if not args:
        print('usage: [--todir dir] logfile ')
        sys.exit(1)

    todir = ''
    if args[0] == '--todir':
        todir = args[1]
        del args[0:2]

    img_urls = read_urls(args[0])

    if todir:
        download_images(img_urls, todir)
    else:
        print('\n'.join(img_urls))

if __name__ == '__main__':
    main()
