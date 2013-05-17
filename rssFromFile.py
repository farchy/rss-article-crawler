#! /usr/bin/env python

import sys    
import threading

from rssItems import getLinks
from rssItems import RssFetcher

RESOURCES = "resources/"

DEFAULT_FILE = RESOURCES + "rss.txt"

class ThreadedRSS(threading.Thread):
    def __init__(self, url):
        self.url = url
        self.links = {}
        threading.Thread.__init__(self)
        
    def run(self):
        rss = RssFetcher(self.url)
        self.links = getLinks(rss.getItems())

def getUniqueLinks(filename=DEFAULT_FILE):
    """
    Gets a set of links (no duplication) from a file of RSS feeds
    
    filename - the RSS feeds filename
    
    return - the set of unique URLs
    """
    links = {}
    rssFile = open(filename, 'r')
    threads = []
    for line in rssFile:
        stripped = line.strip()
        if (not stripped or stripped.startswith("#")):
            continue
        thread = ThreadedRSS(stripped)
        threads.append(thread)
        if len(threads)%100 == 0:
            import time
            time.sleep(1)
        thread.start()

    for thread in threads:
        thread.join()
        if not thread.links:
            sys.stderr.write("ERROR for URL: '" + thread.url + "'\n")
        for (link, date) in thread.links:
            if (link in links):
                pass
                #sys.stderr.write("WARN: '" + link + "' already exists\n")
            elif "video" in link.lower() or "watch" in link.lower() or "play" in link.lower():
                continue
            else:
                links[link] = date
    return links

def main(argv):
    try:
        filename = sys.argv[1]
    except IndexError:
        sys.stderr.write( "WARN: no argument passed, using '" + DEFAULT_FILE + "' as input file\n")
        filename = DEFAULT_FILE

    for link in getUniqueLinks(filename):
        print "\t" + link
    print ""


if __name__ == "__main__":
    main(sys.argv)

