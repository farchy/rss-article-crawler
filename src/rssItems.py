#! /usr/bin/env python

import sys
import urllib2

from xml.dom import minidom, Node

class Item:
    """
    The RSS item structure.
    Contains all the information for an RSS item.

    Title - RSS title,
    Description - RSS item description,
    Link - RSS item destination link,
    ...<TBD>
    """

    def __init__(self, title="", description="", link="", date=""):
        self.title = title
        self.description = description
        self.link = link
        self.date = date

class RssFetcher:
    """
    The RSS fetcher class.
    It gets the RSS for a given URL.
    """

    def __init__(self, url):
        self.url = url
        self.xmldoc = self.getXmlDocument(url)
        self.tags = {}
        if (not self.xmldoc):
            sys.stderr.write("Error: Could not read the XML document.\n")
            return
        if (self.xmldoc.documentElement.nodeName == "rss" or
            self.xmldoc.documentElement.nodeName == "rdf" or
            self.xmldoc.documentElement.nodeName == "rdf:RDF" or
            self.xmldoc.documentElement.nodeName == "channel"):
            self.tags["item"] = "item"
            self.tags["title"] = "title"
            self.tags["desc"] = "description"
            self.tags["link"] = "link"
            self.tags["date"] = "pubDate"
        elif (self.xmldoc.documentElement.nodeName == "feed"):
            self.tags["item"] = "entry"
            self.tags["title"] = "title"
            self.tags["desc"] = "content"
            self.tags["link"] = "link"
            self.tags["date"] = "updated"
        else:
            print self.xmldoc.documentElement.nodeName
            print "Error: Unsupported feed type."

    def getXmlDocument(self, url):
        """
        Read a URL and try to return it's XML root document.

        return - XML document on success, None on failure
        """
        try:
            page = urllib2.urlopen(url)
        except:
            sys.stderr.write("Error: Failed to get URL: " + url + "\n")
            return None
        xmldoc = None
        if (page):
            try:
                xmldoc = minidom.parse(page)
            except:
                sys.stderr.write("Error: Failed to get URL: " + url + "\n")
        else:
            print "Error: Could not get URL."
        return xmldoc
    
    def getItemText(self, node):
        """
        Gets the text for a given XML node.

        return - inner text of the XML node
        """
        text = ""
        for textNode in node.childNodes:
            if (textNode.nodeType == Node.TEXT_NODE):
                text += textNode.nodeValue
        return text.strip(' \t\n\r')
    
    def getChildText(self, node, childName):
        """
        Gets the text for a desired child of a given XML node.

        return - inner text of the desired chilid node
        """
        if (not node):
            print "Error: No XML node given, failed to get child text."
            return ""
        for item in node.childNodes:
            if (item.nodeName == childName):
                return self.getItemText(item)
        return ""
    
    def createRssItem(self, node):
        """
        Creates an RSS item from a given XML node.

        return - a new RSS
        """
        title = self.getChildText(node, self.tags["title"])
        description = self.getChildText(node, self.tags["desc"])
        link = self.getChildText(node, self.tags["link"])
        date = self.getChildText(node, self.tags["date"]) 
        return Item(title, description, link, date)
    
    def getItems(self):
        """
        Generator to get RSS items
        """
        if (not self.xmldoc):
            return
        rootNode = self.xmldoc.documentElement
        
        items = []
        if (rootNode.nodeName.lower() == "rss"):
            for child in rootNode.childNodes:
                if child.nodeName.lower() == "channel":
                    rootNode = child
                    break
        for node in rootNode.childNodes:
            if (node.nodeName == self.tags["item"]):
                item = self.createRssItem(node)
                items.append(item)
        return items

def getLinks(items):
    """
    Generator to get links from RSS items
    """
    if not items:
        sys.stderr.write("Error: no items received.\n")
    results = []
    try:
        for item in items:
            if item.link:
                if item.date:
                    results.append((item.link, item.date))
                else:
    #                now = datetime.datetime.now()
    #                yield item.link, now.strftime("%Y-%m-%d")
                    results.append((item.link, None))
    except Exception as x:
        sys.stderr.write(str(type(x)) + " " + str(x) + "\n")
    return results
    

if __name__ == "__main__":
    rss = RssFetcher('http://feeds.thestreet.com/tsc/feeds/rss/ScottRutt')
    for link in getLinks(rss.getItems()):
        print link
    #rss = RssFetcher('http://rss.slashdot.org/Slashdot/slashdot')
    #rss = RssFetcher('http://news.google.com/news?ned=ca&topic=n&output=atom')
#    for item in rss.getItems():
#        if (item):
#            print "-- TITLE --"
#            print item.title
#            print ""
#            print "-- DESCRIPTION --"
#            print item.description
#            print ""
#            print "-- LINK --"
#            print item.link

