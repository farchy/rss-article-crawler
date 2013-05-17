rss-article-crawler
===================

RSS driven article crawler and scraper.  
To start using first install the requirements:  

    pip install -r base_requirements.txt

If for some reason JPype does not install try:  

    sudo apt-get install python-jpype

And then install the rest of the requirements:

    pip install -r requirements.txt

Now all you have to do is insert a seed of RSS feeds into `resources/rss.txt`, and then simply run:  

    python webCrawler.py

Dependencies:  

 * Misja's [python-boilerpipe][1] (follow the installation instructions)  
   Will also install [`jpype`][2] & [`chardet`][3]

Based on [Boilerpipe][4]'s HTML `ArticleExtractor` (scraper).  



 [1]: https://github.com/misja/python-boilerpipe
 [2]: http://jpype.sourceforge.net/‎
 [3]: https://github.com/erikrose/chardet
 [4]: https://code.google.com/p/boilerpipe/
