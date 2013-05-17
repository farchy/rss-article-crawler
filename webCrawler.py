#! /usr/bin/env python

import sys
import os

import re
import time
import datetime
import threading
from dateutil import parser

from textAnalysis import cleanText
from boilerpipe.extract import Extractor
from fileOperations import saveToFile
from rssFromFile import getUniqueLinks

reload(sys)
sys.setdefaultencoding("utf-8")

OUTPUT_FOLDER = "output/"
RAW_HTML_FOLDER = OUTPUT_FOLDER + "htmls/"

class ThreadedCrawler(threading.Thread):
    def __init__(self, link, date, folderName):
        self.date = date
        self.link = link
        self.folderName = folderName
        self.strippedText = []
        threading.Thread.__init__(self)
        
    def run(self):
        self.strippedText = getPageInfo(self.link, self.date)
        if not self.strippedText:
            self.strippedText = ["", ""]
            return

        filename = self.folderName + "/" + self.strippedText[1] + "/" + cleanText(self.link).replace(" ","_") + ".txt"
        
        if not os.path.isdir(self.folderName + "/" + self.strippedText[1]):
            os.makedirs(self.folderName + "/" + self.strippedText[1])

        if not os.path.isdir(RAW_HTML_FOLDER + self.strippedText[1]):
            os.makedirs(RAW_HTML_FOLDER + self.strippedText[1])

        if os.path.isfile(filename):
            print "skip thread:run"
            return
        
        saveToFile(filename, self.strippedText[0])

def getPageInfo(_url, date=None):
    try:
        if date:
            date = parser.parse(date).strftime("%Y-%m-%d")
            filename = RAW_HTML_FOLDER + date + "/" + cleanText(_url).replace(" ","_") + ".html"
            if os.path.isfile(filename):
                #print "skipping..."
                return None
        
        extractor = Extractor(extractor='ArticleExtractor', url=_url)

        data = extractor.getHTML()

        text = extractor.getText()
        
        if not date:
            regex = re.compile("<span class=\"cnbc_sbhd_comp\">.*?,\s*(\d+\s*.*?\d\d\d\d).*?</span>")
            
            try:
                date = regex.findall(data)[0]
            except:
                print "Couldn't find date, setting for now."
                date = datetime.datetime.now().strftime("%Y-%m-%d")

        date = parser.parse(date).strftime("%Y-%m-%d")
        filename = RAW_HTML_FOLDER + date + "/" + cleanText(_url).replace(" ","_") + ".html"
            
        if os.path.isfile(filename):
            print "Skipping: that's odd"
            return None
        
        saveToFile(filename, data)
        return [text, date]
    except Exception as x:
        sys.stderr.write(str(type(x)) + ", " + str(x) + "'" + _url + "'\n")
        return None

def fetchPages():
    """
    Generator function.
    Fetch pages' inner text and save each to a file (for further analysis) 
    """
    folderName = OUTPUT_FOLDER + "data/"

    ulinks = getUniqueLinks()
    threads = []
    for link, date in ulinks.items():
        thread = ThreadedCrawler(link, date, folderName)
        threads.append(thread)
        if len(threads)%50 == 0:
            time.sleep(1)
        thread.start()
    
    for thread in threads:
        thread.join()
        yield thread.strippedText[0]


def main(argv):
    try:
        for text in fetchPages():
            print text
    except Exception as e:
        print "ERROR: failed to get page text"
        print type(e)
        print e

if __name__ == "__main__":
    i = 1
    sleepTime = 3840 # 64 minutes: empirically stable
    coefficient = 2
    incRateInterval = 5.0
    decRateInterval = 1.0
    print time.ctime(time.time()) + ": Starting cycle."
    while i == 1:
        x = 0
        y = 0
        print time.ctime(time.time()) + ": Fetching pages."
        for page in fetchPages():
            y += 1
            if page:
                print ".",
                x += 1

        print " - !"
        print time.ctime(time.time()) + ": Finished cycle #" + str(i) + " with " + str(x) + " new pages found."
        i = i + 1
        newLinksPerc = 100.0 * float(x) / (float(y) + 1)
        print str(newLinksPerc) + "% of total links (" + str(y) + ") are new, ",
        if newLinksPerc >= incRateInterval:
            sleepTime /= coefficient
            print "decreasing sleep interval to " + str(sleepTime) + "sec."
        elif newLinksPerc <= decRateInterval:
            sleepTime *= coefficient
            print "increasing sleep interval to " + str(sleepTime) + "sec."
        else:
            print "keeping sleep interval at " + str(sleepTime) + "sec."
#        time.sleep(sleepTime)

